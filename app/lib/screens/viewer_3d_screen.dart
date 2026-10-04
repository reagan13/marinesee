import 'package:flutter/material.dart';

import '../data/model_3d_library.dart';
import '../theme/tokens.dart';
import '../widgets/app_states.dart';
import '../widgets/ocean_layout.dart';
import '../widgets/ocean_surface.dart';
import '../widgets/species_clip_player.dart';

class Viewer3dScreen extends StatefulWidget {
  const Viewer3dScreen({super.key, required this.slug});

  final String slug;

  static const placeholderCopy = '3D model coming — drop a .glb or growth clip here later.';

  @override
  State<Viewer3dScreen> createState() => _Viewer3dScreenState();
}

class _Viewer3dScreenState extends State<Viewer3dScreen> {
  late Future<SpeciesMedia> _future = Model3dLibrary.resolve(widget.slug);
  var _videoFailed = false;

  @override
  void didUpdateWidget(covariant Viewer3dScreen oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.slug != widget.slug) {
      _future = Model3dLibrary.resolve(widget.slug);
      _videoFailed = false;
    }
  }

  @override
  Widget build(BuildContext context) {
    return OceanScaffold(
      title: '3D',
      body: FutureBuilder<SpeciesMedia>(
        future: _future,
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return OceanError(
              message: 'Could not open this species clip.',
              onRetry: () {
                setState(() {
                  Model3dLibrary.resetCache();
                  _future = Model3dLibrary.resolve(widget.slug);
                  _videoFailed = false;
                });
              },
            );
          }
          final media = snapshot.data;
          if (media == null) {
            return const OceanLoading(label: 'Opening 3D…');
          }
          return _ViewerBody(
            slug: widget.slug,
            media: media,
            videoFailed: _videoFailed,
            onVideoFailed: () => setState(() => _videoFailed = true),
          );
        },
      ),
    );
  }
}

class _ViewerBody extends StatelessWidget {
  const _ViewerBody({
    required this.slug,
    required this.media,
    required this.videoFailed,
    required this.onVideoFailed,
  });

  final String slug;
  final SpeciesMedia media;
  final bool videoFailed;
  final VoidCallback onVideoFailed;

  @override
  Widget build(BuildContext context) {
    final showVideo = media.hasVideo && !videoFailed;
    final showStill = media.hasStill && !showVideo;
    final showGlbNote = media.hasModel && !showVideo;

    if (!showVideo && !showStill && !showGlbNote) {
      return Padding(
        padding: AppSpace.pageInsets(context),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 420),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const OceanEmpty(
                  icon: Icons.view_in_ar_outlined,
                  title: Viewer3dScreen.placeholderCopy,
                  message: 'Playback only. Modeling stays outside this repo.',
                ),
                Text(
                  slug,
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.labelMedium,
                ),
              ],
            ),
          ),
        ),
      );
    }

    return OceanPage(
      children: [
        if (showVideo)
          SpeciesClipPlayer(
            assetPath: media.videoAsset!,
            onFailed: onVideoFailed,
          ),
        if (showStill) ...[
          if (showVideo) const SizedBox(height: 16),
          OceanSurface(
            glow: true,
            padding: EdgeInsets.zero,
            child: ClipRRect(
              borderRadius: AppRadius.card,
              child: Image.asset(
                media.stillAsset!,
                fit: BoxFit.cover,
                width: double.infinity,
              ),
            ),
          ),
        ],
        const SizedBox(height: 16),
        OceanSurface(
          child: Text(
            _caption(showVideo: showVideo, showStill: showStill, showGlbNote: showGlbNote),
            style: Theme.of(context).textTheme.bodyMedium,
          ),
        ),
      ],
    );
  }

  String _caption({
    required bool showVideo,
    required bool showStill,
    required bool showGlbNote,
  }) {
    if (showVideo) {
      return 'Growth clip for $slug. Playback only — this repo does not author models.';
    }
    if (showGlbNote) {
      return 'A .glb is bundled for $slug. Rotate/zoom is not wired yet. Playback only.';
    }
    return 'Photo preview for $slug. Drop a growth .mp4 or .glb in assets/models-3d/ to replace this.';
  }
}
