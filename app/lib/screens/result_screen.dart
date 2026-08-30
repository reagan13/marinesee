import 'dart:io';

import 'package:flutter/material.dart';

import '../classify/classifier.dart';
import '../classify/stub_classifier.dart';
import '../theme/tokens.dart';

class ResultScreen extends StatelessWidget {
  const ResultScreen({
    super.key,
    required this.image,
    required this.result,
  });

  final File image;
  final IdentifyResult result;

  @override
  Widget build(BuildContext context) {
    final isStub = result.status == IdentifyStatus.stub;
    final message = isStub
        ? StubClassifier.notConnectedMessage
        : (result.message ?? 'Identification did not finish.');

    return Scaffold(
      appBar: AppBar(title: const Text('Result')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
        children: [
          Card(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(AppTokens.radius),
              child: Image.file(image, fit: BoxFit.contain),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Text(
                message,
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: AppTokens.ink,
                ),
              ),
            ),
          ),
          if (!isStub && result.slug != null) ...[
            const SizedBox(height: 8),
            Text(
              'Predicted slug: ${result.slug}',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: AppTokens.inkMuted,
              ),
            ),
          ],
          const SizedBox(height: 16),
          FilledButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Try again'),
          ),
        ],
      ),
    );
  }
}
