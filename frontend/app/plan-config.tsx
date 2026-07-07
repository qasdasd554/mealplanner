import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import { router } from "expo-router";
import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { KeyboardAwareScrollView } from "react-native-keyboard-controller";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { api, Store } from "@/src/lib/api";
import { colors, font, radius, shadow, spacing } from "@/src/lib/theme";

const DAYS_OPTIONS = [1, 2, 3, 5, 7, 10, 14];
const HOUSEHOLD_OPTIONS = [1, 2, 3, 4, 5, 6];

const SLOT_OPTIONS: { key: string; label: string; icon: string }[] = [
  { key: "śniadanie", label: "Śniadanie", icon: "sunny-outline" },
  { key: "obiad", label: "Obiad", icon: "restaurant-outline" },
  { key: "kolacja", label: "Kolacja", icon: "moon-outline" },
  { key: "przekąska", label: "Przekąska", icon: "cafe-outline" },
];

export default function PlanConfigScreen() {
  const insets = useSafeAreaInsets();
  const [stores, setStores] = useState<Store[]>([]);
  const [days, setDays] = useState(5);
  const [selectedSlots, setSelectedSlots] = useState<string[]>(["śniadanie", "obiad", "kolacja"]);
  const [householdSize, setHouseholdSize] = useState(2);
  const [storeId, setStoreId] = useState<string | null>(null);
  const [budgetText, setBudgetText] = useState("");
  const [targetKcalText, setTargetKcalText] = useState("");
  const [minCost, setMinCost] = useState<number | null>(null);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api<Store[]>("/stores")
      .then((data) => {
        setStores(data);
        if (data.length > 0) setStoreId(data[0].id);
      })
      .catch(() => setError("Nie udało się pobrać sklepów"));
  }, []);

  useEffect(() => {
    if (!storeId || selectedSlots.length === 0) return;
    setMinCost(null);
    api<{ min_cost: number }>(
      `/meal-plans/min-cost?days=${days}&meals_per_day=${selectedSlots.length}&store_id=${storeId}&household_size=${householdSize}`,
    )
      .then((data) => setMinCost(data.min_cost))
      .catch(() => setMinCost(null));
  }, [days, selectedSlots, storeId, householdSize]);

  const toggleSlot = (slot: string) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setSelectedSlots((prev) => {
      if (prev.includes(slot)) {
        if (prev.length <= 1) return prev; // minimum 1 slot
        return prev.filter((s) => s !== slot);
      }
      return [...prev, slot];
    });
  };

  const parsedBudget = budgetText.trim()
    ? parseFloat(budgetText.replace(",", "."))
    : null;
  const budgetTooLow =
    parsedBudget !== null && minCost !== null && !isNaN(parsedBudget) && parsedBudget < minCost;

  const parsedKcal = targetKcalText.trim()
    ? parseInt(targetKcalText, 10)
    : null;

  const generate = async () => {
    if (!storeId || selectedSlots.length === 0) return;
    setError(null);
    if (parsedBudget !== null && (isNaN(parsedBudget) || parsedBudget <= 0)) {
      setError("Podaj prawidłową kwotę budżetu");
      return;
    }
    if (budgetTooLow && minCost !== null) {
      setError(
        `Budżet nie może być niższy niż najtańsza opcja: ${minCost.toFixed(2)} zł`,
      );
      return;
    }
    if (parsedKcal !== null && (isNaN(parsedKcal) || parsedKcal < 800 || parsedKcal > 6000)) {
      setError("Cel kaloryczny musi być między 800 a 6000 kcal");
      return;
    }
    setGenerating(true);
    try {
      await api("/meal-plans/generate", {
        method: "POST",
        body: {
          days,
          meals_per_day: selectedSlots.length,
          slots: selectedSlots,
          store_id: storeId,
          household_size: householdSize,
          ...(parsedBudget !== null ? { budget: parsedBudget } : {}),
          ...(parsedKcal !== null ? { target_kcal: parsedKcal } : {}),
        },
      });
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      router.back();
    } catch (e: any) {
      setError(e.message || "Nie udało się wygenerować planu");
      setGenerating(false);
    }
  };

  return (
    <View style={styles.container} testID="plan-config-screen">
      <View style={[styles.header, { paddingTop: insets.top + spacing.md }]}>
        <Pressable testID="plan-config-close" style={styles.closeBtn} onPress={() => router.back()}>
          <Ionicons name="close" size={22} color={colors.onSurface} />
        </Pressable>
        <Text style={styles.headerTitle}>Nowy plan</Text>
        <View style={{ width: 40 }} />
      </View>

      <KeyboardAwareScrollView
        contentContainerStyle={{ paddingBottom: 160 }}
        bottomOffset={110}
        keyboardShouldPersistTaps="handled"
      >
        <Text style={styles.bigTitle}>Skonfiguruj swój plan</Text>
        <Text style={styles.subtitle}>
          Dobierzemy przepisy i przygotujemy listę zakupów
        </Text>

        <Text style={styles.label}>Dla ilu osób</Text>
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.chipScrollRow}
        >
          {HOUSEHOLD_OPTIONS.map((n) => (
            <Pressable
              key={n}
              testID={`household-chip-${n}`}
              style={[styles.chip, householdSize === n && styles.chipActive]}
              onPress={() => {
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
                setHouseholdSize(n);
              }}
            >
              <Text style={[styles.chipText, householdSize === n && styles.chipTextActive]}>
                {n === 1 ? "1 osoba" : `${n} osoby`}
              </Text>
            </Pressable>
          ))}
        </ScrollView>

        <Text style={styles.label}>Liczba dni</Text>
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.chipScrollRow}
        >
          {DAYS_OPTIONS.map((d) => (
            <Pressable
              key={d}
              testID={`days-chip-${d}`}
              style={[styles.chip, days === d && styles.chipActive]}
              onPress={() => {
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
                setDays(d);
              }}
            >
              <Text style={[styles.chipText, days === d && styles.chipTextActive]}>
                {d === 1 ? "1 dzień" : d < 5 ? `${d} dni` : `${d} dni`}
              </Text>
            </Pressable>
          ))}
        </ScrollView>

        <Text style={styles.label}>Jakie posiłki chcesz w planie?</Text>
        <View style={styles.slotGrid}>
          {SLOT_OPTIONS.map((opt) => {
            const active = selectedSlots.includes(opt.key);
            return (
              <Pressable
                key={opt.key}
                testID={`slot-toggle-${opt.key}`}
                style={[styles.slotChip, active && styles.slotChipActive]}
                onPress={() => toggleSlot(opt.key)}
              >
                <Ionicons
                  name={active ? "checkmark-circle" : (opt.icon as any)}
                  size={20}
                  color={active ? colors.brand : colors.muted}
                />
                <Text style={[styles.slotChipText, active && styles.slotChipTextActive]}>
                  {opt.label}
                </Text>
              </Pressable>
            );
          })}
        </View>

        <Text style={styles.label}>Cel kaloryczny dziennie (kcal)</Text>
        <View style={styles.budgetWrap}>
          <TextInput
            testID="kcal-input"
            style={styles.budgetInput}
            placeholder="np. 2000 (opcjonalnie)"
            placeholderTextColor={colors.muted}
            keyboardType="number-pad"
            value={targetKcalText}
            onChangeText={setTargetKcalText}
          />
          <Text style={styles.budgetHint}>
            Plan będzie dążył do tej wartości kalorycznej na każdy dzień
          </Text>
        </View>

        <Text style={styles.label}>Sklep</Text>
        {stores.map((store) => (
          <Pressable
            key={store.id}
            testID={`store-option-${store.name}`}
            style={[styles.storeCard, storeId === store.id && styles.storeCardActive]}
            onPress={() => {
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
              setStoreId(store.id);
            }}
          >
            <View style={styles.storeIcon}>
              <Ionicons name="storefront-outline" size={22} color={colors.brand} />
            </View>
            <Text style={styles.storeName}>{store.name}</Text>
            <Ionicons
              name={storeId === store.id ? "radio-button-on" : "radio-button-off"}
              size={22}
              color={storeId === store.id ? colors.brand : colors.border}
            />
          </Pressable>
        ))}

        <Text style={styles.label}>Budżet na zakupy (zł)</Text>
        <View style={styles.budgetWrap}>
          <TextInput
            testID="budget-input"
            style={[styles.budgetInput, budgetTooLow && styles.budgetInputError]}
            placeholder="np. 150 (opcjonalnie)"
            placeholderTextColor={colors.muted}
            keyboardType="decimal-pad"
            value={budgetText}
            onChangeText={setBudgetText}
          />
          {minCost !== null ? (
            <Text
              testID="min-cost-hint"
              style={[styles.budgetHint, budgetTooLow && styles.budgetHintError]}
            >
              {budgetTooLow
                ? `Za mało — najtańszy możliwy plan to ${minCost.toFixed(2)} zł`
                : `Najtańszy możliwy plan: ${minCost.toFixed(2)} zł`}
            </Text>
          ) : (
            <Text style={styles.budgetHint}>Obliczanie minimalnego kosztu...</Text>
          )}
        </View>

        {error && (
          <Text testID="plan-config-error" style={styles.error}>
            {error}
          </Text>
        )}
      </KeyboardAwareScrollView>

      <View style={[styles.stickyBar, { paddingBottom: insets.bottom + spacing.md }]}>
        <Pressable
          testID="generate-plan-submit"
          style={({ pressed }) => [styles.generateBtn, pressed && { opacity: 0.85 }]}
          onPress={generate}
          disabled={generating || !storeId || selectedSlots.length === 0}
        >
          {generating ? (
            <ActivityIndicator color={colors.onBrand} />
          ) : (
            <>
              <Ionicons name="sparkles-outline" size={18} color={colors.onBrand} />
              <Text style={styles.generateText}>Generuj plan</Text>
            </>
          )}
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.surface },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.sm,
  },
  closeBtn: {
    width: 40,
    height: 40,
    borderRadius: radius.pill,
    backgroundColor: colors.surfaceTertiary,
    alignItems: "center",
    justifyContent: "center",
  },
  headerTitle: { fontFamily: font.regular, fontSize: 16, fontWeight: "600", color: colors.onSurface },
  bigTitle: {
    fontFamily: font.regular,
    fontSize: 26,
    fontWeight: "600",
    color: colors.onSurface,
    paddingHorizontal: spacing.lg,
    marginTop: spacing.md,
  },
  subtitle: {
    fontFamily: font.regular,
    fontSize: 14,
    color: colors.muted,
    paddingHorizontal: spacing.lg,
    marginTop: spacing.xs,
  },
  label: {
    fontFamily: font.regular,
    fontSize: 13,
    fontWeight: "600",
    color: colors.onSurfaceTertiary,
    paddingHorizontal: spacing.lg,
    marginTop: spacing.xl,
    marginBottom: spacing.md,
  },
  chipScrollRow: {
    paddingHorizontal: spacing.lg,
    gap: spacing.sm,
    alignItems: "center",
  },
  chip: {
    height: 40,
    paddingHorizontal: spacing.lg,
    borderRadius: radius.pill,
    backgroundColor: colors.surfaceSecondary,
    borderWidth: 1,
    borderColor: colors.border,
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  },
  chipActive: { backgroundColor: colors.brandTertiary, borderColor: colors.brandSecondary },
  chipText: { fontFamily: font.regular, fontSize: 14, color: colors.onSurfaceTertiary },
  chipTextActive: { color: colors.onBrandTertiary, fontWeight: "600" },
  slotGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    paddingHorizontal: spacing.lg,
    gap: spacing.sm,
  },
  slotChip: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.xs,
    paddingVertical: 10,
    paddingHorizontal: spacing.lg,
    borderRadius: radius.pill,
    backgroundColor: colors.surfaceSecondary,
    borderWidth: 1.5,
    borderColor: colors.border,
  },
  slotChipActive: {
    backgroundColor: colors.brandTertiary,
    borderColor: colors.brand,
  },
  slotChipText: {
    fontFamily: font.regular,
    fontSize: 14,
    color: colors.onSurfaceTertiary,
  },
  slotChipTextActive: {
    color: colors.onBrandTertiary,
    fontWeight: "600",
  },
  storeCard: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.md,
    backgroundColor: colors.surfaceSecondary,
    borderRadius: radius.lg,
    borderWidth: 1.5,
    borderColor: colors.border,
    marginHorizontal: spacing.lg,
    marginBottom: spacing.sm,
    padding: spacing.lg,
    ...shadow.card,
  },
  storeCardActive: { borderColor: colors.brand },
  storeIcon: {
    width: 42,
    height: 42,
    borderRadius: radius.md,
    backgroundColor: colors.brandTertiary,
    alignItems: "center",
    justifyContent: "center",
  },
  storeName: { flex: 1, fontFamily: font.regular, fontSize: 16, fontWeight: "600", color: colors.onSurface },
  error: {
    color: colors.error,
    fontFamily: font.regular,
    fontSize: 13,
    paddingHorizontal: spacing.lg,
    marginTop: spacing.lg,
  },
  budgetWrap: { paddingHorizontal: spacing.lg },
  budgetInput: {
    backgroundColor: colors.surfaceSecondary,
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: colors.border,
    paddingHorizontal: spacing.lg,
    paddingVertical: 13,
    fontSize: 15,
    fontFamily: font.regular,
    color: colors.onSurface,
  },
  budgetInputError: { borderColor: colors.error },
  budgetHint: {
    fontFamily: font.regular,
    fontSize: 12,
    color: colors.muted,
    marginTop: spacing.sm,
  },
  budgetHintError: { color: colors.error },
  stickyBar: {
    position: "absolute",
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: colors.surface,
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  generateBtn: {
    flexDirection: "row",
    gap: spacing.sm,
    backgroundColor: colors.brand,
    borderRadius: radius.md,
    paddingVertical: 15,
    alignItems: "center",
    justifyContent: "center",
    minHeight: 52,
  },
  generateText: { color: colors.onBrand, fontSize: 16, fontFamily: font.regular, fontWeight: "600" },
});
