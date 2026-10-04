import 'package:flutter/material.dart';

import '../widgets/icon_well.dart';
import '../widgets/ocean_layout.dart';
import '../widgets/ocean_surface.dart';
import '../widgets/page_hero.dart';

class AboutScreen extends StatelessWidget {
  const AboutScreen({super.key});

  static const _conservation =
      'Learning the nine documented Mati City seagrass species supports local marine-biodiversity awareness.';

  @override
  Widget build(BuildContext context) {
    final body = Theme.of(context).textTheme.bodyLarge;

    return OceanScaffold(
      title: 'About',
      body: OceanPage(
        children: [
          const PageHero(
            kicker: 'STUDY',
            title: 'Nine local species',
            subtitle:
                'A seagrass education app for Mati City, Davao Oriental. Identification uses an SVM. English only.',
            icon: Icons.menu_book_outlined,
          ),
          const SizedBox(height: 20),
          OceanSurface(
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const IconWell(icon: Icons.phone_android),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'On this device',
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                      const SizedBox(height: 6),
                      Text(
                        'Needs Android 8.0 or newer and at least 3 GB RAM. Use a physical phone. Do not use the Android emulator on the study laptop.',
                        style: body,
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),
          OceanSurface(
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const IconWell(icon: Icons.waves_outlined),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Why it matters',
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                      const SizedBox(height: 6),
                      Text(_conservation, style: body),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
