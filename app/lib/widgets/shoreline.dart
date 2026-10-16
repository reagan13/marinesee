import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../theme/tokens.dart';

/// Sky, shallow water, and foam that washes onto the sand behind [child].
///
/// The dry beach itself is [SandField]. This painter only covers the mast,
/// and its lower edge fades so the grain shows through the wet sand.
class BeachMast extends StatefulWidget {
  const BeachMast({super.key, required this.child});

  final Widget child;

  @override
  State<BeachMast> createState() => _BeachMastState();
}

class _BeachMastState extends State<BeachMast>
    with SingleTickerProviderStateMixin {
  static const seaDepth = 164.0;

  late final AnimationController _motion;

  @override
  void initState() {
    super.initState();
    _motion = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 16),
    );
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final reduce = MediaQuery.disableAnimationsOf(context);
    if (reduce) {
      _motion.stop();
    } else if (!_motion.isAnimating) {
      _motion.repeat();
    }
  }

  @override
  void dispose() {
    _motion.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final reduce = MediaQuery.disableAnimationsOf(context);

    return AnimatedBuilder(
      animation: _motion,
      builder: (context, child) {
        return CustomPaint(
          painter: _BeachPainter(
            phase: reduce ? 0.35 : _motion.value,
            still: reduce,
          ),
          child: Padding(
            padding: const EdgeInsets.only(bottom: seaDepth),
            child: child,
          ),
        );
      },
      child: widget.child,
    );
  }
}

class _Bubble {
  const _Bubble(this.x, this.radius, this.hold);

  final double x;
  final double radius;
  final double hold;
}

const _bubbleSpecs = <_Bubble>[
  _Bubble(0.12, 3.5, 0.15),
  _Bubble(0.28, 5.5, 0.62),
  _Bubble(0.44, 3.0, 0.33),
  _Bubble(0.58, 4.5, 0.8),
  _Bubble(0.73, 6.0, 0.22),
  _Bubble(0.88, 3.2, 0.5),
];

class _BeachPainter extends CustomPainter {
  const _BeachPainter({required this.phase, required this.still});

  final double phase;
  final bool still;

  static const _sea = 164.0;

  @override
  void paint(Canvas canvas, Size size) {
    if (size.height < 80) {
      return;
    }
    final seaTop = math.max(36.0, size.height - _sea);
    final horizon = Color.lerp(SkyPalette.sky, const Color(0xFFFFFFFF), 0.55)!;
    final shallows = Color.lerp(SkyPalette.water, const Color(0xFFFFFFFF), 0.34)!;

    _sky(canvas, size, seaTop, horizon);
    final shore = _shoreline(size, seaTop + 96);
    _water(canvas, size, seaTop, shore, horizon, shallows);
    _bubbles(canvas, size, seaTop, shore);
    _wetSand(canvas, size, shore);
    _foam(canvas, size, shore);
  }

  void _sky(Canvas canvas, Size size, double seaTop, Color horizon) {
    final rect = Rect.fromLTWH(0, 0, size.width, seaTop + 18);
    canvas.drawRect(
      rect,
      Paint()
        ..shader = LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [SkyPalette.skyDeep, SkyPalette.sky, horizon],
          stops: const [0, 0.62, 1],
        ).createShader(rect),
    );
  }

  void _water(
    Canvas canvas,
    Size size,
    double seaTop,
    List<Offset> shore,
    Color horizon,
    Color shallows,
  ) {
    final path = Path()..moveTo(0, seaTop);
    path.lineTo(size.width, seaTop);
    for (var i = shore.length - 1; i >= 0; i--) {
      path.lineTo(shore[i].dx, shore[i].dy);
    }
    path.close();

    final rect = Rect.fromLTWH(0, seaTop - 8, size.width, 130);
    canvas.save();
    canvas.clipPath(path);
    canvas.drawRect(
      rect,
      Paint()
        ..shader = LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [
            Color.lerp(horizon, SkyPalette.waterDeep, 0.2)!,
            SkyPalette.waterDeep,
            SkyPalette.water,
            shallows,
          ],
          stops: const [0, 0.28, 0.7, 1],
        ).createShader(rect),
    );
    _ripples(canvas, size, seaTop);
    canvas.restore();
  }

  void _ripples(Canvas canvas, Size size, double seaTop) {
    final paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2
      ..color = const Color(0x38FFFFFF);
    for (var band = 0; band < 3; band++) {
      final path = Path();
      final base = seaTop + 28 + band * 22;
      for (var x = 0.0; x <= size.width; x += 4) {
        final y = base + _swell(x, size.width, amp: 2.2, freq: 1.4 + band * 0.3, turns: 1);
        if (x == 0) {
          path.moveTo(x, y);
        } else {
          path.lineTo(x, y);
        }
      }
      canvas.drawPath(path, paint);
    }
  }

  void _bubbles(Canvas canvas, Size size, double seaTop, List<Offset> shore) {
    canvas.save();
    canvas.clipRect(Rect.fromLTWH(0, seaTop + 8, size.width, 78));
    for (final bubble in _bubbleSpecs) {
      final travel = still ? bubble.hold : (phase + bubble.hold) % 1;
      final y = seaTop + 70 - travel * 52;
      final drift = still ? 0.0 : math.sin((phase + bubble.hold) * math.pi * 2) * 5;
      final center = Offset(bubble.x * size.width + drift, y);
      final shoreY = _sampleShore(shore, center.dx);
      if (center.dy > shoreY - 14) {
        continue;
      }
      final fade = still ? 0.7 : math.sin(travel * math.pi).clamp(0.0, 1.0);
      if (fade < 0.04) {
        continue;
      }
      canvas.drawCircle(
        center,
        bubble.radius,
        Paint()..color = const Color(0x66FFFFFF).withValues(alpha: 0.4 * fade),
      );
      canvas.drawCircle(
        center,
        bubble.radius,
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = 1.2
          ..color = const Color(0xFFFFFFFF).withValues(alpha: 0.85 * fade),
      );
    }
    canvas.restore();
  }

  void _wetSand(Canvas canvas, Size size, List<Offset> shore) {
    final path = Path()..moveTo(shore.first.dx, shore.first.dy);
    for (final point in shore.skip(1)) {
      path.lineTo(point.dx, point.dy);
    }
    path.lineTo(size.width, size.height);
    path.lineTo(0, size.height);
    path.close();

    final rect = Rect.fromLTWH(0, shore.first.dy - 8, size.width, size.height);
    canvas.drawPath(
      path,
      Paint()
        ..shader = LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [
            const Color(0x88644528),
            const Color(0x554E3518),
            const Color(0x00000000),
          ],
          stops: const [0, 0.42, 1],
        ).createShader(rect),
    );

    final sheen = Path();
    var moved = false;
    for (final point in shore) {
      final y = point.dy + 10 + _swell(point.dx, size.width, amp: 2, freq: 3.2, turns: 2);
      if (!moved) {
        sheen.moveTo(point.dx, y);
        moved = true;
      } else {
        sheen.lineTo(point.dx, y);
      }
    }
    canvas.drawPath(
      sheen,
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 8
        ..strokeCap = StrokeCap.round
        ..color = const Color(0x33FFFFFF)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 4),
    );
  }

  void _foam(Canvas canvas, Size size, List<Offset> shore) {
    final lip = Path()..moveTo(shore.first.dx, shore.first.dy);
    for (final point in shore.skip(1)) {
      lip.lineTo(point.dx, point.dy);
    }
    for (var i = shore.length - 1; i >= 0; i--) {
      final toe = shore[i].dy + 18 + _swell(
        shore[i].dx,
        size.width,
        amp: 7,
        freq: 4.6,
        turns: 2,
        shift: 0.2,
      );
      lip.lineTo(shore[i].dx, toe);
    }
    lip.close();
    canvas.drawPath(lip, Paint()..color = const Color(0xF7FFFFFF));

    final wash = Path()..moveTo(-4, shore.first.dy + 16);
    for (final point in shore) {
      wash.lineTo(
        point.dx,
        point.dy + 16 + _swell(point.dx, size.width, amp: 3, freq: 2.4, turns: 1),
      );
    }
    for (var x = size.width; x >= -4; x -= 4) {
      wash.lineTo(
        x,
        _sampleShore(shore, x) + 34 + _swell(x, size.width, amp: 9, freq: 5.5, turns: 2, shift: 0.4),
      );
    }
    wash.close();
    canvas.drawPath(
      wash,
      Paint()
        ..color = const Color(0x99FFFFFF)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 5),
    );

    final crest = Path();
    for (var i = 0; i < shore.length; i++) {
      if (i == 0) {
        crest.moveTo(shore[i].dx, shore[i].dy);
      } else {
        crest.lineTo(shore[i].dx, shore[i].dy);
      }
    }
    canvas.drawPath(
      crest,
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 3
        ..strokeCap = StrokeCap.round
        ..color = const Color(0xFFFFFFFF),
    );
    canvas.drawPath(
      crest,
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 8
        ..color = const Color(0x66FFFFFF)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 3),
    );
  }

  List<Offset> _shoreline(Size size, double base) {
    final points = <Offset>[];
    for (var x = -8.0; x <= size.width + 8; x += 3) {
      points.add(Offset(x, base + _swell(x, size.width, amp: 8, freq: 1.35, turns: 1)));
    }
    return points;
  }

  double _sampleShore(List<Offset> shore, double x) {
    var nearest = shore.first.dy;
    var best = double.infinity;
    for (final point in shore) {
      final gap = (point.dx - x).abs();
      if (gap < best) {
        best = gap;
        nearest = point.dy;
      }
    }
    return nearest;
  }

  double _swell(
    double x,
    double width, {
    required double amp,
    required double freq,
    required int turns,
    double shift = 0,
  }) {
    final u = width == 0 ? 0.0 : x / width;
    final time = still ? 0.35 : phase;
    final primary = math.sin((u * freq + time * turns + shift) * math.pi * 2);
    final detail = math.sin((u * freq * 2.2 + time * turns + shift * 1.6) * math.pi * 2);
    return primary * amp + detail * amp * 0.32;
  }

  @override
  bool shouldRepaint(covariant _BeachPainter oldDelegate) {
    return oldDelegate.phase != phase || oldDelegate.still != still;
  }
}
