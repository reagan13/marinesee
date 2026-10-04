import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'data/profile_controller.dart';
import 'screens/onboarding_screen.dart';
import 'screens/shell.dart';
import 'theme/theme.dart';
import 'theme/theme_controller.dart';
import 'theme/tokens.dart';
import 'widgets/safe_media_query.dart';

class MarineSeeApp extends StatefulWidget {
  const MarineSeeApp({super.key});

  @override
  State<MarineSeeApp> createState() => _MarineSeeAppState();
}

class _MarineSeeAppState extends State<MarineSeeApp> {
  final _controller = ThemeController();
  final _profile = ProfileController();
  var _onboarded = false;

  @override
  void initState() {
    super.initState();
    _controller.addListener(_onStyle);
  }

  void _onStyle() {
    if (mounted) {
      setState(() {});
    }
  }

  @override
  void dispose() {
    _controller
      ..removeListener(_onStyle)
      ..dispose();
    _profile.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final tokens = _controller.tokens;

    return ThemeScope(
      controller: _controller,
      child: ProfileScope(
        controller: _profile,
        child: MaterialApp(
          title: 'MarineSee',
          debugShowCheckedModeBanner: false,
          theme: buildMarineSeeTheme(tokens),
          themeAnimationDuration: AppMotion.medium,
          themeAnimationCurve: AppMotion.ease,
          builder: (context, child) {
            return SafeMediaQuery(
              child: AnnotatedRegion<SystemUiOverlayStyle>(
                value: tokens.systemUi,
                child: child ?? const SizedBox.shrink(),
              ),
            );
          },
          home: _onboarded
              ? const AppShell()
              : OnboardingScreen(
                  onDone: () => setState(() => _onboarded = true),
                ),
        ),
      ),
    );
  }
}
