import 'package:flutter/material.dart';

import '../theme/tokens.dart';

class DataComingBadge extends StatelessWidget {
  const DataComingBadge({super.key});

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;

    return Semantics(
      label: 'Data coming',
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        decoration: BoxDecoration(
          color: tokens.noticeFill,
          borderRadius: BorderRadius.circular(AppRadius.pill),
          border: Border.all(color: tokens.noticeBorder),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.schedule, size: 14, color: tokens.notice),
            const SizedBox(width: 6),
            Flexible(
              child: Text(
                'Data coming',
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                  color: tokens.notice,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
