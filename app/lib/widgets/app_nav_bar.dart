import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../theme/tokens.dart';

/// One lagoon dock, a wide center hump, a glowing camera.
class AppNavBar extends StatelessWidget {
  const AppNavBar({
    super.key,
    required this.onLibrary,
    required this.onCamera,
    required this.onMenu,
    this.librarySelected = false,
  });

  final VoidCallback onLibrary;
  final VoidCallback onCamera;
  final VoidCallback onMenu;
  final bool librarySelected;

  static const double tabHeight = 88;
  static const double bump = 26;
  static const double buttonSize = 56;

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    final bottom = MediaQuery.paddingOf(context).bottom;
    final height = bump + tabHeight + bottom;

    return SizedBox(
      height: height,
      child: Stack(
        clipBehavior: Clip.none,
        children: [
          Positioned.fill(
            child: CustomPaint(
              painter: _DockPainter(
                top: tokens.teal,
                bottom: tokens.brandDeep,
              ),
            ),
          ),
          Positioned(
            left: 32,
            right: 32,
            height: 44,
            bottom: 22 + bottom,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _SideItem(
                  icon: Icons.menu_book_outlined,
                  selectedIcon: Icons.menu_book,
                  label: 'Library',
                  selected: librarySelected,
                  color: tokens.onBrand,
                  onTap: onLibrary,
                ),
                _SideItem(
                  icon: Icons.menu,
                  label: 'Menu',
                  selected: false,
                  color: tokens.onBrand,
                  onTap: onMenu,
                ),
              ],
            ),
          ),
          Positioned(
            top: 8,
            left: 0,
            right: 0,
            child: Center(child: _CameraButton(onTap: onCamera)),
          ),
        ],
      ),
    );
  }
}

class _DockPainter extends CustomPainter {
  const _DockPainter({required this.top, required this.bottom});

  final Color top;
  final Color bottom;

  @override
  void paint(Canvas canvas, Size size) {
    final path = _dock(size);
    canvas.drawPath(
      path,
      Paint()
        ..shader = LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [top, bottom],
        ).createShader(Offset.zero & size),
    );
  }

  static Path _dock(Size size) {
    final w = size.width;
    final h = size.height;
    final cx = w / 2;
    const flat = AppNavBar.bump;
    const half = 92.0;
    final path = Path()..moveTo(0, flat);

    for (var x = 0.0; x <= w; x += 1) {
      final t = ((x - cx) / half).clamp(-1.0, 1.0);
      final rise = t.abs() >= 1
          ? 0.0
          : AppNavBar.bump * 0.5 * (1 + math.cos(t * math.pi));
      final y = flat - rise;
      if (x == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }

    path
      ..lineTo(w, h)
      ..lineTo(0, h)
      ..close();
    return path;
  }

  @override
  bool shouldRepaint(covariant _DockPainter oldDelegate) =>
      oldDelegate.top != top || oldDelegate.bottom != bottom;
}

class _CameraButton extends StatelessWidget {
  const _CameraButton({required this.onTap});

  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;

    return Tooltip(
      message: 'Camera',
      child: Semantics(
        button: true,
        label: 'Camera',
        child: DecoratedBox(
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            gradient: tokens.cameraGradient,
            boxShadow: [
              ...tokens.glowShadows,
              BoxShadow(color: tokens.shadow, blurRadius: 16, offset: const Offset(0, 6)),
            ],
            border: Border.all(
              color: tokens.surfaceHigh.withValues(alpha: 0.7),
              width: 2,
            ),
          ),
          child: Material(
            type: MaterialType.transparency,
            child: InkWell(
              onTap: onTap,
              customBorder: const CircleBorder(),
              child: SizedBox(
                width: AppNavBar.buttonSize,
                height: AppNavBar.buttonSize,
                child: Icon(
                  Icons.photo_camera_outlined,
                  size: 26,
                  color: tokens.onSand,
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _SideItem extends StatelessWidget {
  const _SideItem({
    required this.icon,
    required this.label,
    required this.selected,
    required this.color,
    required this.onTap,
    this.selectedIcon,
  });

  final IconData icon;
  final IconData? selectedIcon;
  final String label;
  final bool selected;
  final Color color;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Semantics(
      button: true,
      label: label,
      child: Tooltip(
        message: label,
        child: InkWell(
          onTap: onTap,
          customBorder: const CircleBorder(),
          child: SizedBox(
            width: 44,
            height: 44,
            child: Icon(
              selected ? (selectedIcon ?? icon) : icon,
              size: 22,
              color: color,
            ),
          ),
        ),
      ),
    );
  }
}
