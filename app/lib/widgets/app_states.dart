import 'package:flutter/material.dart';

import '../theme/tokens.dart';
import 'aurora_button.dart';
import 'ocean_surface.dart';

class OceanLoading extends StatefulWidget {
  const OceanLoading({super.key, this.label});

  final String? label;

  @override
  State<OceanLoading> createState() => _OceanLoadingState();
}

class _OceanLoadingState extends State<OceanLoading>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1600),
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

    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpace.lg),
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 360),
          child: OceanSurface(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                AnimatedBuilder(
                  animation: _controller,
                  builder: (context, child) {
                    final pulse = animate ? 0.45 + (_controller.value * 0.55) : 0.7;
                    return Container(
                      width: 72,
                      height: 72,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        boxShadow: [
                          BoxShadow(
                            color: context.tokens.cyan.withValues(
                              alpha: 0.18 * pulse,
                            ),
                            blurRadius: 28,
                          ),
                        ],
                      ),
                      child: child,
                    );
                  },
                  child: const Center(
                    child: SizedBox(
                      width: 28,
                      height: 28,
                      child: CircularProgressIndicator(strokeWidth: 2.4),
                    ),
                  ),
                ),
                if (widget.label != null) ...[
                  const SizedBox(height: 16),
                  Text(
                    widget.label!,
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class OceanEmpty extends StatelessWidget {
  const OceanEmpty({
    super.key,
    required this.icon,
    required this.title,
    this.message,
  });

  final IconData icon;
  final String title;
  final String? message;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;

    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpace.lg),
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 360),
          child: OceanSurface(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                _AuraIcon(icon: icon, color: context.tokens.cyan),
                const SizedBox(height: 16),
                Text(title, textAlign: TextAlign.center, style: text.titleMedium),
                if (message != null) ...[
                  const SizedBox(height: 8),
                  Text(
                    message!,
                    textAlign: TextAlign.center,
                    style: text.bodyMedium,
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class OceanError extends StatelessWidget {
  const OceanError({
    super.key,
    required this.message,
    this.onRetry,
  });

  final String message;
  final VoidCallback? onRetry;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;

    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpace.lg),
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 360),
          child: OceanSurface(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                _AuraIcon(icon: Icons.error_outline, color: context.tokens.danger),
                const SizedBox(height: 16),
                Text(
                  'Something went wrong',
                  textAlign: TextAlign.center,
                  style: text.titleMedium,
                ),
                const SizedBox(height: 8),
                Text(
                  message,
                  textAlign: TextAlign.center,
                  style: text.bodyMedium,
                ),
                if (onRetry != null) ...[
                  const SizedBox(height: 20),
                  AuroraButton(
                    label: 'Try again',
                    icon: Icons.refresh,
                    onPressed: onRetry,
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _AuraIcon extends StatelessWidget {
  const _AuraIcon({required this.icon, required this.color});

  final IconData icon;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 72,
      height: 72,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: color.withValues(alpha: 0.12),
        boxShadow: [
          BoxShadow(color: color.withValues(alpha: 0.16), blurRadius: 24),
        ],
      ),
      child: Icon(icon, size: 30, color: color),
    );
  }
}
