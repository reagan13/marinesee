import 'package:flutter/material.dart';

import '../theme/tokens.dart';

class Viewer3dScreen extends StatelessWidget {
  const Viewer3dScreen({super.key, required this.slug});

  final String slug;

  static const placeholderCopy =
      '3D model coming — drop a .glb here later.';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('3D')),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Center(
          child: Text(
            placeholderCopy,
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
              color: AppTokens.ink,
            ),
          ),
        ),
      ),
    );
  }
}
