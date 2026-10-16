import 'package:flutter/material.dart';

import '../data/model_3d_library.dart';
import '../data/species.dart';
import '../data/species_catalog.dart';
import '../theme/tokens.dart';
import '../widgets/app_states.dart';
import '../widgets/species_detail.dart';
import 'viewer_3d_screen.dart';

class SpeciesScreen extends StatefulWidget {
  const SpeciesScreen({super.key, required this.slug});

  final String slug;

  @override
  State<SpeciesScreen> createState() => _SpeciesScreenState();
}

class _SpeciesScreenState extends State<SpeciesScreen> {
  late Future<_SpeciesProfile> _future = _load();

  Future<_SpeciesProfile> _load() async {
    final species = await speciesCatalog.bySlug(widget.slug);
    final media = species == null
        ? const SpeciesMedia()
        : await Model3dLibrary.resolve(species.slug);
    return _SpeciesProfile(species: species, media: media);
  }

  void _reload() => setState(() => _future = _load());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: context.tokens.abyss,
      body: FutureBuilder<_SpeciesProfile>(
        future: _future,
        builder: (context, snapshot) => _body(context, snapshot),
      ),
    );
  }

  Widget _withBack(BuildContext context, Widget child) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        SafeArea(
          bottom: false,
          child: Align(
            alignment: Alignment.centerLeft,
            child: IconButton(
              onPressed: () => Navigator.of(context).pop(),
              icon: const Icon(Icons.arrow_back),
            ),
          ),
        ),
        Expanded(child: child),
      ],
    );
  }

  Widget _body(BuildContext context, AsyncSnapshot<_SpeciesProfile> snapshot) {
    if (snapshot.hasError) {
      return _withBack(
        context,
        OceanError(
          message: 'Could not load this species.',
          onRetry: _reload,
        ),
      );
    }
    if (!snapshot.hasData && snapshot.connectionState != ConnectionState.done) {
      return _withBack(context, const OceanLoading(label: 'Loading profile…'));
    }
    final species = snapshot.data?.species;
    if (species == null) {
      return _withBack(
        context,
        const OceanEmpty(
          icon: Icons.search_off,
          title: 'Species not found',
          message: 'This slug is not in the bundled library.',
        ),
      );
    }

    final still = snapshot.data?.media.stillAsset;
    final width = MediaQuery.sizeOf(context).width;
    final horizontal = width >= 768 ? 32.0 : 20.0;

    return ListView(
      padding: const EdgeInsets.only(bottom: 28),
      children: [
        SpeciesHero(
          stillAsset: still,
          onBack: () => Navigator.of(context).pop(),
          onView3d: () {
            Navigator.of(context).push(
              MaterialPageRoute<void>(
                builder: (_) => Viewer3dScreen(slug: species.slug),
              ),
            );
          },
        ),
        Padding(
          padding: EdgeInsets.symmetric(horizontal: horizontal),
          child: Transform.translate(
            offset: const Offset(0, -36),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                SpeciesNameCard(species: species),
                const SizedBox(height: 16),
                SpeciesFactCard(
                  icon: Icons.spa_outlined,
                  title: 'Botanical characteristics',
                  value: species.botanicalCharacteristics,
                ),
                const SizedBox(height: 12),
                SpeciesFactCard(
                  icon: Icons.water_outlined,
                  title: 'Ecological role',
                  value: species.ecologicalRole,
                ),
                const SizedBox(height: 12),
                SpeciesFactCard(
                  icon: Icons.shield_outlined,
                  title: 'Conservation status',
                  value: species.conservationStatus,
                ),
                const SizedBox(height: 12),
                SpeciesFactCard(
                  icon: Icons.place_outlined,
                  title: 'Habitat',
                  value: species.habitat,
                ),
                const SizedBox(height: 12),
                SpeciesFactCard(
                  icon: Icons.timeline_outlined,
                  title: 'Growth process',
                  value: species.growthProcess,
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class _SpeciesProfile {
  const _SpeciesProfile({required this.species, required this.media});

  final Species? species;
  final SpeciesMedia media;
}
