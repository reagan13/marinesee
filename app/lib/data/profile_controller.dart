import 'dart:typed_data';

import 'package:flutter/material.dart';

/// Local visitor profile. No account or login in v1.
class ProfileController extends ChangeNotifier {
  String firstName = '';
  String lastName = '';
  Uint8List? photoBytes;

  String get displayName {
    final name = '$firstName $lastName'.trim();
    return name.isEmpty ? 'Guest' : name;
  }

  String get initials {
    final first = firstName.trim();
    final last = lastName.trim();
    final letters = '${first.isEmpty ? '' : first[0]}${last.isEmpty ? '' : last[0]}';
    return letters.isEmpty ? '?' : letters.toUpperCase();
  }

  bool get hasName => firstName.trim().isNotEmpty || lastName.trim().isNotEmpty;

  void save({
    required String firstName,
    required String lastName,
    Uint8List? photoBytes,
  }) {
    this.firstName = firstName.trim();
    this.lastName = lastName.trim();
    this.photoBytes = photoBytes;
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
