import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../classify/classifier.dart';
import '../classify/stub_classifier.dart';
import '../data/species.dart';
import '../data/species_catalog.dart';
import '../widgets/aurora_button.dart';
import '../widgets/ocean_layout.dart';
import '../widgets/ocean_surface.dart';
import '../widgets/status_badge.dart';
import 'species_screen.dart';
import 'viewer_3d_screen.dart';

class ResultScreen extends StatelessWidget {
  const ResultScreen({
    super.key,
    required this.imageBytes,
    required this.result,
    this.catalog,
  });

  final Uint8List imageBytes;
  final IdentifyResult result;
  final SpeciesCatalog? catalog;

  @override
  Widget build(BuildContext context) {
    if (result.status == IdentifyStatus.stub) {
      return _ResultScaffold(
        imageBytes: imageBytes,
        badge: const StatusBadge(
          label: 'Model offline',
          icon: Icons.cloud_off_outlined,
          tone: StatusTone.notice,
        ),
        title: StubClassifier.notConnectedMessage,
        actions: const [],
      );
    }

    if (result.status == IdentifyStatus.error || result.slug == null) {
      return _ResultScaffold(
        imageBytes: imageBytes,
        badge: const StatusBadge(
          label: 'Error',
          icon: Icons.error_outline,
          tone: StatusTone.danger,
        ),
        title: result.message ?? 'Identification did not finish.',
        actions: const [],
      );
    }

    final slug = result.slug!;
    return FutureBuilder<Species?>(
      future: (catalog ?? speciesCatalog).bySlug(slug),
      builder: (context, snapshot) {
        final species = snapshot.data;
        final low = result.status == IdentifyStatus.lowConfidence;
        final percent = result.confidence == null
            ? null
            : '${(result.confidence! * 100).toStringAsFixed(0)}%';
        return _ResultScaffold(
          imageBytes: imageBytes,
          badge: StatusBadge(
            label: low ? 'Low confidence' : 'Match',
            icon: low
                ? Icons.help_outline
                : Icons.check_circle_outline,
            tone: low ? StatusTone.notice : StatusTone.neutral,
          ),
          title: species?.scientificName ?? slug.replaceAll('_', ' '),
          subtitle: [
            if (species != null) species.commonName,
            if (percent != null) 'Confidence $percent',
            if (low)
              result.message ??
                  'Low confidence — retake if you can get a closer leaf.',
          ].join('\n'),
          italicTitle: true,
          actions: [
            AuroraButton(
              label: 'Open species profile',
              icon: Icons.menu_book_outlined,
              onPressed: () {
                Navigator.of(context).push(
                  MaterialPageRoute<void>(
                    builder: (_) => SpeciesScreen(slug: slug),
                  ),
                );
              },
            ),
            const SizedBox(height: 12),
            OutlinedButton.icon(
              onPressed: () {
                Navigator.of(context).push(
                  MaterialPageRoute<void>(
                    builder: (_) => Viewer3dScreen(slug: slug),
                  ),
                );
              },
              icon: const Icon(Icons.view_in_ar_outlined),
              label: const Text('Open 3D model'),
            ),
          ],
        );
      },
    );
  }
}

class _ResultScaffold extends StatelessWidget {
  const _ResultScaffold({
    required this.imageBytes,
    required this.badge,
    required this.title,
    this.subtitle,
    this.italicTitle = false,
    required this.actions,
  });

  final Uint8List imageBytes;
  final Widget badge;
  final String title;
  final String? subtitle;
  final bool italicTitle;
  final List<Widget> actions;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;

    return OceanScaffold(
      title: 'Result',
      body: OceanPage(
        children: [
          OceanSurface(
            glow: true,
            padding: EdgeInsets.zero,
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxHeight: 320),
              child: Image.memory(
                imageBytes,
                fit: BoxFit.contain,
                width: double.infinity,
              ),
            ),
          ),
          const SizedBox(height: 18),
          OceanSurface(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                badge,
                const SizedBox(height: 14),
                Text(
                  title,
                  style: text.headlineSmall?.copyWith(
                    fontStyle: italicTitle ? FontStyle.italic : null,
                  ),
                ),
                if (subtitle != null && subtitle!.isNotEmpty) ...[
                  const SizedBox(height: 10),
                  Text(subtitle!, style: text.bodyMedium),
                ],
              ],
            ),
          ),
          const SizedBox(height: 20),
          ...actions,
          if (actions.isNotEmpty) const SizedBox(height: 12),
          OutlinedButton.icon(
            onPressed: () => Navigator.of(context).pop(),
            icon: const Icon(Icons.refresh),
            label: const Text('Try again'),
          ),
        ],
      ),
    );
  }
}
