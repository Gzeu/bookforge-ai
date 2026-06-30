# Release Tag Reference

Acest fișier documentează SHA-urile exacte pentru fiecare release.
Tag-urile se creează local cu comenzile de mai jos.

## Tag SHAs

| Tag | SHA | Commit message |
|---|---|---|
| `v1.4.0` | `4b03406b2176d16790820aef306b4ca04ac088ea` | feat: v1.4.0 — job dashboard, batch ZIP export, sales stats scraper |
| `v1.4.1` | `4566964dd3d3d9e861a58b6abee3a4d9952513f9` | fix: v1.4.1 — route ordering, zip empty guard, XSS sanitize |
| `v1.5.0` | `cb17fc40af39eb613452b0071060b45ce56dcf3c` | docs: README complet v1.5.0 |

## Comenzi locale

```bash
git fetch origin
git tag v1.4.0 4b03406b2176d16790820aef306b4ca04ac088ea
git tag v1.4.1 4566964dd3d3d9e861a58b6abee3a4d9952513f9
git tag v1.5.0 cb17fc40af39eb613452b0071060b45ce56dcf3c
git push origin v1.4.0 v1.4.1 v1.5.0
```
