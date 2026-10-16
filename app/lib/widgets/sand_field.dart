import 'dart:math' as math;
import 'dart:ui' as ui;

import 'package:flutter/material.dart';

import '../theme/tokens.dart';

/// Dry beach under every page. Grain is painted once and reused.
class SandField extends StatelessWidget {
  const SandField({super.key});

  @override
  Widget build(BuildContext context) {
    return const RepaintBoundary(
      child: CustomPaint(
        painter: _SandPainter(),
        child: SizedBox.expand(),
      ),
    );
  }
}

class _SandPainter extends CustomPainter {
  const _SandPainter();

  static ui.Picture? _picture;
  static Size? _size;

  @override
  void paint(Canvas canvas, Size size) {
    if (size.isEmpty) {
      return;
    }
    final cached = _size;
    final same = cached != null &&
        (cached.width - size.width).abs() < 1 &&
        (cached.height - size.height).abs() < 1;
    if (!same || _picture == null) {
      _picture?.dispose();
      final recorder = ui.PictureRecorder();
      _draw(Canvas(recorder), size);
      _picture = recorder.endRecording();
      _size = size;
    }
    canvas.drawPicture(_picture!);
  }

  void _draw(Canvas canvas, Size size) {
    final rect = Offset.zero & size;
    canvas.drawRect(
      rect,
      Paint()
        ..shader = const LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [SkyPalette.sandLight, SkyPalette.sand, Color(0xFFE4C896)],
          stops: [0, 0.35, 1],
        ).createShader(rect),
    );

    final random = math.Random(4);
    final mound = Paint()..maskFilter = const MaskFilter.blur(BlurStyle.normal, 22);
    for (var i = 0; i < 14; i++) {
      mound.color = (i.isEven ? SkyPalette.sandDeep : SkyPalette.sandLight)
          .withValues(alpha: 0.09);
      canvas.drawOval(
        Rect.fromCenter(
          center: Offset(
            random.nextDouble() * size.width,
            random.nextDouble() * size.height,
          ),
          width: 70 + random.nextDouble() * 160,
          height: 28 + random.nextDouble() * 48,
        ),
        mound,
      );
    }

    final grain = Paint();
    final count = (size.width * size.height / 700).clamp(900, 2800).round();
    for (var i = 0; i < count; i++) {
      final roll = random.nextDouble();
      grain.color = roll < 0.2
          ? SkyPalette.sandDeep.withValues(alpha: 0.28)
          : roll < 0.45
          ? const Color(0xFFB8894E).withValues(alpha: 0.22)
          : SkyPalette.sandLight.withValues(alpha: 0.55);
      final center = Offset(
        random.nextDouble() * size.width,
        random.nextDouble() * size.height,
      );
      canvas.drawOval(
        Rect.fromCenter(
          center: center,
          width: 1.1 + random.nextDouble() * 2.6,
          height: 0.7 + random.nextDouble() * 1.3,
        ),
        grain,
      );
    }
  }

  @override
  bool shouldRepaint(covariant _SandPainter oldDelegate) => false;
}
