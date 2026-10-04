import 'package:flutter/material.dart';

import '../theme/tokens.dart';

/// Compact gradient hero. Use once per page, not as a repeating promo strip.
class PageHero extends StatelessWidget {
  const PageHero({
    super.key,
    required this.kicker,
    required this.title,
    required this.subtitle,
    this.icon = Icons.waves_outlined,
  });

  final String kicker;
  final String title;
  final String subtitle;
  final IconData icon;

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    final text = Theme.of(context).textTheme;

    return Container(
      width: double.infinity,
      clipBehavior: Clip.antiAlias,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: tokens.primaryGradient,
        borderRadius: AppRadius.card,
        boxShadow: tokens.glowShadows,
      ),
      child: Stack(
        children: [
          Positioned(
            right: -18,
            bottom: -22,
            child: Icon(
              Icons.waves,
              size: 110,
              color: tokens.onBrand.withValues(alpha: 0.12),
            ),
          ),
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      kicker,
                      style: text.labelMedium?.copyWith(
                        color: tokens.onBrand.withValues(alpha: 0.8),
                        letterSpacing: 1.2,
                      ),
                    ),
                    const SizedBox(height: 6),
                    Text(
                      title,
                      style: text.titleLarge?.copyWith(color: tokens.onBrand),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      subtitle,
                      style: text.bodySmall?.copyWith(
                        color: tokens.onBrand.withValues(alpha: 0.86),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 12),
              Container(
                width: 56,
                height: 56,
                decoration: BoxDecoration(
                  color: tokens.onBrand.withValues(alpha: 0.16),
                  shape: BoxShape.circle,
                ),
                child: Icon(icon, color: tokens.onBrand, size: 28),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
