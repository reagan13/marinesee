import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

enum AppStyle { night, frost }

/// Mati Lagoon swatches. Widgets read [AppTokens], not these directly.
abstract final class LagoonPalette {
  static const foam = Color(0xFFF5FBFC);
  static const mist = Color(0xFFDCEEF2);
  static const shallows = Color(0xFFB4DDE4);
  static const lagoon = Color(0xFF0E6E6A);
  static const lagoonDeep = Color(0xFF0A524F);
  static const ink = Color(0xFF12343C);
  static const sand = Color(0xFFF0C56A);
  static const sandDeep = Color(0xFF8A6A22);
  static const sun = Color(0xFFFFE6A8);

  static const abyss = Color(0xFF051418);
  static const ocean = Color(0xFF0A232B);
  static const navy = Color(0xFF11343E);
  static const surface = Color(0xFF16424D);
  static const surfaceHigh = Color(0xFF1C5360);
  static const aqua = Color(0xFF5EE0D2);
}

/// Color + lighting tokens. Layout sizes stay static; colors come from
/// [AppTokens.night] / [AppTokens.frost] via [MarineSeeThemeX.tokens].
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
  final LinearGradient surfaceSheen;
  final SystemUiOverlayStyle systemUi;
  final double auraCyan;
  final double auraTeal;
  final double auraViolet;

  static const double tapMin = 48;
  static const Size tapSize = Size(double.infinity, 52);
  static const double radius = 20;

  /// Dark mode: night reef. Foam text, sand-gold actions, aqua glow, teal dock.
  static const night = AppTokens(
    style: AppStyle.night,
    brightness: Brightness.dark,
    abyss: LagoonPalette.abyss,
    ocean: LagoonPalette.ocean,
    navy: LagoonPalette.navy,
    surface: LagoonPalette.surface,
    surfaceHigh: LagoonPalette.surfaceHigh,
    ink: LagoonPalette.foam,
    inkMuted: Color(0xFFA5D4CE),
    inkSubtle: Color(0xFF6FA8A2),
    cyan: LagoonPalette.aqua,
    teal: Color(0xFF2BB8AA),
    brand: LagoonPalette.sand,
    brandDeep: LagoonPalette.lagoon,
    violet: Color(0xFF7ED4CC),
    onBrand: LagoonPalette.ink,
    danger: Color(0xFFE39284),
    notice: LagoonPalette.sand,
    noticeFill: Color(0xFF2C2818),
    noticeBorder: Color(0x66F0C56A),
    border: Color(0x335EE0D2),
    borderStrong: Color(0x595EE0D2),
    glowCyan: Color(0x405EE0D2),
    glowTeal: Color(0x59F0C56A),
    shadow: Color(0x8802080C),
    depthGradient: LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      colors: [Color(0xFF071C22), LagoonPalette.ocean, Color(0xFF0C3D42)],
      stops: [0.0, 0.48, 1.0],
    ),
    primaryGradient: LinearGradient(
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
      colors: [LagoonPalette.sand, LagoonPalette.sun],
    ),
    surfaceSheen: LinearGradient(
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
      colors: [LagoonPalette.surfaceHigh, LagoonPalette.surface, LagoonPalette.navy],
    ),
    systemUi: SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
      statusBarBrightness: Brightness.dark,
      systemNavigationBarColor: LagoonPalette.lagoonDeep,
      systemNavigationBarIconBrightness: Brightness.light,
    ),
    auraCyan: 0.28,
    auraTeal: 0.22,
    auraViolet: 0.14,
  );

  /// Light mode: tropical shallows. Foam cards, lagoon actions, sand as accent.
  static const frost = AppTokens(
    style: AppStyle.frost,
    brightness: Brightness.light,
    abyss: LagoonPalette.mist,
    ocean: LagoonPalette.shallows,
    navy: Color(0xFF8EC8D0),
    surface: LagoonPalette.foam,
    surfaceHigh: Color(0xFFFFFFFF),
    ink: LagoonPalette.ink,
    inkMuted: Color(0xFF3D5E66),
    inkSubtle: Color(0xFF6A8A90),
    cyan: LagoonPalette.lagoon,
    teal: LagoonPalette.lagoonDeep,
    brand: LagoonPalette.lagoon,
    brandDeep: LagoonPalette.lagoonDeep,
    violet: Color(0xFF7EC8C4),
    onBrand: LagoonPalette.foam,
    danger: Color(0xFFC45C50),
    notice: LagoonPalette.sandDeep,
    noticeFill: LagoonPalette.sun,
    noticeBorder: Color(0x66C4A24A),
    border: Color(0x338EC8D0),
    borderStrong: Color(0x668EC8D0),
    glowCyan: Color(0x335EE0D2),
    glowTeal: Color(0x40F0C56A),
    shadow: Color(0x2212343C),
    depthGradient: LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      colors: [Color(0xFFEAF7F8), LagoonPalette.mist, Color(0xFF9ED4DC)],
      stops: [0.0, 0.38, 1.0],
    ),
    primaryGradient: LinearGradient(
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
      colors: [Color(0xFF12908A), LagoonPalette.lagoonDeep],
    ),
    surfaceSheen: LinearGradient(
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
      colors: [Color(0xFFFFFFFF), LagoonPalette.foam, Color(0xFFD4EEF2)],
    ),
    systemUi: SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.dark,
      statusBarBrightness: Brightness.light,
      systemNavigationBarColor: LagoonPalette.lagoonDeep,
      systemNavigationBarIconBrightness: Brightness.light,
    ),
    auraCyan: 0.26,
    auraTeal: 0.18,
    auraViolet: 0.16,
  );

  static AppTokens forStyle(AppStyle style) =>
      style == AppStyle.frost ? frost : night;

  bool get isLight => brightness == Brightness.light;

  Color get sun => isLight ? noticeFill : ink;

  Color get onSand => LagoonPalette.ink;

  /// Sand orb so the camera reads on the teal dock in both styles.
  LinearGradient get cameraGradient => const LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [LagoonPalette.sand, LagoonPalette.sun],
  );

  List<BoxShadow> get cardShadows => [
    BoxShadow(
      color: shadow,
      blurRadius: isLight ? 28 : 24,
      offset: Offset(0, isLight ? 8 : 10),
    ),
  ];

  List<BoxShadow> get cardGlowShadows => [
    BoxShadow(color: glowCyan, blurRadius: isLight ? 26 : 32, offset: const Offset(0, 10)),
    BoxShadow(color: shadow, blurRadius: isLight ? 16 : 18, offset: const Offset(0, 8)),
  ];

  List<BoxShadow> get glowShadows => [
    BoxShadow(
      color: glowTeal,
      blurRadius: isLight ? 18 : 26,
      offset: Offset(0, isLight ? 5 : 7),
    ),
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
  AppTokens get tokens =>
      Theme.of(this).extension<AppTokens>() ?? AppTokens.night;
}

abstract final class AppSpace {
  static const double xs = 8;
  static const double sm = 12;
  static const double md = 16;
  static const double lg = 24;
  static const double xl = 32;
  static const double maxContent = 720;
  static const double stackActionsBelow = 300;

  static const double navClearance = 116;

  static EdgeInsets pageInsets(
    BuildContext context, {
    double extraBottom = 0,
  }) {
    final width = MediaQuery.sizeOf(context).width;
    final horizontal = width >= 768 ? 32.0 : 20.0;
    return EdgeInsets.fromLTRB(horizontal, 12, horizontal, 28 + extraBottom);
  }

  static EdgeInsets headerInsets(BuildContext context) {
    final width = MediaQuery.sizeOf(context).width;
    final horizontal = width >= 768 ? 32.0 : 20.0;
    return EdgeInsets.fromLTRB(horizontal, 8, horizontal, 4);
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
