import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';

import '../classify/classifier.dart';
import '../theme/tokens.dart';
import '../widgets/aurora_button.dart';
import 'result_screen.dart';
import 'shell_scope.dart';

class IdentifyScreen extends StatefulWidget {
  const IdentifyScreen({super.key, required this.classifier});

  final Classifier classifier;

  @override
  State<IdentifyScreen> createState() => _IdentifyScreenState();
}

class _IdentifyScreenState extends State<IdentifyScreen> {
  final _picker = ImagePicker();
  XFile? _image;
  Uint8List? _bytes;
  bool _busy = false;

  Future<void> _pick(ImageSource source) async {
    try {
      final picked = await _picker.pickImage(source: source);
      if (picked == null) {
        return;
      }
      final bytes = await picked.readAsBytes();
      setState(() {
        _image = picked;
        _bytes = bytes;
      });
    } catch (error) {
      if (!mounted) {
        return;
      }
      final message = error is PlatformException
          ? (error.message ?? 'Could not open the camera or gallery.')
          : 'Could not open the camera or gallery.';
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
    }
  }

  Future<void> _identify() async {
    final image = _image;
    if (image == null || _busy) {
      return;
    }
    setState(() => _busy = true);
    final result = await widget.classifier.identify(image);
    if (!mounted) {
      return;
    }
    setState(() => _busy = false);
    await Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) => ResultScreen(imageBytes: _bytes!, result: result),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final onWash = context.tokens.onBrand;
    final text = Theme.of(context).textTheme;

    return ColoredBox(
      color: SkyPalette.scannerDeep,
      child: SafeArea(
        bottom: false,
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 8, 16, 12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                children: [
                  _RoundButton(
                    icon: Icons.arrow_back,
                    onPressed: () =>
                        ShellScope.of(context).select(ShellTab.home),
                  ),
                  Expanded(
                    child: Text(
                      'Seagrass Scanner',
                      textAlign: TextAlign.center,
                      style: text.titleLarge?.copyWith(
                        color: onWash,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                  const SizedBox(width: 48),
                ],
              ),
              const SizedBox(height: 12),
              Expanded(child: _Viewfinder(bytes: _bytes)),
              const SizedBox(height: 12),
              DecoratedBox(
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.08),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(14),
                  child: Text(
                    'Frame a seagrass leaf, then tap Identify.',
                    textAlign: TextAlign.center,
                    style: text.bodyMedium?.copyWith(color: onWash),
                  ),
                ),
              ),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                    child: _DarkButton(
                      icon: Icons.photo_camera_outlined,
                      label: 'Camera',
                      onPressed: () => _pick(ImageSource.camera),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: _DarkButton(
                      icon: Icons.photo_library_outlined,
                      label: 'Gallery',
                      onPressed: () => _pick(ImageSource.gallery),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 10),
              AuroraButton(
                label: _busy ? 'Identifying…' : 'Identify',
                icon: Icons.center_focus_strong_outlined,
                loading: _busy,
                onPressed: _image == null || _busy ? null : _identify,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _Viewfinder extends StatelessWidget {
  const _Viewfinder({required this.bytes});

  final Uint8List? bytes;

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    final text = Theme.of(context).textTheme;

    return ClipRRect(
      borderRadius: BorderRadius.circular(24),
      child: ColoredBox(
        color: SkyPalette.scanner,
        child: Stack(
          fit: StackFit.expand,
          children: [
            if (bytes == null)
              Center(
                child: Text(
                  'No photo yet',
                  style: text.titleMedium?.copyWith(color: tokens.onBrand),
                ),
              )
            else
              Image.memory(bytes!, fit: BoxFit.cover),
            IgnorePointer(
              child: CustomPaint(
                painter: _FramePainter(color: SkyPalette.foam),
                child: const SizedBox.expand(),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _FramePainter extends CustomPainter {
  const _FramePainter({required this.color});

  final Color color;

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3
      ..strokeCap = StrokeCap.round;
    const length = 28.0;
    const inset = 16.0;
    final right = size.width - inset;
    final bottom = size.height - inset;

    final corners = <Offset, List<Offset>>{
      const Offset(inset, inset): [
        const Offset(inset + length, inset),
        const Offset(inset, inset + length),
      ],
      Offset(right, inset): [
        Offset(right - length, inset),
        Offset(right, inset + length),
      ],
      Offset(inset, bottom): [
        Offset(inset + length, bottom),
        Offset(inset, bottom - length),
      ],
      Offset(right, bottom): [
        Offset(right - length, bottom),
        Offset(right, bottom - length),
      ],
    };

    for (final entry in corners.entries) {
      for (final end in entry.value) {
        canvas.drawLine(entry.key, end, paint);
      }
    }
  }

  @override
  bool shouldRepaint(covariant _FramePainter oldDelegate) =>
      oldDelegate.color != color;
}

class _RoundButton extends StatelessWidget {
  const _RoundButton({required this.icon, required this.onPressed});

  final IconData icon;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white.withValues(alpha: 0.12),
      shape: const CircleBorder(),
      child: InkWell(
        customBorder: const CircleBorder(),
        onTap: onPressed,
        child: SizedBox(
          width: 48,
          height: 48,
          child: Icon(icon, color: context.tokens.onBrand),
        ),
      ),
    );
  }
}

class _DarkButton extends StatelessWidget {
  const _DarkButton({
    required this.icon,
    required this.label,
    required this.onPressed,
  });

  final IconData icon;
  final String label;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return FilledButton.icon(
      onPressed: onPressed,
      icon: Icon(icon),
      label: Text(label),
      style: FilledButton.styleFrom(
        backgroundColor: Colors.white.withValues(alpha: 0.1),
        foregroundColor: context.tokens.onBrand,
        minimumSize: AppTokens.tapSize,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      ),
    );
  }
}
