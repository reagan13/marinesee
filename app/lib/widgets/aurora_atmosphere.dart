import 'package:flutter/material.dart';

import '../theme/tokens.dart';

/// Quiet page fill behind every screen.
class AuroraAtmosphere extends StatelessWidget {
  const AuroraAtmosphere({super.key});

  @override
  Widget build(BuildContext context) {
    return const ColoredBox(
      color: SkyPalette.page,
      child: SizedBox.expand(),
    );
  }
}
