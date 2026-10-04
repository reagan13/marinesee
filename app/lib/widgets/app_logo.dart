import 'package:flutter/material.dart';

import '../theme/tokens.dart';

/// Swap [assetPath] when the real mark is ready.
class AppLogo extends StatelessWidget {
  const AppLogo({super.key, this.size = 40});

  static const assetPath = 'assets/images/logo.png';

  final double size;

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    final radius = BorderRadius.circular(size * 0.28);

    return Semantics(
      label: 'MarineSee',
      image: true,
      child: Container(
        width: size,
        height: size,
        decoration: BoxDecoration(
          gradient: tokens.primaryGradient,
          borderRadius: radius,
          border: Border.all(color: tokens.borderStrong),
          boxShadow: tokens.glowShadows,
        ),
        clipBehavior: Clip.antiAlias,
        child: Image.asset(
          assetPath,
          fit: BoxFit.cover,
          errorBuilder: (context, error, stackTrace) {
            return Icon(
              Icons.spa_outlined,
              color: tokens.onBrand,
              size: size * 0.5,
            );
          },
        ),
      ),
    );
  }
}
