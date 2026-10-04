import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

import 'classifier.dart';
import 'identify_config.dart';

/// Calls the laptop SVM process. Not on-device.
class ApiClassifier implements Classifier {
  ApiClassifier({http.Client? client, IdentifyConfig? config})
    : _client = client ?? http.Client(),
      _config = config ?? IdentifyConfig.current;

  final http.Client _client;
  final IdentifyConfig _config;

  @override
  Future<IdentifyResult> identify(XFile image) async {
    final bytes = await image.readAsBytes();
    if (bytes.isEmpty) {
      return const IdentifyResult(
        status: IdentifyStatus.error,
        message: 'That photo is empty.',
      );
    }

    final http.Response response;
    try {
      response = await _client.post(
        _config.resolve('/api/v1/identify'),
        headers: const {
          'Content-Type': 'application/octet-stream',
          'Accept': 'application/json',
        },
        body: bytes,
      );
    } catch (_) {
      return IdentifyResult(
        status: IdentifyStatus.error,
        message:
            'Cannot reach the identify API at ${_config.baseUrl}. '
            'Start serve_identify.py and use adb reverse, or pass IDENTIFY_API_URL.',
      );
    }

    return _parse(response);
  }

  IdentifyResult _parse(http.Response response) {
    final decoded = _jsonMap(response.body);
    if (decoded == null) {
      return const IdentifyResult(
        status: IdentifyStatus.error,
        message: 'The identify API did not return JSON.',
      );
    }

    if (decoded['success'] != true) {
      final error = decoded['error'];
      final message = error is Map<String, dynamic>
          ? (error['message'] as String? ?? 'Identify failed.')
          : 'Identify failed.';
      return IdentifyResult(status: IdentifyStatus.error, message: message);
    }

    final data = decoded['data'];
    if (data is! Map<String, dynamic>) {
      return const IdentifyResult(
        status: IdentifyStatus.error,
        message: 'The identify API returned no data.',
      );
    }

    final slug = data['slug'] as String?;
    final confidence = (data['confidence'] as num?)?.toDouble();
    if (slug == null || confidence == null) {
      return const IdentifyResult(
        status: IdentifyStatus.error,
        message: 'The identify API omitted slug or confidence.',
      );
    }

    final low =
        data['low_confidence'] as bool? ??
        confidence < IdentifyConfig.lowConfidence;
    return IdentifyResult(
      slug: slug,
      confidence: confidence,
      status: low ? IdentifyStatus.lowConfidence : IdentifyStatus.ok,
      message: low
          ? 'Low confidence — retake if you can get a closer leaf.'
          : null,
    );
  }

  Map<String, dynamic>? _jsonMap(String body) {
    try {
      final decoded = jsonDecode(body);
      if (decoded is Map<String, dynamic>) {
        return decoded;
      }
    } catch (_) {}
    return null;
  }
}
