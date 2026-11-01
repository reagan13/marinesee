# Artifacts

Drop exported `label_map.json`, `feature_spec.json`, and `metrics.json` here when a run is accepted.

Each inventory, preprocess, and SVM run also appends `run_log.jsonl` and rebuilds `run_log.md`. The full F1 table for that run is `runs/<id>-svm/record.md` plus `scores.csv`. Plot images stay beside that folder and are gitignored with the other png files.

Model binaries (`*.joblib`, `*.onnx`, …) are gitignored, except the locked `v1/svm_seagrass_v1.joblib`. Keep a Drive copy of other runs and, if needed, a release note with the Drive link and the git commit that produced them.
