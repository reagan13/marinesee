import 'package:flutter/material.dart';

import 'tokens.dart';

class ThemeController extends ChangeNotifier {
  AppStyle style = AppStyle.frost;

  AppTokens get tokens => AppTokens.forStyle(style);

  bool get isLight => style == AppStyle.frost;

  void setStyle(AppStyle next) {
    if (style == next) {
      return;
    }
    style = next;
    notifyListeners();
  }

  void toggle() {
    setStyle(isLight ? AppStyle.night : AppStyle.frost);
  }
}

class ThemeScope extends InheritedNotifier<ThemeController> {
  const ThemeScope({
    super.key,
    required ThemeController controller,
    required super.child,
  }) : super(notifier: controller);

  static ThemeController of(BuildContext context) {
    final scope = context.dependOnInheritedWidgetOfExactType<ThemeScope>();
    assert(scope != null, 'ThemeScope not found');
    return scope!.notifier!;
  }
}
