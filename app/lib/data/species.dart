class Species {
  const Species({
    required this.slug,
    required this.scientificName,
    required this.commonName,
    required this.botanicalCharacteristics,
    required this.ecologicalRole,
    required this.conservationStatus,
    required this.habitat,
    required this.growthProcess,
  });

  final String slug;
  final String scientificName;
  final String commonName;
  final String botanicalCharacteristics;
  final String ecologicalRole;
  final String conservationStatus;
  final String habitat;
  final String growthProcess;

  bool get dataComing => slug == 'thalassia_hemprichii';

  factory Species.fromJson(Map<String, dynamic> json) {
    return Species(
      slug: json['slug'] as String,
      scientificName: json['scientificName'] as String,
      commonName: json['commonName'] as String,
      botanicalCharacteristics: json['botanicalCharacteristics'] as String,
      ecologicalRole: json['ecologicalRole'] as String,
      conservationStatus: json['conservationStatus'] as String,
      habitat: json['habitat'] as String,
      growthProcess: json['growthProcess'] as String,
    );
  }
}
