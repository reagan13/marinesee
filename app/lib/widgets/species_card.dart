import 'package:flutter/material.dart';

import '../theme/tokens.dart';

/// Lagoon tile for one library species.
class SpeciesCard extends StatelessWidget {
  const SpeciesCard({
    super.key,
    required this.title,
    required this.subtitle,
    required this.onTap,
    this.badge,
    this.icon = Icons.eco_outlined,
    this.imageAsset,
  });

  final String title;
  final String subtitle;
  final VoidCallback onTap;
  final Widget? badge;
  final IconData icon;
  final String? imageAsset;

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    final text = Theme.of(context).textTheme;
    final wash = [
      tokens.cyan,
      tokens.navy,
      tokens.notice,
    ][title.hashCode.abs() % 3];

    return Material(
      color: tokens.surfaceHigh,
      borderRadius: AppRadius.card,
      child: InkWell(
        onTap: onTap,
        borderRadius: AppRadius.card,
        child: Ink(
          decoration: BoxDecoration(
            borderRadius: AppRadius.card,
            border: Border.all(color: tokens.border),
            boxShadow: tokens.cardShadows,
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Expanded(
                child: Stack(
                  children: [
                    Positioned.fill(
                      child: imageAsset == null
                          ? DecoratedBox(
                              decoration: BoxDecoration(
                                gradient: LinearGradient(
                                  begin: Alignment.topLeft,
                                  end: Alignment.bottomRight,
                                  colors: [
                                    wash.withValues(
                                      alpha: tokens.isLight ? 0.34 : 0.42,
                                    ),
                                    tokens.surfaceHigh,
                                  ],
                                ),
                                borderRadius: const BorderRadius.vertical(
                                  top: Radius.circular(AppRadius.lg),
                                ),
                              ),
                            )
                          : ClipRRect(
                              borderRadius: const BorderRadius.vertical(
                                top: Radius.circular(AppRadius.lg),
                              ),
                              child: Image.asset(
                                imageAsset!,
                                fit: BoxFit.cover,
                              ),
                            ),
                    ),
                    if (imageAsset == null) ...[
                      Positioned(
                        right: -10,
                        bottom: -18,
                        child: Icon(
                          Icons.spa,
                          size: 92,
                          color: wash.withValues(alpha: 0.18),
                        ),
                      ),
                      Center(
                        child: Container(
                          width: 56,
                          height: 56,
                          decoration: BoxDecoration(
                            color: tokens.surfaceHigh.withValues(alpha: 0.88),
                            shape: BoxShape.circle,
                            border: Border.all(color: tokens.border),
                            boxShadow: tokens.cardShadows,
                          ),
                          child: Icon(icon, size: 28, color: wash),
                        ),
                      ),
                    ],
                    if (badge != null)
                      Positioned(
                        top: 8,
                        left: 8,
                        right: 8,
                        child: Align(
                          alignment: Alignment.topLeft,
                          child: badge!,
                        ),
                      ),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(12, 10, 10, 12),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            title,
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                            style: text.titleSmall?.copyWith(
                              color: tokens.ink,
                              fontStyle: FontStyle.italic,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            subtitle,
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                            style: text.bodySmall,
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 8),
                    Container(
                      width: 28,
                      height: 28,
                      decoration: BoxDecoration(
                        color: tokens.brand,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Icon(
                        Icons.arrow_forward,
                        size: 16,
                        color: tokens.onBrand,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
