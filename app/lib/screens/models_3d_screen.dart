import 'package:flutter/material.dart';

import '../data/model_3d_library.dart';
import '../data/species.dart';
import '../data/species_catalog.dart';
import '../widgets/app_states.dart';
import '../widgets/ocean_layout.dart';
import '../widgets/ocean_surface.dart';
import '../widgets/settings_tile.dart';
import 'viewer_3d_screen.dart';

class Models3dScreen extends StatefulWidget {
  const Models3dScreen({super.key});

  @override
  State<Models3dScreen> createState() => _Models3dScreenState();
}

class _Models3dScreenState extends State<Models3dScreen> {
  late Future<_ModelsPayload> _future = _load();

  Future<_ModelsPayload> _load() async {
    final items = await speciesCatalog.all();
    final media = await Model3dLibrary.resolveMany(
      items.map((species) => species.slug),
    );
    return _ModelsPayload(items: items, media: media);
  }

  void _reload() {
    setState(() {
      Model3dLibrary.resetCache();
      _future = _load();
    });
  }

  @override
  Widget build(BuildContext context) {
    return OceanScaffold(
      title: '3D models',
      body: FutureBuilder<_ModelsPayload>(
        future: _future,
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return OceanError(
              message: 'Could not load the 3D list.',
              onRetry: _reload,
            );
          }
          final payload = snapshot.data;
          if (payload == null) {
            return const OceanLoading(label: 'Opening 3D models…');
          }

          return OceanPage(
            children: [
              Text(
                'A bundled .glb can be rotated and zoomed. A growth clip plays when that is the only file.',
                style: Theme.of(context).textTheme.bodyMedium,
              ),
              const SizedBox(height: 16),
              OceanSurface(
                padding: EdgeInsets.zero,
                child: Column(
                  children: [
                    for (var i = 0; i < payload.items.length; i++) ...[
                      if (i > 0) const OceanDivider(),
                      SettingsTile(
                        icon: Icons.view_in_ar_outlined,
                        label: payload.items[i].scientificName,
                        subtitle: Model3dLibrary.statusLabel(
                          payload.media[payload.items[i].slug] ??
                              const SpeciesMedia(),
                        ),
                        onTap: () {
                          Navigator.of(context).push(
                            MaterialPageRoute<void>(
                              builder: (_) => Viewer3dScreen(
                                slug: payload.items[i].slug,
                              ),
                            ),
                          );
                        },
                      ),
                    ],
                  ],
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}

class _ModelsPayload {
  const _ModelsPayload({required this.items, required this.media});

  final List<Species> items;
  final Map<String, SpeciesMedia> media;
}
