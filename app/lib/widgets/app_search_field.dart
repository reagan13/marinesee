import 'package:flutter/material.dart';

import '../theme/tokens.dart';

class AppSearchField extends StatelessWidget {
  const AppSearchField({
    super.key,
    required this.hint,
    this.controller,
    this.onChanged,
    this.onTap,
    this.readOnly = false,
    this.onWash = false,
  });

  final String hint;
  final TextEditingController? controller;
  final ValueChanged<String>? onChanged;
  final VoidCallback? onTap;
  final bool readOnly;
  final bool onWash;

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    final fill = onWash ? const Color(0x2EFFFFFF) : tokens.surfaceHigh;
    final foreground = onWash ? const Color(0xF2FFFFFF) : tokens.inkMuted;
    final borderColor = onWash ? const Color(0x55FFFFFF) : tokens.border;

    final field = TextField(
      controller: controller,
      style: onWash ? const TextStyle(color: SkyPalette.onHeader) : null,
      cursorColor: onWash ? SkyPalette.onHeader : null,
      readOnly: readOnly,
      showCursor: !readOnly,
      enableInteractiveSelection: !readOnly,
      onTap: onTap,
      onChanged: onChanged,
      textInputAction: TextInputAction.search,
      decoration: InputDecoration(
        hintText: hint,
        prefixIcon: Icon(
          Icons.search,
          color: foreground,
        ),
        hintStyle: TextStyle(color: foreground),
        filled: true,
        fillColor: fill,
        constraints: const BoxConstraints(minHeight: AppTokens.tapMin),
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadius.xl),
          borderSide: BorderSide(color: borderColor),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadius.xl),
          borderSide: BorderSide(color: borderColor),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadius.xl),
          borderSide: BorderSide(color: tokens.brand, width: 1.4),
        ),
      ),
    );

    return field;
  }
}
