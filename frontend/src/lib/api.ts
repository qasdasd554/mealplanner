import { storage } from "@/src/utils/storage";

const BASE_URL = process.env.EXPO_PUBLIC_BACKEND_URL;
export const TOKEN_KEY = "auth_token";

export interface Nutrition {
  kcal: number;
  protein: number;
  fat: number;
  carbs: number;
  fiber?: number;
}

export interface Product {
  id: string;
  name: string;
  unit: string;
  default_quantity: number;
  department: string;
  base_price: number;
  nutrition_per_100: Nutrition;
  weight_per_unit_g: number | null;
}

export interface Ingredient {
  product_id: string;
  product_name: string;
  quantity: number;
  unit: string;
}

export interface Recipe {
  id: string;
  name: string;
  description: string;
  cuisine: string;
  meal_type: string;
  prep_time_min: number;
  cook_time_min: number;
  servings: number;
  difficulty: string;
  tags: string[];
  ingredients: Ingredient[];
  nutrition_total: Nutrition;
  nutrition_per_serving: Nutrition;
  image_url: string | null;
  is_custom: boolean;
  owner_id: string | null;
}

export interface Store {
  id: string;
  name: string;
  price_multiplier: number;
}

export interface PlanEntry {
  day: number;
  slot: string;
  recipe_id: string;
  recipe_name: string;
  prep_time_min: number;
  cook_time_min: number;
  nutrition_per_serving: Nutrition;
}

export interface ShoppingItem {
  id: string;
  product_id: string;
  name: string;
  quantity: number;
  unit: string;
  department: string;
  packages: number;
  price: number;
  checked: boolean;
}

export interface MealPlan {
  id: string;
  store_id: string;
  store_name: string;
  days: number;
  meals_per_day: number;
  household_size: number;
  entries: PlanEntry[];
  daily_nutrition: { day: number; kcal: number; protein: number; fat: number; carbs: number }[];
  shopping_items: ShoppingItem[];
  total_price: number;
}

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

export async function api<T>(
  path: string,
  options: { method?: string; body?: unknown } = {},
): Promise<T> {
  const token = await storage.secureGet<string>(TOKEN_KEY, "");
  const res = await fetch(`${BASE_URL}/api${path}`, {
    method: options.method || "GET",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
  });
  if (!res.ok) {
    let detail = "Wystąpił błąd";
    try {
      const data = await res.json();
      if (typeof data.detail === "string") detail = data.detail;
    } catch {
      // ignore
    }
    throw new ApiError(res.status, detail);
  }
  return res.json();
}
