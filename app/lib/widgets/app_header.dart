import 'package:flutter/material.dart';

import '../theme/tokens.dart';

/// Dark type on the sky-to-water header.
class AppHeader extends StatelessWidget {
  const AppHeader({
    super.key,
    required this.title,
    this.subtitle,
    this.greeting,
    this.eyebrow,
  });

  final String title;
  final String? subtitle;
  final String? greeting;
  final String? eyebrow;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final onWash = SkyPalette.onSky;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (greeting != null) ...[
          Text(
            greeting!,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: text.bodyMedium?.copyWith(color: onWash),
          ),
          const SizedBox(height: 4),
        ],
        if (eyebrow != null) ...[
          Text(
            eyebrow!,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: text.labelLarge?.copyWith(color: onWash),
          ),
          const SizedBox(height: 2),
        ],
        Text(
          title,
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
          style: text.displaySmall?.copyWith(color: onWash),
        ),
        if (subtitle != null) ...[
          const SizedBox(height: 4),
          Text(
            subtitle!,
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
            style: text.bodyMedium?.copyWith(color: onWash),
          ),
        ],
      ],
    );
  }
}
