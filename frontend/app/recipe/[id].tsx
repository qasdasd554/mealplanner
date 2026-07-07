import { Ionicons } from "@expo/vector-icons";
import { Image } from "expo-image";
import { LinearGradient } from "expo-linear-gradient";
import { router, useLocalSearchParams } from "expo-router";
import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { useAuth } from "@/src/context/AuthContext";
import { api, Recipe } from "@/src/lib/api";
import { colors, font, MEAL_HERO_IMAGES, radius, shadow, spacing } from "@/src/lib/theme";

function formatIngredientQty(quantity: number, unit: string) {
  if (unit === "szt") return `${quantity} szt`;
  if (unit === "kg" || unit === "l") {
    return quantity < 1 ? `${Math.round(quantity * 1000)} ${unit === "kg" ? "g" : "ml"}` : `${quantity} ${unit}`;
  }
  return `${quantity} ${unit}`;
}

export default function RecipeDetailScreen() {
  const insets = useSafeAreaInsets();
  const { id } = useLocalSearchParams<{ id: string }>();
  const { user } = useAuth();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const data = await api<Recipe>(`/recipes/${id}`);
        setRecipe(data);
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  const removeRecipe = async () => {
    if (!recipe) return;
    setDeleting(true);
    try {
      await api(`/recipes/${recipe.id}`, { method: "DELETE" });
      router.back();
    } catch (e: any) {
      setError(e.message);
      setDeleting(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.brand} />
      </View>
    );
  }

  if (error || !recipe) {
    return (
      <View style={styles.center}>
        <Text style={styles.mutedText}>{error || "Nie znaleziono przepisu"}</Text>
        <Pressable testID="recipe-back-button" style={styles.retryBtn} onPress={() => router.back()}>
          <Text style={styles.retryText}>Wróć</Text>
        </Pressable>
      </View>
    );
  }

  const macro = recipe.nutrition_per_serving;

  return (
    <View style={styles.container} testID="recipe-detail-screen">
      <ScrollView contentContainerStyle={{ paddingBottom: insets.bottom + spacing.xl }}>
        <View style={styles.hero}>
          <Image
            source={{ uri: recipe.image_url || MEAL_HERO_IMAGES[recipe.meal_type] }}
            style={StyleSheet.absoluteFill}
            contentFit="cover"
            transition={200}
          />
          <LinearGradient
            colors={["rgba(0,0,0,0.0)", "rgba(0,0,0,0.75)"]}
            style={StyleSheet.absoluteFill}
          />
          <Pressable
            testID="recipe-detail-back"
            style={[styles.backBtn, { top: insets.top + spacing.sm }]}
            onPress={() => router.back()}
          >
            <Ionicons name="chevron-back" size={22} color="#fff" />
          </Pressable>
          <View style={styles.heroContent}>
            <View style={styles.heroBadge}>
              <Text style={styles.heroBadgeText}>{recipe.meal_type}</Text>
            </View>
            <Text style={styles.heroTitle}>{recipe.name}</Text>
            <Text style={styles.heroMeta}>
              {recipe.prep_time_min + recipe.cook_time_min} min · {recipe.servings} porcje ·{" "}
              {recipe.difficulty}
            </Text>
          </View>
        </View>

        <View style={styles.macroCard} testID="recipe-macro-card">
          <View style={styles.macroItem}>
            <Text style={styles.macroValue}>{Math.round(macro.kcal)}</Text>
            <Text style={styles.macroLabel}>kcal / porcja</Text>
          </View>
          <View style={styles.macroDivider} />
          <View style={styles.macroItem}>
            <Text style={styles.macroValue}>{macro.protein} g</Text>
            <Text style={styles.macroLabel}>Białko</Text>
          </View>
          <View style={styles.macroDivider} />
          <View style={styles.macroItem}>
            <Text style={styles.macroValue}>{macro.fat} g</Text>
            <Text style={styles.macroLabel}>Tłuszcze</Text>
          </View>
          <View style={styles.macroDivider} />
          <View style={styles.macroItem}>
            <Text style={styles.macroValue}>{macro.carbs} g</Text>
            <Text style={styles.macroLabel}>Węgle</Text>
          </View>
        </View>

        {!!recipe.description && (
          <Text style={styles.description}>{recipe.description}</Text>
        )}

        <View style={styles.tagsRow}>
          {recipe.tags.map((tag) => (
            <View key={tag} style={styles.tag}>
              <Text style={styles.tagText}>{tag}</Text>
            </View>
          ))}
        </View>

        <Text style={styles.sectionTitle}>Składniki</Text>
        <View style={styles.ingredientsCard}>
          {recipe.ingredients.map((ing, idx) => (
            <View key={`${ing.product_id}-${idx}`}>
              {idx > 0 && <View style={styles.ingredientDivider} />}
              <View style={styles.ingredientRow} testID={`ingredient-row-${idx}`}>
                <Ionicons name="ellipse" size={6} color={colors.brand} />
                <Text style={styles.ingredientName}>{ing.product_name}</Text>
                <Text style={styles.ingredientQty}>
                  {formatIngredientQty(ing.quantity, ing.unit)}
                </Text>
              </View>
            </View>
          ))}
        </View>

        {recipe.instructions && recipe.instructions.length > 0 && (
          <>
            <View style={styles.sectionRow}>
              <Ionicons name="book-outline" size={20} color={colors.brand} />
              <Text style={styles.sectionTitle}>Jak przygotować</Text>
            </View>
            <View style={styles.instructionsCard}>
              {recipe.instructions.map((step, idx) => (
                <View key={idx}>
                  {idx > 0 && <View style={styles.ingredientDivider} />}
                  <View style={styles.instructionRow} testID={`instruction-step-${idx}`}>
                    <View style={styles.stepBadge}>
                      <Text style={styles.stepBadgeText}>{idx + 1}</Text>
                    </View>
                    <Text style={styles.instructionText}>{step}</Text>
                  </View>
                </View>
              ))}
            </View>
          </>
        )}

        {recipe.is_custom && recipe.owner_id === user?.id && (
          <Pressable
            testID="delete-recipe-button"
            style={styles.deleteBtn}
            onPress={removeRecipe}
            disabled={deleting}
          >
            {deleting ? (
              <ActivityIndicator color={colors.error} />
            ) : (
              <>
                <Ionicons name="trash-outline" size={18} color={colors.error} />
                <Text style={styles.deleteText}>Usuń przepis</Text>
              </>
            )}
          </Pressable>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.surface },
  center: {
    flex: 1,
    backgroundColor: colors.surface,
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: spacing.xl,
  },
  mutedText: { fontFamily: font.regular, color: colors.muted, fontSize: 14, textAlign: "center" },
  retryBtn: {
    marginTop: spacing.lg,
    paddingHorizontal: spacing.xl,
    paddingVertical: spacing.md,
    backgroundColor: colors.brandTertiary,
    borderRadius: radius.pill,
  },
  retryText: { color: colors.onBrandTertiary, fontFamily: font.regular, fontWeight: "600" },
  hero: { height: 300, justifyContent: "flex-end" },
  backBtn: {
    position: "absolute",
    left: spacing.lg,
    width: 40,
    height: 40,
    borderRadius: radius.pill,
    backgroundColor: "rgba(0,0,0,0.35)",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 2,
  },
  heroContent: { padding: spacing.lg },
  heroBadge: {
    alignSelf: "flex-start",
    backgroundColor: colors.brand,
    borderRadius: radius.pill,
    paddingHorizontal: spacing.md,
    paddingVertical: 4,
    marginBottom: spacing.sm,
  },
  heroBadgeText: { color: colors.onBrand, fontSize: 11, fontFamily: font.regular, fontWeight: "600" },
  heroTitle: { color: "#fff", fontSize: 26, fontFamily: font.regular, fontWeight: "600" },
  heroMeta: { color: "rgba(255,255,255,0.85)", fontSize: 13, fontFamily: font.regular, marginTop: 4 },
  macroCard: {
    flexDirection: "row",
    backgroundColor: colors.surfaceSecondary,
    borderRadius: radius.lg,
    marginHorizontal: spacing.lg,
    marginTop: -spacing.lg,
    paddingVertical: spacing.lg,
    ...shadow.card,
  },
  macroItem: { flex: 1, alignItems: "center" },
  macroValue: { fontFamily: font.regular, fontSize: 17, fontWeight: "600", color: colors.brand },
  macroLabel: { fontFamily: font.regular, fontSize: 10, color: colors.muted, marginTop: 2 },
  macroDivider: { width: 1, backgroundColor: colors.divider },
  description: {
    fontFamily: font.regular,
    fontSize: 14,
    lineHeight: 21,
    color: colors.onSurfaceTertiary,
    paddingHorizontal: spacing.lg,
    marginTop: spacing.lg,
  },
  tagsRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.sm,
    paddingHorizontal: spacing.lg,
    marginTop: spacing.md,
  },
  tag: {
    backgroundColor: colors.brandTertiary,
    borderRadius: radius.pill,
    paddingHorizontal: spacing.md,
    paddingVertical: 4,
  },
  tagText: { fontFamily: font.regular, fontSize: 12, color: colors.onBrandTertiary },
  sectionRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    paddingHorizontal: spacing.lg,
    marginTop: spacing.xl,
    marginBottom: spacing.md,
  },
  sectionTitle: {
    fontFamily: font.regular,
    fontSize: 18,
    fontWeight: "600",
    color: colors.onSurface,
    paddingHorizontal: spacing.lg,
    marginTop: spacing.xl,
    marginBottom: spacing.md,
  },
  instructionsCard: {
    backgroundColor: colors.surfaceSecondary,
    borderRadius: radius.lg,
    marginHorizontal: spacing.lg,
    paddingHorizontal: spacing.lg,
    ...shadow.card,
  },
  instructionRow: {
    flexDirection: "row",
    alignItems: "flex-start",
    gap: spacing.md,
    paddingVertical: 14,
  },
  stepBadge: {
    width: 26,
    height: 26,
    borderRadius: radius.pill,
    backgroundColor: colors.brandTertiary,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 1,
    flexShrink: 0,
  },
  stepBadgeText: {
    fontFamily: font.regular,
    fontSize: 13,
    fontWeight: "600",
    color: colors.brand,
  },
  instructionText: {
    flex: 1,
    fontFamily: font.regular,
    fontSize: 15,
    lineHeight: 22,
    color: colors.onSurface,
  },
  ingredientsCard: {
    backgroundColor: colors.surfaceSecondary,
    borderRadius: radius.lg,
    marginHorizontal: spacing.lg,
    paddingHorizontal: spacing.lg,
    ...shadow.card,
  },
  ingredientRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.md,
    paddingVertical: 14,
  },
  ingredientDivider: { height: 1, backgroundColor: colors.divider },
  ingredientName: { flex: 1, fontFamily: font.regular, fontSize: 15, color: colors.onSurface },
  ingredientQty: { fontFamily: font.regular, fontSize: 14, color: colors.muted },
  deleteBtn: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: spacing.sm,
    marginHorizontal: spacing.lg,
    marginTop: spacing.xl,
    paddingVertical: 14,
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: colors.error,
    minHeight: 48,
  },
  deleteText: { color: colors.error, fontFamily: font.regular, fontSize: 15, fontWeight: "600" },
});
