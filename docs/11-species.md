# Nine Seagrass Species (Mati City)

**STUDY** — Chapters 1.3, 1.5, 2.2. Do not add or drop a row without changing the paper.

Documented in coastal assessments of Lawigan, Taitaidaga, Manguihay, and Pujada Bay (Angsinco-Jimenez et al., 2003; Sanchez-Delute et al., 2025; Fortes, 2013 as cited).

## Locked class list

Use these **scientific names as class labels** in folders, `label_map.json`, and the app.

| # | Scientific name | Suggested folder slug |
|---|-----------------|------------------------|
| 1 | *Cymodocea rotundata* | `cymodocea_rotundata` |
| 2 | *Cymodocea serrulata* | `cymodocea_serrulata` |
| 3 | *Enhalus acoroides* | `enhalus_acoroides` |
| 4 | *Halodule pinifolia* | `halodule_pinifolia` |
| 5 | *Halodule uninervis* | `halodule_uninervis` |
| 6 | *Halophila minor* | `halophila_minor` |
| 7 | *Halophila ovalis* | `halophila_ovalis` |
| 8 | *Syringodium isoetifolium* | `syringodium_isoetifolium` |
| 9 | *Thalassia hemprichii* | `thalassia_hemprichii` |

## v1 training set (IMPLEMENTATION)

A local dump (19 Sep 2026) had *Thalassia hemprichii* photos nested under *Enhalus* / *Halodule* folders. Those files now live at the top-level `Thalassia hemprichii dataset (research-grade)` and `(all)` folders. v1 still trains the other **eight** slugs until that folder is audited for mix-ins. The paper’s ninth class is not deleted — it is held out. See `ml/src/dataset_contract.py` (`TRAINABLE_SPECIES`).

## On Drive but out of the study

The shared [Seagrass](https://drive.google.com/drive/folders/1MU31a5BG3MKn1fEYV-ljhc2zS4CoE79F) folder also has **Halophila spinulosa**. Do not add it as a tenth class. The paper’s limitation is nine Mati species only. Inventory treats that folder as `extra`.

## Profile fields each species must have

**STUDY:**

- Scientific name
- Common name
- Botanical characteristics
- Ecological role
- Conservation status
- Habitat / distribution notes for Mati (educational, not GIS)
- Growth / development process

**IMPLEMENTATION:** a cited draft of those paragraphs is in `app/assets/data/species.json`. Global IUCN categories come from Short et al. (2011) and the IUCN Red List pages linked there. They are not a Mati City survey. An adviser should still check the wording before it is treated as final study text.

## Conservation status wording

The paper’s definition of terms says status may be described as stable, vulnerable, threatened, or in need of conservation. That is educational language, not an automatic IUCN badge. Mark the source of each status sentence in the content file.
