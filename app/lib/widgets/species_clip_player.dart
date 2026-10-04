import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';

import '../theme/tokens.dart';
import 'ocean_surface.dart';

/// Loops a bundled growth clip. Play/pause only — no modeling.
class SpeciesClipPlayer extends StatefulWidget {
  const SpeciesClipPlayer({
    super.key,
    required this.assetPath,
    this.onFailed,
  });

  final String assetPath;
  final VoidCallback? onFailed;

  @override
  State<SpeciesClipPlayer> createState() => _SpeciesClipPlayerState();
}

class _SpeciesClipPlayerState extends State<SpeciesClipPlayer> {
  VideoPlayerController? _controller;
  var _failed = false;

  @override
  void initState() {
    super.initState();
    _open();
  }

  Future<void> _open() async {
    final controller = VideoPlayerController.asset(widget.assetPath);
    try {
      await controller.initialize();
      await controller.setLooping(true);
      await controller.setVolume(0);
      await controller.play();
      if (!mounted) {
        await controller.dispose();
        return;
      }
      setState(() => _controller = controller);
    } catch (_) {
      await controller.dispose();
      if (!mounted) {
        return;
      }
      setState(() => _failed = true);
      widget.onFailed?.call();
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  Future<void> _toggle() async {
    final controller = _controller;
    if (controller == null || !controller.value.isInitialized) {
      return;
    }
    if (controller.value.isPlaying) {
      await controller.pause();
    } else {
      await controller.play();
    }
    if (mounted) {
      setState(() {});
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_failed) {
      return const SizedBox.shrink();
    }
    final controller = _controller;
    if (controller == null || !controller.value.isInitialized) {
      return const SizedBox(
        height: 280,
        child: Center(child: CircularProgressIndicator(strokeWidth: 2.4)),
      );
    }

    final tokens = context.tokens;
    final playing = controller.value.isPlaying;

    return OceanSurface(
      glow: true,
      padding: EdgeInsets.zero,
      child: ClipRRect(
        borderRadius: AppRadius.card,
        child: AspectRatio(
          aspectRatio: controller.value.aspectRatio == 0
              ? 9 / 16
              : controller.value.aspectRatio,
          child: Stack(
            fit: StackFit.expand,
            children: [
              ColoredBox(
                color: tokens.abyss,
                child: FittedBox(
                  fit: BoxFit.cover,
                  child: SizedBox(
                    width: controller.value.size.width,
                    height: controller.value.size.height,
                    child: VideoPlayer(controller),
                  ),
                ),
              ),
              Positioned(
                right: 12,
                bottom: 12,
                child: Material(
                  color: tokens.surfaceHigh.withValues(alpha: 0.88),
                  borderRadius: BorderRadius.circular(AppRadius.md),
                  child: InkWell(
                    onTap: _toggle,
                    borderRadius: BorderRadius.circular(AppRadius.md),
                    child: SizedBox(
                      width: 48,
                      height: 48,
                      child: Icon(
                        playing
                            ? Icons.pause_rounded
                            : Icons.play_arrow_rounded,
                        color: tokens.ink,
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
