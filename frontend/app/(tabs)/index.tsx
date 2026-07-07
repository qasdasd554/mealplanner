import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import { router, useFocusEffect } from "expo-router";
import { useCallback, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  RefreshControl,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { useAuth } from "@/src/context/AuthContext";
import { api, MealPlan } from "@/src/lib/api";
import {
  colors,
  font,
  MEAL_TYPE_ICONS,
  radius,
  shadow,
  spacing,
} from "@/src/lib/theme";

const SLOT_ORDER = ["śniadanie", "II śniadanie", "obiad", "przekąska", "podwieczorek", "kolacja"];

export default function HomeScreen() {
  const insets = useSafeAreaInsets();
  const { user } = useAuth();
  const [plan, setPlan] = useState<MealPlan | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedDay, setSelectedDay] = useState(1);
  const [swapping, setSwapping] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      setError(null);
      const data = await api<MealPlan | null>("/meal-plans/active");
      setPlan(data);
      if (data && selectedDay > data.days) setSelectedDay(1);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [selectedDay]);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load]),
  );

  const swapMeal = async (day: number, slot: string) => {
    if (!plan) return;
    const key = `${day}-${slot}`;
    setSwapping(key);
    try {
      const updated = await api<MealPlan>("/meal-plans/active/swap", {
        method: "POST",
        body: { day, slot },
      });
      setPlan(updated);
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    } catch (e: any) {
      setError(e.message || "Nie udało się podmienić posiłku");
    } finally {
      setSwapping(null);
    }
  };

  const dayNutrition = plan?.daily_nutrition.find((d) => d.day === selectedDay);
  const dayEntries = (plan?.entries || [])
    .filter((e) => e.day === selectedDay)
    .sort((a, b) => SLOT_ORDER.indexOf(a.slot) - SLOT_ORDER.indexOf(b.slot));

  return (
    <View style={styles.container} testID="home-screen">
      <View style={[styles.header, { paddingTop: insets.top + spacing.md }]}>
        <View>
          <Text style={styles.greeting}>Cześć, {user?.display_name || ""} 👋</Text>
          <Text style={styles.headerTitle}>Twój plan posiłków</Text>
          {plan && (
            <Text style={styles.headerMeta} testID="plan-summary">
              {plan.days === 1 ? "1 dzień" : `${plan.days} dni`} ·{" "}
              {plan.meals_per_day === 1 ? "1 posiłek" : `${plan.meals_per_day} posiłki dziennie`}
              {" · "}
              {plan.household_size === 1 ? "1 osoba" : `${plan.household_size} osoby`}
            </Text>
          )}
        </View>
        {plan && (
          <Pressable
            testID="regenerate-plan-button"
            style={styles.headerAction}
            onPress={() => router.push("/plan-config")}
          >
            <Ionicons name="refresh-outline" size={20} color={colors.brand} />
          </Pressable>
        )}
      </View>

      {loading ? (
        <View style={styles.center}>
          <ActivityIndicator size="large" color={colors.brand} />
          <Text style={styles.mutedText}>Ładowanie planu...</Text>
        </View>
      ) : error ? (
        <View style={styles.center}>
          <Text style={styles.mutedText}>Nie udało się pobrać planu</Text>
          <Pressable testID="retry-plan-button" style={styles.retryBtn} onPress={load}>
            <Text style={styles.retryText}>Spróbuj ponownie</Text>
          </Pressable>
        </View>
      ) : !plan ? (
        <View style={styles.center} testID="empty-plan-state">
          <View style={styles.emptyBadge}>
            <Ionicons name="restaurant-outline" size={40} color={colors.brand} />
          </View>
          <Text style={styles.emptyTitle}>Brak aktywnego planu</Text>
          <Text style={styles.mutedText}>
            Wygeneruj plan posiłków dopasowany do Ciebie
          </Text>
          <Pressable
            testID="generate-plan-button"
            style={styles.generateBtn}
            onPress={() => {
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
              router.push("/plan-config");
            }}
          >
            <Ionicons name="sparkles-outline" size={18} color={colors.onBrand} />
            <Text style={styles.generateText}>Wygeneruj plan</Text>
          </Pressable>
        </View>
      ) : (
        <>
          <View style={styles.daysWrap}>
            <ScrollView
              horizontal
              showsHorizontalScrollIndicator={false}
              contentContainerStyle={styles.daysRow}
            >
              {Array.from({ length: plan.days }, (_, i) => i + 1).map((day) => (
                <Pressable
                  key={day}
                  testID={`day-chip-${day}`}
                  style={[styles.dayChip, selectedDay === day && styles.dayChipActive]}
                  onPress={() => {
                    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
                    setSelectedDay(day);
                  }}
                >
                  <Text
                    style={[
                      styles.dayChipText,
                      selectedDay === day && styles.dayChipTextActive,
                    ]}
                  >
                    Dzień {day}
                  </Text>
                </Pressable>
              ))}
            </ScrollView>
          </View>

          <ScrollView
            contentContainerStyle={{ paddingBottom: spacing.xl }}
            refreshControl={
              <RefreshControl
                refreshing={refreshing}
                onRefresh={() => {
                  setRefreshing(true);
                  load();
                }}
                tintColor={colors.brand}
              />
            }
          >
            {dayNutrition && (
              <View style={styles.macroCard} testID="daily-macro-card">
                <View style={styles.macroItem}>
                  <Text style={styles.macroValue}>{dayNutrition.kcal}</Text>
                  <Text style={styles.macroLabel}>kcal</Text>
                </View>
                <View style={styles.macroDivider} />
                <View style={styles.macroItem}>
                  <Text style={styles.macroValue}>{dayNutrition.protein} g</Text>
                  <Text style={styles.macroLabel}>Białko</Text>
                </View>
                <View style={styles.macroDivider} />
                <View style={styles.macroItem}>
                  <Text style={styles.macroValue}>{dayNutrition.fat} g</Text>
                  <Text style={styles.macroLabel}>Tłuszcze</Text>
                </View>
                <View style={styles.macroDivider} />
                <View style={styles.macroItem}>
                  <Text style={styles.macroValue}>{dayNutrition.carbs} g</Text>
                  <Text style={styles.macroLabel}>Węgle</Text>
                </View>
              </View>
            )}

            {dayEntries.map((entry) => (
              <Pressable
                key={`${entry.day}-${entry.slot}`}
                testID={`meal-card-${entry.slot}`}
                style={({ pressed }) => [styles.mealCard, pressed && { opacity: 0.9 }]}
                onPress={() => router.push(`/recipe/${entry.recipe_id}`)}
              >
                <View style={styles.mealIconWrap}>
                  <Ionicons
                    name={(MEAL_TYPE_ICONS[entry.slot] || "restaurant-outline") as any}
                    size={22}
                    color={colors.brand}
                  />
                </View>
                <View style={styles.mealInfo}>
                  <Text style={styles.mealSlot}>{entry.slot.toUpperCase()}</Text>
                  <Text style={styles.mealName} numberOfLines={2}>
                    {entry.recipe_name}
                  </Text>
                  <Text style={styles.mealMeta}>
                    {Math.round(entry.nutrition_per_serving.kcal)} kcal ·{" "}
                    {entry.prep_time_min + entry.cook_time_min} min
                  </Text>
                </View>
                <Pressable
                  testID={`swap-meal-${entry.slot}`}
                  style={styles.swapBtn}
                  onPress={(e) => {
                    e.stopPropagation();
                    swapMeal(entry.day, entry.slot);
                  }}
                  disabled={swapping === `${entry.day}-${entry.slot}`}
                  hitSlop={8}
                >
                  {swapping === `${entry.day}-${entry.slot}` ? (
                    <ActivityIndicator size="small" color={colors.brand} />
                  ) : (
                    <Ionicons name="swap-horizontal-outline" size={18} color={colors.brand} />
                  )}
                </Pressable>
                <Ionicons name="chevron-forward" size={18} color={colors.muted} />
              </Pressable>
            ))}
          </ScrollView>
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.surface },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-end",
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.md,
    backgroundColor: colors.surface,
  },
  greeting: { fontFamily: font.regular, fontSize: 13, color: colors.muted },
  headerTitle: {
    fontFamily: font.regular,
    fontSize: 24,
    fontWeight: "600",
    color: colors.onSurface,
    marginTop: 2,
  },
  headerMeta: {
    fontFamily: font.regular,
    fontSize: 12,
    color: colors.muted,
    marginTop: 4,
  },
  headerAction: {
    width: 44,
    height: 44,
    borderRadius: radius.pill,
    backgroundColor: colors.brandTertiary,
    alignItems: "center",
    justifyContent: "center",
  },
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: spacing.xl,
  },
  mutedText: {
    fontFamily: font.regular,
    color: colors.muted,
    fontSize: 14,
    marginTop: spacing.md,
    textAlign: "center",
  },
  retryBtn: {
    marginTop: spacing.lg,
    paddingHorizontal: spacing.xl,
    paddingVertical: spacing.md,
    backgroundColor: colors.brandTertiary,
    borderRadius: radius.pill,
  },
  retryText: { color: colors.onBrandTertiary, fontFamily: font.regular, fontWeight: "600" },
  emptyBadge: {
    width: 88,
    height: 88,
    borderRadius: radius.pill,
    backgroundColor: colors.brandTertiary,
    alignItems: "center",
    justifyContent: "center",
  },
  emptyTitle: {
    fontFamily: font.regular,
    fontSize: 20,
    fontWeight: "600",
    color: colors.onSurface,
    marginTop: spacing.lg,
  },
  generateBtn: {
    flexDirection: "row",
    gap: spacing.sm,
    alignItems: "center",
    backgroundColor: colors.brand,
    borderRadius: radius.pill,
    paddingHorizontal: spacing.xl,
    paddingVertical: 14,
    marginTop: spacing.xl,
  },
  generateText: { color: colors.onBrand, fontSize: 16, fontFamily: font.regular, fontWeight: "600" },
  daysWrap: { height: 56, justifyContent: "center" },
  daysRow: { paddingHorizontal: spacing.lg, gap: spacing.sm, alignItems: "center" },
  dayChip: {
    height: 36,
    paddingHorizontal: spacing.lg,
    borderRadius: radius.pill,
    backgroundColor: colors.surfaceSecondary,
    borderWidth: 1,
    borderColor: colors.border,
    justifyContent: "center",
    flexShrink: 0,
  },
  dayChipActive: { backgroundColor: colors.surfaceInverse, borderColor: colors.surfaceInverse },
  dayChipText: { fontFamily: font.regular, fontSize: 13, color: colors.onSurfaceTertiary },
  dayChipTextActive: { color: colors.onSurfaceInverse },
  macroCard: {
    flexDirection: "row",
    backgroundColor: colors.surfaceSecondary,
    borderRadius: radius.lg,
    marginHorizontal: spacing.lg,
    marginTop: spacing.md,
    marginBottom: spacing.lg,
    paddingVertical: spacing.lg,
    ...shadow.card,
  },
  macroItem: { flex: 1, alignItems: "center" },
  macroValue: {
    fontFamily: font.regular,
    fontSize: 17,
    fontWeight: "600",
    color: colors.brand,
  },
  macroLabel: { fontFamily: font.regular, fontSize: 11, color: colors.muted, marginTop: 2 },
  macroDivider: { width: 1, backgroundColor: colors.divider },
  mealCard: {
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
  mealIconWrap: {
    width: 48,
    height: 48,
    borderRadius: radius.md,
    backgroundColor: colors.brandTertiary,
    alignItems: "center",
    justifyContent: "center",
  },
  mealInfo: { flex: 1 },
  mealSlot: {
    fontFamily: font.regular,
    fontSize: 10,
    color: colors.brand,
    letterSpacing: 1,
    fontWeight: "600",
  },
  mealName: {
    fontFamily: font.regular,
    fontSize: 16,
    color: colors.onSurface,
    fontWeight: "600",
    marginTop: 2,
  },
  mealMeta: { fontFamily: font.regular, fontSize: 12, color: colors.muted, marginTop: 2 },
  swapBtn: {
    width: 36,
    height: 36,
    borderRadius: radius.pill,
    backgroundColor: colors.brandTertiary,
    alignItems: "center",
    justifyContent: "center",
  },
});
