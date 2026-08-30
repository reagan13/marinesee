import 'package:flutter/material.dart';

import '../data/species.dart';
import '../data/species_catalog.dart';
import '../theme/tokens.dart';
import '../widgets/data_coming_badge.dart';
import '../widgets/profile_field.dart';
import 'viewer_3d_screen.dart';

class SpeciesScreen extends StatelessWidget {
  const SpeciesScreen({super.key, required this.slug});

  final String slug;

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Species?>(
      future: speciesCatalog.bySlug(slug),
      builder: (context, snapshot) {
        final species = snapshot.data;
        return Scaffold(
          appBar: AppBar(
            title: Text(species?.scientificName ?? 'Species'),
          ),
          body: _body(context, snapshot),
        );
      },
    );
  }

  Widget _body(BuildContext context, AsyncSnapshot<Species?> snapshot) {
    if (snapshot.hasError) {
      return Center(
        child: Text(
          'Could not load this species.',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            color: AppTokens.danger,
          ),
        ),
      );
    }
    if (!snapshot.hasData && snapshot.connectionState != ConnectionState.done) {
      return const Center(child: CircularProgressIndicator());
    }
    final species = snapshot.data;
    if (species == null) {
      return Center(
        child: Text(
          'Species not found.',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            color: AppTokens.ink,
          ),
        ),
      );
    }

    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
      children: [
        if (species.dataComing) ...[
          const Align(
            alignment: Alignment.centerLeft,
            child: DataComingBadge(),
          ),
          const SizedBox(height: 16),
        ],
        ProfileField(label: 'Scientific name', value: species.scientificName),
        ProfileField(label: 'Common name', value: species.commonName),
        ProfileField(
          label: 'Botanical characteristics',
          value: species.botanicalCharacteristics,
        ),
        ProfileField(label: 'Ecological role', value: species.ecologicalRole),
        ProfileField(
          label: 'Conservation status',
          value: species.conservationStatus,
        ),
        ProfileField(label: 'Habitat', value: species.habitat),
        ProfileField(label: 'Growth process', value: species.growthProcess),
        FilledButton(
          onPressed: () {
            Navigator.of(context).push(
              MaterialPageRoute<void>(
                builder: (_) => Viewer3dScreen(slug: species.slug),
              ),
            );
          },
          child: const Text('Open 3D model'),
        ),
      ],
    );
  }
}
