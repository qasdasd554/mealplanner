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
    "Smażony ryż z kurczakiem i warzywami": _IMG.format("photo-1512058564366-18510be2db19"),
    "Domowy kebab z TikToka": _IMG.format("photo-1561651188-d207bbec4ec3"),
    "Carbonara klasyczna": _IMG.format("photo-1612874742237-6526221588e3"),
    "Shakshuka z jajkami": _IMG.format("photo-1590947132387-155cc02f3212"),
    "Granola z jogurtem i owocami": _IMG.format("photo-1517093728432-a0440f8d45af"),
    "Owsianka z bananem i masłem orzechowym": _IMG.format("photo-1571748982800-fa51082c2224"),
    "Wrap z kurczakiem i warzywami": _IMG.format("photo-1626700051175-6818013e1d4f"),
    "Quesadilla z serem i pieczarkami": _IMG.format("photo-1618040996337-56904b7850b7"),
    "Bruschetta z pomidorami i bazylią": _IMG.format("photo-1572695157366-5e585ab2b69f"),
    "Hummus z warzywami i pitą": _IMG.format("photo-1447175008436-054170c2e979"),
    "Smoothie bowl z owocami": _IMG.format("photo-1590301157890-4810ed352733"),
    "Tosty z awokado i jajkiem na miękko": _IMG.format("photo-1525351484163-7529414344d8"),
}

# (nazwa, jednostka, wielkość_opakowania, dział, cena_bazowa, nutrition/100g, waga_1szt_g)
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
    ("Tortilla pszenna", "szt", 1, "Pieczywo", 2.49, {"kcal": 310, "protein": 8.0, "fat": 7.0, "carbs": 52.0, "fiber": 2.0}, 65),
    ("Majonez", "g", 400, "Przyprawy i sosy", 6.99, {"kcal": 680, "protein": 1.0, "fat": 75.0, "carbs": 1.0, "fiber": 0.0}, None),
    ("Boczek wędzony", "g", 150, "Mięso i wędliny", 7.99, {"kcal": 350, "protein": 12.0, "fat": 33.0, "carbs": 0.5, "fiber": 0.0}, None),
    ("Parmezan tarty", "g", 100, "Nabiał", 8.99, {"kcal": 431, "protein": 38.5, "fat": 29.0, "carbs": 3.2, "fiber": 0.0}, None),
    ("Śmietanka 30%", "ml", 200, "Nabiał", 4.49, {"kcal": 292, "protein": 2.2, "fat": 30.0, "carbs": 3.4, "fiber": 0.0}, None),
    ("Sos sojowy", "ml", 150, "Przyprawy i sosy", 5.99, {"kcal": 53, "protein": 8.0, "fat": 0.0, "carbs": 4.0, "fiber": 0.0}, None),
    ("Imbir świeży", "szt", 1, "Warzywa i owoce", 1.99, {"kcal": 80, "protein": 1.8, "fat": 0.8, "carbs": 18.0, "fiber": 2.0}, 15),
    ("Oregano suszone", "g", 10, "Przyprawy i sosy", 2.99, {"kcal": 265, "protein": 9.0, "fat": 4.3, "carbs": 69.0, "fiber": 42.5}, None),
    ("Kumin rzymski mielony", "g", 20, "Przyprawy i sosy", 3.99, {"kcal": 375, "protein": 17.8, "fat": 22.3, "carbs": 44.2, "fiber": 10.5}, None),
    ("Pieczarki", "g", 500, "Warzywa i owoce", 4.99, {"kcal": 22, "protein": 3.1, "fat": 0.3, "carbs": 3.3, "fiber": 1.0}, None),
    ("Kapusta czerwona", "szt", 1, "Warzywa i owoce", 3.99, {"kcal": 31, "protein": 1.4, "fat": 0.2, "carbs": 7.4, "fiber": 2.1}, 500),
    ("Granola", "g", 350, "Produkty suche", 9.99, {"kcal": 440, "protein": 10.0, "fat": 15.0, "carbs": 65.0, "fiber": 7.0}, None),
    ("Cynamon mielony", "g", 15, "Przyprawy i sosy", 3.49, {"kcal": 247, "protein": 4.0, "fat": 1.2, "carbs": 81.0, "fiber": 53.0}, None),
    ("Pita chlebowa", "szt", 1, "Pieczywo", 1.99, {"kcal": 275, "protein": 9.0, "fat": 1.2, "carbs": 55.0, "fiber": 2.0}, 80),
    ("Tymianek suszony", "g", 10, "Przyprawy i sosy", 2.99, {"kcal": 276, "protein": 9.1, "fat": 7.4, "carbs": 63.9, "fiber": 37.0}, None),
    ("Kurkuma mielona", "g", 20, "Przyprawy i sosy", 3.99, {"kcal": 354, "protein": 8.0, "fat": 10.0, "carbs": 65.0, "fiber": 21.0}, None),
]

# ══════════════════════════════════════════════════════════════════
# PRZEPISY — kcal/makro liczone automatycznie ze składników.
# ══════════════════════════════════════════════════════════════════
RECIPES = [
    # ── PRZEKĄSKI ────────────────────────────────────────────────
    {
        "name": "Jabłko z masłem orzechowym",
        "description": "Szybka i pożywna przekąska na słodko. Pokrój jabłko w cząstki i maczaj w maśle orzechowym.",
        "cuisine": "polska", "meal_type": "przekąska", "prep_time_min": 2, "cook_time_min": 0,
        "servings": 1, "difficulty": "łatwy", "tags": ["szybkie", "bezglutenowe", "wegańskie"],
        "ingredients": [("Jabłka", 1, "szt"), ("Masło orzechowe", 30, "g")],
        "instructions": ["Umyj jabłko i pokrój na cząstki.", "Nałóż masło orzechowe na talerzyk.", "Maczaj cząstki jabłka w maśle orzechowym."]
    },
    {
        "name": "Marchewki z hummusem",
        "description": "Chrupiące słupki marchewki maczane w kremowym hummusie.",
        "cuisine": "azjatycka", "meal_type": "przekąska", "prep_time_min": 5, "cook_time_min": 0,
        "servings": 1, "difficulty": "łatwy", "tags": ["szybkie", "bezglutenowe", "wegańskie"],
        "ingredients": [("Marchew", 0.2, "kg"), ("Hummus", 50, "g")],
        "instructions": ["Obierz marchewki i pokrój w słupki.", "Wyłóż hummus na talerzyk.", "Podawaj marchewki z hummusem do maczania."]
    },
    {
        "name": "Jogurt naturalny z malinami",
        "description": "Lekka przekąska białkowa — jogurt z garścią świeżych malin.",
        "cuisine": "polska", "meal_type": "przekąska", "prep_time_min": 2, "cook_time_min": 0,
        "servings": 1, "difficulty": "łatwy", "tags": ["szybkie", "bezglutenowe", "wegetariańskie"],
        "ingredients": [("Jogurt naturalny", 150, "g"), ("Maliny", 50, "g"), ("Cynamon mielony", 1, "g")],
        "instructions": ["Przełóż jogurt do miseczki.", "Umyj maliny i osusz na ręczniku papierowym.", "Ułóż maliny na jogurcie. Opcjonalnie posyp cynamonem."]
    },
    {
        "name": "Koktajl bananowo-malinowy",
        "description": "Kremowy koktajl: zblenduj banana, maliny, jogurt i mleko. Gotowe w 3 minuty.",
        "cuisine": "polska", "meal_type": "przekąska", "prep_time_min": 3, "cook_time_min": 0,
        "servings": 1, "difficulty": "łatwy", "tags": ["szybkie", "wegetariańskie", "nowość"],
        "ingredients": [("Banan", 1, "szt"), ("Maliny", 60, "g"), ("Jogurt naturalny", 150, "g"), ("Mleko 2%", 0.1, "l")],
        "instructions": ["Obierz banana i wrzuć do blendera.", "Dodaj maliny, jogurt i mleko.", "Blenduj przez 30–60 sekund na gładki koktajl.", "Przelej do szklanki i podawaj od razu."]
    },
    {
        "name": "Bułka z hummusem i papryką",
        "description": "Chrupiąca kajzerka posmarowana hummusem, z plastrami świeżej papryki.",
        "cuisine": "polska", "meal_type": "przekąska", "prep_time_min": 4, "cook_time_min": 0,
        "servings": 1, "difficulty": "łatwy", "tags": ["szybkie", "wegańskie", "nowość"],
        "ingredients": [("Bułka kajzerka", 1, "szt"), ("Hummus", 40, "g"), ("Papryka czerwona", 0.5, "szt")],
        "instructions": ["Przekrój bułkę na pół.", "Posmaruj obie połówki hummusem.", "Pokrój paprykę w cienkie paski i ułóż na bułce."]
    },
    {
        "name": "Hummus z warzywami i pitą",
        "description": "Kremowy hummus podawany z ciepłą pitą i świeżymi warzywami do maczania.",
        "cuisine": "azjatycka", "meal_type": "przekąska", "prep_time_min": 5, "cook_time_min": 3,
        "servings": 2, "difficulty": "łatwy", "tags": ["wegańskie", "zdrowe"],
        "ingredients": [("Hummus", 100, "g"), ("Pita chlebowa", 2, "szt"), ("Marchew", 0.1, "kg"),
                        ("Ogórek", 0.5, "szt"), ("Papryka czerwona", 0.5, "szt")],
        "instructions": ["Przełóż hummus do miseczki.", "Podgrzej pity na suchej patelni lub w piekarniku.", "Pokrój marchew, ogórka i paprykę w słupki.", "Podawaj hummus z ciepłą pitą i warzywami."]
    },
    {
        "name": "Smoothie bowl z owocami",
        "description": "Gęsty koktajl w miseczce z bananem i malinami, posypany granolą.",
        "cuisine": "polska", "meal_type": "przekąska", "prep_time_min": 5, "cook_time_min": 0,
        "servings": 1, "difficulty": "łatwy", "tags": ["wegetariańskie", "zdrowe"],
        "ingredients": [("Banan", 1, "szt"), ("Maliny", 60, "g"), ("Jogurt naturalny", 100, "g"),
                        ("Granola", 30, "g"), ("Mleko 2%", 0.05, "l")],
        "instructions": ["Zblenduj banana, maliny, jogurt i mleko na gęsty koktajl.", "Przelej do miseczki.", "Posyp granolą i udekoruj kilkoma malinami."]
    },
    {
        "name": "Tosty z awokado i jajkiem na miękko",
        "description": "Chrupiące tosty z kremowym awokado i jajkiem na miękko — idealna przekąska.",
        "cuisine": "polska", "meal_type": "przekąska", "prep_time_min": 5, "cook_time_min": 6,
        "servings": 1, "difficulty": "łatwy", "tags": ["wegetariańskie", "zdrowe"],
        "ingredients": [("Chleb pszenny", 80, "g"), ("Awokado", 0.5, "szt"), ("Jajka", 1, "szt"),
                        ("Sól", 1, "g"), ("Pieprz czarny mielony", 1, "g")],
        "instructions": ["Ugotuj jajko na miękko (6 minut w gotującej wodzie).", "Opiecz kromki chleba.", "Rozgnieć połówkę awokado widelcem, dopraw solą i pieprzem.", "Nałóż pastę z awokado na tosty.", "Obierz jajko, przekrój na pół i ułóż na toście."]
    },
    # ── ŚNIADANIA ────────────────────────────────────────────────
    {
        "name": "Owsianka na mleku migdałowym",
        "description": "Owsianka na mleku roślinnym z plastrami banana.",
        "cuisine": "polska", "meal_type": "śniadanie", "prep_time_min": 10, "cook_time_min": 0,
        "servings": 1, "difficulty": "łatwy", "tags": ["wegetariańskie", "zdrowe"],
        "ingredients": [("Płatki owsiane", 50, "g"), ("Mleko migdałowe", 0.2, "l"), ("Banan", 1, "szt"), ("Cynamon mielony", 2, "g")],
        "instructions": ["Wsyp płatki owsiane do garnka.", "Zalej mlekiem migdałowym i gotuj na małym ogniu 5–7 minut, mieszając.", "Przełóż do miseczki, ułóż plastry banana na wierzchu.", "Opcjonalnie posyp cynamonem."]
    },
    {
        "name": "Jajecznica z pomidorami",
        "description": "Klasyczna jajecznica z dojrzałymi pomidorami, podawana z pieczywem.",
        "cuisine": "polska", "meal_type": "śniadanie", "prep_time_min": 5, "cook_time_min": 5,
        "servings": 2, "difficulty": "łatwy", "tags": ["szybkie"],
        "ingredients": [("Jajka", 4, "szt"), ("Pomidory", 0.2, "kg"), ("Masło extra", 20, "g"),
                        ("Chleb pszenny", 100, "g"), ("Sól", 2, "g"), ("Pieprz czarny mielony", 1, "g")],
        "instructions": ["Pokrój pomidory na drobne kawałki.", "Rozpuść masło na patelni na średnim ogniu.", "Wbij jajka, dodaj pomidory, sól i pieprz.", "Mieszaj delikatnie drewnianą łyżką aż jajka się zetną.", "Podawaj z pieczywem."]
    },
    {
        "name": "Kanapki z szynką i serem",
        "description": "Proste kanapki na śniadanie z szynką, serem i warzywami.",
        "cuisine": "polska", "meal_type": "śniadanie", "prep_time_min": 5, "cook_time_min": 0,
        "servings": 2, "difficulty": "łatwy", "tags": ["szybkie"],
        "ingredients": [("Chleb pszenny", 200, "g"), ("Masło extra", 20, "g"), ("Szynka konserwowa", 100, "g"),
                        ("Ser żółty gouda", 80, "g"), ("Ogórek", 1, "szt"), ("Sałata lodowa", 0.25, "szt")],
        "instructions": ["Pokrój chleb na kromki i posmaruj masłem.", "Na każdą kromkę ułóż plasterek szynki i sera.", "Dodaj plastry ogórka i liść sałaty.", "Podawaj od razu."]
    },
    {
        "name": "Owsianka z jogurtem",
        "description": "Ciepła owsianka z jogurtem naturalnym, idealna na pożywne śniadanie.",
        "cuisine": "polska", "meal_type": "śniadanie", "prep_time_min": 5, "cook_time_min": 5,
        "servings": 2, "difficulty": "łatwy", "tags": ["wegetariańskie", "zdrowe"],
        "ingredients": [("Płatki owsiane", 100, "g"), ("Mleko 2%", 0.3, "l"), ("Jogurt naturalny", 150, "g"), ("Sól", 1, "g"), ("Cynamon mielony", 1, "g")],
        "instructions": ["Gotuj płatki owsiane z mlekiem na małym ogniu przez 5 minut.", "Dodaj szczyptę soli i mieszaj.", "Przełóż do miseczki i dodaj jogurt na wierzch.", "Opcjonalnie posyp cynamonem."]
    },
    {
        "name": "Tosty francuskie",
        "description": "Kromki chleba moczone w jajku z mlekiem, smażone na maśle na złoto.",
        "cuisine": "francuska", "meal_type": "śniadanie", "prep_time_min": 5, "cook_time_min": 10,
        "servings": 2, "difficulty": "łatwy", "tags": ["szybkie", "wegetariańskie", "nowość"],
        "ingredients": [("Chleb pszenny", 150, "g"), ("Jajka", 2, "szt"), ("Mleko 2%", 0.1, "l"), ("Masło extra", 20, "g")],
        "instructions": ["Roztrzep jajka z mlekiem w głębokim talerzu.", "Namocz kromki chleba w mieszance jajecznej.", "Rozgrzej masło na patelni.", "Smaż namoczone kromki na złoty kolor z obu stron (po 2 min)."]
    },
    {
        "name": "Omlet ze szpinakiem i fetą",
        "description": "Puszysty omlet z podsmażonym szpinakiem i pokruszoną fetą.",
        "cuisine": "polska", "meal_type": "śniadanie", "prep_time_min": 5, "cook_time_min": 8,
        "servings": 1, "difficulty": "łatwy", "tags": ["wysokobiałkowe", "bezglutenowe", "nowość"],
        "ingredients": [("Jajka", 3, "szt"), ("Mrożony szpinak", 100, "g"), ("Ser feta", 40, "g"),
                        ("Masło extra", 10, "g"), ("Sól", 1, "g"), ("Pieprz czarny mielony", 1, "g")],
        "instructions": ["Rozmroź szpinak i odciśnij nadmiar wody.", "Roztrzep jajka z solą i pieprzem.", "Rozgrzej masło na patelni i wylej jajka.", "Gdy omlet zacznie się ścinać, rozłóż szpinak i pokruszoną fetę.", "Złóż na pół i smaż jeszcze minutę."]
    },
    {
        "name": "Shakshuka z jajkami",
        "description": "Jajka gotowane w pikantnym sosie pomidorowym z papryką i cebulą — popularne śniadanie z Bliskiego Wschodu.",
        "cuisine": "azjatycka", "meal_type": "śniadanie", "prep_time_min": 10, "cook_time_min": 15,
        "servings": 2, "difficulty": "łatwy", "tags": ["wegetariańskie", "bezglutenowe"],
        "ingredients": [("Jajka", 4, "szt"), ("Passata pomidorowa", 300, "g"), ("Papryka czerwona", 1, "szt"),
                        ("Cebula", 0.15, "kg"), ("Czosnek", 2, "szt"), ("Oliwa z oliwek", 15, "ml"),
                        ("Papryka słodka", 3, "g"), ("Kumin rzymski mielony", 2, "g"), ("Sól", 2, "g"), ("Pieprz czarny mielony", 1, "g")],
        "instructions": ["Na patelni rozgrzej oliwę i podsmaż pokrojoną cebulę i paprykę.", "Dodaj czosnek, paprykę słodką i kumin, smaż minutę.", "Wlej passatę pomidorową, dopraw solą i pieprzem.", "Gotuj sos 5 minut na małym ogniu.", "Zrób 4 wgłębienia w sosie i wbij w nie jajka.", "Przykryj i gotuj 8–10 minut, aż białka się zetną."]
    },
    {
        "name": "Granola z jogurtem i owocami",
        "description": "Chrupiąca granola z kremowym jogurtem, bananem i malinami — szybkie i pożywne śniadanie.",
        "cuisine": "polska", "meal_type": "śniadanie", "prep_time_min": 3, "cook_time_min": 0,
        "servings": 1, "difficulty": "łatwy", "tags": ["szybkie", "wegetariańskie", "zdrowe"],
        "ingredients": [("Granola", 60, "g"), ("Jogurt naturalny", 150, "g"), ("Banan", 0.5, "szt"), ("Maliny", 40, "g")],
        "instructions": ["Przełóż jogurt do miseczki.", "Posyp granolą.", "Pokrój banana w plastry i ułóż na wierzchu.", "Dodaj maliny i podawaj od razu."]
    },
    {
        "name": "Owsianka z bananem i masłem orzechowym",
        "description": "Kremowa owsianka z plastrami banana, masłem orzechowym i odrobiną cynamonu.",
        "cuisine": "polska", "meal_type": "śniadanie", "prep_time_min": 5, "cook_time_min": 7,
        "servings": 1, "difficulty": "łatwy", "tags": ["wegetariańskie", "zdrowe", "wysokobiałkowe"],
        "ingredients": [("Płatki owsiane", 50, "g"), ("Mleko 2%", 0.2, "l"), ("Banan", 1, "szt"),
                        ("Masło orzechowe", 20, "g"), ("Cynamon mielony", 2, "g")],
        "instructions": ["Wsyp płatki owsiane do garnka i zalej mlekiem.", "Gotuj na małym ogniu 5–7 minut, mieszając.", "Przełóż do miseczki.", "Ułóż plastry banana na wierzchu.", "Dodaj łyżkę masła orzechowego i posyp cynamonem."]
    },
    # ── OBIADY ───────────────────────────────────────────────────
    {
        "name": "Kotlet schabowy z ziemniakami",
        "description": "Tradycyjny polski kotlet schabowy w panierce, podawany z ziemniakami.",
        "cuisine": "polska", "meal_type": "obiad", "prep_time_min": 15, "cook_time_min": 25,
        "servings": 2, "difficulty": "średni", "tags": ["tradycyjne", "polska kuchnia"],
        "ingredients": [("Schab wieprzowy", 0.4, "kg"), ("Mąka pszenna", 30, "g"), ("Jajka", 2, "szt"),
                        ("Bułka tarta", 60, "g"), ("Ziemniaki", 0.5, "kg"), ("Olej rzepakowy", 0.04, "l"),
                        ("Sól", 3, "g"), ("Pieprz czarny mielony", 1, "g"), ("Papryka słodka", 2, "g")],
        "instructions": ["Rozbij schabu tłuczkiem na cienkie plastry.", "Przygotuj 3 miski: mąkę, roztrzepane jajka, bułkę tartą.", "Dopraw mięso solą i pieprzem, obtocz kolejno w mące, jajku i bułce tartej.", "Smaż na rozgrzanym oleju po 3–4 minuty z każdej strony.", "Ugotuj ziemniaki w osolonej wodzie do miękkości (ok. 20 min)."]
    },
    {
        "name": "Spaghetti bolognese",
        "description": "Klasyczne spaghetti z mięsnym sosem bolońskim na passacie pomidorowej.",
        "cuisine": "włoska", "meal_type": "obiad", "prep_time_min": 10, "cook_time_min": 25,
        "servings": 2, "difficulty": "średni", "tags": ["włoska kuchnia"],
        "ingredients": [("Makaron penne", 200, "g"), ("Mielone wieprzowo-wołowe", 250, "g"),
                        ("Passata pomidorowa", 250, "g"), ("Cebula", 0.15, "kg"), ("Czosnek", 0.5, "szt"),
                        ("Oliwa z oliwek", 15, "ml"), ("Sól", 3, "g"), ("Pieprz czarny mielony", 1, "g"),
                        ("Bazylia suszona", 2, "g"), ("Oregano suszone", 2, "g")],
        "instructions": ["Podsmaż pokrojoną cebulę i czosnek na oliwie.", "Dodaj mięso mielone i smaż do zrumienienia.", "Wlej passatę, dodaj bazylię, oregano, sól i pieprz.", "Gotuj sos na małym ogniu 15 minut.", "Ugotuj makaron al dente wg instrukcji na opakowaniu.", "Podawaj makaron z sosem."]
    },
    {
        "name": "Kurczak z ryżem i warzywami",
        "description": "Lekki obiad — grillowana pierś z kurczaka z ryżem i warzywami.",
        "cuisine": "polska", "meal_type": "obiad", "prep_time_min": 10, "cook_time_min": 20,
        "servings": 2, "difficulty": "łatwy", "tags": ["zdrowe", "wysokobiałkowe"],
        "ingredients": [("Pierś z kurczaka", 0.4, "kg"), ("Ryż biały", 0.15, "kg"), ("Marchew", 0.2, "kg"),
                        ("Papryka czerwona", 1, "szt"), ("Cebula", 0.1, "kg"), ("Olej rzepakowy", 0.02, "l"),
                        ("Sól", 3, "g"), ("Pieprz czarny mielony", 1, "g"), ("Papryka słodka", 3, "g"), ("Kurkuma mielona", 2, "g")],
        "instructions": ["Pokrój pierś z kurczaka w kostkę, dopraw solą, pieprzem, papryką i kurkumą.", "Ugotuj ryż wg instrukcji na opakowaniu.", "Na patelni rozgrzej olej, podsmaż cebulę, dodaj kurczaka i smaż 5–7 minut.", "Dodaj pokrojoną marchew i paprykę, smaż kolejne 5 minut.", "Podawaj kurczaka z warzywami na ryżu."]
    },
    {
        "name": "Zupa pomidorowa z makaronem",
        "description": "Domowa zupa pomidorowa na passacie, podawana z drobnym makaronem.",
        "cuisine": "polska", "meal_type": "obiad", "prep_time_min": 10, "cook_time_min": 20,
        "servings": 4, "difficulty": "łatwy", "tags": ["tradycyjne", "polska kuchnia", "zupy"],
        "ingredients": [("Passata pomidorowa", 500, "g"), ("Makaron penne", 150, "g"), ("Marchew", 0.2, "kg"),
                        ("Cebula", 0.1, "kg"), ("Masło extra", 20, "g"), ("Śmietana 18%", 100, "ml"),
                        ("Sól", 5, "g"), ("Pieprz czarny mielony", 1, "g"), ("Bazylia suszona", 2, "g")],
        "instructions": ["Podsmaż pokrojoną cebulę i marchew na maśle.", "Dodaj passatę pomidorową i 500 ml wody.", "Gotuj 15 minut na małym ogniu.", "Dodaj sól, pieprz i opcjonalnie bazylię.", "Ugotuj makaron osobno i dodaj do zupy.", "Podawaj ze śmietaną."]
    },
    {
        "name": "Gulasz z kurczaka z warzywami",
        "description": "Prosty gulasz z piersi kurczaka duszony z papryką, marchewką i ziemniakami.",
        "cuisine": "polska", "meal_type": "obiad", "prep_time_min": 15, "cook_time_min": 30,
        "servings": 2, "difficulty": "łatwy", "tags": ["zdrowe", "wysokobiałkowe", "nowość"],
        "ingredients": [("Pierś z kurczaka", 0.4, "kg"), ("Ziemniaki", 0.5, "kg"), ("Cebula", 0.1, "kg"),
                        ("Papryka czerwona", 1, "szt"), ("Marchew", 0.15, "kg"), ("Passata pomidorowa", 200, "g"),
                        ("Olej rzepakowy", 0.02, "l"), ("Papryka słodka", 4, "g"), ("Sól", 3, "g"), ("Tymianek suszony", 2, "g")],
        "instructions": ["Pokrój kurczaka w kostkę i podsmaż na oleju.", "Dodaj pokrojoną cebulę, marchew i paprykę.", "Dodaj pokrojone ziemniaki i passatę.", "Dopraw papryką słodką, solą i tymiankiem.", "Duś pod przykryciem na małym ogniu ok. 25 minut."]
    },
    {
        "name": "Makaron ze szpinakiem i fetą",
        "description": "Penne w kremowym sosie szpinakowym z fetą i czosnkiem. Obiad w 20 minut.",
        "cuisine": "włoska", "meal_type": "obiad", "prep_time_min": 5, "cook_time_min": 15,
        "servings": 2, "difficulty": "łatwy", "tags": ["wegetariańskie", "szybkie", "nowość"],
        "ingredients": [("Makaron penne", 200, "g"), ("Mrożony szpinak", 300, "g"), ("Ser feta", 100, "g"),
                        ("Czosnek", 2, "szt"), ("Oliwa z oliwek", 15, "ml"), ("Śmietana 18%", 100, "ml"),
                        ("Sól", 2, "g"), ("Pieprz czarny mielony", 1, "g")],
        "instructions": ["Ugotuj makaron al dente.", "Na patelni rozgrzej oliwę i podsmaż posiekany czosnek.", "Dodaj rozmrożony szpinak i śmietanę, wymieszaj.", "Dodaj pokruszoną fetę, sól i pieprz.", "Wymieszaj z makaronem i podawaj."]
    },
    {
        "name": "Smażony ryż z kurczakiem i warzywami",
        "description": "Chiński smażony ryż z kawałkami kurczaka, marchewką, papryką i sosem sojowym.",
        "cuisine": "azjatycka", "meal_type": "obiad", "prep_time_min": 15, "cook_time_min": 15,
        "servings": 2, "difficulty": "średni", "tags": ["azjatyckie", "wysokobiałkowe"],
        "ingredients": [("Ryż biały", 0.15, "kg"), ("Pierś z kurczaka", 0.3, "kg"), ("Marchew", 0.1, "kg"),
                        ("Papryka czerwona", 1, "szt"), ("Cebula", 0.1, "kg"), ("Czosnek", 2, "szt"),
                        ("Imbir świeży", 1, "szt"), ("Jajka", 2, "szt"), ("Sos sojowy", 30, "ml"),
                        ("Olej rzepakowy", 0.02, "l"), ("Sól", 2, "g"), ("Pieprz czarny mielony", 1, "g")],
        "instructions": ["Ugotuj ryż wg instrukcji na opakowaniu i ostudź (najlepiej ryż z dnia poprzedniego).", "Pokrój kurczaka w kostkę, dopraw solą i pieprzem.", "Na dużej patelni lub woku rozgrzej olej i podsmaż kurczaka 5 minut. Odłóż na bok.", "Na tej samej patelni podsmaż pokrojoną cebulę, marchew i paprykę 3 minuty.", "Dodaj starty imbir i posiekany czosnek, smaż minutę.", "Dodaj ugotowany ryż, wlej sos sojowy i mieszaj 2 minuty.", "Zrób miejsce na środku patelni, wbij jajka i jajecznicuj je.", "Wymieszaj wszystko razem z kurczakiem i podawaj."]
    },
    {
        "name": "Domowy kebab z TikToka",
        "description": "Viralowy przepis z TikToka — mięso mielone formowane w rulon, pieczone i podawane w tortilli z sosem czosnkowym i warzywami.",
        "cuisine": "azjatycka", "meal_type": "obiad", "prep_time_min": 20, "cook_time_min": 30,
        "servings": 4, "difficulty": "średni", "tags": ["viralowe", "TikTok", "kebab"],
        "ingredients": [("Mielone wieprzowo-wołowe", 500, "g"), ("Jogurt naturalny", 100, "g"),
                        ("Cebula", 0.15, "kg"), ("Czosnek", 3, "szt"), ("Sól", 4, "g"),
                        ("Pieprz czarny mielony", 2, "g"), ("Papryka słodka", 4, "g"),
                        ("Kumin rzymski mielony", 3, "g"), ("Tortilla pszenna", 4, "szt"),
                        ("Majonez", 30, "g"), ("Sałata lodowa", 0.25, "szt"),
                        ("Pomidory", 0.15, "kg"), ("Kapusta czerwona", 0.1, "szt")],
        "instructions": ["Do mięsa mielonego dodaj zblendowaną cebulę, przeciśnięty czosnek, jogurt (100g) oraz wszystkie przyprawy (sól, pieprz, paprykę, kumin).", "Całość bardzo dokładnie wyrób dłońmi przez kilka minut, aby składniki się połączyły.", "Podziel mięso na 3–4 równe porcje. Każdą ułóż na papierze do pieczenia i rozwałkuj na cienki placek (ok. 0,5 cm).", "Za pomocą papieru zwiń mięso w ciasny, zwarty rulon.", "Ułóż rulony na blaszce i piecz w piekarniku rozgrzanym do 190°C przez 25–30 minut.", "Wyjmij z piekarnika, rozwiń z papieru i posiekaj nożem na drobne, podłużne kawałki.", "Przygotuj sos czosnkowy: wymieszaj jogurt (z nowej porcji — weź z lodówki) z majonezem i przeciśniętym czosnkiem.", "Podgrzej tortille, posmaruj sosem, dodaj sałatę, pomidory, kapustę i mięso. Zwiń jak wrap.", "Opcjonalnie przypiecz chwilę na suchej patelni."]
    },
    {
        "name": "Carbonara klasyczna",
        "description": "Klasyczna włoska carbonara — makaron z boczkiem, żółtkami, parmezanem i pieprzem. Bez śmietany!",
        "cuisine": "włoska", "meal_type": "obiad", "prep_time_min": 10, "cook_time_min": 15,
        "servings": 2, "difficulty": "średni", "tags": ["włoska kuchnia", "klasyczne"],
        "ingredients": [("Makaron penne", 200, "g"), ("Boczek wędzony", 150, "g"),
                        ("Jajka", 3, "szt"), ("Parmezan tarty", 50, "g"),
                        ("Pieprz czarny mielony", 2, "g"), ("Sól", 3, "g"), ("Czosnek", 1, "szt")],
        "instructions": ["Ugotuj makaron al dente w osolonej wodzie. Zachowaj szklankę wody z gotowania.", "Pokrój boczek w paski i smaż na suchej patelni, aż będzie chrupiący. Dodaj rozgnieciony czosnek na ostatnią minutę.", "W miseczce wymieszaj żółtka (z 3 jajek) z tartym parmezanem i pieprzem na kremowy sos.", "Odcedź makaron i od razu wrzuć na patelnię z boczkiem (zdejmij z ognia!).", "Wlej sos jajeczny i szybko mieszaj — ciepło makaronu ugotuje jajka na kremowy sos.", "Jeśli sos jest za gęsty, dodaj odrobinę wody z gotowania makaronu.", "Podawaj od razu, posypany dodatkowym parmezanem i pieprzem."]
    },
    # ── KOLACJE ──────────────────────────────────────────────────
    {
        "name": "Sałatka grecka",
        "description": "Klasyczna sałatka z fetą i oliwkami.",
        "cuisine": "grecka", "meal_type": "kolacja", "prep_time_min": 15, "cook_time_min": 0,
        "servings": 2, "difficulty": "łatwy", "tags": ["wegetariańskie", "bezglutenowe"],
        "ingredients": [("Pomidory", 0.3, "kg"), ("Ogórek", 1, "szt"), ("Cebula", 0.1, "kg"),
                        ("Ser feta", 100, "g"), ("Oliwki czarne", 50, "g"), ("Oliwa z oliwek", 20, "ml"), ("Oregano suszone", 1, "g")],
        "instructions": ["Pokrój pomidory i ogórka w kostkę.", "Pokrój cebulę w cienkie plasterki.", "Pokrusz fetę na kawałki.", "Wymieszaj warzywa z oliwkami.", "Polej oliwą, dopraw solą i oregano."]
    },
    {
        "name": "Sałatka z łososiem",
        "description": "Lekka sałatka z wędzonym łososiem, ogórkiem i pomidorami.",
        "cuisine": "polska", "meal_type": "kolacja", "prep_time_min": 15, "cook_time_min": 0,
        "servings": 2, "difficulty": "łatwy", "tags": ["zdrowe", "lekkie", "wysokobiałkowe"],
        "ingredients": [("Łosoś wędzony", 100, "g"), ("Sałata lodowa", 0.5, "szt"), ("Ogórek", 1, "szt"),
                        ("Pomidory", 0.2, "kg"), ("Oliwa z oliwek", 20, "ml"), ("Sól", 2, "g"),
                        ("Pieprz czarny mielony", 1, "g")],
        "instructions": ["Porwij sałatę lodową na kawałki.", "Pokrój ogórka i pomidory.", "Ułóż na talerzu sałatę, warzywa i plastry łososia.", "Polej oliwą, dopraw solą i pieprzem."]
    },
    {
        "name": "Naleśniki z serem",
        "description": "Delikatne naleśniki nadziewane twarogiem z masłem.",
        "cuisine": "polska", "meal_type": "kolacja", "prep_time_min": 10, "cook_time_min": 15,
        "servings": 2, "difficulty": "łatwy", "tags": ["wegetariańskie", "tradycyjne"],
        "ingredients": [("Mąka pszenna", 150, "g"), ("Jajka", 2, "szt"), ("Mleko 2%", 0.25, "l"),
                        ("Twaróg półtłusty", 250, "g"), ("Masło extra", 30, "g"), ("Sól", 2, "g")],
        "instructions": ["Wymieszaj mąkę, jajka, mleko i szczyptę soli na gładkie ciasto.", "Smaż cienkie naleśniki na rozgrzanej patelni z odrobiną masła.", "Wymieszaj twaróg z resztą masła (roztopionego).", "Nadziewaj naleśniki twarożkiem i zwiń w ruloniki."]
    },
    {
        "name": "Tosty z jajkiem i awokado",
        "description": "Chrupiące tosty z jajkiem sadzonym i kremowym awokado.",
        "cuisine": "polska", "meal_type": "kolacja", "prep_time_min": 5, "cook_time_min": 5,
        "servings": 2, "difficulty": "łatwy", "tags": ["szybkie", "zdrowe"],
        "ingredients": [("Chleb pszenny", 200, "g"), ("Jajka", 2, "szt"), ("Awokado", 1, "szt"),
                        ("Sól", 2, "g"), ("Pieprz czarny mielony", 1, "g"), ("Oliwa z oliwek", 10, "ml")],
        "instructions": ["Opiecz kromki chleba w tosterze lub na patelni.", "Rozgrzej oliwę na patelni i usmaż jajka sadzone.", "Rozgnieć awokado widelcem, dopraw solą i pieprzem.", "Na tosty nałóż pastę z awokado, a na nią jajka sadzone."]
    },
    {
        "name": "Sałatka z kurczakiem i awokado",
        "description": "Sycąca sałatka z grillowanym kurczakiem, awokado i pomidorkami.",
        "cuisine": "polska", "meal_type": "kolacja", "prep_time_min": 10, "cook_time_min": 10,
        "servings": 2, "difficulty": "łatwy", "tags": ["wysokobiałkowe", "bezglutenowe", "nowość"],
        "ingredients": [("Pierś z kurczaka", 0.25, "kg"), ("Sałata lodowa", 0.5, "szt"), ("Pomidory", 0.15, "kg"),
                        ("Awokado", 1, "szt"), ("Oliwa z oliwek", 15, "ml"), ("Sól", 2, "g"),
                        ("Pieprz czarny mielony", 1, "g")],
        "instructions": ["Pokrój pierś z kurczaka w paski i podsmaż na oliwie z solą i pieprzem.", "Porwij sałatę, pokrój pomidory i awokado.", "Ułóż warzywa na talerzu, a na nich ciepłego kurczaka.", "Polej resztą oliwy."]
    },
    {
        "name": "Kanapki z twarożkiem i ogórkiem",
        "description": "Lekka kolacja — pełnoziarniste pieczywo z twarożkiem i plasterkami ogórka.",
        "cuisine": "polska", "meal_type": "kolacja", "prep_time_min": 8, "cook_time_min": 0,
        "servings": 2, "difficulty": "łatwy", "tags": ["lekkie", "wegetariańskie", "nowość"],
        "ingredients": [("Chleb pszenny", 150, "g"), ("Twaróg półtłusty", 200, "g"), ("Jogurt naturalny", 40, "g"),
                        ("Ogórek", 1, "szt"), ("Sól", 1, "g"), ("Pieprz czarny mielony", 1, "g")],
        "instructions": ["Wymieszaj twaróg z jogurtem, solą i pieprzem na pastę.", "Pokrój chleb na kromki.", "Posmaruj kromki pastą twarożkową.", "Ułóż plasterki ogórka na kanapkach."]
    },
    {
        "name": "Wrap z kurczakiem i warzywami",
        "description": "Chrupiący wrap z grillowanym kurczakiem, sałatą, pomidorem i sosem jogurtowym.",
        "cuisine": "polska", "meal_type": "kolacja", "prep_time_min": 10, "cook_time_min": 10,
        "servings": 2, "difficulty": "łatwy", "tags": ["szybkie", "wysokobiałkowe"],
        "ingredients": [("Tortilla pszenna", 2, "szt"), ("Pierś z kurczaka", 0.2, "kg"),
                        ("Sałata lodowa", 0.25, "szt"), ("Pomidory", 0.1, "kg"),
                        ("Jogurt naturalny", 60, "g"), ("Czosnek", 1, "szt"),
                        ("Olej rzepakowy", 0.01, "l"), ("Sól", 2, "g"), ("Pieprz czarny mielony", 1, "g")],
        "instructions": ["Pokrój kurczaka w paski, dopraw solą i pieprzem.", "Podsmaż kurczaka na oleju na patelni 5–7 minut.", "Przygotuj sos: wymieszaj jogurt z przeciśniętym czosnkiem i solą.", "Podgrzej tortille na suchej patelni.", "Na tortillę nałóż sałatę, plasterki pomidora, kurczaka i polej sosem.", "Zwiń ciasno w wrap i opcjonalnie przypiecz na patelni."]
    },
    {
        "name": "Quesadilla z serem i pieczarkami",
        "description": "Chrupiąca tortilla z ciągnącym się serem i smażonymi pieczarkami.",
        "cuisine": "polska", "meal_type": "kolacja", "prep_time_min": 10, "cook_time_min": 10,
        "servings": 2, "difficulty": "łatwy", "tags": ["wegetariańskie", "szybkie"],
        "ingredients": [("Tortilla pszenna", 2, "szt"), ("Ser żółty gouda", 100, "g"),
                        ("Pieczarki", 150, "g"), ("Cebula", 0.1, "kg"),
                        ("Masło extra", 10, "g"), ("Sól", 1, "g"), ("Pieprz czarny mielony", 1, "g")],
        "instructions": ["Pokrój pieczarki w plasterki, a cebulę w drobną kostkę.", "Podsmaż cebulę na maśle, dodaj pieczarki i smaż 5 minut. Dopraw solą i pieprzem.", "Na jedną połowę tortilli nałóż starty ser i pieczarki, złóż na pół.", "Smaż quesadillę na suchej patelni po 2 minuty z każdej strony, aż ser się rozpuści.", "Pokrój na trójkąty i podawaj."]
    },
    {
        "name": "Bruschetta z pomidorami i bazylią",
        "description": "Włoska bruschetta — chrupiące grzanki z dojrzałymi pomidorami, czosnkiem i bazylią.",
        "cuisine": "włoska", "meal_type": "kolacja", "prep_time_min": 10, "cook_time_min": 5,
        "servings": 2, "difficulty": "łatwy", "tags": ["wegetariańskie", "włoska kuchnia", "szybkie"],
        "ingredients": [("Chleb pszenny", 200, "g"), ("Pomidory", 0.3, "kg"), ("Czosnek", 2, "szt"),
                        ("Oliwa z oliwek", 20, "ml"), ("Bazylia suszona", 2, "g"),
                        ("Sól", 2, "g"), ("Pieprz czarny mielony", 1, "g")],
        "instructions": ["Pokrój chleb na grube kromki i opiecz w piekarniku lub na patelni na złoto.", "Pokrój pomidory w drobną kostkę.", "Wymieszaj pomidory z posiekanym czosnkiem, oliwą, bazylią, solą i pieprzem.", "Natrzyj gorące grzanki przekrojonym ząbkiem czosnku.", "Nałóż mieszankę pomidorową na grzanki i podawaj."]
    },
]
