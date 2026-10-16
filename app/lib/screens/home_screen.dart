import 'package:flutter/material.dart';

import '../data/model_3d_library.dart';
import '../data/profile_controller.dart';
import '../data/species.dart';
import '../data/species_catalog.dart';
import '../theme/tokens.dart';
import '../widgets/app_search_field.dart';
import '../widgets/ocean_surface.dart';
import 'shell_scope.dart';
import 'species_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late final Future<_Featured> _future = _load();

  Future<_Featured> _load() async {
    final items = await speciesCatalog.all();
    if (items.isEmpty) {
      return const _Featured();
    }
    final species = items.first;
    final media = await Model3dLibrary.resolve(species.slug);
    return _Featured(species: species, stillAsset: media.stillAsset);
  }

  void _open(int tab) => ShellScope.of(context).select(tab);

  @override
  Widget build(BuildContext context) {
    final profile = ProfileScope.of(context);
    final width = MediaQuery.sizeOf(context).width;
    final horizontal = width >= 768 ? 32.0 : 20.0;

    return ListView(
      padding: const EdgeInsets.only(bottom: 28),
      children: [
        ClipRRect(
          borderRadius: const BorderRadius.vertical(
            bottom: Radius.circular(32),
          ),
          child: DecoratedBox(
            decoration: BoxDecoration(gradient: context.tokens.headerGradient),
            child: _HomeSky(
              name: profile.displayName,
              horizontal: horizontal,
              onSearch: () => _open(ShellTab.library),
              onProfile: () => _open(ShellTab.profile),
            ),
          ),
        ),
        Transform.translate(
          offset: const Offset(0, -40),
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: horizontal),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                _ActionRow(onOpen: _open),
                const SizedBox(height: 22),
                _FeaturedHeader(onViewAll: () => _open(ShellTab.library)),
                const SizedBox(height: 8),
                FutureBuilder<_Featured>(
                  future: _future,
                  builder: (context, snapshot) {
                    final featured = snapshot.data;
                    if (featured?.species == null) {
                      return const SizedBox(height: 48);
                    }
                    return _FeaturedCard(
                      species: featured!.species!,
                      stillAsset: featured.stillAsset,
                    );
                  },
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class _HomeSky extends StatelessWidget {
  const _HomeSky({
    required this.name,
    required this.horizontal,
    required this.onSearch,
    required this.onProfile,
  });

  final String name;
  final double horizontal;
  final VoidCallback onSearch;
  final VoidCallback onProfile;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final initial = name.trim().isEmpty ? 'G' : name.trim()[0].toUpperCase();

    return SafeArea(
      bottom: false,
      child: Padding(
        padding: EdgeInsets.fromLTRB(horizontal, 8, horizontal, 52),
        child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                children: [
                  _FoamMark(
                    child: Text(
                      initial,
                      style: text.titleMedium?.copyWith(
                        color: SkyPalette.primary,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Welcome back,',
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: text.bodyMedium?.copyWith(
                            color: SkyPalette.onHeader,
                          ),
                        ),
                        Text(
                          name,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: text.headlineSmall?.copyWith(
                            color: SkyPalette.onHeader,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                        Text(
                          'Mati City',
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: text.bodySmall?.copyWith(
                            color: SkyPalette.onHeader,
                          ),
                        ),
                      ],
                    ),
                  ),
                  _FoamIconButton(
                    tooltip: 'Profile',
                    icon: Icons.settings_outlined,
                    onPressed: onProfile,
                  ),
                ],
              ),
              const SizedBox(height: 16),
              AppSearchField(
                hint: 'Search seagrass species',
                readOnly: true,
                onWash: true,
                onTap: onSearch,
              ),
            ],
          ),
        ),
    );
  }
}

class _FoamMark extends StatelessWidget {
  const _FoamMark({required this.child});

  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 48,
      height: 48,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        color: SkyPalette.foam,
        shape: BoxShape.circle,
        border: Border.all(color: SkyPalette.lineOnSky),
        boxShadow: const [
          BoxShadow(
            color: SkyPalette.shadow,
            blurRadius: 12,
            offset: Offset(0, 4),
          ),
        ],
      ),
      child: child,
    );
  }
}

class _FoamIconButton extends StatelessWidget {
  const _FoamIconButton({
    required this.tooltip,
    required this.icon,
    required this.onPressed,
  });

  final String tooltip;
  final IconData icon;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: tooltip,
      child: DecoratedBox(
        decoration: const BoxDecoration(shape: BoxShape.circle),
        child: Material(
          color: const Color(0x33FFFFFF),
          shape: const CircleBorder(
            side: BorderSide(color: Color(0x55FFFFFF)),
          ),
          child: InkWell(
            customBorder: const CircleBorder(),
            onTap: onPressed,
            child: SizedBox(
              width: 48,
              height: 48,
              child: Icon(icon, color: SkyPalette.onHeader),
            ),
          ),
        ),
      ),
    );
  }
}

class _ActionRow extends StatelessWidget {
  const _ActionRow({required this.onOpen});

  final void Function(int tab) onOpen;

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _HomeAction(
          icon: Icons.photo_camera_outlined,
          iconColor: SkyPalette.primary,
          label: 'Scan Seagrass',
          onTap: () => onOpen(ShellTab.scan),
        ),
        const SizedBox(width: 10),
        _HomeAction(
          icon: Icons.storage_outlined,
          iconColor: SkyPalette.seagrass,
          label: '3D Library',
          onTap: () => onOpen(ShellTab.library),
        ),
        const SizedBox(width: 10),
        _HomeAction(
          icon: Icons.favorite_border,
          iconColor: SkyPalette.seagrass,
          label: 'Conservation',
          onTap: () => onOpen(ShellTab.conservation),
        ),
      ],
    );
  }
}

class _HomeAction extends StatelessWidget {
  const _HomeAction({
    required this.icon,
    required this.iconColor,
    required this.label,
    required this.onTap,
  });

  final IconData icon;
  final Color iconColor;
  final String label;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;

    return Expanded(
      child: OceanSurface(
        onTap: onTap,
        padding: const EdgeInsets.fromLTRB(8, 16, 8, 14),
        child: ConstrainedBox(
          constraints: const BoxConstraints(minHeight: 108),
          child: Column(
            children: [
              Container(
                width: 48,
                height: 48,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  color: iconColor,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Icon(icon, color: Colors.white, size: 26),
              ),
              const SizedBox(height: 10),
              Text(
                label,
                textAlign: TextAlign.center,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: text.labelLarge?.copyWith(
                  color: context.tokens.ink,
                  height: 1.15,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _FeaturedHeader extends StatelessWidget {
  const _FeaturedHeader({required this.onViewAll});

  final VoidCallback onViewAll;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: Text(
            'Featured Species',
            style: Theme.of(context).textTheme.titleLarge,
          ),
        ),
        TextButton(
          onPressed: onViewAll,
          child: const Text('View All'),
        ),
      ],
    );
  }
}

class _Featured {
  const _Featured({this.species, this.stillAsset});

  final Species? species;
  final String? stillAsset;
}

class _FeaturedCard extends StatelessWidget {
  const _FeaturedCard({required this.species, this.stillAsset});

  final Species species;
  final String? stillAsset;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final tokens = context.tokens;

    return OceanSurface(
      onTap: () {
        Navigator.of(context).push(
          MaterialPageRoute<void>(
            builder: (_) => SpeciesScreen(slug: species.slug),
          ),
        );
      },
      padding: const EdgeInsets.all(12),
      child: Row(
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(16),
            child: SizedBox(
              width: 76,
              height: 76,
              child: stillAsset == null
                  ? ColoredBox(
                      color: tokens.border,
                      child: Icon(Icons.spa_outlined, color: tokens.brand),
                    )
                  : Image.asset(stillAsset!, fit: BoxFit.cover),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  species.scientificName,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: text.titleMedium?.copyWith(
                    fontStyle: FontStyle.italic,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  species.commonName,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: text.bodyMedium,
                ),
              ],
            ),
          ),
          const SizedBox(width: 8),
          Icon(Icons.spa_outlined, color: tokens.brand, size: 28),
        ],
      ),
    );
  }
}
