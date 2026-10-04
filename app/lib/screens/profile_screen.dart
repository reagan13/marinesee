import 'package:flutter/material.dart';

import '../data/profile_controller.dart';
import '../theme/theme_controller.dart';
import '../theme/tokens.dart';
import '../widgets/ocean_layout.dart';
import '../widgets/ocean_surface.dart';
import '../widgets/profile_avatar.dart';
import '../widgets/settings_tile.dart';
import 'profile_settings_screen.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  void _openSettings(BuildContext context) {
    Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) => const ProfileSettingsScreen(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final profile = ProfileScope.of(context);
    final theme = ThemeScope.of(context);
    final light = theme.isLight;
    final text = Theme.of(context).textTheme;
    final tokens = context.tokens;

    return OceanScaffold(
      title: 'Profile',
      body: OceanPage(
        children: [
          OceanSurface(
            glow: true,
            child: Column(
              children: [
                ProfileAvatar(
                  initials: profile.initials,
                  photoBytes: profile.photoBytes,
                  size: 96,
                  onTap: () => _openSettings(context),
                ),
                const SizedBox(height: 16),
                Text(
                  profile.displayName,
                  textAlign: TextAlign.center,
                  style: text.headlineSmall,
                ),
                const SizedBox(height: 4),
                Text(
                  profile.hasName
                      ? '${profile.firstName} ${profile.lastName}'.trim()
                      : 'Add your first and last name',
                  textAlign: TextAlign.center,
                  style: text.bodyMedium,
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          OceanSurface(
            padding: EdgeInsets.zero,
            child: Column(
              children: [
                SettingsTile(
                  icon: Icons.manage_accounts_outlined,
                  label: 'Profile settings',
                  subtitle: 'Photo, first name, last name',
                  onTap: () => _openSettings(context),
                ),
                const OceanDivider(),
                SettingsTile(
                  icon: light
                      ? Icons.dark_mode_outlined
                      : Icons.wb_sunny_outlined,
                  label: 'Appearance',
                  subtitle: light
                      ? 'Lagoon by day. Switch to night reef.'
                      : 'Night reef. Switch to day lagoon.',
                  onTap: theme.toggle,
                  trailing: Switch(
                    value: !light,
                    onChanged: (_) => theme.toggle(),
                    activeThumbColor: tokens.onBrand,
                    activeTrackColor: tokens.brand,
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
