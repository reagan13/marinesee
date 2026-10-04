import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:wave/wave.dart';

import '../theme/tokens.dart';

/// Lagoon wash: sun or moon, drifting caustics, one loop of water.
class AuroraAtmosphere extends StatefulWidget {
  const AuroraAtmosphere({super.key});

  @override
  State<AuroraAtmosphere> createState() => _AuroraAtmosphereState();
}

class _AuroraAtmosphereState extends State<AuroraAtmosphere>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: AppMotion.aurora,
    );
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final animate = !MediaQuery.disableAnimationsOf(context);
    if (animate && !_controller.isAnimating) {
      _controller.repeat(reverse: true);
    } else if (!animate && _controller.isAnimating) {
      _controller.stop();
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final animate = !MediaQuery.disableAnimationsOf(context);
    final tokens = context.tokens;

    return IgnorePointer(
      child: Stack(
        fit: StackFit.expand,
        children: [
          DecoratedBox(
            decoration: BoxDecoration(gradient: tokens.depthGradient),
          ),
          AnimatedBuilder(
            animation: _controller,
            builder: (context, _) {
              final t = animate ? _controller.value : 0.35;
              return CustomPaint(
                painter: _AuroraPainter(t: t, tokens: tokens),
                child: const SizedBox.expand(),
              );
            },
          ),
          Align(
            alignment: Alignment.bottomCenter,
            child: SizedBox(
              height: 200,
              width: double.infinity,
              child: _OceanWaves(tokens: tokens, animate: animate),
            ),
          ),
        ],
      ),
    );
  }
}

class _OceanWaves extends StatelessWidget {
  const _OceanWaves({required this.tokens, required this.animate});

  final AppTokens tokens;
  final bool animate;

  @override
  Widget build(BuildContext context) {
    final colors = tokens.isLight
        ? [
            tokens.cyan.withValues(alpha: 0.34),
            tokens.navy.withValues(alpha: 0.42),
            tokens.teal.withValues(alpha: 0.28),
          ]
        : [
            tokens.cyan.withValues(alpha: 0.22),
            tokens.brand.withValues(alpha: 0.16),
            tokens.navy.withValues(alpha: 0.62),
          ];

    return WaveWidget(
      config: CustomConfig(
        colors: colors,
        durations: const [16000, 22000, 30000],
        heightPercentages: const [0.36, 0.48, 0.58],
        blur: const MaskFilter.blur(BlurStyle.normal, 10),
      ),
      size: const Size(double.infinity, double.infinity),
      waveAmplitude: 14,
      waveFrequency: 1.15,
      isLoop: animate,
    );
  }
}

class _AuroraPainter extends CustomPainter {
  const _AuroraPainter({required this.t, required this.tokens});

  final double t;
  final AppTokens tokens;

  @override
  void paint(Canvas canvas, Size size) {
    if (tokens.isLight) {
      _paintDay(canvas, size);
    } else {
      _paintNight(canvas, size);
    }
    _paintCaustics(canvas, size);
  }

  void _paintDay(Canvas canvas, Size size) {
    _blob(
      canvas,
      Offset(size.width * (0.78 - 0.03 * t), size.height * (0.10 + 0.02 * t)),
      size.shortestSide * 0.42,
      tokens.sun.withValues(alpha: 0.55),
    );
    _blob(
      canvas,
      Offset(size.width * (0.78 - 0.03 * t), size.height * (0.10 + 0.02 * t)),
      size.shortestSide * 0.18,
      tokens.sun.withValues(alpha: 0.9),
    );
    _blob(
      canvas,
      Offset(size.width * (0.18 + 0.03 * t), size.height * 0.22),
      size.shortestSide * 0.7,
      tokens.surfaceHigh.withValues(alpha: tokens.auraViolet),
    );
    _blob(
      canvas,
      Offset(size.width * 0.5, size.height * 0.92),
      size.shortestSide * 1.05,
      tokens.cyan.withValues(alpha: tokens.auraTeal),
    );
  }

  void _paintNight(Canvas canvas, Size size) {
    _blob(
      canvas,
      Offset(size.width * (0.22 + 0.04 * t), size.height * 0.10),
      size.shortestSide * 0.28,
      tokens.ink.withValues(alpha: 0.14),
    );
    _blob(
      canvas,
      Offset(size.width * (0.76 - 0.04 * t), size.height * 0.18),
      size.shortestSide * 0.72,
      tokens.cyan.withValues(alpha: tokens.auraCyan),
    );
    _blob(
      canvas,
      Offset(size.width * 0.5, size.height * 0.90),
      size.shortestSide * 1.05,
      tokens.brand.withValues(alpha: tokens.auraTeal),
    );
  }

  void _paintCaustics(Canvas canvas, Size size) {
    final paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = tokens.isLight ? 1.3 : 1.1
      ..color = tokens.cyan.withValues(alpha: tokens.isLight ? 0.18 : 0.14);
    final bands = 6;
    for (var i = 0; i < bands; i++) {
      final path = Path();
      final y0 = size.height * (0.28 + i * 0.09);
      path.moveTo(0, y0);
      for (var x = 0.0; x <= size.width; x += 10) {
        final phase = (x / size.width) * math.pi * 2.4 + t * math.pi * 2 + i * 0.7;
        final y = y0 + math.sin(phase) * (7.0 + i);
        path.lineTo(x, y);
      }
      canvas.drawPath(path, paint);
    }
  }

  void _blob(Canvas canvas, Offset center, double radius, Color color) {
    final paint = Paint()
      ..shader = RadialGradient(
        colors: [color, color.withValues(alpha: 0)],
      ).createShader(Rect.fromCircle(center: center, radius: radius));
    canvas.drawCircle(center, radius, paint);
  }

  @override
  bool shouldRepaint(covariant _AuroraPainter oldDelegate) =>
      oldDelegate.t != t || oldDelegate.tokens.style != tokens.style;
}
