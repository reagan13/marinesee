import 'package:image_picker/image_picker.dart';

enum IdentifyStatus { stub, ok, lowConfidence, error }

class IdentifyResult {
  const IdentifyResult({
    this.slug,
    this.confidence,
    required this.status,
    this.message,
  });

  final String? slug;
  final double? confidence;
  final IdentifyStatus status;
  final String? message;
}

abstract class Classifier {
  Future<IdentifyResult> identify(XFile image);
}
