import 'dart:typed_data';

import 'package:flutter/material.dart';

import '../theme/tokens.dart';

class ProfileAvatar extends StatelessWidget {
  const ProfileAvatar({
    super.key,
    required this.initials,
    this.photoBytes,
    this.size = 88,
    this.onTap,
  });

  final String initials;
  final Uint8List? photoBytes;
  final double size;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    final image = photoBytes == null ? null : MemoryImage(photoBytes!);

    return Material(
      type: MaterialType.transparency,
      child: InkWell(
        onTap: onTap,
        customBorder: const CircleBorder(),
        child: Container(
          width: size,
          height: size,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            border: Border.all(color: tokens.borderStrong, width: 2),
            boxShadow: tokens.cardShadows,
          ),
          child: CircleAvatar(
            radius: (size / 2) - 2,
            backgroundColor: tokens.brand.withValues(alpha: 0.18),
            backgroundImage: image,
            child: image == null
                ? Text(
                    initials,
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      color: tokens.brand,
                    ),
                  )
                : null,
          ),
        ),
      ),
    );
  }
}
