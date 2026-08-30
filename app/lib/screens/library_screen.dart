import 'package:flutter/material.dart';

import '../data/species.dart';
import '../data/species_catalog.dart';
import '../theme/tokens.dart';
import '../widgets/data_coming_badge.dart';
import 'species_screen.dart';

class LibraryScreen extends StatelessWidget {
  const LibraryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Library')),
      body: FutureBuilder<List<Species>>(
        future: speciesCatalog.all(),
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Text(
                  'Could not load the species library.',
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    color: AppTokens.danger,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            );
          }
          final items = snapshot.data;
          if (items == null) {
            return const Center(child: CircularProgressIndicator());
          }
          return ListView.separated(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
            itemCount: items.length,
            separatorBuilder: (_, _) => const SizedBox(height: 8),
            itemBuilder: (context, index) {
              final species = items[index];
              return _SpeciesTile(species: species);
            },
          );
        },
      ),
    );
  }
}

class _SpeciesTile extends StatelessWidget {
  const _SpeciesTile({required this.species});

  final Species species;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        contentPadding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
        minVerticalPadding: 16,
        title: Text(
          species.scientificName,
          style: Theme.of(context).textTheme.titleMedium?.copyWith(
            color: AppTokens.ink,
            fontStyle: FontStyle.italic,
          ),
        ),
        subtitle: Text(
          species.commonName,
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
            color: AppTokens.inkMuted,
          ),
        ),
        trailing: species.dataComing ? const DataComingBadge() : null,
        onTap: () {
          Navigator.of(context).push(
            MaterialPageRoute<void>(
              builder: (_) => SpeciesScreen(slug: species.slug),
            ),
          );
        },
      ),
    );
  }
}
