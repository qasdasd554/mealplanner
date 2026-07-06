import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import { router } from "expo-router";
import { useEffect, useMemo, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  Modal,
  Pressable,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import {
  KeyboardAwareScrollView,
  KeyboardStickyView,
} from "react-native-keyboard-controller";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { api, Nutrition, Product } from "@/src/lib/api";
import { colors, font, MEAL_TYPES, radius, shadow, spacing } from "@/src/lib/theme";

interface DraftIngredient {
  product: Product;
  quantityText: string;
  unit: string;
}

function weightG(product: Product, quantity: number, unit: string): number {
  if (unit === "kg" || unit === "l") return quantity * 1000;
  if (unit === "g" || unit === "ml") return quantity;
  if (unit === "szt") return quantity * (product.weight_per_unit_g || 100);
  return quantity;
}

function unitOptions(product: Product): string[] {
  if (product.unit === "kg") return ["g", "kg"];
  if (product.unit === "l") return ["ml", "l"];
  if (product.unit === "szt") return ["szt"];
  return [product.unit];
}

export default function AddRecipeScreen() {
  const insets = useSafeAreaInsets();
  const [products, setProducts] = useState<Product[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [mealType, setMealType] = useState<string>("śniadanie");
  const [servings, setServings] = useState(2);
  const [prepTime, setPrepTime] = useState("15");
  const [ingredients, setIngredients] = useState<DraftIngredient[]>([]);
  const [pickerVisible, setPickerVisible] = useState(false);
  const [search, setSearch] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    api<Product[]>("/products").then(setProducts).catch(() => {});
  }, []);

  const totals: Nutrition = useMemo(() => {
    const sum = { kcal: 0, protein: 0, fat: 0, carbs: 0 };
    for (const ing of ingredients) {
      const qty = parseFloat(ing.quantityText.replace(",", "."));
      if (!qty || qty <= 0) continue;
      const w = weightG(ing.product, qty, ing.unit);
      const n = ing.product.nutrition_per_100;
      sum.kcal += (n.kcal * w) / 100;
      sum.protein += (n.protein * w) / 100;
      sum.fat += (n.fat * w) / 100;
      sum.carbs += (n.carbs * w) / 100;
    }
    return {
      kcal: Math.round(sum.kcal),
      protein: Math.round(sum.protein * 10) / 10,
      fat: Math.round(sum.fat * 10) / 10,
      carbs: Math.round(sum.carbs * 10) / 10,
    };
  }, [ingredients]);

  const perServing = {
    kcal: Math.round(totals.kcal / servings),
    protein: Math.round((totals.protein / servings) * 10) / 10,
    fat: Math.round((totals.fat / servings) * 10) / 10,
    carbs: Math.round((totals.carbs / servings) * 10) / 10,
  };

  const filteredProducts = products.filter((p) =>
    p.name.toLowerCase().includes(search.toLowerCase()),
  );

  const addIngredient = (product: Product) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    const defaultUnit = unitOptions(product)[0];
    setIngredients((prev) => [
      ...prev,
      { product, quantityText: defaultUnit === "szt" ? "1" : "100", unit: defaultUnit },
    ]);
    setPickerVisible(false);
    setSearch("");
  };

  const save = async () => {
    setError(null);
    if (name.trim().length < 2) {
      setError("Podaj nazwę przepisu (min. 2 znaki)");
      return;
    }
    const parsed = ingredients
      .map((ing) => ({
        product_id: ing.product.id,
        quantity: parseFloat(ing.quantityText.replace(",", ".")),
        unit: ing.unit === "g" && ing.product.unit === "kg" ? "g" : ing.unit,
      }))
      .filter((i) => i.quantity > 0);
    if (parsed.length === 0) {
      setError("Dodaj przynajmniej jeden składnik z ilością");
      return;
    }
    setSaving(true);
    try {
      await api("/recipes", {
        method: "POST",
        body: {
          name: name.trim(),
          description: description.trim(),
          meal_type: mealType,
          servings,
          prep_time_min: parseInt(prepTime, 10) || 0,
          cook_time_min: 0,
          ingredients: parsed,
        },
      });
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      router.back();
    } catch (e: any) {
      setError(e.message || "Nie udało się zapisać przepisu");
      setSaving(false);
    }
  };

  return (
    <View style={styles.container} testID="add-recipe-screen">
      <View style={[styles.header, { paddingTop: insets.top + spacing.md }]}>
        <Pressable testID="add-recipe-close" style={styles.closeBtn} onPress={() => router.back()}>
          <Ionicons name="close" size={22} color={colors.onSurface} />
        </Pressable>
        <Text style={styles.headerTitle}>Nowy przepis</Text>
        <View style={{ width: 40 }} />
      </View>

      <View style={styles.liveMacroBar} testID="live-macro-bar">
        <Text style={styles.liveMacroTitle}>Na porcję:</Text>
        <Text style={styles.liveMacroText}>
          {perServing.kcal} kcal · B {perServing.protein} g · T {perServing.fat} g · W{" "}
          {perServing.carbs} g
        </Text>
      </View>

      <KeyboardAwareScrollView
        contentContainerStyle={{ paddingBottom: 140 }}
        bottomOffset={100}
        keyboardShouldPersistTaps="handled"
      >
        <Text style={styles.label}>Nazwa przepisu</Text>
        <TextInput
          testID="recipe-name-input"
          style={styles.input}
          placeholder="np. Owsianka z owocami"
          placeholderTextColor={colors.muted}
          value={name}
          onChangeText={setName}
        />

        <Text style={styles.label}>Opis (opcjonalnie)</Text>
        <TextInput
          testID="recipe-description-input"
          style={[styles.input, styles.inputMultiline]}
          placeholder="Krótki opis przygotowania..."
          placeholderTextColor={colors.muted}
          value={description}
          onChangeText={setDescription}
          multiline
        />

        <Text style={styles.label}>Pora posiłku</Text>
        <View style={styles.chipsWrapRow}>
          {MEAL_TYPES.map((mt) => (
            <Pressable
              key={mt}
              testID={`meal-type-chip-${mt}`}
              style={[styles.chip, mealType === mt && styles.chipActive]}
              onPress={() => setMealType(mt)}
            >
              <Text style={[styles.chipText, mealType === mt && styles.chipTextActive]}>
                {mt.charAt(0).toUpperCase() + mt.slice(1)}
              </Text>
            </Pressable>
          ))}
        </View>

        <View style={styles.rowSplit}>
          <View style={{ flex: 1 }}>
            <Text style={styles.label}>Porcje</Text>
            <View style={styles.stepper}>
              <Pressable
                testID="servings-minus"
                style={styles.stepperBtn}
                onPress={() => setServings((s) => Math.max(1, s - 1))}
              >
                <Ionicons name="remove" size={18} color={colors.onSurface} />
              </Pressable>
              <Text style={styles.stepperValue} testID="servings-value">
                {servings}
              </Text>
              <Pressable
                testID="servings-plus"
                style={styles.stepperBtn}
                onPress={() => setServings((s) => Math.min(12, s + 1))}
              >
                <Ionicons name="add" size={18} color={colors.onSurface} />
              </Pressable>
            </View>
          </View>
          <View style={{ flex: 1 }}>
            <Text style={styles.label}>Czas (min)</Text>
            <TextInput
              testID="prep-time-input"
              style={styles.input}
              keyboardType="number-pad"
              value={prepTime}
              onChangeText={setPrepTime}
            />
          </View>
        </View>

        <Text style={styles.label}>Składniki</Text>
        {ingredients.map((ing, idx) => (
          <View key={`${ing.product.id}-${idx}`} style={styles.ingredientCard}>
            <View style={{ flex: 1 }}>
              <Text style={styles.ingredientName} numberOfLines={1}>
                {ing.product.name}
              </Text>
              <View style={styles.ingredientControls}>
                <TextInput
                  testID={`ingredient-qty-${idx}`}
                  style={styles.qtyInput}
                  keyboardType="decimal-pad"
                  value={ing.quantityText}
                  onChangeText={(text) =>
                    setIngredients((prev) =>
                      prev.map((p, i) => (i === idx ? { ...p, quantityText: text } : p)),
                    )
                  }
                />
                <View style={styles.unitRow}>
                  {unitOptions(ing.product).map((u) => (
                    <Pressable
                      key={u}
                      testID={`ingredient-unit-${idx}-${u}`}
                      style={[styles.unitChip, ing.unit === u && styles.unitChipActive]}
                      onPress={() =>
                        setIngredients((prev) =>
                          prev.map((p, i) => (i === idx ? { ...p, unit: u } : p)),
                        )
                      }
                    >
                      <Text
                        style={[styles.unitText, ing.unit === u && styles.unitTextActive]}
                      >
                        {u}
                      </Text>
                    </Pressable>
                  ))}
                </View>
              </View>
            </View>
            <Pressable
              testID={`ingredient-remove-${idx}`}
              style={styles.removeBtn}
              onPress={() =>
                setIngredients((prev) => prev.filter((_, i) => i !== idx))
              }
            >
              <Ionicons name="trash-outline" size={18} color={colors.error} />
            </Pressable>
          </View>
        ))}

        <Pressable
          testID="add-ingredient-button"
          style={styles.addIngredientBtn}
          onPress={() => setPickerVisible(true)}
        >
          <Ionicons name="add-circle-outline" size={20} color={colors.brand} />
          <Text style={styles.addIngredientText}>Dodaj składnik</Text>
        </Pressable>

        {error && (
          <Text testID="add-recipe-error" style={styles.error}>
            {error}
          </Text>
        )}
      </KeyboardAwareScrollView>

      <KeyboardStickyView offset={{ closed: 0, opened: insets.bottom }}>
        <View style={[styles.stickyBar, { paddingBottom: insets.bottom + spacing.md }]}>
          <Pressable
            testID="save-recipe-button"
            style={({ pressed }) => [styles.saveBtn, pressed && { opacity: 0.85 }]}
            onPress={save}
            disabled={saving}
          >
            {saving ? (
              <ActivityIndicator color={colors.onBrand} />
            ) : (
              <Text style={styles.saveText}>Zapisz przepis</Text>
            )}
          </Pressable>
        </View>
      </KeyboardStickyView>

      <Modal
        visible={pickerVisible}
        animationType="slide"
        transparent
        onRequestClose={() => setPickerVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={[styles.modalSheet, { paddingBottom: insets.bottom + spacing.md }]}>
            <View style={styles.modalHandle} />
            <Text style={styles.modalTitle}>Wybierz produkt</Text>
            <TextInput
              testID="product-search-input"
              style={styles.input}
              placeholder="Szukaj produktu..."
              placeholderTextColor={colors.muted}
              value={search}
              onChangeText={setSearch}
            />
            <FlatList
              data={filteredProducts}
              keyExtractor={(item) => item.id}
              keyboardShouldPersistTaps="handled"
              style={{ maxHeight: 380 }}
              renderItem={({ item }) => (
                <Pressable
                  testID={`product-option-${item.id}`}
                  style={styles.productRow}
                  onPress={() => addIngredient(item)}
                >
                  <View style={{ flex: 1 }}>
                    <Text style={styles.productName}>{item.name}</Text>
                    <Text style={styles.productMeta}>
                      {item.nutrition_per_100.kcal} kcal / 100{" "}
                      {item.unit === "szt" ? "g" : item.unit === "kg" || item.unit === "l" ? (item.unit === "kg" ? "g" : "ml") : item.unit}
                    </Text>
                  </View>
                  <Ionicons name="add-circle" size={24} color={colors.brand} />
                </Pressable>
              )}
              ListEmptyComponent={
                <Text style={styles.emptyPicker}>Brak produktów</Text>
              }
            />
            <Pressable
              testID="product-picker-close"
              style={styles.modalClose}
              onPress={() => setPickerVisible(false)}
            >
              <Text style={styles.modalCloseText}>Zamknij</Text>
            </Pressable>
          </View>
        </View>
      </Modal>
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
    paddingBottom: spacing.md,
  },
  closeBtn: {
    width: 40,
    height: 40,
    borderRadius: radius.pill,
    backgroundColor: colors.surfaceTertiary,
    alignItems: "center",
    justifyContent: "center",
  },
  headerTitle: { fontFamily: font.regular, fontSize: 18, fontWeight: "600", color: colors.onSurface },
  liveMacroBar: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    backgroundColor: colors.brandTertiary,
    marginHorizontal: spacing.lg,
    marginBottom: spacing.md,
    borderRadius: radius.md,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
  },
  liveMacroTitle: { fontFamily: font.regular, fontSize: 13, fontWeight: "600", color: colors.onBrandTertiary },
  liveMacroText: { fontFamily: font.regular, fontSize: 13, color: colors.onBrandTertiary, flex: 1 },
  label: {
    fontFamily: font.regular,
    fontSize: 13,
    fontWeight: "600",
    color: colors.onSurfaceTertiary,
    paddingHorizontal: spacing.lg,
    marginTop: spacing.lg,
    marginBottom: spacing.sm,
  },
  input: {
    backgroundColor: colors.surfaceSecondary,
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: colors.border,
    paddingHorizontal: spacing.lg,
    paddingVertical: 12,
    fontSize: 15,
    fontFamily: font.regular,
    color: colors.onSurface,
    marginHorizontal: spacing.lg,
  },
  inputMultiline: { minHeight: 70, textAlignVertical: "top" },
  chipsWrapRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.sm,
    paddingHorizontal: spacing.lg,
  },
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
  rowSplit: { flexDirection: "row", gap: spacing.md, paddingRight: spacing.lg },
  stepper: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.md,
    marginLeft: spacing.lg,
    backgroundColor: colors.surfaceSecondary,
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: colors.border,
    paddingHorizontal: spacing.sm,
    height: 46,
    justifyContent: "space-between",
  },
  stepperBtn: {
    width: 34,
    height: 34,
    borderRadius: radius.sm,
    backgroundColor: colors.surfaceTertiary,
    alignItems: "center",
    justifyContent: "center",
  },
  stepperValue: { fontFamily: font.regular, fontSize: 16, fontWeight: "600", color: colors.onSurface },
  ingredientCard: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: colors.surfaceSecondary,
    borderRadius: radius.md,
    marginHorizontal: spacing.lg,
    marginBottom: spacing.sm,
    padding: spacing.md,
    gap: spacing.md,
    ...shadow.card,
  },
  ingredientName: { fontFamily: font.regular, fontSize: 15, fontWeight: "600", color: colors.onSurface },
  ingredientControls: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.md,
    marginTop: spacing.sm,
  },
  qtyInput: {
    backgroundColor: colors.surfaceTertiary,
    borderRadius: radius.sm,
    paddingHorizontal: spacing.md,
    paddingVertical: 8,
    fontSize: 14,
    fontFamily: font.regular,
    color: colors.onSurface,
    width: 80,
  },
  unitRow: { flexDirection: "row", gap: spacing.xs },
  unitChip: {
    paddingHorizontal: spacing.md,
    paddingVertical: 6,
    borderRadius: radius.pill,
    backgroundColor: colors.surfaceTertiary,
  },
  unitChipActive: { backgroundColor: colors.brand },
  unitText: { fontFamily: font.regular, fontSize: 12, color: colors.onSurfaceTertiary },
  unitTextActive: { color: colors.onBrand },
  removeBtn: {
    width: 38,
    height: 38,
    borderRadius: radius.sm,
    alignItems: "center",
    justifyContent: "center",
  },
  addIngredientBtn: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: spacing.sm,
    marginHorizontal: spacing.lg,
    marginTop: spacing.sm,
    paddingVertical: 14,
    borderRadius: radius.md,
    borderWidth: 1,
    borderStyle: "dashed",
    borderColor: colors.brandSecondary,
  },
  addIngredientText: { fontFamily: font.regular, fontSize: 14, fontWeight: "600", color: colors.brand },
  error: {
    color: colors.error,
    fontFamily: font.regular,
    fontSize: 13,
    paddingHorizontal: spacing.lg,
    marginTop: spacing.md,
  },
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
  saveBtn: {
    backgroundColor: colors.brand,
    borderRadius: radius.md,
    paddingVertical: 15,
    alignItems: "center",
    justifyContent: "center",
    minHeight: 52,
  },
  saveText: { color: colors.onBrand, fontSize: 16, fontFamily: font.regular, fontWeight: "600" },
  modalOverlay: { flex: 1, backgroundColor: "rgba(0,0,0,0.4)", justifyContent: "flex-end" },
  modalSheet: {
    backgroundColor: colors.surface,
    borderTopLeftRadius: radius.lg,
    borderTopRightRadius: radius.lg,
    paddingTop: spacing.sm,
  },
  modalHandle: {
    width: 40,
    height: 4,
    borderRadius: 2,
    backgroundColor: colors.border,
    alignSelf: "center",
    marginBottom: spacing.md,
  },
  modalTitle: {
    fontFamily: font.regular,
    fontSize: 17,
    fontWeight: "600",
    color: colors.onSurface,
    paddingHorizontal: spacing.lg,
    marginBottom: spacing.md,
  },
  productRow: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: spacing.lg,
    paddingVertical: 12,
    gap: spacing.md,
  },
  productName: { fontFamily: font.regular, fontSize: 15, color: colors.onSurface },
  productMeta: { fontFamily: font.regular, fontSize: 12, color: colors.muted, marginTop: 1 },
  emptyPicker: {
    fontFamily: font.regular,
    color: colors.muted,
    textAlign: "center",
    paddingVertical: spacing.xl,
  },
  modalClose: {
    marginHorizontal: spacing.lg,
    marginTop: spacing.sm,
    paddingVertical: 13,
    borderRadius: radius.md,
    backgroundColor: colors.surfaceTertiary,
    alignItems: "center",
  },
  modalCloseText: { fontFamily: font.regular, fontSize: 15, fontWeight: "600", color: colors.onSurface },
});
