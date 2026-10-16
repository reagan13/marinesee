import 'package:flutter/widgets.dart';

/// Tab indexes for [AppShell].
abstract final class ShellTab {
  static const home = 0;
  static const scan = 1;
  static const library = 2;
  static const conservation = 3;
  static const profile = 4;
}

/// Lets a tab open another tab. Scan does not open the camera.
class ShellScope extends InheritedWidget {
  const ShellScope({super.key, required this.select, required super.child});

  final ValueChanged<int> select;

  static ShellScope of(BuildContext context) {
    final scope = context.dependOnInheritedWidgetOfExactType<ShellScope>();
    assert(scope != null, 'ShellScope not found');
    return scope!;
  }

  @override
  bool updateShouldNotify(ShellScope oldWidget) => false;
}
