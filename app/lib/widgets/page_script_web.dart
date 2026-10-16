import 'dart:js_interop';

@JS('eval')
external void _eval(JSString source);

/// Runs a script in the browser page, where the 3D viewer element lives.
Future<void> runPageScript(String source) async {
  _eval(source.toJS);
}
