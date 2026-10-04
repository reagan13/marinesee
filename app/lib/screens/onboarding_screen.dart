import 'package:flutter/material.dart';

import '../data/onboarding.dart';
import '../theme/tokens.dart';
import '../widgets/aurora_atmosphere.dart';
import '../widgets/aurora_button.dart';

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key, required this.onDone});

  final VoidCallback onDone;

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  final _pages = PageController();
  var _index = 0;

  bool get _last => _index == onboardingSlides.length - 1;

  void _next() {
    if (_last) {
      widget.onDone();
      return;
    }
    _pages.nextPage(duration: AppMotion.medium, curve: AppMotion.ease);
  }

  @override
  void dispose() {
    _pages.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    final text = Theme.of(context).textTheme;

    return Stack(
      fit: StackFit.expand,
      children: [
        const AuroraAtmosphere(),
        SafeArea(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(24, 4, 24, 20),
            child: Column(
              children: [
                Align(
                  alignment: Alignment.centerRight,
                  child: TextButton(
                    onPressed: widget.onDone,
                    child: const Text('Skip'),
                  ),
                ),
                Expanded(
                  child: PageView.builder(
                    controller: _pages,
                    itemCount: onboardingSlides.length,
                    onPageChanged: (value) => setState(() => _index = value),
                    itemBuilder: (context, index) {
                      final slide = onboardingSlides[index];
                      return Column(
                        children: [
                          Expanded(
                            child: _HeroPhoto(slide: slide),
                          ),
                          const SizedBox(height: 32),
                          Text(
                            slide.title,
                            textAlign: TextAlign.center,
                            style: text.displaySmall,
                          ),
                          const SizedBox(height: 12),
                          Text(
                            slide.body,
                            textAlign: TextAlign.center,
                            style: text.bodyLarge?.copyWith(
                              color: tokens.inkMuted,
                            ),
                          ),
                        ],
                      );
                    },
                  ),
                ),
                const SizedBox(height: 24),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    for (var i = 0; i < onboardingSlides.length; i++)
                      AnimatedContainer(
                        duration: AppMotion.fast,
                        margin: const EdgeInsets.symmetric(horizontal: 4),
                        height: 8,
                        width: i == _index ? 22 : 8,
                        decoration: BoxDecoration(
                          color: i == _index ? tokens.brand : tokens.navy,
                          borderRadius: BorderRadius.circular(AppRadius.pill),
                        ),
                      ),
                  ],
                ),
                const SizedBox(height: 20),
                AuroraButton(
                  label: _last ? 'Get started' : 'Next',
                  onPressed: _next,
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class _HeroPhoto extends StatelessWidget {
  const _HeroPhoto({required this.slide});

  final OnboardingSlide slide;

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;

    return DecoratedBox(
      decoration: BoxDecoration(
        color: tokens.surfaceHigh,
        borderRadius: BorderRadius.circular(AppRadius.xl),
        border: Border.all(color: tokens.border),
        boxShadow: tokens.cardShadows,
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(AppRadius.xl),
        child: Image.asset(
          slide.imageAsset,
          fit: BoxFit.cover,
          width: double.infinity,
          errorBuilder: (context, error, stackTrace) {
            return ColoredBox(
              color: tokens.surfaceHigh,
              child: Center(
                child: Icon(slide.icon, size: 72, color: tokens.brand),
              ),
            );
          },
        ),
      ),
    );
  }
}
