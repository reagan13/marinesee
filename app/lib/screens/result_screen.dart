import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../classify/classifier.dart';
import '../data/species.dart';
import '../data/species_catalog.dart';
import '../theme/tokens.dart';
import '../widgets/aurora_button.dart';
import '../widgets/ocean_layout.dart';
import '../widgets/ocean_surface.dart';
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

  static const retakeSentence =
      'Low confidence — retake if you can get a closer leaf.';

  @override
  Widget build(BuildContext context) {
    if (result.slug == null) {
      return _ResultScaffold(
        imageBytes: imageBytes,
        error: result.message ?? 'Identification did not finish.',
      );
    }

    final slug = result.slug!;
    return FutureBuilder<Species?>(
      future: (catalog ?? speciesCatalog).bySlug(slug),
      builder: (context, snapshot) {
        if (!snapshot.hasData &&
            snapshot.connectionState != ConnectionState.done) {
          return _ResultScaffold(imageBytes: imageBytes, loading: true);
        }
        final species = snapshot.data;
        final low = result.status == IdentifyStatus.lowConfidence;
        final percent = result.confidence == null
            ? null
            : '${(result.confidence! * 100).toStringAsFixed(0)}%';
        return _ResultScaffold(
          imageBytes: imageBytes,
          scientificName: species?.scientificName ?? slug.replaceAll('_', ' '),
          percent: percent,
          notice: low ? (result.message ?? retakeSentence) : null,
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
              label: const Text('Open 3D'),
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
    this.scientificName,
    this.percent,
    this.notice,
    this.error,
    this.loading = false,
    this.actions = const [],
  });

  final Uint8List imageBytes;
  final String? scientificName;
  final String? percent;
  final String? notice;
  final String? error;
  final bool loading;
  final List<Widget> actions;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;

    return OceanScaffold(
      title: 'Result',
      body: OceanPage(
        children: [
          OceanSurface(
            padding: EdgeInsets.zero,
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxHeight: 280),
              child: Image.memory(
                imageBytes,
                fit: BoxFit.contain,
                width: double.infinity,
              ),
            ),
          ),
          const SizedBox(height: 16),
          if (loading)
            const OceanSurface(
              child: Center(child: CircularProgressIndicator(strokeWidth: 2.4)),
            )
          else
            OceanSurface(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (scientificName != null) ...[
                    Text(
                      scientificName!,
                      style: text.headlineSmall?.copyWith(
                        fontStyle: FontStyle.italic,
                      ),
                    ),
                    const SizedBox(height: 12),
                  ],
                  if (percent != null) ...[
                    Text('Confidence', style: text.labelMedium),
                    const SizedBox(height: 4),
                    Text(percent!, style: text.headlineSmall),
                  ],
                  if (notice != null) ...[
                    const SizedBox(height: 14),
                    _Notice(message: notice!, tone: _NoticeTone.notice),
                  ],
                  if (error != null)
                    _Notice(message: error!, tone: _NoticeTone.danger),
                ],
              ),
            ),
          const SizedBox(height: 16),
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

enum _NoticeTone { notice, danger }

class _Notice extends StatelessWidget {
  const _Notice({required this.message, required this.tone});

  final String message;
  final _NoticeTone tone;

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    final color = tone == _NoticeTone.danger ? tokens.danger : tokens.notice;
    final fill = tone == _NoticeTone.danger
        ? tokens.danger.withValues(alpha: 0.08)
        : tokens.noticeFill;
    final border = tone == _NoticeTone.danger
        ? tokens.danger.withValues(alpha: 0.35)
        : tokens.noticeBorder;

    return DecoratedBox(
      decoration: BoxDecoration(
        color: fill,
        borderRadius: BorderRadius.circular(AppRadius.md),
        border: Border.all(color: border),
      ),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(
              tone == _NoticeTone.danger
                  ? Icons.error_outline
                  : Icons.info_outline,
              color: color,
              size: 20,
            ),
            const SizedBox(width: 10),
            Expanded(
              child: Text(
                message,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: color,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
