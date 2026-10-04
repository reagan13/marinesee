import 'package:flutter/material.dart';

import '../theme/tokens.dart';

/// Elevated ocean panel. Glow is reserved for a few important cards.
class OceanSurface extends StatelessWidget {
  const OceanSurface({
    super.key,
    required this.child,
    this.padding = const EdgeInsets.all(18),
    this.glow = false,
    this.onTap,
    this.height,
  });

  final Widget child;
  final EdgeInsetsGeometry padding;
  final bool glow;
  final VoidCallback? onTap;
  final double? height;

  @override
  Widget build(BuildContext context) {
    final radius = AppRadius.card;
    final tokens = context.tokens;

    Widget content = Padding(padding: padding, child: child);
    if (onTap != null) {
      content = Material(
        type: MaterialType.transparency,
        child: InkWell(
          onTap: onTap,
          borderRadius: radius,
          splashColor: tokens.cyan.withValues(alpha: 0.10),
          highlightColor: tokens.cyan.withValues(alpha: 0.05),
          child: content,
        ),
      );
    }

    return DecoratedBox(
      decoration: BoxDecoration(
        color: glow
            ? null
            : (tokens.isLight ? tokens.surfaceHigh : tokens.surface)
                .withValues(alpha: tokens.isLight ? 0.94 : 0.78),
        gradient: glow ? tokens.surfaceSheen : null,
        borderRadius: radius,
        border: Border.all(
          color: glow ? tokens.borderStrong : tokens.border,
        ),
        boxShadow: glow ? tokens.cardGlowShadows : tokens.cardShadows,
      ),
      child: ClipRRect(
        borderRadius: radius,
        child: SizedBox(height: height, width: double.infinity, child: content),
      ),
    );
  }
}

class OceanDivider extends StatelessWidget {
  const OceanDivider({super.key});

  @override
  Widget build(BuildContext context) {
    return const Divider(height: 28);
  }
}
