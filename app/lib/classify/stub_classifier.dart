import 'dart:io';

import 'classifier.dart';

/// Scaffold only. Does not invent a species or a confidence score.
class StubClassifier implements Classifier {
  static const notConnectedMessage =
      'SVM not connected yet (Colab v1 is 22%).';

  @override
  Future<IdentifyResult> identify(File image) async {
    return const IdentifyResult(
      status: IdentifyStatus.stub,
      message: notConnectedMessage,
    );
  }
}
