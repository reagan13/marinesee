# Open Questions

Do not silently answer these in code. When the team (or adviser) decides, write the answer here and update the related doc.

## Must confirm before we write much app code

### Product / paper

1. **Authors and official short title** for the cover page and README?
2. Keep the limitation sentence that forbids “automated species recognition,” or strike it in the next paper revision? (Repo default: SVM stays.)
3. Dataset counts: Drive inventory (30 Aug 2026) still says *Thalassia* = 0 at the Drive root. A **local** dump (19 Sep 2026) had Thalassia nested under other taxa; those folders were relocated to a top-level class. Paper still needs `[INSERT NUMBER]` updated. **No longer a zero-image blocker locally** — still held out of v1 until a mix-in audit.
4. Drive folder confirmed at `/content/drive/MyDrive/Seagrass`. **Decision (30 Aug 2026):** v1 trains **eight** classes on **`all`** folders (no research-grade, no ovalis `- Copy`). *Thalassia* remains a paper class and is **held out** of training until the relocated folder is audited. Tell the adviser this was a folder-layout gap, not a scope change.

### Mobile stack

5. **Flutter** (locked 30 Aug 2026). Android 8+ APK, physical phone, no emulator. Paper’s “Android Studio” = SDK toolchain, not daily IDE. See `16-flutter-audit-and-scaffold.md`.
6. Visitor **login** or guest-first?
7. **3D:** App **integrates** only. We do not build Blender files. Viewer plays `app/assets/models-3d/<slug>_growth.mp4` when present, else a species still, else the placeholder. **OPEN:** who delivers the remaining eight clips / `.glb` files and when.
8. Identification **on-device** or **API**? **Decision (20 Sep 2026):** v1 is a **laptop Python API** (`ml/src/serve_identify.py`) that the phone calls. On-device export stays later.

### Content store

9. **Firebase**, **MySQL + API**, or **bundled JSON** in the APK for v1 profiles?
10. Do admins edit content in a web console, in Firebase console, or only via a JSON PR?

### Model

11. Fixed **resize** (width × height)?
12. Exact **feature vector** (histogram bins, GLCM distances/angles, which shape metrics)?
13. SVM **kernel**, `C`, gamma, class weights?
14. **Confidence threshold** for “please retake”? **IMPLEMENTATION default 0.20** (`LOW_CONFIDENCE` in `identify.py`). Not a paper number.
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
| Inventory | Drive 30 Aug 2026: 8/9, *Thalassia* missing at Drive root. Local 19 Sep 2026: *Thalassia* relocated to its own folders; still held out of v1 | `ml/artifacts/inventory.md` |
| v1 classes | Eight Drive classes; *Thalassia* held out | `ml/src/dataset_contract.py` |
| v1 smoke test | 22.4% test acc on 100/class — baseline only | `ml/artifacts/v1_smoke_metrics.md` |
| Client toolkit | Flutter; phone only | `16-flutter-audit-and-scaffold.md` |
| v1 inference | Laptop SVM API; phone POSTs the photo | `ml/src/serve_identify.py` |
| Colab v1 (full `all`) | Test acc **35.0%** (not 85%) | `ml/artifacts/v1/metrics.json` |
| SVM-vs-limitation sentence | Identification is in scope | `00-study-review.md` |
