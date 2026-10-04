import 'package:flutter/material.dart';

import '../data/model_3d_library.dart';
import '../data/species.dart';
import '../data/species_catalog.dart';
import '../theme/tokens.dart';
import '../widgets/app_header.dart';
import '../widgets/app_search_field.dart';
import '../widgets/app_states.dart';
import '../widgets/data_coming_badge.dart';
import '../widgets/filter_chip_bar.dart';
import '../widgets/ocean_layout.dart';
import '../widgets/section_header.dart';
import '../widgets/species_card.dart';
import 'species_screen.dart';

class LibraryScreen extends StatefulWidget {
  const LibraryScreen({super.key});

  @override
  State<LibraryScreen> createState() => _LibraryScreenState();
}

class _LibraryScreenState extends State<LibraryScreen> {
  late Future<_LibraryPayload> _future = _load();
  String _query = '';
  String _genus = 'All';

  Future<_LibraryPayload> _load() async {
    final items = await speciesCatalog.all();
    final media = await Model3dLibrary.resolveMany(
      items.map((species) => species.slug),
    );
    return _LibraryPayload(items: items, media: media);
  }

  void _reload() {
    setState(() {
      Model3dLibrary.resetCache();
      _future = _load();
    });
  }

  List<Species> _filter(List<Species> items) {
    return items.where((species) {
      final genus = species.scientificName.split(' ').first;
      final matchesGenus = _genus == 'All' || genus == _genus;
      final haystack =
          '${species.scientificName} ${species.commonName}'.toLowerCase();
      final matchesQuery = _query.isEmpty || haystack.contains(_query);
      return matchesGenus && matchesQuery;
    }).toList();
  }

  @override
  Widget build(BuildContext context) {
    return OceanScaffold(
      atmosphere: false,
      header: const AppHeader(
        title: 'Library',
        subtitle: 'Nine documented seagrass species.',
      ),
      body: FutureBuilder<_LibraryPayload>(
        future: _future,
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return OceanError(
              message: 'Could not load the species library.',
              onRetry: _reload,
            );
          }
          final payload = snapshot.data;
          if (payload == null) {
            return const OceanLoading(label: 'Opening the library…');
          }
          final items = payload.items;

          final genera = [
            'All',
            ...{for (final species in items) species.scientificName.split(' ').first},
          ];
          final visible = _filter(items);

          return OceanPage(
            extraBottom: AppSpace.navClearance,
            children: [
              AppSearchField(
                hint: 'Search species',
                onChanged: (value) => setState(() => _query = value.toLowerCase()),
              ),
              const SizedBox(height: 14),
              FilterChipBar(
                labels: genera,
                selected: _genus,
                onSelected: (value) => setState(() => _genus = value),
              ),
              const SizedBox(height: 22),
              const SectionHeader(title: 'Nine species'),
              const SizedBox(height: 12),
              if (visible.isEmpty)
                const OceanEmpty(
                  icon: Icons.search_off,
                  title: 'No matching species',
                  message: 'Try another name or clear the genus filter.',
                )
              else
                GridView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: visible.length,
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    mainAxisSpacing: 12,
                    crossAxisSpacing: 12,
                    childAspectRatio: 0.78,
                  ),
                  itemBuilder: (context, index) {
                    final species = visible[index];
                    return SpeciesCard(
                      title: species.scientificName,
                      subtitle: species.commonName,
                      imageAsset: payload.media[species.slug]?.stillAsset,
                      badge: species.dataComing ? const DataComingBadge() : null,
                      onTap: () {
                        Navigator.of(context).push(
                          MaterialPageRoute<void>(
                            builder: (_) => SpeciesScreen(slug: species.slug),
                          ),
                        );
                      },
                    );
                  },
                ),
            ],
          );
        },
      ),
    );
  }
}

class _LibraryPayload {
  const _LibraryPayload({required this.items, required this.media});

  final List<Species> items;
  final Map<String, SpeciesMedia> media;
}
