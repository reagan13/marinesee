import 'package:flutter/material.dart';

import '../theme/tokens.dart';

class AboutScreen extends StatelessWidget {
  const AboutScreen({super.key});

  static const _conservation =
      'Learning the nine documented Mati City seagrass species supports local marine-biodiversity awareness.';

  @override
  Widget build(BuildContext context) {
    final title = Theme.of(context).textTheme.headlineSmall?.copyWith(
      color: AppTokens.ink,
      fontWeight: FontWeight.w700,
    );
    final body = Theme.of(context).textTheme.bodyLarge?.copyWith(
      color: AppTokens.ink,
    );

    return Scaffold(
      appBar: AppBar(title: const Text('About')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
        children: [
          Text('MarineSee', style: title),
          const SizedBox(height: 8),
          Text(
            'A seagrass education app for Mati City, Davao Oriental.',
            style: body,
          ),
          const SizedBox(height: 16),
          Text(
            'The library covers the nine documented local species. Identification uses an SVM. This build is English only.',
            style: body,
          ),
          const SizedBox(height: 16),
          Text(
            'Needs Android 8.0 or newer and at least 3 GB RAM. Use a physical phone. Do not use the Android emulator on the study laptop.',
            style: body,
          ),
          const SizedBox(height: 16),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Text(_conservation, style: body),
            ),
          ),
        ],
      ),
    );
  }
}
