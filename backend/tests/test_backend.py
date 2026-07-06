"""Full backend test suite for Smart Meal Planner PL."""
import os
import uuid
import pytest
import requests

BASE_URL = os.environ.get("EXPO_PUBLIC_BACKEND_URL", "").rstrip("/")
API = f"{BASE_URL}/api"


# ── AUTH ─────────────────────────────────────────────────────────
class TestAuth:
    def test_register_login_me(self, http):
        email = f"test_{uuid.uuid4().hex[:8]}@mealplanner.pl"
        r = http.post(f"{API}/auth/register", json={
            "email": email, "password": "Passw0rd!", "display_name": "New User"
        })
        assert r.status_code == 201, r.text
        body = r.json()
        assert "token" in body and body["user"]["email"] == email.lower()
        assert "password_hash" not in body["user"]
        assert "_id" not in body["user"]

        r = http.post(f"{API}/auth/login", json={"email": email, "password": "Passw0rd!"})
        assert r.status_code == 200
        token = r.json()["token"]

        r = http.get(f"{API}/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert r.json()["email"] == email

    def test_login_wrong_password(self, http):
        r = http.post(f"{API}/auth/login", json={"email": "test@mealplanner.pl", "password": "wrong"})
        assert r.status_code == 401

    def test_register_duplicate(self, http):
        r = http.post(f"{API}/auth/register", json={
            "email": "test@mealplanner.pl", "password": "Test123!", "display_name": "X"
        })
        assert r.status_code == 400

    def test_me_no_auth(self, http):
        r = http.get(f"{API}/auth/me")
        assert r.status_code == 401


# ── STORES / PRODUCTS ────────────────────────────────────────────
class TestCatalog:
    def test_stores(self, http):
        r = http.get(f"{API}/stores")
        assert r.status_code == 200
        stores = r.json()
        names = {s["name"] for s in stores}
        assert {"Biedronka", "Lidl", "Dino"}.issubset(names)
        for s in stores:
            assert "_id" not in s
            assert "price_multiplier" in s

    def test_products(self, http):
        r = http.get(f"{API}/products")
        assert r.status_code == 200
        products = r.json()
        assert len(products) >= 40
        for p in products[:5]:
            assert "_id" not in p
            assert "nutrition_per_100" in p


# ── RECIPES ──────────────────────────────────────────────────────
class TestRecipes:
    def test_list_recipes_requires_auth(self, http):
        r = http.get(f"{API}/recipes")
        assert r.status_code == 401

    def test_list_recipes_23(self, http, auth_headers):
        r = http.get(f"{API}/recipes", headers=auth_headers)
        assert r.status_code == 200
        recipes = r.json()
        base = [x for x in recipes if not x.get("is_custom")]
        assert len(base) == 23, f"Expected 23 base recipes, got {len(base)}"
        # sanity on macros
        for rec in base[:5]:
            per = rec["nutrition_per_serving"]
            assert per["kcal"] > 0
            assert "_id" not in rec

    def test_filter_meal_types(self, http, auth_headers):
        counts = {}
        for mt in ["śniadanie", "obiad", "kolacja", "przekąska"]:
            r = http.get(f"{API}/recipes", headers=auth_headers, params={"meal_type": mt})
            assert r.status_code == 200
            recs = r.json()
            counts[mt] = len(recs)
            for rec in recs:
                assert rec["meal_type"] == mt
        # 23 base recipes total
        total_base = sum(
            len([x for x in http.get(f"{API}/recipes", headers=auth_headers, params={"meal_type": mt}).json() if not x.get("is_custom")])
            for mt in ["śniadanie", "obiad", "kolacja", "przekąska"]
        )
        assert total_base == 23

    def test_get_recipe_by_id(self, http, auth_headers):
        recipes = http.get(f"{API}/recipes", headers=auth_headers).json()
        rid = recipes[0]["id"]
        r = http.get(f"{API}/recipes/{rid}", headers=auth_headers)
        assert r.status_code == 200
        assert r.json()["id"] == rid

    def test_get_recipe_404(self, http, auth_headers):
        r = http.get(f"{API}/recipes/nonexistent-id", headers=auth_headers)
        assert r.status_code == 404


# ── CUSTOM RECIPE CRUD + NUTRITION ───────────────────────────────
class TestCustomRecipe:
    def test_create_custom_recipe_and_delete(self, http, auth_headers):
        products = http.get(f"{API}/products").json()
        # find a couple of known products
        by_name = {p["name"]: p for p in products}
        eggs = by_name["Jajka"]
        milk = by_name["Mleko 2%"]

        payload = {
            "name": "TEST_Custom Omelet",
            "description": "test",
            "meal_type": "śniadanie",
            "servings": 2,
            "prep_time_min": 5,
            "cook_time_min": 5,
            "ingredients": [
                {"product_id": eggs["id"], "quantity": 4, "unit": "szt"},
                {"product_id": milk["id"], "quantity": 0.1, "unit": "l"},
            ],
        }
        r = http.post(f"{API}/recipes", json=payload, headers=auth_headers)
        assert r.status_code == 201, r.text
        recipe = r.json()
        assert recipe["is_custom"] is True
        assert "_id" not in recipe

        # Verify nutrition math: 4 eggs * 50g = 200g eggs -> 200*143/100 = 286 kcal
        # 100 ml milk -> 100*50/100 = 50 kcal. Total ~336 kcal
        total = recipe["nutrition_total"]
        assert 300 <= total["kcal"] <= 360, f"Unexpected kcal: {total['kcal']}"
        per = recipe["nutrition_per_serving"]
        assert abs(per["kcal"] - total["kcal"] / 2) < 1

        # GET verify persistence
        rid = recipe["id"]
        g = http.get(f"{API}/recipes/{rid}", headers=auth_headers)
        assert g.status_code == 200
        assert g.json()["name"] == "TEST_Custom Omelet"

        # DELETE own recipe works
        d = http.delete(f"{API}/recipes/{rid}", headers=auth_headers)
        assert d.status_code == 200

        # Verify 404 after delete
        g2 = http.get(f"{API}/recipes/{rid}", headers=auth_headers)
        assert g2.status_code == 404

    def test_delete_base_recipe_forbidden(self, http, auth_headers):
        recipes = http.get(f"{API}/recipes", headers=auth_headers).json()
        base = [r for r in recipes if not r.get("is_custom")][0]
        r = http.delete(f"{API}/recipes/{base['id']}", headers=auth_headers)
        assert r.status_code == 403

    def test_delete_other_users_recipe_forbidden(self, http, auth_headers, fresh_user):
        # Fresh user creates recipe, main test user attempts to delete
        products = http.get(f"{API}/products").json()
        p0 = products[0]
        payload = {
            "name": "TEST_Fresh Recipe",
            "meal_type": "obiad",
            "servings": 1,
            "ingredients": [{"product_id": p0["id"], "quantity": 100, "unit": "g"}],
        }
        r = http.post(f"{API}/recipes", json=payload, headers=fresh_user["headers"])
        assert r.status_code == 201
        rid = r.json()["id"]

        # main user tries to delete
        d = http.delete(f"{API}/recipes/{rid}", headers=auth_headers)
        assert d.status_code == 403

        # cleanup
        http.delete(f"{API}/recipes/{rid}", headers=fresh_user["headers"])


# ── MEAL PLANS ───────────────────────────────────────────────────
class TestMealPlans:
    def test_generate_plan_3days_4meals(self, http, auth_headers):
        stores = http.get(f"{API}/stores").json()
        biedronka = next(s for s in stores if s["name"] == "Biedronka")

        r = http.post(f"{API}/meal-plans/generate",
                      json={"days": 3, "meals_per_day": 4, "store_id": biedronka["id"]},
                      headers=auth_headers)
        assert r.status_code == 201, r.text
        plan = r.json()
        assert "_id" not in plan
        assert len(plan["entries"]) == 12
        assert len(plan["daily_nutrition"]) == 3
        assert plan["store_name"] == "Biedronka"
        assert plan["total_price"] > 0
        assert len(plan["shopping_items"]) > 0
        # All shopping items must have required fields
        for it in plan["shopping_items"]:
            assert {"id", "name", "quantity", "unit", "department", "price", "checked"}.issubset(it.keys())
            assert it["checked"] is False
        # meal slots include all 4
        slots = {e["slot"] for e in plan["entries"]}
        assert slots == {"śniadanie", "obiad", "kolacja", "przekąska"}

    def test_generate_3meals(self, http, auth_headers):
        stores = http.get(f"{API}/stores").json()
        lidl = next(s for s in stores if s["name"] == "Lidl")
        r = http.post(f"{API}/meal-plans/generate",
                      json={"days": 2, "meals_per_day": 3, "store_id": lidl["id"]},
                      headers=auth_headers)
        assert r.status_code == 201
        plan = r.json()
        assert len(plan["entries"]) == 6
        slots = {e["slot"] for e in plan["entries"]}
        assert slots == {"śniadanie", "obiad", "kolacja"}

    def test_invalid_store(self, http, auth_headers):
        r = http.post(f"{API}/meal-plans/generate",
                      json={"days": 1, "meals_per_day": 3, "store_id": "invalid-id"},
                      headers=auth_headers)
        assert r.status_code == 400

    def test_active_plan_and_toggle(self, http, auth_headers):
        # Ensure a plan exists
        stores = http.get(f"{API}/stores").json()
        r = http.post(f"{API}/meal-plans/generate",
                      json={"days": 1, "meals_per_day": 3, "store_id": stores[0]["id"]},
                      headers=auth_headers)
        assert r.status_code == 201

        r = http.get(f"{API}/meal-plans/active", headers=auth_headers)
        assert r.status_code == 200
        plan = r.json()
        assert plan is not None
        item = plan["shopping_items"][0]
        item_id = item["id"]

        # PATCH toggle
        p = http.patch(f"{API}/meal-plans/active/items/{item_id}",
                       json={"checked": True}, headers=auth_headers)
        assert p.status_code == 200

        # Verify persistence
        r2 = http.get(f"{API}/meal-plans/active", headers=auth_headers)
        toggled = next(x for x in r2.json()["shopping_items"] if x["id"] == item_id)
        assert toggled["checked"] is True

        # PATCH unknown item
        p2 = http.patch(f"{API}/meal-plans/active/items/unknown",
                        json={"checked": True}, headers=auth_headers)
        assert p2.status_code == 404

    def test_delete_active_plan(self, http, auth_headers):
        stores = http.get(f"{API}/stores").json()
        http.post(f"{API}/meal-plans/generate",
                  json={"days": 1, "meals_per_day": 3, "store_id": stores[0]["id"]},
                  headers=auth_headers)
        d = http.delete(f"{API}/meal-plans/active", headers=auth_headers)
        assert d.status_code == 200
        r = http.get(f"{API}/meal-plans/active", headers=auth_headers)
        assert r.status_code == 200
        assert r.json() is None
