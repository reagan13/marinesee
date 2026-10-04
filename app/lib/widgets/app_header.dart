import 'package:flutter/material.dart';

import '../theme/tokens.dart';
import 'app_logo.dart';

/// Shared top chrome for the main tabs. Detail screens keep an AppBar.
class AppHeader extends StatelessWidget {
  const AppHeader({
    super.key,
    this.greeting,
    this.title,
    this.subtitle,
    this.place,
    this.trailing,
  });

  final String? greeting;
  final String? title;
  final String? subtitle;
  final String? place;
  final Widget? trailing;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final tokens = context.tokens;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const AppLogo(),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'MarineSee',
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: text.titleMedium?.copyWith(
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  Text(
                    'Seagrass · Mati City',
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: text.labelSmall?.copyWith(color: tokens.inkMuted),
                  ),
                ],
              ),
            ),
            if (trailing != null) ...[const SizedBox(width: 12), trailing!],
          ],
        ),
        if (greeting != null) ...[
          const SizedBox(height: 20),
          Text(greeting!, style: text.bodyMedium),
        ],
        if (title != null) ...[
          SizedBox(height: greeting == null ? 18 : 4),
          Text(title!, style: text.displaySmall),
        ],
        if (place != null) ...[
          const SizedBox(height: 10),
          Container(
            padding: const EdgeInsets.fromLTRB(10, 6, 12, 6),
            decoration: BoxDecoration(
              color: tokens.brand.withValues(alpha: tokens.isLight ? 0.10 : 0.16),
              borderRadius: BorderRadius.circular(AppRadius.pill),
              border: Border.all(color: tokens.brand.withValues(alpha: 0.28)),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.location_on, size: 15, color: tokens.brand),
                const SizedBox(width: 4),
                Flexible(
                  child: Text(
                    place!,
                    overflow: TextOverflow.ellipsis,
                    style: text.labelMedium?.copyWith(color: tokens.brand),
                  ),
                ),
              ],
            ),
          ),
        ],
        if (subtitle != null) ...[
          const SizedBox(height: 8),
          Text(subtitle!, style: text.bodyMedium),
        ],
      ],
    );
  }
}
