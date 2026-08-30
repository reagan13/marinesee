import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:marine_see/classify/classifier.dart';
import 'package:marine_see/classify/stub_classifier.dart';

void main() {
  test('StubClassifier does not invent a species or confidence', () async {
    final result = await StubClassifier().identify(File('dummy.jpg'));
    expect(result.status, IdentifyStatus.stub);
    expect(result.slug, isNull);
    expect(result.confidence, isNull);
    expect(result.message, StubClassifier.notConnectedMessage);
  });
}
