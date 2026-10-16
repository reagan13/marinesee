import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

enum AppStyle { night, frost }

/// Bright shoreline. Widgets read [AppTokens]; these swatches are the roles.
abstract final class SkyPalette {
  static const primary = Color(0xFF1496C4);
  static const onPrimary = Color(0xFFFFFFFF);
  static const primaryDark = Color(0xFF0E7EAB);
  static const water = Color(0xFF3EC8EA);
  static const waterDeep = Color(0xFF2EAADE);
  static const primaryContainer = Color(0xFFC9F1F8);

  static const sky = Color(0xFF6EC6F5);
  static const skyDeep = Color(0xFF4FB4F0);
  static const onSky = Color(0xFF143A4A);
  static const onHeader = Color(0xFFFFFFFF);
  static const headerTop = Color(0xFF2EC8E6);
  static const headerMid = Color(0xFF14A8C8);
  static const headerBottom = Color(0xFF0E9488);

  static const sand = Color(0xFFEBD3A4);
  static const sandDeep = Color(0xFFC49B62);
  static const sandLight = Color(0xFFF7E8C8);
  static const onSand = Color(0xFF3A2A10);
  static const sandContainer = Color(0xFFF8EFDC);

  static const mist = Color(0xFFF3FBFC);
  static const mistDeep = Color(0xFFE6F5F7);
  static const foam = Color(0xFFFFFFFF);
  static const seagrass = Color(0xFF3AAA40);
  static const onSeagrass = Color(0xFFFFFFFF);

  static const ink = onSky;
  static const inkMuted = Color(0xFF3E5A62);
  static const inkSubtle = Color(0xFF6D7D78);
  static const lineOnSand = Color(0xFFD7E7EA);
  static const lineOnSky = Color(0x66FFFFFF);
  static const shadow = Color(0x1A143A4A);

  static const inverse = Color(0xFF0C6E90);
  static const inverseContainer = Color(0xFF1490B4);
  static const onInverse = Color(0xFFFFFFFF);

  static const danger = Color(0xFFB3261E);
  static const dangerFill = Color(0xFFFDECEA);
  static const notice = Color(0xFF8A4B12);
  static const noticeFill = Color(0xFFFFF6E8);
  static const noticeBorder = Color(0xFFE4C48A);

  static const page = mist;
  static const pageDeep = mistDeep;
  static const ocean = primary;
  static const oceanDeep = primaryDark;
  static const card = foam;
  static const line = lineOnSand;
  static const lineStrong = Color(0xFFC5DCE1);
  static const tileBlue = primary;
  static const tileGreen = seagrass;
  static const scanner = Color(0xFF125E68);
  static const scannerDeep = Color(0xFF0A3E48);

  static const darkStatusBar = SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.dark,
    statusBarBrightness: Brightness.light,
    systemNavigationBarColor: foam,
    systemNavigationBarIconBrightness: Brightness.dark,
  );

  static const lightStatusBar = SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.light,
    statusBarBrightness: Brightness.dark,
    systemNavigationBarColor: scannerDeep,
    systemNavigationBarIconBrightness: Brightness.light,
  );

  static const headerStatusBar = SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.light,
    statusBarBrightness: Brightness.dark,
    systemNavigationBarColor: foam,
    systemNavigationBarIconBrightness: Brightness.dark,
  );
}

/// Color tokens for the teal header and light page.
///
/// [night] and [frost] are the same palette. Primary buttons use [brand].
/// The page below a header is [abyss].
@immutable
class AppTokens extends ThemeExtension<AppTokens> {
  const AppTokens({
    required this.style,
    required this.brightness,
    required this.abyss,
    required this.ocean,
    required this.navy,
    required this.surface,
    required this.surfaceHigh,
    required this.ink,
    required this.inkMuted,
    required this.inkSubtle,
    required this.cyan,
    required this.teal,
    required this.brand,
    required this.brandDeep,
    required this.violet,
    required this.onBrand,
    required this.danger,
    required this.notice,
    required this.noticeFill,
    required this.noticeBorder,
    required this.border,
    required this.borderStrong,
    required this.glowCyan,
    required this.glowTeal,
    required this.shadow,
    required this.depthGradient,
    required this.primaryGradient,
    required this.headerGradient,
    required this.surfaceSheen,
    required this.systemUi,
    required this.auraCyan,
    required this.auraTeal,
    required this.auraViolet,
  });

  final AppStyle style;
  final Brightness brightness;
  final Color abyss;
  final Color ocean;
  final Color navy;
  final Color surface;
  final Color surfaceHigh;
  final Color ink;
  final Color inkMuted;
  final Color inkSubtle;
  final Color cyan;
  final Color teal;
  final Color brand;
  final Color brandDeep;
  final Color violet;
  final Color onBrand;
  final Color danger;
  final Color notice;
  final Color noticeFill;
  final Color noticeBorder;
  final Color border;
  final Color borderStrong;
  final Color glowCyan;
  final Color glowTeal;
  final Color shadow;
  final LinearGradient depthGradient;
  final LinearGradient primaryGradient;
  final LinearGradient headerGradient;
  final LinearGradient surfaceSheen;
  final SystemUiOverlayStyle systemUi;
  final double auraCyan;
  final double auraTeal;
  final double auraViolet;

  static const double tapMin = 48;
  static const Size tapSize = Size(double.infinity, 52);
  static const double radius = 20;

  static const sky = AppTokens(
    style: AppStyle.frost,
    brightness: Brightness.light,
    abyss: SkyPalette.mist,
    ocean: SkyPalette.mistDeep,
    navy: SkyPalette.primaryContainer,
    surface: SkyPalette.foam,
    surfaceHigh: SkyPalette.foam,
    ink: SkyPalette.ink,
    inkMuted: SkyPalette.inkMuted,
    inkSubtle: SkyPalette.inkSubtle,
    cyan: SkyPalette.primary,
    teal: SkyPalette.water,
    brand: SkyPalette.primary,
    brandDeep: SkyPalette.primaryDark,
    violet: SkyPalette.sky,
    onBrand: SkyPalette.onPrimary,
    danger: SkyPalette.danger,
    notice: SkyPalette.notice,
    noticeFill: SkyPalette.noticeFill,
    noticeBorder: SkyPalette.noticeBorder,
    border: SkyPalette.lineOnSand,
    borderStrong: SkyPalette.lineOnSand,
    glowCyan: Color(0x331496C4),
    glowTeal: Color(0x291496C4),
    shadow: SkyPalette.shadow,
    depthGradient: LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      colors: [SkyPalette.mist, SkyPalette.mist, SkyPalette.mistDeep],
      stops: [0.0, 0.22, 1.0],
    ),
    primaryGradient: LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      colors: [SkyPalette.primary, SkyPalette.primaryDark],
    ),
    headerGradient: LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      colors: [
        SkyPalette.headerTop,
        SkyPalette.headerMid,
        SkyPalette.headerBottom,
      ],
      stops: [0.0, 0.48, 1.0],
    ),
    surfaceSheen: LinearGradient(
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
      colors: [SkyPalette.foam, SkyPalette.foam, SkyPalette.primaryContainer],
    ),
    systemUi: SkyPalette.darkStatusBar,
    auraCyan: 0.08,
    auraTeal: 0.05,
    auraViolet: 0.04,
  );

  static const night = sky;
  static const frost = sky;

  static AppTokens forStyle(AppStyle style) => sky;

  bool get isLight => brightness == Brightness.light;

  List<BoxShadow> get cardShadows => [
    BoxShadow(color: shadow, blurRadius: 18, offset: const Offset(0, 8)),
  ];

  List<BoxShadow> get cardGlowShadows => [
    BoxShadow(color: glowCyan, blurRadius: 22, offset: const Offset(0, 8)),
    BoxShadow(color: shadow, blurRadius: 12, offset: const Offset(0, 6)),
  ];

  List<BoxShadow> get glowShadows => [
    BoxShadow(color: glowTeal, blurRadius: 16, offset: const Offset(0, 6)),
  ];

  @override
  AppTokens copyWith({AppStyle? style}) => forStyle(style ?? this.style);

  @override
  AppTokens lerp(ThemeExtension<AppTokens>? other, double t) {
    if (other is! AppTokens) {
      return this;
    }
    return t < 0.5 ? this : other;
  }
}

extension MarineSeeThemeX on BuildContext {
  AppTokens get tokens => Theme.of(this).extension<AppTokens>() ?? AppTokens.sky;
}

abstract final class AppSpace {
  static const double xs = 8;
  static const double sm = 12;
  static const double md = 16;
  static const double lg = 24;
  static const double xl = 32;
  static const double maxContent = 720;
  static const double stackActionsBelow = 300;

  static const double navClearance = 24;

  static EdgeInsets pageInsets(
    BuildContext context, {
    double extraBottom = 0,
  }) {
    final width = MediaQuery.sizeOf(context).width;
    final horizontal = width >= 768 ? 32.0 : 20.0;
    return EdgeInsets.fromLTRB(horizontal, 16, horizontal, 28 + extraBottom);
  }

  static EdgeInsets headerInsets(BuildContext context) {
    final width = MediaQuery.sizeOf(context).width;
    final horizontal = width >= 768 ? 32.0 : 20.0;
    return EdgeInsets.fromLTRB(horizontal, 12, horizontal, 20);
  }
}

abstract final class AppRadius {
  static const double sm = 12;
  static const double md = 16;
  static const double lg = 24;
  static const double xl = 28;
  static const double pill = 999;

  static BorderRadius get button => BorderRadius.circular(xl);
  static BorderRadius get card => BorderRadius.circular(lg);
  static BorderRadius get sheet => BorderRadius.circular(xl);
}

abstract final class AppMotion {
  static const Duration fast = Duration(milliseconds: 180);
  static const Duration medium = Duration(milliseconds: 280);
  static const Duration aurora = Duration(seconds: 14);
  static const Curve ease = Curves.easeInOutCubic;
}
