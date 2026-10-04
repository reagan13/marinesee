import 'package:flutter/material.dart';

import '../data/species.dart';
import '../data/species_catalog.dart';
import '../theme/tokens.dart';
import '../widgets/app_states.dart';
import '../widgets/aurora_button.dart';
import '../widgets/data_coming_badge.dart';
import '../widgets/ocean_layout.dart';
import '../widgets/ocean_surface.dart';
import '../widgets/profile_field.dart';
import '../widgets/section_header.dart';
import '../widgets/status_badge.dart';
import 'viewer_3d_screen.dart';

class SpeciesScreen extends StatefulWidget {
  const SpeciesScreen({super.key, required this.slug});

  final String slug;

  @override
  State<SpeciesScreen> createState() => _SpeciesScreenState();
}

class _SpeciesScreenState extends State<SpeciesScreen> {
  late Future<Species?> _future = speciesCatalog.bySlug(widget.slug);

  void _reload() {
    setState(() {
      _future = speciesCatalog.bySlug(widget.slug);
    });
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Species?>(
      future: _future,
      builder: (context, snapshot) {
        return OceanScaffold(
          title: snapshot.data?.scientificName ?? 'Species',
          body: _body(context, snapshot),
        );
      },
    );
  }

  Widget _body(BuildContext context, AsyncSnapshot<Species?> snapshot) {
    if (snapshot.hasError) {
      return OceanError(
        message: 'Could not load this species.',
        onRetry: _reload,
      );
    }
    if (!snapshot.hasData && snapshot.connectionState != ConnectionState.done) {
      return const OceanLoading(label: 'Loading profile…');
    }
    final species = snapshot.data;
    if (species == null) {
      return const OceanEmpty(
        icon: Icons.search_off,
        title: 'Species not found',
        message: 'This slug is not in the bundled library.',
      );
    }

    final tokens = context.tokens;
    final text = Theme.of(context).textTheme;

    return OceanPage(
      children: [
        OceanSurface(
          glow: true,
          child: Column(
            children: [
              Icon(Icons.eco_outlined, size: 40, color: tokens.brand),
              const SizedBox(height: 12),
              Text(
                species.scientificName,
                textAlign: TextAlign.center,
                style: text.headlineSmall?.copyWith(
                  fontStyle: FontStyle.italic,
                ),
              ),
              const SizedBox(height: 6),
              Text(
                species.commonName,
                textAlign: TextAlign.center,
                style: text.titleMedium,
              ),
              const SizedBox(height: 12),
              StatusBadge(
                label: species.conservationStatus,
                icon: Icons.shield_outlined,
              ),
              if (species.dataComing) ...[
                const SizedBox(height: 10),
                const DataComingBadge(),
              ],
            ],
          ),
        ),
        const SizedBox(height: 22),
        const SectionHeader(title: 'Identity'),
        const SizedBox(height: 10),
        OceanSurface(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              ProfileField(
                label: 'Scientific name',
                value: species.scientificName,
                italic: true,
              ),
              const OceanDivider(),
              ProfileField(label: 'Common name', value: species.commonName),
            ],
          ),
        ),
        const SizedBox(height: 18),
        const SectionHeader(title: 'Ecology'),
        const SizedBox(height: 10),
        OceanSurface(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              ProfileField(
                label: 'Botanical characteristics',
                value: species.botanicalCharacteristics,
              ),
              const OceanDivider(),
              ProfileField(
                label: 'Ecological role',
                value: species.ecologicalRole,
              ),
              const OceanDivider(),
              ProfileField(
                label: 'Conservation status',
                value: species.conservationStatus,
              ),
            ],
          ),
        ),
        const SizedBox(height: 18),
        const SectionHeader(title: 'Place'),
        const SizedBox(height: 10),
        OceanSurface(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              ProfileField(label: 'Habitat', value: species.habitat),
              const OceanDivider(),
              ProfileField(
                label: 'Growth process',
                value: species.growthProcess,
              ),
            ],
          ),
        ),
        const SizedBox(height: 20),
        AuroraButton(
          label: 'Open 3D model',
          icon: Icons.view_in_ar_outlined,
          onPressed: () {
            Navigator.of(context).push(
              MaterialPageRoute<void>(
                builder: (_) => Viewer3dScreen(slug: species.slug),
              ),
            );
          },
        ),
      ],
    );
  }
}
