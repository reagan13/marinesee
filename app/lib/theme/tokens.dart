import 'package:flutter/material.dart';

/// Coastal / educational tokens. Screens must use these, never raw hex.
abstract final class AppTokens {
  static const Color background = Color(0xFFEEF3F0);
  static const Color surface = Color(0xFFF7FBFA);
  static const Color ink = Color(0xFF14323A);
  static const Color brand = Color(0xFF0F6B66);
  static const Color danger = Color(0xFFB5473A);
  static const double radius = 16;

  static const Color inkMuted = Color(0xFF3D565C);
  static const Color onBrand = Color(0xFFF7FBFA);
  static const Color notice = Color(0xFF6B5420);
  static const Color noticeFill = Color(0xFFF3E6C0);

  static const double tapMin = 48;
  static const Size tapSize = Size(tapMin, 52);
}

ThemeData buildMarineSeeTheme() {
  const scheme = ColorScheme(
    brightness: Brightness.light,
    primary: AppTokens.brand,
    onPrimary: AppTokens.onBrand,
    secondary: AppTokens.brand,
    onSecondary: AppTokens.onBrand,
    error: AppTokens.danger,
    onError: AppTokens.onBrand,
    surface: AppTokens.surface,
    onSurface: AppTokens.ink,
  );

  final radius = BorderRadius.circular(AppTokens.radius);

  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    scaffoldBackgroundColor: AppTokens.background,
    appBarTheme: const AppBarTheme(
      backgroundColor: AppTokens.background,
      foregroundColor: AppTokens.ink,
      elevation: 0,
      centerTitle: false,
    ),
    navigationBarTheme: NavigationBarThemeData(
      backgroundColor: AppTokens.surface,
      indicatorColor: AppTokens.brand.withValues(alpha: 0.16),
      height: 72,
      labelTextStyle: WidgetStatePropertyAll(
        const TextStyle(fontWeight: FontWeight.w600, fontSize: 12),
      ),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        minimumSize: AppTokens.tapSize,
        backgroundColor: AppTokens.brand,
        foregroundColor: AppTokens.onBrand,
        shape: RoundedRectangleBorder(borderRadius: radius),
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        minimumSize: AppTokens.tapSize,
        foregroundColor: AppTokens.ink,
        side: const BorderSide(color: AppTokens.brand),
        shape: RoundedRectangleBorder(borderRadius: radius),
      ),
    ),
    cardTheme: CardThemeData(
      color: AppTokens.surface,
      elevation: 0,
      shape: RoundedRectangleBorder(borderRadius: radius),
    ),
  );
}
