import 'package:flutter/services.dart';

/// Bundled clip / still / glb for one species.
class SpeciesMedia {
  const SpeciesMedia({
    this.videoAsset,
    this.modelAsset,
    this.stillAsset,
  });

  final String? videoAsset;
  final String? modelAsset;
  final String? stillAsset;

  bool get hasVideo => videoAsset != null;
  bool get hasModel => modelAsset != null;
  bool get hasStill => stillAsset != null;
}

/// Resolves dropped 3D files from the Flutter asset bundle.
///
/// Convention (see `docs/11-species.md` slugs):
/// - `assets/models-3d/<slug>_growth.mp4`
/// - `assets/models-3d/<slug>.glb`
/// - `assets/images/species/<slug>.{png,jpg,jpeg}`
class Model3dLibrary {
  static const videoFolder = 'assets/models-3d/';
  static const stillFolder = 'assets/images/species/';

  static Iterable<String>? _assets;

  static Future<Iterable<String>> _listAssets() async {
    if (_assets != null) {
      return _assets!;
    }
    final manifest = await AssetManifest.loadFromAssetBundle(rootBundle);
    _assets = manifest.listAssets();
    return _assets!;
  }

  static Future<SpeciesMedia> resolve(String slug) async {
    return fromAssets(slug, await _listAssets());
  }

  static Future<Map<String, SpeciesMedia>> resolveMany(
    Iterable<String> slugs,
  ) async {
    final assets = await _listAssets();
    return {
      for (final slug in slugs) slug: fromAssets(slug, assets),
    };
  }

  static SpeciesMedia fromAssets(String slug, Iterable<String> assets) {
    final listed = assets.toSet();
    final video = '$videoFolder${slug}_growth.mp4';
    final model = '$videoFolder$slug.glb';
    String? still;
    for (final suffix in const ['.png', '.jpg', '.jpeg']) {
      final candidate = '$stillFolder$slug$suffix';
      if (listed.contains(candidate)) {
        still = candidate;
        break;
      }
    }
    return SpeciesMedia(
      videoAsset: listed.contains(video) ? video : null,
      modelAsset: listed.contains(model) ? model : null,
      stillAsset: still,
    );
  }

  static String statusLabel(SpeciesMedia media) {
    if (media.hasVideo) {
      return 'Growth clip ready';
    }
    if (media.hasModel) {
      return '3D file ready';
    }
    if (media.hasStill) {
      return 'Photo preview';
    }
    return 'Clip coming';
  }

  static void resetCache() {
    _assets = null;
  }
}
