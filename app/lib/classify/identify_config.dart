/// LAN identify API (Python `ml/src/serve_identify.py`).
///
/// Default is `adb reverse` to the laptop. For Wi-Fi:
/// `flutter run --dart-define=IDENTIFY_API_URL=http://<laptop-lan-ip>:8765`
class IdentifyConfig {
  const IdentifyConfig({required this.baseUrl});

  final String baseUrl;

  static const String defaultBaseUrl = String.fromEnvironment(
    'IDENTIFY_API_URL',
    defaultValue: 'http://127.0.0.1:8765',
  );

  static const IdentifyConfig current = IdentifyConfig(baseUrl: defaultBaseUrl);

  /// IMPLEMENTATION default until open question 14 is locked.
  static const double lowConfidence = 0.20;

  Uri resolve(String path) {
    final root = baseUrl.endsWith('/')
        ? baseUrl.substring(0, baseUrl.length - 1)
        : baseUrl;
    final suffix = path.startsWith('/') ? path : '/$path';
    return Uri.parse('$root$suffix');
  }
}
