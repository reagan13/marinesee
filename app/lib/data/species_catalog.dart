import 'dart:convert';

import 'package:flutter/services.dart';

import 'species.dart';

/// Bundled library. Slug order matches `ml/src/dataset_contract.py`.
class SpeciesCatalog {
  static const assetPath = 'assets/data/species.json';

  static const List<String> studyOrder = [
    'cymodocea_rotundata',
    'cymodocea_serrulata',
    'enhalus_acoroides',
    'halodule_pinifolia',
    'halodule_uninervis',
    'halophila_minor',
    'halophila_ovalis',
    'syringodium_isoetifolium',
    'thalassia_hemprichii',
  ];

  List<Species>? _cached;

  Future<List<Species>> all() async {
    if (_cached != null) {
      return _cached!;
    }

    final raw = await rootBundle.loadString(assetPath);
    final decoded = jsonDecode(raw) as List<dynamic>;
    final bySlug = <String, Species>{};
    for (final item in decoded) {
      final species = Species.fromJson(item as Map<String, dynamic>);
      bySlug[species.slug] = species;
    }

    final ordered = <Species>[];
    for (final slug in studyOrder) {
      final species = bySlug[slug];
      if (species == null) {
        throw StateError('species.json is missing slug $slug');
      }
      ordered.add(species);
    }

    _cached = ordered;
    return ordered;
  }

  Future<Species?> bySlug(String slug) async {
    final items = await all();
    for (final species in items) {
      if (species.slug == slug) {
        return species;
      }
    }
    return null;
  }
}

final speciesCatalog = SpeciesCatalog();
