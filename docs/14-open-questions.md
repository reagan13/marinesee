# Open Questions

Do not silently answer these in code. When the team (or adviser) decides, write the answer here and update the related doc.

## Must confirm before we write much app code

### Product / paper

1. **Authors and official short title** for the cover page and README?
2. Keep the limitation sentence that forbids “automated species recognition,” or strike it in the next paper revision? (Repo default: SVM stays.)
3. Dataset counts (30 Aug 2026 inventory): see `ml/artifacts/inventory.md`. Paper still needs `[INSERT NUMBER]` updated. **Blocker:** *Thalassia hemprichii* = 0 images.
4. Drive folder confirmed at `/content/drive/MyDrive/Seagrass`. **Decision (30 Aug 2026):** v1 trains **eight** classes on **`all`** folders (no research-grade, no ovalis `- Copy`). *Thalassia* remains a paper class and is **held out** until images exist. Tell the adviser this is a data gap, not a scope change.

### Mobile stack

5. **Flutter** (locked 30 Aug 2026). Android 8+ APK, physical phone, no emulator. Paper’s “Android Studio” = SDK toolchain, not daily IDE. See `16-flutter-audit-and-scaffold.md`.
6. Visitor **login** or guest-first?
7. **3D:** App **integrates** only. We do not build Blender files. Placeholder until a teammate drops `.glb` / `.mp4`. **OPEN:** who delivers those assets and when.
8. Identification **on-device** or **API**?

### Content store

9. **Firebase**, **MySQL + API**, or **bundled JSON** in the APK for v1 profiles?
10. Do admins edit content in a web console, in Firebase console, or only via a JSON PR?

### Model

11. Fixed **resize** (width × height)?
12. Exact **feature vector** (histogram bins, GLCM distances/angles, which shape metrics)?
13. SVM **kernel**, `C`, gamma, class weights?
14. **Confidence threshold** for “please retake”?
15. Split **random seed** and stratification by class?

### Evaluation

16. How many respondents per user group?
17. Final questionnaire items (Likert text)?

## Nice to confirm early, not blockers for docs

18. Common names in English only, or also local names once approved?
19. May we store anonymous identify metrics (predicted class + confidence, no photo)?
20. Git remote: GitHub, Cursor-hosted, or local-only for now?

## Decisions already made in this repo

| Item | Decision | Where |
|------|----------|--------|
| One repo for app + training + docs | Yes | `06-architecture.md` |
| Images in git | No | `data/README.md` |
| Train in Colab on Drive-mounted data | Yes | `12-colab-and-training.md` |
| Classifier | SVM only | `09-ml-pipeline.md` |
| Species list | Nine names locked; Drive *Halophila spinulosa* excluded | `11-species.md` |
| Drive folder | Shared Seagrass id `1MU31a5BG3MKn1fEYV-ljhc2zS4CoE79F` | `data/README.md` |
| Inventory | 8/9 species; *Thalassia* missing; v1 = `all` not research-grade | `ml/artifacts/inventory.md` |
| v1 classes | Eight Drive classes; *Thalassia* held out | `ml/src/dataset_contract.py` |
| v1 smoke test | 22.4% test acc on 100/class — baseline only | `ml/artifacts/v1_smoke_metrics.md` |
| Client toolkit | Flutter; phone only | `16-flutter-audit-and-scaffold.md` |
| SVM-vs-limitation sentence | Identification is in scope | `00-study-review.md` |
