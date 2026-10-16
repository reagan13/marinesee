import 'package:flutter/material.dart';

import '../theme/tokens.dart';
import '../widgets/ocean_layout.dart';
import '../widgets/ocean_surface.dart';
import '../widgets/wash_title.dart';
import 'shell_scope.dart';

/// Short FR-7 note. Uncited claims stay with the adviser.
class ConservationScreen extends StatelessWidget {
  const ConservationScreen({super.key});

  static const whyItMatters =
      'Learning the nine documented Mati City seagrass species supports local marine-biodiversity awareness.';

  static const uncited = 'TBD — adviser source';

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final tokens = context.tokens;

    return OceanScaffold(
      atmosphere: false,
      header: WashTitle(
        title: 'Conservation',
        subtitle: 'Mati City',
        onBack: () => ShellScope.of(context).select(ShellTab.home),
      ),
      body: OceanPage(
        children: [
          Text('Why seagrass matters', style: text.titleLarge),
          const SizedBox(height: 12),
          OceanSurface(
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 48,
                  height: 48,
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    color: tokens.brand,
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Icon(Icons.spa_outlined, color: tokens.onBrand),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(whyItMatters, style: text.bodyLarge),
                      const SizedBox(height: 12),
                      Text(
                        'Habitat, sediment, and nursery claims',
                        style: text.titleSmall?.copyWith(color: tokens.inkMuted),
                      ),
                      const SizedBox(height: 6),
                      Text(uncited, style: text.bodyLarge),
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
