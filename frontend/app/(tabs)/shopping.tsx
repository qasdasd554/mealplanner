import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import { router, useFocusEffect } from "expo-router";
import { useCallback, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  SectionList,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { api, MealPlan, ShoppingItem } from "@/src/lib/api";
import { colors, font, radius, shadow, spacing } from "@/src/lib/theme";

function formatQty(item: ShoppingItem) {
  if (item.unit === "szt") return `${item.quantity} szt`;
  if (item.unit === "kg" || item.unit === "l") return `${item.quantity} ${item.unit}`;
  return `${Math.round(item.quantity)} ${item.unit}`;
}

export default function ShoppingScreen() {
  const insets = useSafeAreaInsets();
  const [plan, setPlan] = useState<MealPlan | null>(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    try {
      const data = await api<MealPlan | null>("/meal-plans/active");
      setPlan(data);
    } catch {
      // ignore
    } finally {
      setLoading(false);
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load]),
  );

  const toggle = async (item: ShoppingItem) => {
    if (!plan) return;
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    const updated = {
      ...plan,
      shopping_items: plan.shopping_items.map((i) =>
        i.id === item.id ? { ...i, checked: !i.checked } : i,
      ),
    };
    setPlan(updated);
    try {
      await api(`/meal-plans/active/items/${item.id}`, {
        method: "PATCH",
        body: { checked: !item.checked },
      });
    } catch {
      setPlan(plan);
    }
  };

  const sections = (() => {
    if (!plan) return [];
    const map = new Map<string, ShoppingItem[]>();
    for (const item of plan.shopping_items) {
      if (!map.has(item.department)) map.set(item.department, []);
      map.get(item.department)!.push(item);
    }
    return Array.from(map.entries()).map(([title, data]) => ({ title, data }));
  })();

  const checkedCount = plan?.shopping_items.filter((i) => i.checked).length || 0;

  return (
    <View style={styles.container} testID="shopping-screen">
      <View style={[styles.header, { paddingTop: insets.top + spacing.md }]}>
        <Text style={styles.headerTitle}>Lista zakupów</Text>
        {plan && (
          <Text style={styles.headerSub}>
            {plan.store_name} ·{" "}
            {plan.household_size === 1 ? "1 osoba" : `${plan.household_size} osoby`} ·{" "}
            {checkedCount}/{plan.shopping_items.length} kupione
          </Text>
        )}
      </View>

      {loading ? (
        <View style={styles.center}>
          <ActivityIndicator size="large" color={colors.brand} />
        </View>
      ) : !plan ? (
        <View style={styles.center} testID="empty-shopping-state">
          <View style={styles.emptyBadge}>
            <Ionicons name="cart-outline" size={40} color={colors.brand} />
          </View>
          <Text style={styles.emptyTitle}>Twoja lista zakupów jest pusta</Text>
          <Text style={styles.mutedText}>Wygeneruj plan posiłków, aby ją utworzyć</Text>
          <Pressable
            testID="shopping-generate-plan-button"
            style={styles.generateBtn}
            onPress={() => router.push("/plan-config")}
          >
            <Text style={styles.generateText}>Wygeneruj plan</Text>
          </Pressable>
        </View>
      ) : (
        <>
          <SectionList
            sections={sections}
            keyExtractor={(item) => item.id}
            contentContainerStyle={{ paddingBottom: 120 }}
            stickySectionHeadersEnabled={false}
            renderSectionHeader={({ section }) => (
              <Text style={styles.sectionTitle}>{section.title}</Text>
            )}
            renderItem={({ item }) => (
              <Pressable
                testID={`shopping-item-${item.id}`}
                style={styles.row}
                onPress={() => toggle(item)}
              >
                <Ionicons
                  name={item.checked ? "checkmark-circle" : "ellipse-outline"}
                  size={24}
                  color={item.checked ? colors.success : colors.borderStrong ?? colors.border}
                />
                <View style={[styles.rowInfo, item.checked && { opacity: 0.45 }]}>
                  <Text
                    style={[styles.rowName, item.checked && styles.rowNameChecked]}
                    numberOfLines={1}
                  >
                    {item.name}
                  </Text>
                  <Text style={styles.rowMeta}>
                    {formatQty(item)} · {item.packages} opak.
                  </Text>
                </View>
                <Text style={[styles.rowPrice, item.checked && { opacity: 0.45 }]}>
                  {item.price.toFixed(2)} zł
                </Text>
              </Pressable>
            )}
          />
          <View style={[styles.totalBar, { paddingBottom: spacing.md }]} testID="shopping-total-bar">
            <Text style={styles.totalLabel}>Szacowany koszt</Text>
            <Text style={styles.totalValue}>{plan.total_price.toFixed(2)} zł</Text>
          </View>
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.surface },
  header: { paddingHorizontal: spacing.lg, paddingBottom: spacing.md },
  headerTitle: {
    fontFamily: font.regular,
    fontSize: 24,
    fontWeight: "600",
    color: colors.onSurface,
  },
  headerSub: { fontFamily: font.regular, fontSize: 13, color: colors.muted, marginTop: 2 },
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: spacing.xl,
  },
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
    fontSize: 18,
    fontWeight: "600",
    color: colors.onSurface,
    marginTop: spacing.lg,
    textAlign: "center",
  },
  mutedText: {
    fontFamily: font.regular,
    color: colors.muted,
    fontSize: 14,
    marginTop: spacing.sm,
    textAlign: "center",
  },
  generateBtn: {
    backgroundColor: colors.brand,
    borderRadius: radius.pill,
    paddingHorizontal: spacing.xl,
    paddingVertical: 14,
    marginTop: spacing.xl,
  },
  generateText: { color: colors.onBrand, fontFamily: font.regular, fontSize: 15, fontWeight: "600" },
  sectionTitle: {
    fontFamily: font.regular,
    fontSize: 13,
    fontWeight: "600",
    color: colors.onSurfaceTertiary,
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.lg,
    paddingBottom: spacing.sm,
    textTransform: "uppercase",
    letterSpacing: 0.5,
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: colors.surfaceSecondary,
    marginHorizontal: spacing.lg,
    marginBottom: spacing.sm,
    borderRadius: radius.md,
    padding: spacing.md,
    gap: spacing.md,
    ...shadow.card,
  },
  rowInfo: { flex: 1 },
  rowName: { fontFamily: font.regular, fontSize: 15, color: colors.onSurface, fontWeight: "500" },
  rowNameChecked: { textDecorationLine: "line-through" },
  rowMeta: { fontFamily: font.regular, fontSize: 12, color: colors.muted, marginTop: 1 },
  rowPrice: { fontFamily: font.regular, fontSize: 14, fontWeight: "600", color: colors.onSurface },
  totalBar: {
    position: "absolute",
    left: 0,
    right: 0,
    bottom: 0,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: spacing.xl,
    paddingTop: spacing.md,
    backgroundColor: colors.surfaceSecondary,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  totalLabel: { fontFamily: font.regular, fontSize: 14, color: colors.muted },
  totalValue: { fontFamily: font.regular, fontSize: 20, fontWeight: "600", color: colors.brand },
});
