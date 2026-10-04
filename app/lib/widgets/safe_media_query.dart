import 'dart:math' as math;

import 'package:flutter/material.dart';

/// Clamps MediaQuery metrics so a Chrome keyboard/resize glitch cannot
/// feed negative insets into [SafeArea] and padding.
class SafeMediaQuery extends StatelessWidget {
  const SafeMediaQuery({super.key, required this.child});

  final Widget child;

  static MediaQueryData sanitize(MediaQueryData data) {
    return data.copyWith(
      padding: _clamp(data.padding),
      viewPadding: _clamp(data.viewPadding),
      viewInsets: _clamp(data.viewInsets),
      size: Size(
        math.max(0, data.size.width),
        math.max(0, data.size.height),
      ),
    );
  }

  static EdgeInsets _clamp(EdgeInsets insets) {
    return EdgeInsets.only(
      left: math.max(0, insets.left),
      top: math.max(0, insets.top),
      right: math.max(0, insets.right),
      bottom: math.max(0, insets.bottom),
    );
  }

  @override
  Widget build(BuildContext context) {
    return MediaQuery(
      data: sanitize(MediaQuery.of(context)),
      child: child,
    );
  }
}
