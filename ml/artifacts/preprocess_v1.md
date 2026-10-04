# SVM v1 preprocess (local)

Date: 2026-09-19
Root: `D:\pepot\marinesee\assets\species\Seagrass`
Dest: `D:\pepot\marinesee\data\processed\v1`

Paper order: select frames that show leaf → resize 256 → count classes. Augment stays train-only. *Thalassia* is listed in the hold-out count, not written.

- Listed (`all`, eight classes): **2175**
- Kept: **2175**
- Skipped: **0** `{}`
- Plant-crop applied: **648**
- Review (not dropped): low green-mask **333**, high sky-like top **318**
- Held-out *Thalassia* `all` listed (not written): **743**

| slug | listed | kept |
|------|--------|------|
| cymodocea_rotundata | 158 | 158 |
| cymodocea_serrulata | 87 | 87 |
| enhalus_acoroides | 666 | 666 |
| halodule_pinifolia | 85 | 85 |
| halodule_uninervis | 375 | 375 |
| halophila_minor | 24 | 24 |
| halophila_ovalis | 619 | 619 |
| syringodium_isoetifolium | 161 | 161 |

This laptop dump is **not** the Drive training root (*H. pinifolia* `all` is 85 here vs 876 on Drive).
