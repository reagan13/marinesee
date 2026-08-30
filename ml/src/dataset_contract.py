"""Locked study classes and Drive-folder matching.

The paper allows exactly nine Mati species. Extra folders on Drive
(e.g. Halophila spinulosa) stay out of training.
"""

from __future__ import annotations

STUDY_SPECIES: tuple[str, ...] = (
    "cymodocea_rotundata",
    "cymodocea_serrulata",
    "enhalus_acoroides",
    "halodule_pinifolia",
    "halodule_uninervis",
    "halophila_minor",
    "halophila_ovalis",
    "syringodium_isoetifolium",
    "thalassia_hemprichii",
)

# Paper still lists nine. Drive has no Thalassia images (30 Aug 2026).
# v1 trains the eight classes that exist. Add Thalassia back when the folder appears.
HELD_OUT_SPECIES: tuple[str, ...] = ("thalassia_hemprichii",)
TRAINABLE_SPECIES: tuple[str, ...] = tuple(
    s for s in STUDY_SPECIES if s not in HELD_OUT_SPECIES
)

# Use the large `all` folders. Skip research-grade and `- Copy`.
TRAIN_VARIANT = "all"

IMAGE_SIZE = 256
SPLIT_SEED = 42
SPLIT_RATIOS = (0.70, 0.15, 0.15)

# Substrings as they appear in the shared Drive folder titles.
SPECIES_PHRASES: dict[str, str] = {
    "cymodocea_rotundata": "cymodocea rotundata",
    "cymodocea_serrulata": "cymodocea serrulata",
    "enhalus_acoroides": "enhalus acoroides",
    "halodule_pinifolia": "halodule pinifolia",
    "halodule_uninervis": "halodule uninervis",
    "halophila_minor": "halophila minor",
    "halophila_ovalis": "halophila ovalis",
    "syringodium_isoetifolium": "syringodium isoetifolium",
    "thalassia_hemprichii": "thalassia hemprichii",
}

# Present on Drive in the Aug 2026 dump; not in the capstone species list.
OUT_OF_SCOPE_PHRASES: dict[str, str] = {
    "halophila_spinulosa": "halophila spinulosa",
}

IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff")

DRIVE_FOLDER_ID = "1MU31a5BG3MKn1fEYV-ljhc2zS4CoE79F"
DRIVE_FOLDER_URL = (
    "https://drive.google.com/drive/folders/1MU31a5BG3MKn1fEYV-ljhc2zS4CoE79F"
)


def normalize_folder_name(name: str) -> str:
    return " ".join(name.lower().replace("_", " ").split())


def classify_folder(name: str) -> tuple[str | None, str, str]:
    """Return (slug_or_none, scope, variant).

    scope: study | extra | unknown
    variant: research-grade | all | copy | unknown
    """
    n = normalize_folder_name(name)

    variant = "unknown"
    if "copy" in n:
        variant = "copy"
    elif "research-grade" in n or "research grade" in n:
        variant = "research-grade"
    elif "dataset (all)" in n or n.endswith("(all)") or " (all)" in n:
        variant = "all"
    elif "dataset" in n:
        variant = "all"

    for slug, phrase in SPECIES_PHRASES.items():
        if phrase in n:
            return slug, "study", variant

    for slug, phrase in OUT_OF_SCOPE_PHRASES.items():
        if phrase in n:
            return slug, "extra", variant

    return None, "unknown", variant
