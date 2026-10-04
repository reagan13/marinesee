import 'package:flutter_test/flutter_test.dart';
import 'package:marine_see/data/model_3d_library.dart';

void main() {
  test('fromAssets prefers growth mp4, then glb, then still', () {
    const slug = 'cymodocea_rotundata';
    final media = Model3dLibrary.fromAssets(slug, [
      'assets/models-3d/${slug}_growth.mp4',
      'assets/models-3d/$slug.glb',
      'assets/images/species/$slug.png',
      'assets/images/onboarding/learn.png',
    ]);

    expect(media.videoAsset, 'assets/models-3d/${slug}_growth.mp4');
    expect(media.modelAsset, 'assets/models-3d/$slug.glb');
    expect(media.stillAsset, 'assets/images/species/$slug.png');
    expect(Model3dLibrary.statusLabel(media), 'Growth clip ready');
  });

  test('fromAssets is empty when nothing is bundled', () {
    final media = Model3dLibrary.fromAssets('thalassia_hemprichii', [
      'assets/images/onboarding/learn.png',
    ]);
    expect(media.hasVideo, isFalse);
    expect(media.hasModel, isFalse);
    expect(media.hasStill, isFalse);
    expect(Model3dLibrary.statusLabel(media), 'Clip coming');
  });
}
