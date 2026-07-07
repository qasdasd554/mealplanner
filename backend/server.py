"""Smart Meal Planner PL — FastAPI + MongoDB."""
import os
import random
import uuid
import logging
from datetime import datetime, timedelta, timezone
from math import ceil
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from motor.motor_asyncio import AsyncIOMotorClient
from pwdlib import PasswordHash
from pydantic import BaseModel, Field, EmailStr
from starlette.middleware.cors import CORSMiddleware

from seed_data import STORES, PRODUCTS, RECIPES, RECIPE_IMAGES, DEPARTMENT_ORDER, uid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = 7

pwd_hasher = PasswordHash.recommended()
security_scheme = HTTPBearer(auto_error=False)

app = FastAPI(title="Smart Meal Planner PL")
api = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Elastyczne konfiguracje posiłków — 1..5 posiłków dziennie.
# Sloty w 5-posiłkowym planie mają unikalne etykiety (II śniadanie, podwieczorek)
# ale sięgają z puli przepisów meal_type="przekąska".
MEAL_SLOT_LAYOUTS: dict = {
    1: ["obiad"],
    2: ["śniadanie", "kolacja"],
    3: ["śniadanie", "obiad", "kolacja"],
    4: ["śniadanie", "obiad", "przekąska", "kolacja"],
    5: ["śniadanie", "II śniadanie", "obiad", "podwieczorek", "kolacja"],
}

_SLOT_TO_MEAL_TYPE = {"II śniadanie": "przekąska", "podwieczorek": "przekąska"}


def slots_for(meals_per_day: int) -> list:
    """Zwraca listę pór (slotów) dla danej liczby posiłków dziennie."""
    return MEAL_SLOT_LAYOUTS[meals_per_day]


def slot_meal_type(slot: str) -> str:
    """Zwraca meal_type z bazy odpowiadający slotowi (dla II śniadania / podwieczorka: przekąska)."""
    return _SLOT_TO_MEAL_TYPE.get(slot, slot)


def unique_meal_types(slots: list) -> list:
    """Unikalne meal_type potrzebne dla podanych slotów."""
    seen: list = []
    for s in slots:
        mt = slot_meal_type(s)
        if mt not in seen:
            seen.append(mt)
    return seen


# ── Modele ───────────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    display_name: str = Field(min_length=1, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class IngredientInput(BaseModel):
    product_id: str
    quantity: float = Field(gt=0)
    unit: str


class RecipeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    description: str = ""
    meal_type: str
    servings: int = Field(ge=1, le=12)
    prep_time_min: int = Field(ge=0, le=600, default=10)
    cook_time_min: int = Field(ge=0, le=600, default=0)
    ingredients: List[IngredientInput] = Field(min_length=1)


class GeneratePlanRequest(BaseModel):
    days: int = Field(ge=1, le=14)
    meals_per_day: int = Field(ge=1, le=5, default=3)
    store_id: str
    household_size: int = Field(ge=1, le=12, default=2)
    budget: Optional[float] = Field(default=None, gt=0)
    target_kcal: Optional[int] = Field(default=None, ge=800, le=6000)
    slots: Optional[List[str]] = Field(default=None)


class ToggleItemRequest(BaseModel):
    checked: bool


class SwapRequest(BaseModel):
    day: int
    slot: str


# ── Auth utils ───────────────────────────────────────────────────
def create_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
) -> dict:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Brak autoryzacji")
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Nieprawidłowy lub wygasły token")
    user = await db.users.find_one({"id": user_id}, {"_id": 0, "password_hash": 0})
    if not user:
        raise HTTPException(status_code=401, detail="Użytkownik nie istnieje")
    return user


# ── Odżywianie ───────────────────────────────────────────────────
def ingredient_weight_g(product: dict, quantity: float, unit: str) -> float:
    if unit in ("kg", "l"):
        return quantity * 1000
    if unit in ("g", "ml"):
        return quantity
    if unit == "szt":
        return quantity * (product.get("weight_per_unit_g") or 100)
    return quantity


def compute_nutrition(products_by_id: dict, ingredients: list) -> dict:
    total = {"kcal": 0.0, "protein": 0.0, "fat": 0.0, "carbs": 0.0, "fiber": 0.0}
    for ing in ingredients:
        product = products_by_id.get(ing["product_id"])
        if not product:
            continue
        weight = ingredient_weight_g(product, ing["quantity"], ing["unit"])
        nutr = product.get("nutrition_per_100") or {}
        for key in total:
            total[key] += (nutr.get(key, 0) or 0) * weight / 100.0
    return {k: round(v, 1) for k, v in total.items()}


async def products_map() -> dict:
    docs = await db.products.find({}, {"_id": 0}).to_list(500)
    return {p["id"]: p for p in docs}


# ── Auth endpoints ───────────────────────────────────────────────
@api.post("/auth/register", status_code=201)
async def register(payload: RegisterRequest):
    existing = await db.users.find_one({"email": payload.email.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="Ten e-mail jest już zarejestrowany")
    user = {
        "id": str(uuid.uuid4()),
        "email": payload.email.lower(),
        "display_name": payload.display_name,
        "password_hash": pwd_hasher.hash(payload.password),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.users.insert_one(dict(user))
    user.pop("password_hash")
    user.pop("_id", None)
    return {"token": create_token(user["id"]), "user": user}


@api.post("/auth/login")
async def login(payload: LoginRequest):
    user = await db.users.find_one({"email": payload.email.lower()}, {"_id": 0})
    if not user or not pwd_hasher.verify(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Nieprawidłowy e-mail lub hasło")
    user.pop("password_hash")
    return {"token": create_token(user["id"]), "user": user}


@api.get("/auth/me")
async def me(user: dict = Depends(get_current_user)):
    return user


# ── Produkty i sklepy ────────────────────────────────────────────
@api.get("/products")
async def list_products():
    return await db.products.find({}, {"_id": 0}).sort("name", 1).to_list(500)


@api.get("/stores")
async def list_stores():
    return await db.stores.find({}, {"_id": 0}).to_list(50)


# ── Przepisy ─────────────────────────────────────────────────────
@api.get("/recipes")
async def list_recipes(meal_type: Optional[str] = None, user: dict = Depends(get_current_user)):
    query = {"$or": [{"is_custom": False}, {"owner_id": user["id"]}]}
    if meal_type:
        query["meal_type"] = meal_type
    return await db.recipes.find(query, {"_id": 0}).sort([("is_custom", -1), ("name", 1)]).to_list(500)


@api.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: str, user: dict = Depends(get_current_user)):
    recipe = await db.recipes.find_one({"id": recipe_id}, {"_id": 0})
    if not recipe:
        raise HTTPException(status_code=404, detail="Nie znaleziono przepisu")
    return recipe


@api.post("/recipes", status_code=201)
async def create_recipe(payload: RecipeCreate, user: dict = Depends(get_current_user)):
    if payload.meal_type not in ("śniadanie", "obiad", "kolacja", "przekąska"):
        raise HTTPException(status_code=400, detail="Nieprawidłowa pora posiłku")
    pmap = await products_map()
    ingredients = []
    for ing in payload.ingredients:
        product = pmap.get(ing.product_id)
        if not product:
            raise HTTPException(status_code=400, detail="Nieznany produkt w składnikach")
        ingredients.append({
            "product_id": product["id"],
            "product_name": product["name"],
            "quantity": ing.quantity,
            "unit": ing.unit,
        })
    total = compute_nutrition(pmap, ingredients)
    per_serving = {k: round(v / payload.servings, 1) for k, v in total.items()}
    recipe = {
        "id": str(uuid.uuid4()),
        "name": payload.name.strip(),
        "description": payload.description.strip(),
        "cuisine": "własna",
        "meal_type": payload.meal_type,
        "prep_time_min": payload.prep_time_min,
        "cook_time_min": payload.cook_time_min,
        "servings": payload.servings,
        "difficulty": "łatwy",
        "tags": ["własny przepis"],
        "ingredients": ingredients,
        "nutrition_total": total,
        "nutrition_per_serving": per_serving,
        "is_custom": True,
        "owner_id": user["id"],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.recipes.insert_one(dict(recipe))
    recipe.pop("_id", None)
    return recipe


@api.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: str, user: dict = Depends(get_current_user)):
    recipe = await db.recipes.find_one({"id": recipe_id}, {"_id": 0})
    if not recipe:
        raise HTTPException(status_code=404, detail="Nie znaleziono przepisu")
    if not recipe.get("is_custom") or recipe.get("owner_id") != user["id"]:
        raise HTTPException(status_code=403, detail="Możesz usuwać tylko własne przepisy")
    await db.recipes.delete_one({"id": recipe_id})
    return {"ok": True}


# ── Plan posiłków ────────────────────────────────────────────────
def build_shopping_items(pmap: dict, entries: list, recipes_by_id: dict,
                         multiplier: float, household_size: int = 1) -> list:
    needed: dict = {}
    for entry in entries:
        recipe = recipes_by_id[entry["recipe_id"]]
        # 1 porcja przepisu przypadająca na osobę × liczba osób w gospodarstwie.
        scale = float(household_size) / recipe["servings"]
        for ing in recipe["ingredients"]:
            key = ing["product_id"]
            needed.setdefault(key, {"quantity": 0.0, "unit": ing["unit"]})
            needed[key]["quantity"] += ing["quantity"] * scale
    items = []
    for product_id, info in needed.items():
        product = pmap.get(product_id)
        if not product:
            continue
        qty = round(info["quantity"], 2)
        pack = product.get("default_quantity") or 1
        packages = max(1, ceil(qty / pack - 1e-9))
        price = round(packages * round(product["base_price"] * multiplier, 2), 2)
        items.append({
            "id": str(uuid.uuid4()),
            "product_id": product_id,
            "name": product["name"],
            "quantity": qty,
            "unit": info["unit"],
            "department": product["department"],
            "packages": packages,
            "price": price,
            "checked": False,
        })
    dept_rank = {d: i for i, d in enumerate(DEPARTMENT_ORDER)}
    items.sort(key=lambda x: (dept_rank.get(x["department"], 99), x["name"]))
    return items


def recipe_unit_cost(recipe: dict, pmap: dict, multiplier: float) -> float:
    """Proporcjonalny koszt 1 porcji przepisu (do rankingu taniości)."""
    cost = 0.0
    for ing in recipe["ingredients"]:
        product = pmap.get(ing["product_id"])
        if not product:
            continue
        pack = product.get("default_quantity") or 1
        price = product["base_price"] * multiplier
        cost += (ing["quantity"] / recipe["servings"]) / pack * price
    return cost


def make_entry(recipe: dict, day: int, slot: str) -> dict:
    return {
        "day": day,
        "slot": slot,
        "recipe_id": recipe["id"],
        "recipe_name": recipe["name"],
        "prep_time_min": recipe["prep_time_min"],
        "cook_time_min": recipe["cook_time_min"],
        "nutrition_per_serving": recipe["nutrition_per_serving"],
    }


async def plan_context(user: dict, store_id: str, meals_per_day: int, custom_slots: Optional[List[str]] = None):
    store = await db.stores.find_one({"id": store_id}, {"_id": 0})
    if not store:
        raise HTTPException(status_code=400, detail="Nieznany sklep")
    if custom_slots:
        valid = {"śniadanie", "obiad", "kolacja", "przekąska"}
        for s in custom_slots:
            if s not in valid:
                raise HTTPException(status_code=400, detail=f"Nieprawidłowy slot: {s}")
        slots = custom_slots
    else:
        slots = slots_for(meals_per_day)
    query = {"$or": [{"is_custom": False}, {"owner_id": user["id"]}]}
    all_recipes = await db.recipes.find(query, {"_id": 0}).to_list(500)
    by_type: dict = {}
    for r in all_recipes:
        by_type.setdefault(r["meal_type"], []).append(r)
    for meal_type in unique_meal_types(slots):
        if not by_type.get(meal_type):
            raise HTTPException(status_code=400, detail=f"Brak przepisów dla pory: {meal_type}")
    return store, slots, all_recipes, by_type


def min_plan_cost(days: int, slots: list, by_type: dict, pmap: dict,
                  recipes_by_id: dict, multiplier: float, household_size: int = 1) -> float:
    """Koszt najtańszego możliwego planu (najtańszy przepis w każdym slocie)."""
    entries = []
    for day in range(1, days + 1):
        for slot in slots:
            pool = by_type[slot_meal_type(slot)]
            cheapest = min(pool, key=lambda r: recipe_unit_cost(r, pmap, multiplier))
            entries.append(make_entry(cheapest, day, slot))
    items = build_shopping_items(pmap, entries, recipes_by_id, multiplier, household_size)
    return round(sum(i["price"] for i in items), 2)


@api.get("/meal-plans/min-cost")
async def get_min_cost(
    days: int, meals_per_day: int, store_id: str,
    household_size: int = 2, user: dict = Depends(get_current_user),
):
    if meals_per_day not in MEAL_SLOT_LAYOUTS:
        raise HTTPException(status_code=400, detail="Nieobsługiwana liczba posiłków")
    if not 1 <= household_size <= 12:
        raise HTTPException(status_code=400, detail="Liczba osób poza zakresem 1–12")
    store, slots, all_recipes, by_type = await plan_context(user, store_id, meals_per_day)
    pmap = await products_map()
    recipes_by_id = {r["id"]: r for r in all_recipes}
    cost = min_plan_cost(days, slots, by_type, pmap, recipes_by_id,
                         store["price_multiplier"], household_size)
    return {"min_cost": cost}


@api.post("/meal-plans/generate", status_code=201)
async def generate_plan(payload: GeneratePlanRequest, user: dict = Depends(get_current_user)):
    if payload.slots:
        effective_meals_per_day = len(payload.slots)
    else:
        effective_meals_per_day = payload.meals_per_day
        if payload.meals_per_day not in MEAL_SLOT_LAYOUTS:
            raise HTTPException(status_code=400, detail="Nieobsługiwana liczba posiłków")
    store, slots, all_recipes, by_type = await plan_context(
        user, payload.store_id, effective_meals_per_day, payload.slots
    )
    pmap = await products_map()
    recipes_by_id = {r["id"]: r for r in all_recipes}
    multiplier = store["price_multiplier"]
    household_size = payload.household_size

    if payload.budget is not None:
        min_cost = min_plan_cost(payload.days, slots, by_type, pmap, recipes_by_id,
                                 multiplier, household_size)
        if payload.budget < min_cost:
            raise HTTPException(
                status_code=400,
                detail=f"Budżet zbyt niski. Najtańszy możliwy plan kosztuje {min_cost:.2f} zł",
            )

    entries = []
    # Osobna pula losowań per meal_type (a nie per slot), żeby II śniadanie i
    # podwieczorek nie dublowały tego samego przepisu w jednym dniu.
    pools: dict = {}
    for day in range(1, payload.days + 1):
        for slot in slots:
            mt = slot_meal_type(slot)
            if not pools.get(mt):
                pools[mt] = random.sample(by_type[mt], len(by_type[mt]))
            recipe = pools[mt].pop()
            entries.append(make_entry(recipe, day, slot))

    # Dopasowanie do budżetu: podmieniaj najdroższe pozycje na najtańsze w slocie.
    if payload.budget is not None:
        cheapest_for = {
            slot: min(by_type[slot_meal_type(slot)],
                      key=lambda r: recipe_unit_cost(r, pmap, multiplier))
            for slot in slots
        }
        MAX_RECIPE_REPEATS_BUDGET = 3
        def total_cost():
            items = build_shopping_items(pmap, entries, recipes_by_id, multiplier, household_size)
            return round(sum(i["price"] for i in items), 2)
        while total_cost() > payload.budget:
            candidates = [
                (i, recipe_unit_cost(recipes_by_id[e["recipe_id"]], pmap, multiplier))
                for i, e in enumerate(entries)
                if e["recipe_id"] != cheapest_for[e["slot"]]["id"]
                and sum(1 for x in entries if x["recipe_id"] == cheapest_for[e["slot"]]["id"]) < MAX_RECIPE_REPEATS_BUDGET
            ]
            if not candidates:
                break
            idx = max(candidates, key=lambda c: c[1])[0]
            entry = entries[idx]
            entries[idx] = make_entry(cheapest_for[entry["slot"]], entry["day"], entry["slot"])

    # ── Dopasowanie do celu kalorycznego ──
    if payload.target_kcal is not None:
        MAX_RECIPE_REPEATS = 3
        for _kcal_pass in range(payload.days * len(slots) * 2):
            worst_day = None
            worst_diff = 0
            for day in range(1, payload.days + 1):
                day_kcal = sum(
                    e["nutrition_per_serving"].get("kcal", 0)
                    for e in entries if e["day"] == day
                )
                diff = abs(day_kcal - payload.target_kcal)
                if diff > worst_diff:
                    worst_diff = diff
                    worst_day = day
            if worst_day is None or worst_diff <= payload.target_kcal * 0.15:
                break
            day_entries = [e for e in entries if e["day"] == worst_day]
            day_kcal = sum(e["nutrition_per_serving"].get("kcal", 0) for e in day_entries)
            need_less = day_kcal > payload.target_kcal
            best_swap = None
            best_new_diff = worst_diff
            for entry in day_entries:
                mt = slot_meal_type(entry["slot"])
                for candidate in by_type.get(mt, []):
                    if candidate["id"] == entry["recipe_id"]:
                        continue
                    count = sum(1 for e in entries if e["recipe_id"] == candidate["id"])
                    if count >= MAX_RECIPE_REPEATS:
                        continue
                    new_kcal = day_kcal - entry["nutrition_per_serving"].get("kcal", 0) + candidate["nutrition_per_serving"].get("kcal", 0)
                    new_diff = abs(new_kcal - payload.target_kcal)
                    if new_diff < best_new_diff:
                        if need_less and candidate["nutrition_per_serving"].get("kcal", 0) < entry["nutrition_per_serving"].get("kcal", 0):
                            best_new_diff = new_diff
                            best_swap = (entry, candidate)
                        elif not need_less and candidate["nutrition_per_serving"].get("kcal", 0) > entry["nutrition_per_serving"].get("kcal", 0):
                            best_new_diff = new_diff
                            best_swap = (entry, candidate)
            if best_swap is None:
                break
            old_entry, new_recipe = best_swap
            idx = entries.index(old_entry)
            entries[idx] = make_entry(new_recipe, old_entry["day"], old_entry["slot"])

    daily = []
    for day in range(1, payload.days + 1):
        totals = {"kcal": 0.0, "protein": 0.0, "fat": 0.0, "carbs": 0.0}
        for e in entries:
            if e["day"] == day:
                for k in totals:
                    totals[k] += e["nutrition_per_serving"].get(k, 0)
        daily.append({"day": day, **{k: round(v) for k, v in totals.items()}})

    shopping_items = build_shopping_items(pmap, entries, recipes_by_id, multiplier, household_size)

    await db.meal_plans.delete_many({"user_id": user["id"]})
    plan = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "store_id": store["id"],
        "store_name": store["name"],
        "days": payload.days,
        "meals_per_day": len(slots),
        "household_size": household_size,
        "budget": payload.budget,
        "entries": entries,
        "daily_nutrition": daily,
        "shopping_items": shopping_items,
        "total_price": round(sum(i["price"] for i in shopping_items), 2),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.meal_plans.insert_one(dict(plan))
    plan.pop("_id", None)
    return plan


@api.get("/meal-plans/active")
async def active_plan(user: dict = Depends(get_current_user)):
    plan = await db.meal_plans.find_one({"user_id": user["id"]}, {"_id": 0})
    return plan or None


@api.delete("/meal-plans/active")
async def delete_plan(user: dict = Depends(get_current_user)):
    await db.meal_plans.delete_many({"user_id": user["id"]})
    return {"ok": True}


@api.patch("/meal-plans/active/items/{item_id}")
async def toggle_item(item_id: str, payload: ToggleItemRequest, user: dict = Depends(get_current_user)):
    result = await db.meal_plans.update_one(
        {"user_id": user["id"], "shopping_items.id": item_id},
        {"$set": {"shopping_items.$.checked": payload.checked}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Nie znaleziono pozycji")
    return {"ok": True}


@api.post("/meal-plans/active/swap")
async def swap_meal(payload: SwapRequest, user: dict = Depends(get_current_user)):
    plan = await db.meal_plans.find_one({"user_id": user["id"]}, {"_id": 0})
    if not plan:
        raise HTTPException(status_code=404, detail="Brak aktywnego planu")
    entry_idx = None
    for i, e in enumerate(plan["entries"]):
        if e["day"] == payload.day and e["slot"] == payload.slot:
            entry_idx = i
            break
    if entry_idx is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono posiłku")
    old_entry = plan["entries"][entry_idx]
    mt = slot_meal_type(payload.slot)
    query = {"$or": [{"is_custom": False}, {"owner_id": user["id"]}], "meal_type": mt}
    candidates = await db.recipes.find(query, {"_id": 0}).to_list(500)
    candidates = [r for r in candidates if r["id"] != old_entry["recipe_id"]]
    if not candidates:
        raise HTTPException(status_code=400, detail="Brak alternatywnych przepisów")
    new_recipe = random.choice(candidates)
    plan["entries"][entry_idx] = make_entry(new_recipe, payload.day, payload.slot)
    # Przelicz dzienną kaloryczność
    daily = []
    for day in range(1, plan["days"] + 1):
        totals = {"kcal": 0.0, "protein": 0.0, "fat": 0.0, "carbs": 0.0}
        for e in plan["entries"]:
            if e["day"] == day:
                for k in totals:
                    totals[k] += e["nutrition_per_serving"].get(k, 0)
        daily.append({"day": day, **{k: round(v) for k, v in totals.items()}})
    plan["daily_nutrition"] = daily
    # Przelicz listę zakupów
    pmap = await products_map()
    store = await db.stores.find_one({"id": plan["store_id"]}, {"_id": 0})
    multiplier = store["price_multiplier"] if store else 1.0
    all_recipes = await db.recipes.find({}, {"_id": 0}).to_list(500)
    recipes_by_id = {r["id"]: r for r in all_recipes}
    plan["shopping_items"] = build_shopping_items(
        pmap, plan["entries"], recipes_by_id, multiplier, plan.get("household_size", 1)
    )
    plan["total_price"] = round(sum(i["price"] for i in plan["shopping_items"]), 2)
    await db.meal_plans.update_one(
        {"user_id": user["id"]},
        {"$set": {
            "entries": plan["entries"],
            "daily_nutrition": plan["daily_nutrition"],
            "shopping_items": plan["shopping_items"],
            "total_price": plan["total_price"],
        }},
    )
    return plan


@api.get("/")
async def root():
    return {"message": "Smart Meal Planner PL API"}


app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Seed ─────────────────────────────────────────────────────────
@app.on_event("startup")
async def seed():
    await db.users.create_index("email", unique=True)
    for store in STORES:
        doc = {"id": uid(f"store:{store['name']}"), **store}
        await db.stores.update_one({"id": doc["id"]}, {"$set": doc}, upsert=True)
    for name, unit, default_qty, dept, price, nutrition, weight in PRODUCTS:
        doc = {
            "id": uid(f"product:{name}"),
            "name": name,
            "unit": unit,
            "default_quantity": default_qty,
            "department": dept,
            "base_price": price,
            "nutrition_per_100": nutrition,
            "weight_per_unit_g": weight,
        }
        await db.products.update_one({"id": doc["id"]}, {"$set": doc}, upsert=True)
    pmap = await products_map()
    by_name = {p["name"]: p for p in pmap.values()}
    for r in RECIPES:
        ingredients = [
            {
                "product_id": by_name[n]["id"],
                "product_name": n,
                "quantity": q,
                "unit": u,
            }
            for n, q, u in r["ingredients"]
        ]
        total = compute_nutrition(pmap, ingredients)
        per_serving = {k: round(v / r["servings"], 1) for k, v in total.items()}
        doc = {
            "id": uid(f"recipe:{r['name']}"),
            "name": r["name"],
            "description": r["description"],
            "cuisine": r["cuisine"],
            "meal_type": r["meal_type"],
            "prep_time_min": r["prep_time_min"],
            "cook_time_min": r["cook_time_min"],
            "servings": r["servings"],
            "difficulty": r["difficulty"],
            "tags": r["tags"],
            "ingredients": ingredients,
            "nutrition_total": total,
            "nutrition_per_serving": per_serving,
            "image_url": RECIPE_IMAGES.get(r["name"]),
            "instructions": r.get("instructions", []),
            "is_custom": False,
            "owner_id": None,
        }
        await db.recipes.update_one({"id": doc["id"]}, {"$set": doc}, upsert=True)
    logger.info("Seed zakończony: %d przepisów", len(RECIPES))


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
