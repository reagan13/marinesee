import 'package:image_picker/image_picker.dart';

import 'classifier.dart';

/// Scaffold only. Does not invent a species or a confidence score.
class StubClassifier implements Classifier {
  static const notConnectedMessage =
      'SVM not connected yet. Use ApiClassifier + serve_identify.py.';

  @override
  Future<IdentifyResult> identify(XFile image) async {
    return const IdentifyResult(
      status: IdentifyStatus.stub,
      message: notConnectedMessage,
    );
  }
}
