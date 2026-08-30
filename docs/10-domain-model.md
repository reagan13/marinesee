# Domain Model

The paper has no ERD. This is an **IMPLEMENTATION** sketch so the app and admin screens share names.

## Species

The only first-class educational entity.

| Field | Required by study |
|-------|-------------------|
| `id` | slug or uuid |
| `scientific_name` | yes |
| `common_name` | yes |
| `botanical_characteristics` | yes |
| `ecological_role` | yes |
| `conservation_status` | yes |
| `habitat` / geographic notes (Mati sites) | yes |
| `growth_process` | yes (scope: “development growth processes”) |
| `model_3d_uri` | needed for M3 |
| `cover_image_uri` | useful, not named as mandatory |

Nine rows only in v1. See `11-species.md`.

## IdentificationResult (optional persist)

The paper does not require a history of user photos. Default: **do not store visitor photos** unless admin analytics is added later (that would be a scope expansion — ask first).

If we persist for debugging:

- `predicted_species_id`
- `confidence`
- `created_at`
- no raw image, or short-lived only

## Administrator

Minimal account for content management. Fields **OPEN**.

## TrainingImage (Drive only)

Not a database table in v1. Folder layout on Drive **is** the dataset. Do not sync thousands of JPEGs into MySQL or git.
