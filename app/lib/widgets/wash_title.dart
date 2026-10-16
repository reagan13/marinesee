import 'package:flutter/material.dart';

import '../theme/tokens.dart';

/// Centered title on the curved wash. Back sits on the left.
class WashTitle extends StatelessWidget {
  const WashTitle({
    super.key,
    required this.title,
    this.subtitle,
    this.onBack,
    this.bottom,
  });

  final String title;
  final String? subtitle;
  final VoidCallback? onBack;
  final Widget? bottom;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final onWash = SkyPalette.onHeader;

    final heading = Column(
      children: [
        Text(
          title,
          textAlign: TextAlign.center,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: text.headlineSmall?.copyWith(
            color: onWash,
            fontWeight: FontWeight.w700,
          ),
        ),
        if (subtitle != null) ...[
          const SizedBox(height: 4),
          Text(
            subtitle!,
            textAlign: TextAlign.center,
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
            style: text.bodyMedium?.copyWith(color: onWash),
          ),
        ],
      ],
    );

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        if (onBack == null)
          heading
        else
          Row(
            children: [
              _RoundIconButton(icon: Icons.arrow_back, onPressed: onBack!),
              Expanded(child: heading),
              const SizedBox(width: 48),
            ],
          ),
        if (bottom != null) ...[
          const SizedBox(height: 14),
          bottom!,
        ],
      ],
    );
  }
}

class _RoundIconButton extends StatelessWidget {
  const _RoundIconButton({required this.icon, required this.onPressed});

  final IconData icon;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return DecoratedBox(
      decoration: const BoxDecoration(shape: BoxShape.circle),
      child: Material(
        color: Color(0x33FFFFFF),
        shape: const CircleBorder(
          side: BorderSide(color: Color(0x55FFFFFF)),
        ),
        child: InkWell(
          customBorder: const CircleBorder(),
          onTap: onPressed,
          child: SizedBox(
            width: 48,
            height: 48,
            child: Icon(icon, color: SkyPalette.onHeader),
          ),
        ),
      ),
    );
  }
}
