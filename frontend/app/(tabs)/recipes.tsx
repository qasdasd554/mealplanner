import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import { Image } from "expo-image";
import { router, useFocusEffect } from "expo-router";
import { useCallback, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { api, Recipe } from "@/src/lib/api";
import {
  colors,
  font,
  MEAL_TYPE_ICONS,
  MEAL_TYPES,
  radius,
  shadow,
  spacing,
} from "@/src/lib/theme";

const FILTERS = ["wszystkie", ...MEAL_TYPES];

export default function RecipesScreen() {
  const insets = useSafeAreaInsets();
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("wszystkie");

  const load = useCallback(async () => {
    try {
      const data = await api<Recipe[]>("/recipes");
      setRecipes(data);
    } catch {
      // keep previous
    } finally {
      setLoading(false);
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load]),
  );

  const filtered =
    filter === "wszystkie" ? recipes : recipes.filter((r) => r.meal_type === filter);

  return (
    <View style={styles.container} testID="recipes-screen">
      <View style={[styles.header, { paddingTop: insets.top + spacing.md }]}>
        <Text style={styles.headerTitle}>Przepisy</Text>
        <Text style={styles.headerCount}>{filtered.length}</Text>
      </View>

      <View style={styles.chipsWrap}>
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.chipsRow}
        >
          {FILTERS.map((f) => (
            <Pressable
              key={f}
              testID={`filter-chip-${f}`}
              style={[styles.chip, filter === f && styles.chipActive]}
              onPress={() => {
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
                setFilter(f);
              }}
            >
              <Text style={[styles.chipText, filter === f && styles.chipTextActive]}>
                {f.charAt(0).toUpperCase() + f.slice(1)}
              </Text>
            </Pressable>
          ))}
        </ScrollView>
      </View>

      {loading ? (
        <View style={styles.center}>
          <ActivityIndicator size="large" color={colors.brand} />
        </View>
      ) : (
        <FlatList
          data={filtered}
          keyExtractor={(item) => item.id}
          contentContainerStyle={{ paddingTop: spacing.sm, paddingBottom: 100 }}
          renderItem={({ item }) => (
            <Pressable
              testID={`recipe-card-${item.id}`}
              style={({ pressed }) => [styles.card, pressed && { opacity: 0.9 }]}
              onPress={() => router.push(`/recipe/${item.id}`)}
            >
              {item.image_url ? (
                <Image
                  source={{ uri: item.image_url }}
                  style={styles.cardThumb}
                  contentFit="cover"
                  transition={150}
                />
              ) : (
                <View style={styles.cardIcon}>
                  <Ionicons
                    name={(MEAL_TYPE_ICONS[item.meal_type] || "restaurant-outline") as any}
                    size={22}
                    color={colors.brand}
                  />
                </View>
              )}
              <View style={styles.cardInfo}>
                <View style={styles.cardTitleRow}>
                  <Text style={styles.cardName} numberOfLines={1}>
                    {item.name}
                  </Text>
                  {item.is_custom && (
                    <View style={styles.ownBadge}>
                      <Text style={styles.ownBadgeText}>Mój</Text>
                    </View>
                  )}
                </View>
                <Text style={styles.cardMeta}>
                  {item.meal_type} · {item.prep_time_min + item.cook_time_min} min ·{" "}
                  {item.servings} porcje
                </Text>
                <Text style={styles.cardMacros}>
                  {Math.round(item.nutrition_per_serving.kcal)} kcal · B{" "}
                  {item.nutrition_per_serving.protein} g · T {item.nutrition_per_serving.fat} g
                  · W {item.nutrition_per_serving.carbs} g
                </Text>
              </View>
              <Ionicons name="chevron-forward" size={18} color={colors.muted} />
            </Pressable>
          )}
          ListEmptyComponent={
            <View style={styles.center}>
              <Text style={styles.emptyText}>Brak przepisów w tej kategorii</Text>
            </View>
          }
        />
      )}

      <Pressable
        testID="add-recipe-fab"
        style={styles.fab}
        onPress={() => {
          Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
          router.push("/add-recipe");
        }}
      >
        <Ionicons name="add" size={26} color={colors.onBrand} />
        <Text style={styles.fabText}>Dodaj przepis</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.surface },
  header: {
    flexDirection: "row",
    alignItems: "flex-end",
    justifyContent: "space-between",
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.md,
  },
  headerTitle: {
    fontFamily: font.regular,
    fontSize: 24,
    fontWeight: "600",
    color: colors.onSurface,
  },
  headerCount: { fontFamily: font.regular, fontSize: 14, color: colors.muted },
  chipsWrap: { height: 56, justifyContent: "center" },
  chipsRow: { paddingHorizontal: spacing.lg, gap: spacing.sm, alignItems: "center" },
  chip: {
    height: 36,
    paddingHorizontal: spacing.lg,
    borderRadius: radius.pill,
    backgroundColor: colors.surfaceSecondary,
    borderWidth: 1,
    borderColor: colors.border,
    justifyContent: "center",
    flexShrink: 0,
  },
  chipActive: { backgroundColor: colors.brandTertiary, borderColor: colors.brandSecondary },
  chipText: { fontFamily: font.regular, fontSize: 13, color: colors.onSurfaceTertiary },
  chipTextActive: { color: colors.onBrandTertiary },
  center: { flex: 1, alignItems: "center", justifyContent: "center", paddingTop: spacing.xxxl },
  emptyText: { fontFamily: font.regular, color: colors.muted, fontSize: 14 },
  card: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: colors.surfaceSecondary,
    borderRadius: radius.lg,
    marginHorizontal: spacing.lg,
    marginBottom: spacing.md,
    padding: spacing.lg,
    gap: spacing.md,
    ...shadow.card,
  },
  cardIcon: {
    width: 52,
    height: 52,
    borderRadius: radius.md,
    backgroundColor: colors.brandTertiary,
    alignItems: "center",
    justifyContent: "center",
  },
  cardThumb: {
    width: 52,
    height: 52,
    borderRadius: radius.md,
    backgroundColor: colors.surfaceTertiary,
  },
  cardInfo: { flex: 1 },
  cardTitleRow: { flexDirection: "row", alignItems: "center", gap: spacing.sm },
  cardName: {
    fontFamily: font.regular,
    fontSize: 16,
    fontWeight: "600",
    color: colors.onSurface,
    flexShrink: 1,
  },
  ownBadge: {
    backgroundColor: colors.success,
    borderRadius: radius.sm,
    paddingHorizontal: 6,
    paddingVertical: 1,
  },
  ownBadgeText: { color: "#fff", fontSize: 10, fontFamily: font.regular, fontWeight: "600" },
  cardMeta: { fontFamily: font.regular, fontSize: 12, color: colors.muted, marginTop: 2 },
  cardMacros: { fontFamily: font.regular, fontSize: 12, color: colors.onSurfaceTertiary, marginTop: 2 },
  fab: {
    position: "absolute",
    right: spacing.lg,
    bottom: spacing.lg,
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.xs,
    backgroundColor: colors.brand,
    borderRadius: radius.pill,
    paddingLeft: spacing.md,
    paddingRight: spacing.lg,
    height: 52,
    ...shadow.card,
  },
  fabText: { color: colors.onBrand, fontFamily: font.regular, fontSize: 15, fontWeight: "600" },
});
