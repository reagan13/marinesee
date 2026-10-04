import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:image_picker/image_picker.dart';
import 'package:marine_see/classify/api_classifier.dart';
import 'package:marine_see/classify/classifier.dart';
import 'package:marine_see/classify/identify_config.dart';

void main() {
  const config = IdentifyConfig(baseUrl: 'http://identify.test');

  XFile photo() => XFile.fromData(Uint8List.fromList([1, 2, 3]), name: 'leaf.jpg');

  test('maps a successful SVM response', () async {
    final client = MockClient((request) async {
      expect(request.url.path, '/api/v1/identify');
      expect(request.method, 'POST');
      return http.Response(
        jsonEncode({
          'success': true,
          'data': {
            'slug': 'enhalus_acoroides',
            'confidence': 0.48,
            'low_confidence': false,
          },
        }),
        200,
      );
    });

    final result = await ApiClassifier(client: client, config: config).identify(photo());
    expect(result.status, IdentifyStatus.ok);
    expect(result.slug, 'enhalus_acoroides');
    expect(result.confidence, 0.48);
  });

  test('flags low confidence from the API', () async {
    final client = MockClient((request) async {
      return http.Response(
        jsonEncode({
          'success': true,
          'data': {
            'slug': 'halodule_pinifolia',
            'confidence': 0.11,
            'low_confidence': true,
          },
        }),
        200,
      );
    });

    final result = await ApiClassifier(client: client, config: config).identify(photo());
    expect(result.status, IdentifyStatus.lowConfidence);
    expect(result.slug, 'halodule_pinifolia');
  });

  test('maps a failed envelope to an error, not a fake species', () async {
    final client = MockClient((request) async {
      return http.Response(
        jsonEncode({
          'success': false,
          'error': {'message': 'Could not read image (UnidentifiedImageError).'},
        }),
        400,
      );
    });

    final result = await ApiClassifier(client: client, config: config).identify(photo());
    expect(result.status, IdentifyStatus.error);
    expect(result.slug, isNull);
    expect(result.confidence, isNull);
    expect(result.message, contains('Could not read image'));
  });
}
