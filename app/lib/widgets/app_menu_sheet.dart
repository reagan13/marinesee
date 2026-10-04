import 'package:flutter/material.dart';

import '../screens/about_screen.dart';
import '../screens/models_3d_screen.dart';
import '../screens/profile_screen.dart';
import '../theme/tokens.dart';
import 'ocean_surface.dart';
import 'settings_tile.dart';

Future<void> showAppMenu(BuildContext context) {
  return showModalBottomSheet<void>(
    context: context,
    backgroundColor: Colors.transparent,
    builder: (context) => const AppMenuSheet(),
  );
}

class AppMenuSheet extends StatelessWidget {
  const AppMenuSheet({super.key});

  void _open(BuildContext context, Widget page) {
    final navigator = Navigator.of(context);
    navigator.pop();
    navigator.push(MaterialPageRoute<void>(builder: (_) => page));
  }

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    final bottom = MediaQuery.paddingOf(context).bottom;

    return Padding(
      padding: EdgeInsets.fromLTRB(16, 0, 16, 16 + bottom),
      child: OceanSurface(
        padding: const EdgeInsets.symmetric(vertical: 8),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 36,
              height: 4,
              margin: const EdgeInsets.only(bottom: 8),
              decoration: BoxDecoration(
                color: tokens.borderStrong,
                borderRadius: BorderRadius.circular(AppRadius.pill),
              ),
            ),
            SettingsTile(
              icon: Icons.view_in_ar_outlined,
              label: '3D models',
              subtitle: 'Playback placeholder for each species',
              onTap: () => _open(context, const Models3dScreen()),
            ),
            SettingsTile(
              icon: Icons.info_outline,
              label: 'About',
              subtitle: 'Study, device, and conservation',
              onTap: () => _open(context, const AboutScreen()),
            ),
            SettingsTile(
              icon: Icons.person_outline,
              label: 'Profile',
              subtitle: 'Photo, first name, last name',
              onTap: () => _open(context, const ProfileScreen()),
            ),
          ],
        ),
      ),
    );
  }
}
