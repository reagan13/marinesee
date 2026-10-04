import 'package:flutter/material.dart';

import '../theme/tokens.dart';

class SectionHeader extends StatelessWidget {
  const SectionHeader({
    super.key,
    required this.title,
    this.action,
    this.onAction,
  });

  final String title;
  final String? action;
  final VoidCallback? onAction;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final tokens = context.tokens;

    return Row(
      children: [
        Expanded(child: Text(title, style: text.titleLarge)),
        if (action != null)
          TextButton(
            onPressed: onAction,
            child: Text(
              action!,
              style: text.labelLarge?.copyWith(color: tokens.brand),
            ),
          ),
      ],
    );
  }
}
