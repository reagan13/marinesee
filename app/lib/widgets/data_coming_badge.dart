import 'package:flutter/material.dart';

import '../theme/tokens.dart';

class DataComingBadge extends StatelessWidget {
  const DataComingBadge({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: AppTokens.noticeFill,
        borderRadius: BorderRadius.circular(AppTokens.radius),
      ),
      child: Text(
        'data coming',
        style: Theme.of(context).textTheme.labelLarge?.copyWith(
          color: AppTokens.notice,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }
}
