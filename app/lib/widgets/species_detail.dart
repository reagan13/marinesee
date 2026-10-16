import 'package:flutter/material.dart';

import '../data/species.dart';
import '../theme/tokens.dart';
import 'ocean_surface.dart';

class SpeciesHero extends StatelessWidget {
  const SpeciesHero({
    super.key,
    required this.onBack,
    required this.onView3d,
    this.stillAsset,
  });

  final String? stillAsset;
  final VoidCallback onBack;
  final VoidCallback onView3d;

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;

    return SizedBox(
      height: 320,
      child: Stack(
        fit: StackFit.expand,
        children: [
          stillAsset == null
              ? ColoredBox(
                  color: tokens.brand,
                  child: Center(
                    child: Icon(
                      Icons.spa_outlined,
                      size: 48,
                      color: tokens.onBrand,
                    ),
                  ),
                )
              : Image.asset(
                  stillAsset!,
                  fit: BoxFit.cover,
                  errorBuilder: (_, _, _) => ColoredBox(
                    color: tokens.brand,
                    child: Center(
                      child: Icon(Icons.spa_outlined, color: tokens.onBrand),
                    ),
                  ),
                ),
          const DecoratedBox(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [Color(0x66000000), Color(0x00000000), Color(0x33000000)],
                stops: [0, 0.4, 1],
              ),
            ),
          ),
          Positioned(
            top: 8,
            left: 12,
            child: SafeArea(
              bottom: false,
              child: _CircleButton(icon: Icons.arrow_back, onPressed: onBack),
            ),
          ),
          Positioned(
            right: 16,
            bottom: 48,
            child: FilledButton.icon(
              onPressed: onView3d,
              icon: const Icon(Icons.open_in_full, size: 18),
              label: const Text('View in 3D'),
              style: FilledButton.styleFrom(
                backgroundColor: tokens.brand,
                foregroundColor: tokens.onBrand,
                minimumSize: const Size(48, 48),
                shape: const StadiumBorder(),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class SpeciesNameCard extends StatelessWidget {
  const SpeciesNameCard({super.key, required this.species});

  final Species species;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final tokens = context.tokens;

    return OceanSurface(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  species.scientificName,
                  style: text.headlineSmall?.copyWith(
                    fontStyle: FontStyle.italic,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 4),
                Text(species.commonName, style: text.titleMedium),
              ],
            ),
          ),
          Icon(Icons.spa_outlined, color: tokens.brand, size: 28),
        ],
      ),
    );
  }
}

class SpeciesFactCard extends StatelessWidget {
  const SpeciesFactCard({
    super.key,
    required this.icon,
    required this.title,
    required this.value,
  });

  final IconData icon;
  final String title;
  final String value;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final tokens = context.tokens;

    return OceanSurface(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: tokens.brand, size: 20),
              const SizedBox(width: 8),
              Expanded(child: Text(title, style: text.titleMedium)),
            ],
          ),
          const SizedBox(height: 8),
          Text(value, style: text.bodyLarge),
        ],
      ),
    );
  }
}

class _CircleButton extends StatelessWidget {
  const _CircleButton({required this.icon, required this.onPressed});

  final IconData icon;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white.withValues(alpha: 0.88),
      shape: const CircleBorder(),
      child: InkWell(
        customBorder: const CircleBorder(),
        onTap: onPressed,
        child: SizedBox(
          width: 48,
          height: 48,
          child: Icon(icon, color: SkyPalette.ink),
        ),
      ),
    );
  }
}
