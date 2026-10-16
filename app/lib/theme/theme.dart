import 'package:flutter/material.dart';

import 'tokens.dart';

ThemeData buildMarineSeeTheme(AppTokens tokens) {
  final scheme = ColorScheme(
    brightness: tokens.brightness,
    primary: SkyPalette.primary,
    onPrimary: SkyPalette.onPrimary,
    primaryContainer: SkyPalette.primaryContainer,
    onPrimaryContainer: SkyPalette.onSky,
    secondary: SkyPalette.headerBottom,
    onSecondary: SkyPalette.onHeader,
    secondaryContainer: SkyPalette.mistDeep,
    onSecondaryContainer: SkyPalette.ink,
    tertiary: SkyPalette.seagrass,
    onTertiary: SkyPalette.onSeagrass,
    tertiaryContainer: SkyPalette.mistDeep,
    onTertiaryContainer: SkyPalette.ink,
    error: SkyPalette.danger,
    onError: SkyPalette.onPrimary,
    errorContainer: SkyPalette.dangerFill,
    onErrorContainer: SkyPalette.danger,
    surface: SkyPalette.foam,
    onSurface: SkyPalette.ink,
    onSurfaceVariant: SkyPalette.inkMuted,
    outline: SkyPalette.lineOnSand,
    outlineVariant: SkyPalette.lineOnSky,
    shadow: SkyPalette.shadow,
    inverseSurface: SkyPalette.inverse,
    onInverseSurface: SkyPalette.onInverse,
    inversePrimary: SkyPalette.water,
    surfaceTint: SkyPalette.primary,
    surfaceContainerHighest: SkyPalette.foam,
    surfaceContainerLow: SkyPalette.mist,
  );

  final textTheme = _textTheme(tokens);
  final radius = AppRadius.button;

  return ThemeData(
    useMaterial3: true,
    brightness: tokens.brightness,
    colorScheme: scheme,
    scaffoldBackgroundColor: tokens.abyss,
    canvasColor: tokens.ocean,
    textTheme: textTheme,
    iconTheme: IconThemeData(color: tokens.inkMuted),
    splashColor: tokens.cyan.withValues(alpha: 0.12),
    highlightColor: tokens.cyan.withValues(alpha: 0.06),
    materialTapTargetSize: MaterialTapTargetSize.padded,
    extensions: [tokens],
    appBarTheme: AppBarTheme(
      backgroundColor: Colors.transparent,
      foregroundColor: tokens.ink,
      elevation: 0,
      scrolledUnderElevation: 0,
      centerTitle: false,
      titleTextStyle: textTheme.titleLarge,
      iconTheme: IconThemeData(color: tokens.ink),
    ),
    navigationBarTheme: NavigationBarThemeData(
      backgroundColor: tokens.surfaceHigh,
      elevation: 0,
      height: 64,
      indicatorColor: tokens.brand.withValues(alpha: 0.16),
      overlayColor: WidgetStatePropertyAll(
        tokens.cyan.withValues(alpha: 0.08),
      ),
      iconTheme: WidgetStateProperty.resolveWith((states) {
        final selected = states.contains(WidgetState.selected);
        return IconThemeData(
          color: selected ? SkyPalette.primaryDark : tokens.inkMuted,
          size: 24,
        );
      }),
      labelTextStyle: WidgetStateProperty.resolveWith((states) {
        final selected = states.contains(WidgetState.selected);
        return TextStyle(
          fontSize: 12,
          fontWeight: selected ? FontWeight.w600 : FontWeight.w500,
          letterSpacing: 0.2,
          color: selected ? SkyPalette.primaryDark : tokens.inkMuted,
        );
      }),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: ButtonStyle(
        minimumSize: const WidgetStatePropertyAll(AppTokens.tapSize),
        backgroundColor: WidgetStateProperty.resolveWith((states) {
          if (states.contains(WidgetState.disabled)) {
            return tokens.brand.withValues(alpha: 0.28);
          }
          if (states.contains(WidgetState.pressed)) {
            return SkyPalette.primaryDark;
          }
          return tokens.brand;
        }),
        foregroundColor: WidgetStateProperty.resolveWith((states) {
          if (states.contains(WidgetState.disabled)) {
            return tokens.onBrand.withValues(alpha: 0.55);
          }
          return tokens.onBrand;
        }),
        shape: WidgetStatePropertyAll(
          RoundedRectangleBorder(borderRadius: radius),
        ),
        textStyle: WidgetStatePropertyAll(textTheme.labelLarge),
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        minimumSize: AppTokens.tapSize,
        foregroundColor: tokens.isLight ? tokens.brandDeep : tokens.ink,
        backgroundColor: tokens.isLight
            ? tokens.surface
            : tokens.surface.withValues(alpha: 0.55),
        disabledForegroundColor: tokens.inkMuted,
        side: BorderSide(
          color: tokens.isLight
              ? tokens.brandDeep.withValues(alpha: 0.55)
              : tokens.borderStrong,
        ),
        shape: RoundedRectangleBorder(borderRadius: radius),
        textStyle: textTheme.labelLarge,
      ),
    ),
    textButtonTheme: TextButtonThemeData(
      style: TextButton.styleFrom(
        minimumSize: const Size(AppTokens.tapMin, 44),
        foregroundColor: SkyPalette.primary,
        textStyle: textTheme.labelLarge,
      ),
    ),
    cardTheme: CardThemeData(
      color: tokens.isLight ? tokens.surfaceHigh : tokens.surface.withValues(alpha: 0.92),
      elevation: 0,
      margin: EdgeInsets.zero,
      shape: RoundedRectangleBorder(
        borderRadius: AppRadius.card,
        side: BorderSide(color: tokens.border),
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: tokens.surfaceHigh,
      hintStyle: textTheme.bodyMedium?.copyWith(color: tokens.inkMuted),
      labelStyle: textTheme.labelLarge?.copyWith(color: tokens.inkMuted),
      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
      border: OutlineInputBorder(
        borderRadius: AppRadius.button,
        borderSide: BorderSide(color: tokens.border),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: AppRadius.button,
        borderSide: BorderSide(color: tokens.border),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: AppRadius.button,
        borderSide: BorderSide(color: tokens.cyan, width: 1.4),
      ),
      errorBorder: OutlineInputBorder(
        borderRadius: AppRadius.button,
        borderSide: BorderSide(color: tokens.danger),
      ),
      focusedErrorBorder: OutlineInputBorder(
        borderRadius: AppRadius.button,
        borderSide: BorderSide(color: tokens.danger, width: 1.4),
      ),
    ),
    snackBarTheme: SnackBarThemeData(
      backgroundColor: tokens.surfaceHigh,
      contentTextStyle: textTheme.bodyMedium,
      behavior: SnackBarBehavior.floating,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppRadius.md),
        side: BorderSide(color: tokens.border),
      ),
    ),
    dialogTheme: DialogThemeData(
      backgroundColor: tokens.surface,
      titleTextStyle: textTheme.titleLarge,
      contentTextStyle: textTheme.bodyLarge,
      shape: RoundedRectangleBorder(borderRadius: AppRadius.sheet),
    ),
    progressIndicatorTheme: ProgressIndicatorThemeData(
      color: tokens.cyan,
      circularTrackColor: tokens.navy,
    ),
    dividerTheme: DividerThemeData(
      color: tokens.border,
      space: 24,
      thickness: 1,
    ),
  );
}

TextTheme _textTheme(AppTokens tokens) {
  final icy = tokens.ink;
  return TextTheme(
    displaySmall: TextStyle(
      fontSize: 34,
      height: 1.12,
      fontWeight: FontWeight.w800,
      letterSpacing: -1.1,
      color: icy,
    ),
    headlineMedium: TextStyle(
      fontSize: 30,
      height: 1.2,
      fontWeight: FontWeight.w700,
      letterSpacing: -0.4,
      color: icy,
    ),
    headlineSmall: TextStyle(
      fontSize: 24,
      height: 1.25,
      fontWeight: FontWeight.w700,
      letterSpacing: -0.3,
      color: icy,
    ),
    titleLarge: TextStyle(
      fontSize: 20,
      height: 1.3,
      fontWeight: FontWeight.w600,
      letterSpacing: -0.2,
      color: icy,
    ),
    titleMedium: TextStyle(
      fontSize: 17,
      height: 1.35,
      fontWeight: FontWeight.w600,
      color: icy,
    ),
    titleSmall: TextStyle(
      fontSize: 14,
      height: 1.35,
      fontWeight: FontWeight.w600,
      letterSpacing: 0.15,
      color: tokens.inkMuted,
    ),
    bodyLarge: TextStyle(
      fontSize: 16,
      height: 1.5,
      fontWeight: FontWeight.w400,
      color: icy,
    ),
    bodyMedium: TextStyle(
      fontSize: 15,
      height: 1.45,
      fontWeight: FontWeight.w400,
      color: tokens.inkMuted,
    ),
    bodySmall: TextStyle(
      fontSize: 13,
      height: 1.4,
      fontWeight: FontWeight.w400,
      color: tokens.inkMuted,
    ),
    labelLarge: TextStyle(
      fontSize: 15,
      height: 1.25,
      fontWeight: FontWeight.w600,
      letterSpacing: 0.15,
      color: icy,
    ),
    labelMedium: TextStyle(
      fontSize: 12,
      height: 1.3,
      fontWeight: FontWeight.w600,
      letterSpacing: 0.3,
      color: tokens.inkMuted,
    ),
    labelSmall: TextStyle(
      fontSize: 11,
      height: 1.3,
      fontWeight: FontWeight.w600,
      letterSpacing: 0.4,
      color: tokens.inkMuted,
    ),
  );
}
