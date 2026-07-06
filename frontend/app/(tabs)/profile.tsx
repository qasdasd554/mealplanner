import { Ionicons } from "@expo/vector-icons";
import { router } from "expo-router";
import { StyleSheet, Pressable, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { useAuth } from "@/src/context/AuthContext";
import { colors, font, radius, shadow, spacing } from "@/src/lib/theme";

export default function ProfileScreen() {
  const insets = useSafeAreaInsets();
  const { user, logout } = useAuth();

  return (
    <View style={styles.container} testID="profile-screen">
      <View style={[styles.header, { paddingTop: insets.top + spacing.md }]}>
        <Text style={styles.headerTitle}>Profil</Text>
      </View>

      <View style={styles.card}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>
            {(user?.display_name || "?").charAt(0).toUpperCase()}
          </Text>
        </View>
        <View style={{ flex: 1 }}>
          <Text style={styles.name} testID="profile-display-name">
            {user?.display_name}
          </Text>
          <Text style={styles.email} testID="profile-email">
            {user?.email}
          </Text>
        </View>
      </View>

      <View style={styles.menu}>
        <Pressable
          testID="profile-my-recipes-button"
          style={styles.menuRow}
          onPress={() => router.push("/(tabs)/recipes")}
        >
          <Ionicons name="book-outline" size={20} color={colors.onSurfaceTertiary} />
          <Text style={styles.menuText}>Moje przepisy</Text>
          <Ionicons name="chevron-forward" size={18} color={colors.muted} />
        </Pressable>
        <View style={styles.menuDivider} />
        <Pressable
          testID="profile-new-plan-button"
          style={styles.menuRow}
          onPress={() => router.push("/plan-config")}
        >
          <Ionicons name="calendar-outline" size={20} color={colors.onSurfaceTertiary} />
          <Text style={styles.menuText}>Nowy plan posiłków</Text>
          <Ionicons name="chevron-forward" size={18} color={colors.muted} />
        </Pressable>
      </View>

      <Pressable
        testID="logout-button"
        style={styles.logout}
        onPress={async () => {
          await logout();
          router.replace("/auth");
        }}
      >
        <Ionicons name="log-out-outline" size={20} color={colors.error} />
        <Text style={styles.logoutText}>Wyloguj się</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.surface },
  header: { paddingHorizontal: spacing.lg, paddingBottom: spacing.lg },
  headerTitle: {
    fontFamily: font.regular,
    fontSize: 24,
    fontWeight: "600",
    color: colors.onSurface,
  },
  card: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.lg,
    backgroundColor: colors.surfaceSecondary,
    borderRadius: radius.lg,
    marginHorizontal: spacing.lg,
    padding: spacing.lg,
    ...shadow.card,
  },
  avatar: {
    width: 56,
    height: 56,
    borderRadius: radius.pill,
    backgroundColor: colors.brand,
    alignItems: "center",
    justifyContent: "center",
  },
  avatarText: { color: colors.onBrand, fontSize: 24, fontFamily: font.regular, fontWeight: "600" },
  name: { fontFamily: font.regular, fontSize: 18, fontWeight: "600", color: colors.onSurface },
  email: { fontFamily: font.regular, fontSize: 13, color: colors.muted, marginTop: 2 },
  menu: {
    backgroundColor: colors.surfaceSecondary,
    borderRadius: radius.lg,
    marginHorizontal: spacing.lg,
    marginTop: spacing.lg,
    ...shadow.card,
  },
  menuRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.md,
    padding: spacing.lg,
    minHeight: 52,
  },
  menuDivider: { height: 1, backgroundColor: colors.divider, marginLeft: 52 },
  menuText: { flex: 1, fontFamily: font.regular, fontSize: 15, color: colors.onSurface },
  logout: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: spacing.sm,
    marginHorizontal: spacing.lg,
    marginTop: spacing.xl,
    paddingVertical: 14,
    borderRadius: radius.md,
    backgroundColor: colors.surfaceSecondary,
    borderWidth: 1,
    borderColor: colors.border,
  },
  logoutText: { fontFamily: font.regular, fontSize: 15, fontWeight: "600", color: colors.error },
});
