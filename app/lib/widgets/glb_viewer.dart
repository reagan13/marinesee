import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:model_viewer_plus/model_viewer_plus.dart';

import '../theme/tokens.dart';
import 'page_script_stub.dart'
    if (dart.library.js_interop) 'page_script_web.dart';

/// Pinch, drag, and playback for one bundled `.glb`.
///
/// The plant animation loops. The camera stays put until the user turns it.
class GlbViewer extends StatefulWidget {
  const GlbViewer({super.key, required this.assetPath, required this.label});

  final String assetPath;
  final String label;

  @override
  State<GlbViewer> createState() => _GlbViewerState();
}

class _GlbViewerState extends State<GlbViewer> {
  Future<void> Function(String source)? _run;
  var _playing = true;
  var _choseMotion = false;

  String get _src {
    if (kIsWeb && !widget.assetPath.startsWith('assets/assets/')) {
      return 'assets/${widget.assetPath}';
    }
    return widget.assetPath;
  }

  Future<void> _runJs(String source) async {
    if (kIsWeb) {
      await runPageScript(source);
      return;
    }
    final run = _run;
    if (run == null) {
      return;
    }
    await run(source);
  }

  Future<void> _nudge({double thetaDeg = 0, double radiusScale = 1}) async {
    try {
      await _runJs('''
        (() => {
          const mv = document.getElementById('marinesee-model');
          if (!mv || !mv.getCameraOrbit) return;
          const orbit = mv.getCameraOrbit();
          const theta = orbit.theta * 180 / Math.PI + $thetaDeg;
          const phi = orbit.phi * 180 / Math.PI;
          const radius = Math.min(8, Math.max(0.15, orbit.radius * $radiusScale));
          mv.cameraOrbit = theta.toFixed(2) + 'deg ' + phi.toFixed(2) + 'deg ' + radius.toFixed(3) + 'm';
        })();
      ''');
    } on Object {
      // The viewer may still be loading the model.
    }
  }

  @override
  void initState() {
    super.initState();
    if (kIsWeb) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted && _playing) {
          _setPlaying(true);
        }
      });
    }
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (_choseMotion) {
      return;
    }
    _playing = !MediaQuery.disableAnimationsOf(context);
    _choseMotion = true;
  }

  Future<void> _setPlaying(bool playing) async {
    setState(() => _playing = playing);
    final call = playing
        ? '''
            if (!mv.loaded) {
              if (tries++ < 40) setTimeout(start, 200);
              return;
            }
            const clips = mv.availableAnimations || [];
            if (clips.length) mv.animationName = clips[0];
            try { mv.currentTime = 0; } catch (e) {}
            mv.play({repetitions: Infinity});
          '''
        : 'mv.pause();';
    try {
      await _runJs('''
        (() => {
          let tries = 0;
          const start = () => {
            const mv = document.getElementById('marinesee-model');
            if (!mv || !mv.play) {
              if (tries++ < 40) setTimeout(start, 200);
              return;
            }
            $call
          };
          start();
        })();
      ''');
    } on Object {
      // The viewer may still be loading the model.
    }
  }

  @override
  Widget build(BuildContext context) {
    final ready = kIsWeb || _run != null;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        SizedBox(
          height: 320,
          child: ColoredBox(
            color: const Color(0xFF1E8C98),
            child: ModelViewer(
              id: 'marinesee-model',
              src: _src,
              loading: Loading.eager,
              alt: widget.label,
              ar: false,
              autoRotate: false,
                autoPlay: false,
              cameraControls: true,
              disableZoom: false,
              interactionPrompt: InteractionPrompt.none,
              cameraOrbit: '0deg 75deg 105%',
              backgroundColor: const Color(0xFF1E8C98),
              debugLogging: false,
              onWebViewCreated: (controller) {
                if (!mounted) {
                  return;
                }
                _run = controller.runJavaScript;
                setState(() {});
                _setPlaying(_playing);
              },
            ),
          ),
        ),
        const SizedBox(height: 12),
        DecoratedBox(
          decoration: BoxDecoration(
            color: SkyPalette.scanner.withValues(alpha: 0.55),
            borderRadius: AppRadius.card,
            border: Border.all(color: Colors.white.withValues(alpha: 0.16)),
          ),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(8, 14, 8, 10),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  '3D Controls',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 10),
                Row(
                  children: [
                    _ControlTile(
                      icon: _playing ? Icons.pause : Icons.play_arrow,
                      label: _playing ? 'Pause' : 'Play',
                      onPressed: ready ? () => _setPlaying(!_playing) : null,
                    ),
                    const SizedBox(width: 8),
                    _ControlTile(
                      icon: Icons.rotate_right,
                      label: 'Rotate',
                      onPressed: ready ? () => _nudge(thetaDeg: 40) : null,
                    ),
                    const SizedBox(width: 8),
                    _ControlTile(
                      icon: Icons.zoom_in,
                      label: 'Zoom in',
                      onPressed: ready ? () => _nudge(radiusScale: 0.82) : null,
                    ),
                    const SizedBox(width: 8),
                    _ControlTile(
                      icon: Icons.zoom_out,
                      label: 'Zoom out',
                      onPressed: ready ? () => _nudge(radiusScale: 1.22) : null,
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class _ControlTile extends StatelessWidget {
  const _ControlTile({
    required this.icon,
    required this.label,
    required this.onPressed,
  });

  final IconData icon;
  final String label;
  final VoidCallback? onPressed;

  @override
  Widget build(BuildContext context) {
    final enabled = onPressed != null;
    final color = enabled ? Colors.white : Colors.white38;

    return Expanded(
      child: Material(
        color: Colors.white.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(16),
        child: InkWell(
          onTap: onPressed,
          borderRadius: BorderRadius.circular(16),
          child: ConstrainedBox(
            constraints: const BoxConstraints(minHeight: AppTokens.tapMin),
            child: Padding(
              padding: const EdgeInsets.symmetric(vertical: 10),
              child: Column(
                children: [
                  Icon(icon, color: color),
                  const SizedBox(height: 4),
                  Text(
                    label,
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.labelMedium?.copyWith(
                      color: color,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
