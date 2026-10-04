import 'package:flutter/material.dart';

import '../theme/tokens.dart';

/// Primary action: brand fill, restrained glow, 52px tap target.
class AuroraButton extends StatelessWidget {
  const AuroraButton({
    super.key,
    required this.label,
    required this.onPressed,
    this.icon,
    this.loading = false,
  });

  final String label;
  final VoidCallback? onPressed;
  final IconData? icon;
  final bool loading;

  @override
  Widget build(BuildContext context) {
    final enabled = onPressed != null && !loading;
    final radius = AppRadius.button;
    final tokens = context.tokens;

    return ConstrainedBox(
      constraints: const BoxConstraints(minHeight: 52, minWidth: AppTokens.tapMin),
      child: DecoratedBox(
        decoration: BoxDecoration(
          gradient: enabled ? tokens.primaryGradient : null,
          color: enabled ? null : tokens.brand.withValues(alpha: 0.28),
          borderRadius: radius,
          boxShadow: enabled ? tokens.glowShadows : null,
        ),
        child: Material(
          type: MaterialType.transparency,
          child: InkWell(
            onTap: enabled ? onPressed : null,
            borderRadius: radius,
            splashColor: tokens.ink.withValues(alpha: 0.12),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  if (loading) ...[
                    SizedBox(
                      width: 18,
                      height: 18,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: tokens.onBrand,
                      ),
                    ),
                    const SizedBox(width: 10),
                  ] else if (icon != null) ...[
                    Icon(icon, size: 20, color: tokens.onBrand),
                    const SizedBox(width: 8),
                  ],
                  Flexible(
                    child: Text(
                      label,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context).textTheme.labelLarge?.copyWith(
                        color: enabled
                            ? tokens.onBrand
                            : tokens.onBrand.withValues(alpha: 0.55),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
