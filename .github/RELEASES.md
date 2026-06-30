# Release Tag Reference

Acest fișier documentează SHA-urile exacte pentru fiecare release.
Tag-urile se creează local cu comenzile de mai jos.

## Tag SHAs

| Tag | SHA | Commit message |
|---|---|---|
| `v1.0.0` | `f83e4f2a56f46df4b5239eeaba73996a654a6095` | 🚀 Initial release: BookForge AI pipeline |
| `v1.1.0` | `ba0d2304a172377e5238e01c0f0afef8918b519d` | feat: bump to v1.1.0 — add web UI |
| `v1.2.0` | `494347197a303ac4d99ba2a47ad536ec46796996` | feat(v1.2.0): add /categories and /batch routes |
| `v1.3.0` | `4aa3d5192f96339f3a765a58f7dc35ab3076b7f0` | feat: prepare v1.3.0 with covers, DOCX, scheduler |
| `v1.3.1` | `80e56cb2b2418304754f1659427bbbb757945fff` | chore: bump version to 1.3.1 |
| `v1.4.0` | `4b03406b2176d16790820aef306b4ca04ac088ea` | feat: v1.4.0 — job dashboard, batch ZIP, sales stats |
| `v1.4.1` | `4566964dd3d3d9e861a58b6abee3a4d9952513f9` | fix: v1.4.1 — route ordering, zip guard, XSS |
| `v1.5.0` | `cb17fc40af39eb613452b0071060b45ce56dcf3c` | docs: README complet v1.5.0 |
| `v1.5.1` | `0ab47ff588d49f69318b8519d195ac6b9adbbb38` | fix: v1.5.1 — import re, kdp FileNotFoundError, timeout, version |
| `v1.5.2` | `102bc8580c840a8bfd7270aa8c4c2ad3a5e120a0` | fix: v1.5.2 — libasound2t64, requirements sync, .gitignore |

## Comenzi locale (toate tag-urile)

```bash
git fetch origin
git tag v1.0.0 f83e4f2a56f46df4b5239eeaba73996a654a6095
git tag v1.1.0 ba0d2304a172377e5238e01c0f0afef8918b519d
git tag v1.2.0 494347197a303ac4d99ba2a47ad536ec46796996
git tag v1.3.0 4aa3d5192f96339f3a765a58f7dc35ab3076b7f0
git tag v1.3.1 80e56cb2b2418304754f1659427bbbb757945fff
git tag v1.4.0 4b03406b2176d16790820aef306b4ca04ac088ea
git tag v1.4.1 4566964dd3d3d9e861a58b6abee3a4d9952513f9
git tag v1.5.0 cb17fc40af39eb613452b0071060b45ce56dcf3c
git tag v1.5.1 0ab47ff588d49f69318b8519d195ac6b9adbbb38
git tag v1.5.2 102bc8580c840a8bfd7270aa8c4c2ad3a5e120a0
git push origin --tags
```
