import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import { router } from "expo-router";
import { useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { KeyboardAwareScrollView } from "react-native-keyboard-controller";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { useAuth } from "@/src/context/AuthContext";
import { colors, font, radius, spacing } from "@/src/lib/theme";

export default function AuthScreen() {
  const insets = useSafeAreaInsets();
  const { login, register } = useAuth();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    setError(null);
    if (!email.trim() || !password) {
      setError("Podaj e-mail i hasło");
      return;
    }
    if (mode === "register" && !name.trim()) {
      setError("Podaj swoje imię");
      return;
    }
    if (mode === "register" && password.length < 6) {
      setError("Hasło musi mieć min. 6 znaków");
      return;
    }
    setLoading(true);
    try {
      if (mode === "login") await login(email.trim(), password);
      else await register(email.trim(), password, name.trim());
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      router.replace("/(tabs)");
    } catch (e: any) {
      setError(e.message || "Wystąpił błąd");
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <KeyboardAwareScrollView
        contentContainerStyle={[
          styles.scroll,
          { paddingTop: insets.top + spacing.xxxl, paddingBottom: insets.bottom + spacing.xl },
        ]}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.logoBadge}>
          <Ionicons name="nutrition-outline" size={36} color={colors.brand} />
        </View>
        <Text style={styles.title}>Smart Meal Planner</Text>
        <Text style={styles.subtitle}>
          Planuj posiłki, licz makro i twórz listy zakupów
        </Text>

        <View style={styles.switchRow}>
          <Pressable
            testID="auth-mode-login"
            style={[styles.switchBtn, mode === "login" && styles.switchBtnActive]}
            onPress={() => setMode("login")}
          >
            <Text style={[styles.switchText, mode === "login" && styles.switchTextActive]}>
              Logowanie
            </Text>
          </Pressable>
          <Pressable
            testID="auth-mode-register"
            style={[styles.switchBtn, mode === "register" && styles.switchBtnActive]}
            onPress={() => setMode("register")}
          >
            <Text style={[styles.switchText, mode === "register" && styles.switchTextActive]}>
              Rejestracja
            </Text>
          </Pressable>
        </View>

        {mode === "register" && (
          <TextInput
            testID="auth-name-input"
            style={styles.input}
            placeholder="Imię"
            placeholderTextColor={colors.muted}
            value={name}
            onChangeText={setName}
          />
        )}
        <TextInput
          testID="auth-email-input"
          style={styles.input}
          placeholder="E-mail"
          placeholderTextColor={colors.muted}
          autoCapitalize="none"
          keyboardType="email-address"
          value={email}
          onChangeText={setEmail}
        />
        <TextInput
          testID="auth-password-input"
          style={styles.input}
          placeholder="Hasło"
          placeholderTextColor={colors.muted}
          secureTextEntry
          value={password}
          onChangeText={setPassword}
        />

        {error && (
          <Text testID="auth-error-text" style={styles.error}>
            {error}
          </Text>
        )}

        <Pressable
          testID="auth-submit-button"
          style={({ pressed }) => [styles.submit, pressed && { opacity: 0.85 }]}
          onPress={submit}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color={colors.onBrand} />
          ) : (
            <Text style={styles.submitText}>
              {mode === "login" ? "Zaloguj się" : "Załóż konto"}
            </Text>
          )}
        </Pressable>
      </KeyboardAwareScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.surface },
  scroll: { paddingHorizontal: spacing.xl },
  logoBadge: {
    width: 72,
    height: 72,
    borderRadius: radius.lg,
    backgroundColor: colors.brandTertiary,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: spacing.lg,
  },
  title: {
    fontFamily: font.regular,
    fontSize: 28,
    color: colors.onSurface,
    fontWeight: "600",
  },
  subtitle: {
    fontFamily: font.regular,
    fontSize: 15,
    color: colors.muted,
    marginTop: spacing.sm,
    marginBottom: spacing.xl,
  },
  switchRow: {
    flexDirection: "row",
    backgroundColor: colors.surfaceTertiary,
    borderRadius: radius.pill,
    padding: 4,
    marginBottom: spacing.xl,
  },
  switchBtn: {
    flex: 1,
    paddingVertical: spacing.md,
    borderRadius: radius.pill,
    alignItems: "center",
  },
  switchBtnActive: { backgroundColor: colors.surfaceSecondary },
  switchText: { fontFamily: font.regular, fontSize: 14, color: colors.muted },
  switchTextActive: { color: colors.onSurface, fontWeight: "600" },
  input: {
    backgroundColor: colors.surfaceSecondary,
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: colors.border,
    paddingHorizontal: spacing.lg,
    paddingVertical: 14,
    fontSize: 16,
    fontFamily: font.regular,
    color: colors.onSurface,
    marginBottom: spacing.md,
  },
  error: {
    color: colors.error,
    fontFamily: font.regular,
    fontSize: 13,
    marginBottom: spacing.sm,
  },
  submit: {
    backgroundColor: colors.brand,
    borderRadius: radius.md,
    paddingVertical: 16,
    alignItems: "center",
    marginTop: spacing.md,
    minHeight: 52,
    justifyContent: "center",
  },
  submitText: {
    color: colors.onBrand,
    fontSize: 16,
    fontFamily: font.regular,
    fontWeight: "600",
  },
});
