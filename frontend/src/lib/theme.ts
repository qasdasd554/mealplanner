export const colors = {
  surface: "#F9F9F8",
  onSurface: "#1C1C1E",
  surfaceSecondary: "#FFFFFF",
  surfaceTertiary: "#F0F0EE",
  onSurfaceTertiary: "#3C3C3E",
  surfaceInverse: "#1C1C1E",
  onSurfaceInverse: "#FFFFFF",
  brand: "#E05D3D",
  onBrand: "#FFFFFF",
  brandSecondary: "#EBA896",
  brandTertiary: "#FCEEEA",
  onBrandTertiary: "#993B22",
  success: "#648261",
  warning: "#E8A341",
  error: "#D94A4A",
  border: "#E5E5E3",
  borderStrong: "#CFCFD0",
  divider: "#EFEFF0",
  muted: "#8E8E93",
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  xxl: 32,
  xxxl: 48,
};

export const radius = {
  sm: 6,
  md: 12,
  lg: 20,
  pill: 999,
};

export const font = {
  regular: "Jakarta",
  medium: "Jakarta",
};

export const shadow = {
  card: {
    shadowColor: "#000",
    shadowOpacity: 0.06,
    shadowRadius: 8,
    shadowOffset: { width: 0, height: 2 },
    elevation: 2,
  },
};

export const MEAL_TYPES = ["śniadanie", "obiad", "kolacja", "przekąska"] as const;

export const MEAL_TYPE_ICONS: Record<string, string> = {
  "śniadanie": "sunny-outline",
  "II śniadanie": "cafe-outline",
  "obiad": "restaurant-outline",
  "kolacja": "moon-outline",
  "przekąska": "cafe-outline",
  "podwieczorek": "ice-cream-outline",
};

export const MEAL_HERO_IMAGES: Record<string, string> = {
  "śniadanie":
    "https://images.unsplash.com/photo-1493770348161-369560ae357d?crop=entropy&cs=srgb&fm=jpg&q=85&w=1200",
  "obiad":
    "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?crop=entropy&cs=srgb&fm=jpg&q=85&w=1200",
  "kolacja":
    "https://images.unsplash.com/photo-1547592180-85f173990554?crop=entropy&cs=srgb&fm=jpg&q=85&w=1200",
  "przekąska":
    "https://images.unsplash.com/photo-1493770348161-369560ae357d?crop=entropy&cs=srgb&fm=jpg&q=85&w=1200",
};
