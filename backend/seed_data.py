"""Dane startowe Smart Meal Planner PL — produkty, sklepy, przepisy.

Wartości odżywcze na 100 g/ml zweryfikowane z tabelami wartości odżywczych
(USDA / Kunachowicz). Kcal i makro przepisów liczone automatycznie ze składników.
"""
import uuid

NS = uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567890")


def uid(name: str) -> str:
    return str(uuid.uuid5(NS, name))


STORES = [
    {"name": "Biedronka", "price_multiplier": 1.00},
    {"name": "Lidl", "price_multiplier": 1.05},
    {"name": "Dino", "price_multiplier": 1.12},
]

DEPARTMENT_ORDER = [
    "Warzywa i owoce",
    "Pieczywo",
    "Mięso i wędliny",
    "Ryby",
    "Nabiał",
    "Produkty suche",
    "Mrożonki",
    "Przyprawy i sosy",
]

# Zdjęcia przepisów (Unsplash) — dobrane i zweryfikowane wizualnie per potrawa.
_IMG = "https://images.unsplash.com/{}?w=1200&q=80&fm=jpg"
RECIPE_IMAGES = {
    "Jabłko z masłem orzechowym": _IMG.format("photo-1568702846914-96b305d2aaeb"),
    "Marchewki z hummusem": _IMG.format("photo-1447175008436-054170c2e979"),
    "Jogurt naturalny z malinami": _IMG.format("photo-1488477181946-6428a0291777"),
    "Koktajl bananowo-malinowy": _IMG.format("photo-1553530666-ba11a7da3888"),
    "Bułka z hummusem i papryką": _IMG.format("photo-1637949385162-e416fb15b2ce"),
    "Owsianka na mleku migdałowym": _IMG.format("photo-1571748982800-fa51082c2224"),
    "Owsianka z jogurtem": _IMG.format("photo-1571748982800-fa51082c2224"),
    "Jajecznica z pomidorami": _IMG.format("photo-1551185618-5d8656fd00b1"),
    "Kanapki z szynką i serem": _IMG.format("photo-1554433607-66b5efe9d304"),
    "Tosty francuskie": _IMG.format("photo-1484723091739-30a097e8f929"),
    "Omlet ze szpinakiem i fetą": _IMG.format("photo-1510693206972-df098062cb71"),
    "Kotlet schabowy z ziemniakami": _IMG.format("photo-1599921841143-819065a55cc6"),
    "Spaghetti bolognese": _IMG.format("photo-1551892374-ecf8754cf8b0"),
    "Kurczak z ryżem i warzywami": _IMG.format("photo-1512058564366-18510be2db19"),
    "Zupa pomidorowa z makaronem": _IMG.format("photo-1547592166-23ac45744acd"),
    "Gulasz z kurczaka z warzywami": _IMG.format("photo-1541518763669-27fef04b14ea"),
    "Makaron ze szpinakiem i fetą": _IMG.format("photo-1473093295043-cdd812d0e601"),
    "Sałatka grecka": _IMG.format("photo-1540420773420-3366772f4999"),
    "Sałatka z łososiem": _IMG.format("photo-1467003909585-2f8a72700288"),
    "Naleśniki z serem": _IMG.format("photo-1519676867240-f03562e64548"),
    "Tosty z jajkiem i awokado": _IMG.format("photo-1525351484163-7529414344d8"),
    "Sałatka z kurczakiem i awokado": _IMG.format("photo-1512621776951-a57141f2eefd"),
    "Kanapki z twarożkiem i ogórkiem": _IMG.format("photo-1598373182133-52452f7691ef"),
}

# (nazwa, jednostka, wielkość_opakowania, dział, cena_bazowa, nutrition/100g, waga_1szt_g)
# UWAGA: "Ryż biały" — wartości dla ryżu SUCHEGO (przepisy podają wagę suchą),
# poprzednio 130 kcal (ryż ugotowany) zaniżało kaloryczność obiadów.
PRODUCTS = [
    ("Mleko 2%", "l", 1, "Nabiał", 3.49, {"kcal": 50, "protein": 3.3, "fat": 2.0, "carbs": 4.8, "fiber": 0.0}, None),
    ("Masło extra", "g", 200, "Nabiał", 6.99, {"kcal": 748, "protein": 0.7, "fat": 82.5, "carbs": 0.7, "fiber": 0.0}, None),
    ("Ser żółty gouda", "g", 200, "Nabiał", 7.49, {"kcal": 356, "protein": 24.9, "fat": 27.4, "carbs": 2.2, "fiber": 0.0}, None),
    ("Jogurt naturalny", "g", 400, "Nabiał", 3.29, {"kcal": 61, "protein": 4.3, "fat": 3.0, "carbs": 4.2, "fiber": 0.0}, None),
    ("Śmietana 18%", "ml", 200, "Nabiał", 2.49, {"kcal": 186, "protein": 2.5, "fat": 18.0, "carbs": 3.6, "fiber": 0.0}, None),
    ("Twaróg półtłusty", "g", 250, "Nabiał", 4.99, {"kcal": 133, "protein": 18.7, "fat": 4.7, "carbs": 3.7, "fiber": 0.0}, None),
    ("Chleb pszenny", "g", 500, "Pieczywo", 4.29, {"kcal": 265, "protein": 8.0, "fat": 1.3, "carbs": 55.0, "fiber": 3.0}, None),
    ("Bułka kajzerka", "szt", 1, "Pieczywo", 0.59, {"kcal": 296, "protein": 8.5, "fat": 1.6, "carbs": 61.0, "fiber": 2.0}, 50),
    ("Pierś z kurczaka", "kg", 1, "Mięso i wędliny", 21.99, {"kcal": 120, "protein": 22.5, "fat": 2.6, "carbs": 0.0, "fiber": 0.0}, None),
    ("Mielone wieprzowo-wołowe", "g", 500, "Mięso i wędliny", 12.99, {"kcal": 250, "protein": 16.0, "fat": 20.0, "carbs": 0.0, "fiber": 0.0}, None),
    ("Szynka konserwowa", "g", 100, "Mięso i wędliny", 4.49, {"kcal": 105, "protein": 16.0, "fat": 4.0, "carbs": 1.0, "fiber": 0.0}, None),
    ("Schab wieprzowy", "kg", 1, "Mięso i wędliny", 18.99, {"kcal": 152, "protein": 21.0, "fat": 7.0, "carbs": 0.0, "fiber": 0.0}, None),
    ("Jajka", "szt", 10, "Nabiał", 8.99, {"kcal": 143, "protein": 12.6, "fat": 9.5, "carbs": 0.7, "fiber": 0.0}, 50),
    ("Łosoś wędzony", "g", 100, "Ryby", 9.99, {"kcal": 162, "protein": 25.4, "fat": 5.4, "carbs": 0.0, "fiber": 0.0}, None),
    ("Pomidory", "kg", 1, "Warzywa i owoce", 7.99, {"kcal": 18, "protein": 0.9, "fat": 0.2, "carbs": 3.9, "fiber": 1.2}, None),
    ("Ogórek", "szt", 1, "Warzywa i owoce", 2.49, {"kcal": 15, "protein": 0.7, "fat": 0.1, "carbs": 3.6, "fiber": 0.5}, 150),
    ("Cebula", "kg", 1, "Warzywa i owoce", 2.99, {"kcal": 40, "protein": 1.1, "fat": 0.1, "carbs": 9.3, "fiber": 1.7}, None),
    ("Ziemniaki", "kg", 1, "Warzywa i owoce", 3.49, {"kcal": 77, "protein": 2.0, "fat": 0.1, "carbs": 17.5, "fiber": 2.2}, None),
    ("Marchew", "kg", 1, "Warzywa i owoce", 2.99, {"kcal": 41, "protein": 0.9, "fat": 0.2, "carbs": 9.6, "fiber": 2.8}, None),
    ("Papryka czerwona", "szt", 1, "Warzywa i owoce", 4.49, {"kcal": 31, "protein": 1.0, "fat": 0.3, "carbs": 6.0, "fiber": 2.1}, 200),
    ("Sałata lodowa", "szt", 1, "Warzywa i owoce", 3.99, {"kcal": 14, "protein": 0.9, "fat": 0.1, "carbs": 3.0, "fiber": 1.2}, 300),
    ("Czosnek", "szt", 1, "Warzywa i owoce", 1.99, {"kcal": 149, "protein": 6.4, "fat": 0.5, "carbs": 33.0, "fiber": 2.1}, 5),
    ("Awokado", "szt", 1, "Warzywa i owoce", 5.99, {"kcal": 160, "protein": 2.0, "fat": 14.7, "carbs": 8.5, "fiber": 6.7}, 150),
    ("Makaron penne", "g", 500, "Produkty suche", 4.49, {"kcal": 350, "protein": 12.0, "fat": 1.5, "carbs": 71.0, "fiber": 3.0}, None),
    ("Ryż biały", "kg", 1, "Produkty suche", 5.99, {"kcal": 349, "protein": 7.0, "fat": 0.6, "carbs": 77.0, "fiber": 1.3}, None),
    ("Mąka pszenna", "kg", 1, "Produkty suche", 3.49, {"kcal": 364, "protein": 10.3, "fat": 1.0, "carbs": 76.0, "fiber": 2.7}, None),
    ("Passata pomidorowa", "g", 500, "Produkty suche", 4.99, {"kcal": 32, "protein": 1.6, "fat": 0.2, "carbs": 5.3, "fiber": 1.5}, None),
    ("Fasola konserwowa", "g", 400, "Produkty suche", 3.49, {"kcal": 85, "protein": 5.5, "fat": 0.4, "carbs": 12.0, "fiber": 5.0}, None),
    ("Płatki owsiane", "g", 500, "Produkty suche", 3.99, {"kcal": 389, "protein": 16.9, "fat": 6.9, "carbs": 66.0, "fiber": 10.6}, None),
    ("Bułka tarta", "g", 500, "Produkty suche", 3.99, {"kcal": 395, "protein": 14.0, "fat": 2.0, "carbs": 78.0, "fiber": 4.0}, None),
    ("Olej rzepakowy", "l", 1, "Produkty suche", 7.99, {"kcal": 884, "protein": 0.0, "fat": 100.0, "carbs": 0.0, "fiber": 0.0}, None),
    ("Oliwa z oliwek", "ml", 500, "Produkty suche", 16.99, {"kcal": 884, "protein": 0.0, "fat": 100.0, "carbs": 0.0, "fiber": 0.0}, None),
    ("Sól", "kg", 1, "Przyprawy i sosy", 1.99, {"kcal": 0, "protein": 0.0, "fat": 0.0, "carbs": 0.0, "fiber": 0.0}, None),
    ("Pieprz czarny mielony", "g", 20, "Przyprawy i sosy", 3.49, {"kcal": 251, "protein": 10.4, "fat": 3.3, "carbs": 64.0, "fiber": 25.3}, None),
    ("Papryka słodka", "g", 20, "Przyprawy i sosy", 3.29, {"kcal": 282, "protein": 14.1, "fat": 12.9, "carbs": 54.0, "fiber": 34.9}, None),
    ("Bazylia suszona", "g", 10, "Przyprawy i sosy", 2.99, {"kcal": 233, "protein": 23.0, "fat": 4.1, "carbs": 47.8, "fiber": 37.7}, None),
    ("Mrożone warzywa mieszanka", "g", 450, "Mrożonki", 5.49, {"kcal": 35, "protein": 2.0, "fat": 0.2, "carbs": 6.0, "fiber": 2.5}, None),
    ("Mrożony szpinak", "g", 450, "Mrożonki", 4.99, {"kcal": 23, "protein": 2.9, "fat": 0.4, "carbs": 3.6, "fiber": 2.2}, None),
    ("Jabłka", "kg", 1, "Warzywa i owoce", 3.49, {"kcal": 52, "protein": 0.3, "fat": 0.2, "carbs": 13.8, "fiber": 2.4}, 150),
    ("Masło orzechowe", "g", 300, "Produkty suche", 9.99, {"kcal": 588, "protein": 25.0, "fat": 50.0, "carbs": 20.0, "fiber": 6.0}, None),
    ("Hummus", "g", 200, "Nabiał", 4.99, {"kcal": 166, "protein": 7.9, "fat": 9.6, "carbs": 14.3, "fiber": 6.0}, None),
    ("Banan", "kg", 1, "Warzywa i owoce", 4.99, {"kcal": 89, "protein": 1.1, "fat": 0.3, "carbs": 22.8, "fiber": 2.6}, 120),
    ("Maliny", "g", 125, "Warzywa i owoce", 7.99, {"kcal": 52, "protein": 1.2, "fat": 0.6, "carbs": 11.9, "fiber": 6.5}, None),
    ("Mleko migdałowe", "l", 1, "Produkty suche", 7.99, {"kcal": 15, "protein": 0.5, "fat": 1.2, "carbs": 0.3, "fiber": 0.0}, None),
    ("Ser feta", "g", 200, "Nabiał", 6.49, {"kcal": 264, "protein": 14.2, "fat": 21.3, "carbs": 4.1, "fiber": 0.0}, None),
    ("Oliwki czarne", "g", 150, "Produkty suche", 5.99, {"kcal": 115, "protein": 0.8, "fat": 10.7, "carbs": 6.3, "fiber": 3.2}, None),
]

# ══════════════════════════════════════════════════════════════════
# PRZEPISY — kcal/makro liczone automatycznie ze składników.
# Korekty "sensowności":
#  • olej do smażenia liczony wg realnej absorpcji (schabowy 100→40 ml),
#  • spaghetti: makaron 250→200 g, mięso 300→250 g (realna porcja ~800 kcal),
#  • ryż liczony jako suchy (349 kcal/100 g zamiast 130 dla ugotowanego),
#  • jajecznica: dodano pieczywo (było w opisie, brakowało w składnikach).
# ══════════════════════════════════════════════════════════════════
RECIPES = [
    # ── PRZEKĄSKI ────────────────────────────────────────────────
    {
        "name": "Jabłko z masłem orzechowym",
        "description": "Szybka i pożywna przekąska na słodko. Pokrój jabłko w cząstki i maczaj w maśle orzechowym.",
        "cuisine": "polska", "meal_type": "przekąska", "prep_time_min": 2, "cook_time_min": 0,
        "servings": 1, "difficulty": "łatwy", "tags": ["szybkie", "bezglutenowe", "wegańskie"],
        "ingredients": [("Jabłka", 1, "szt"), ("Masło orzechowe", 30, "g")],
    },
    {
        "name": "Marchewki z hummusem",
        "description": "Chrupiące słupki marchewki maczane w kremowym hummusie.",
        "cuisine": "azjatycka", "meal_type": "przekąska", "prep_time_min": 5, "cook_time_min": 0,
        "servings": 1, "difficulty": "łatwy", "tags": ["szybkie", "bezglutenowe", "wegańskie"],
        "ingredients": [("Marchew", 0.2, "kg"), ("Hummus", 50, "g")],
    },
    {
        "name": "Jogurt naturalny z malinami",
        "description": "Lekka przekąska białkowa — jogurt z garścią świeżych malin.",
        "cuisine": "polska", "meal_type": "przekąska", "prep_time_min": 2, "cook_time_min": 0,
        "servings": 1, "difficulty": "łatwy", "tags": ["szybkie", "bezglutenowe", "wegetariańskie"],
        "ingredients": [("Jogurt naturalny", 150, "g"), ("Maliny", 50, "g")],
    },
    {   # NOWOŚĆ
        "name": "Koktajl bananowo-malinowy",
        "description": "Kremowy koktajl: zblenduj banana, maliny, jogurt i mleko. Gotowe w 3 minuty.",
        "cuisine": "polska", "meal_type": "przekąska", "prep_time_min": 3, "cook_time_min": 0,
        "servings": 1, "difficulty": "łatwy", "tags": ["szybkie", "wegetariańskie", "nowość"],
        "ingredients": [("Banan", 1, "szt"), ("Maliny", 60, "g"), ("Jogurt naturalny", 150, "g"), ("Mleko 2%", 0.1, "l")],
    },
    {   # NOWOŚĆ
        "name": "Bułka z hummusem i papryką",
        "description": "Chrupiąca kajzerka posmarowana hummusem, z plastrami świeżej papryki.",
        "cuisine": "polska", "meal_type": "przekąska", "prep_time_min": 4, "cook_time_min": 0,
        "servings": 1, "difficulty": "łatwy", "tags": ["szybkie", "wegańskie", "nowość"],
        "ingredients": [("Bułka kajzerka", 1, "szt"), ("Hummus", 40, "g"), ("Papryka czerwona", 0.5, "szt")],
    },
    # ── ŚNIADANIA ────────────────────────────────────────────────
    {
        "name": "Owsianka na mleku migdałowym",
        "description": "Owsianka na mleku roślinnym z plastrami banana.",
        "cuisine": "polska", "meal_type": "śniadanie", "prep_time_min": 10, "cook_time_min": 0,
        "servings": 1, "difficulty": "łatwy", "tags": ["wegetariańskie", "zdrowe"],
        "ingredients": [("Płatki owsiane", 50, "g"), ("Mleko migdałowe", 0.2, "l"), ("Banan", 1, "szt")],
    },
    {
        "name": "Jajecznica z pomidorami",
        "description": "Klasyczna jajecznica z dojrzałymi pomidorami, podawana z pieczywem.",
        "cuisine": "polska", "meal_type": "śniadanie", "prep_time_min": 5, "cook_time_min": 5,
        "servings": 2, "difficulty": "łatwy", "tags": ["szybkie"],
        "ingredients": [("Jajka", 4, "szt"), ("Pomidory", 0.2, "kg"), ("Masło extra", 20, "g"),
                        ("Chleb pszenny", 100, "g"), ("Sól", 2, "g"), ("Pieprz czarny mielony", 1, "g")],
    },
    {
        "name": "Kanapki z szynką i serem",
        "description": "Proste kanapki na śniadanie z szynką, serem i warzywami.",
        "cuisine": "polska", "meal_type": "śniadanie", "prep_time_min": 5, "cook_time_min": 0,
        "servings": 2, "difficulty": "łatwy", "tags": ["szybkie"],
        "ingredients": [("Chleb pszenny", 200, "g"), ("Masło extra", 20, "g"), ("Szynka konserwowa", 100, "g"),
                        ("Ser żółty gouda", 80, "g"), ("Ogórek", 1, "szt"), ("Sałata lodowa", 0.25, "szt")],
    },
    {
        "name": "Owsianka z jogurtem",
        "description": "Ciepła owsianka z jogurtem naturalnym, idealna na pożywne śniadanie.",
        "cuisine": "polska", "meal_type": "śniadanie", "prep_time_min": 5, "cook_time_min": 5,
        "servings": 2, "difficulty": "łatwy", "tags": ["wegetariańskie", "zdrowe"],
        "ingredients": [("Płatki owsiane", 100, "g"), ("Mleko 2%", 0.3, "l"), ("Jogurt naturalny", 150, "g"), ("Sól", 1, "g")],
    },
    {   # NOWOŚĆ
        "name": "Tosty francuskie",
        "description": "Kromki chleba moczone w jajku z mlekiem, smażone na maśle na złoto.",
        "cuisine": "francuska", "meal_type": "śniadanie", "prep_time_min": 5, "cook_time_min": 10,
        "servings": 2, "difficulty": "łatwy", "tags": ["szybkie", "wegetariańskie", "nowość"],
        "ingredients": [("Chleb pszenny", 150, "g"), ("Jajka", 2, "szt"), ("Mleko 2%", 0.1, "l"), ("Masło extra", 20, "g")],
    },
    {   # NOWOŚĆ
        "name": "Omlet ze szpinakiem i fetą",
        "description": "Puszysty omlet z podsmażonym szpinakiem i pokruszoną fetą.",
        "cuisine": "polska", "meal_type": "śniadanie", "prep_time_min": 5, "cook_time_min": 8,
        "servings": 1, "difficulty": "łatwy", "tags": ["wysokobiałkowe", "bezglutenowe", "nowość"],
        "ingredients": [("Jajka", 3, "szt"), ("Mrożony szpinak", 100, "g"), ("Ser feta", 40, "g"),
                        ("Masło extra", 10, "g"), ("Sól", 1, "g"), ("Pieprz czarny mielony", 1, "g")],
    },
    # ── OBIADY ───────────────────────────────────────────────────
    {
        "name": "Kotlet schabowy z ziemniakami",
        "description": "Tradycyjny polski kotlet schabowy w panierce, podawany z ziemniakami.",
        "cuisine": "polska", "meal_type": "obiad", "prep_time_min": 15, "cook_time_min": 25,
        "servings": 2, "difficulty": "średni", "tags": ["tradycyjne", "polska kuchnia"],
        "ingredients": [("Schab wieprzowy", 0.4, "kg"), ("Mąka pszenna", 30, "g"), ("Jajka", 2, "szt"),
                        ("Bułka tarta", 60, "g"), ("Ziemniaki", 0.5, "kg"), ("Olej rzepakowy", 0.04, "l"),
                        ("Sól", 3, "g"), ("Pieprz czarny mielony", 1, "g")],
    },
    {
        "name": "Spaghetti bolognese",
        "description": "Klasyczne spaghetti z mięsnym sosem bolońskim na passacie pomidorowej.",
        "cuisine": "włoska", "meal_type": "obiad", "prep_time_min": 10, "cook_time_min": 25,
        "servings": 2, "difficulty": "średni", "tags": ["włoska kuchnia"],
        "ingredients": [("Makaron penne", 200, "g"), ("Mielone wieprzowo-wołowe", 250, "g"),
                        ("Passata pomidorowa", 250, "g"), ("Cebula", 0.15, "kg"), ("Czosnek", 0.5, "szt"),
                        ("Oliwa z oliwek", 15, "ml"), ("Sól", 3, "g"), ("Pieprz czarny mielony", 1, "g"),
                        ("Bazylia suszona", 2, "g")],
    },
    {
        "name": "Kurczak z ryżem i warzywami",
        "description": "Lekki obiad — grillowana pierś z kurczaka z ryżem i warzywami.",
        "cuisine": "polska", "meal_type": "obiad", "prep_time_min": 10, "cook_time_min": 20,
        "servings": 2, "difficulty": "łatwy", "tags": ["zdrowe", "wysokobiałkowe"],
        "ingredients": [("Pierś z kurczaka", 0.4, "kg"), ("Ryż biały", 0.15, "kg"), ("Marchew", 0.2, "kg"),
                        ("Papryka czerwona", 1, "szt"), ("Cebula", 0.1, "kg"), ("Olej rzepakowy", 0.02, "l"),
                        ("Sól", 3, "g"), ("Pieprz czarny mielony", 1, "g")],
    },
    {
        "name": "Zupa pomidorowa z makaronem",
        "description": "Domowa zupa pomidorowa na passacie, podawana z drobnym makaronem.",
        "cuisine": "polska", "meal_type": "obiad", "prep_time_min": 10, "cook_time_min": 20,
        "servings": 4, "difficulty": "łatwy", "tags": ["tradycyjne", "polska kuchnia", "zupy"],
        "ingredients": [("Passata pomidorowa", 500, "g"), ("Makaron penne", 150, "g"), ("Marchew", 0.2, "kg"),
                        ("Cebula", 0.1, "kg"), ("Masło extra", 20, "g"), ("Śmietana 18%", 100, "ml"),
                        ("Sól", 5, "g"), ("Pieprz czarny mielony", 1, "g")],
    },
    {   # NOWOŚĆ
        "name": "Gulasz z kurczaka z warzywami",
        "description": "Prosty gulasz z piersi kurczaka duszony z papryką, marchewką i ziemniakami.",
        "cuisine": "polska", "meal_type": "obiad", "prep_time_min": 15, "cook_time_min": 30,
        "servings": 2, "difficulty": "łatwy", "tags": ["zdrowe", "wysokobiałkowe", "nowość"],
        "ingredients": [("Pierś z kurczaka", 0.4, "kg"), ("Ziemniaki", 0.5, "kg"), ("Cebula", 0.1, "kg"),
                        ("Papryka czerwona", 1, "szt"), ("Marchew", 0.15, "kg"), ("Passata pomidorowa", 200, "g"),
                        ("Olej rzepakowy", 0.02, "l"), ("Papryka słodka", 4, "g"), ("Sól", 3, "g")],
    },
    {   # NOWOŚĆ
        "name": "Makaron ze szpinakiem i fetą",
        "description": "Penne w kremowym sosie szpinakowym z fetą i czosnkiem. Obiad w 20 minut.",
        "cuisine": "włoska", "meal_type": "obiad", "prep_time_min": 5, "cook_time_min": 15,
        "servings": 2, "difficulty": "łatwy", "tags": ["wegetariańskie", "szybkie", "nowość"],
        "ingredients": [("Makaron penne", 200, "g"), ("Mrożony szpinak", 300, "g"), ("Ser feta", 100, "g"),
                        ("Czosnek", 2, "szt"), ("Oliwa z oliwek", 15, "ml"), ("Śmietana 18%", 100, "ml"),
                        ("Sól", 2, "g"), ("Pieprz czarny mielony", 1, "g")],
    },
    # ── KOLACJE ──────────────────────────────────────────────────
    {
        "name": "Sałatka grecka",
        "description": "Klasyczna sałatka z fetą i oliwkami.",
        "cuisine": "grecka", "meal_type": "kolacja", "prep_time_min": 15, "cook_time_min": 0,
        "servings": 2, "difficulty": "łatwy", "tags": ["wegetariańskie", "bezglutenowe"],
        "ingredients": [("Pomidory", 0.3, "kg"), ("Ogórek", 1, "szt"), ("Cebula", 0.1, "kg"),
                        ("Ser feta", 100, "g"), ("Oliwki czarne", 50, "g"), ("Oliwa z oliwek", 20, "ml")],
    },
    {
        "name": "Sałatka z łososiem",
        "description": "Lekka sałatka z wędzonym łososiem, ogórkiem i pomidorami.",
        "cuisine": "polska", "meal_type": "kolacja", "prep_time_min": 15, "cook_time_min": 0,
        "servings": 2, "difficulty": "łatwy", "tags": ["zdrowe", "lekkie", "wysokobiałkowe"],
        "ingredients": [("Łosoś wędzony", 100, "g"), ("Sałata lodowa", 0.5, "szt"), ("Ogórek", 1, "szt"),
                        ("Pomidory", 0.2, "kg"), ("Oliwa z oliwek", 20, "ml"), ("Sól", 2, "g"),
                        ("Pieprz czarny mielony", 1, "g")],
    },
    {
        "name": "Naleśniki z serem",
        "description": "Delikatne naleśniki nadziewane twarogiem z masłem.",
        "cuisine": "polska", "meal_type": "kolacja", "prep_time_min": 10, "cook_time_min": 15,
        "servings": 2, "difficulty": "łatwy", "tags": ["wegetariańskie", "tradycyjne"],
        "ingredients": [("Mąka pszenna", 150, "g"), ("Jajka", 2, "szt"), ("Mleko 2%", 0.25, "l"),
                        ("Twaróg półtłusty", 250, "g"), ("Masło extra", 30, "g"), ("Sól", 2, "g")],
    },
    {
        "name": "Tosty z jajkiem i awokado",
        "description": "Chrupiące tosty z jajkiem sadzonym i kremowym awokado.",
        "cuisine": "polska", "meal_type": "kolacja", "prep_time_min": 5, "cook_time_min": 5,
        "servings": 2, "difficulty": "łatwy", "tags": ["szybkie", "zdrowe"],
        "ingredients": [("Chleb pszenny", 200, "g"), ("Jajka", 2, "szt"), ("Awokado", 1, "szt"),
                        ("Sól", 2, "g"), ("Pieprz czarny mielony", 1, "g"), ("Oliwa z oliwek", 10, "ml")],
    },
    {   # NOWOŚĆ
        "name": "Sałatka z kurczakiem i awokado",
        "description": "Sycąca sałatka z grillowanym kurczakiem, awokado i pomidorkami.",
        "cuisine": "polska", "meal_type": "kolacja", "prep_time_min": 10, "cook_time_min": 10,
        "servings": 2, "difficulty": "łatwy", "tags": ["wysokobiałkowe", "bezglutenowe", "nowość"],
        "ingredients": [("Pierś z kurczaka", 0.25, "kg"), ("Sałata lodowa", 0.5, "szt"), ("Pomidory", 0.15, "kg"),
                        ("Awokado", 1, "szt"), ("Oliwa z oliwek", 15, "ml"), ("Sól", 2, "g"),
                        ("Pieprz czarny mielony", 1, "g")],
    },
    {   # NOWOŚĆ
        "name": "Kanapki z twarożkiem i ogórkiem",
        "description": "Lekka kolacja — pełnoziarniste pieczywo z twarożkiem i plasterkami ogórka.",
        "cuisine": "polska", "meal_type": "kolacja", "prep_time_min": 8, "cook_time_min": 0,
        "servings": 2, "difficulty": "łatwy", "tags": ["lekkie", "wegetariańskie", "nowość"],
        "ingredients": [("Chleb pszenny", 150, "g"), ("Twaróg półtłusty", 200, "g"), ("Jogurt naturalny", 40, "g"),
                        ("Ogórek", 1, "szt"), ("Sól", 1, "g"), ("Pieprz czarny mielony", 1, "g")],
    },
]
