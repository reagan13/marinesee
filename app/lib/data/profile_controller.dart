import 'package:flutter/material.dart';

/// Local visitor name for the home greeting. No account or login.
class ProfileController extends ChangeNotifier {
  String name = '';

  String get displayName {
    final trimmed = name.trim();
    return trimmed.isEmpty ? 'Guest' : trimmed;
  }

  void setName(String value) {
    if (name == value) {
      return;
    }
    name = value;
    notifyListeners();
  }
}

class ProfileScope extends InheritedNotifier<ProfileController> {
  const ProfileScope({
    super.key,
    required ProfileController controller,
    required super.child,
  }) : super(notifier: controller);

  static ProfileController of(BuildContext context) {
    final scope = context.dependOnInheritedWidgetOfExactType<ProfileScope>();
    assert(scope != null, 'ProfileScope not found');
    return scope!.notifier!;
  }
}
