import 'package:flutter/material.dart';

import '../theme/tokens.dart';

class IconWell extends StatelessWidget {
  const IconWell({
    super.key,
    required this.icon,
    this.size = 44,
  });

  final IconData icon;
  final double size;

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        color: tokens.cyan.withValues(alpha: tokens.isLight ? 0.12 : 0.18),
        borderRadius: BorderRadius.circular(AppRadius.md),
      ),
      child: Icon(icon, color: tokens.brand, size: size * 0.45),
    );
  }
}
