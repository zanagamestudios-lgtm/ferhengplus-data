# Ferheng+ Flutter app data

`dictionary.json.gz` is a compact, app-optimised export of the Ferheng+ v2.5.0
Kurdish Wiktionary catalogue.

- Source: <https://ku.wiktionary.org> via the Ferheng+ rebuild kit
- Licence: CC BY-SA 4.0
- Entries: 119,926 Kurdish lemma entries
- Translations: 260,916 Turkish / English / German translations
- Shape: JSON schema version 1, gzip-compressed

## Files

| File | Purpose |
| --- | --- |
| `manifest.json` | Version, counts, sizes and SHA-256 checksums used by the app |
| `dictionary.json.gz` | Compressed app dataset downloaded on first launch |
| `export_app_dataset.py` | Reproducible exporter from `ferheng_remote.db` |

## Update procedure

1. Build the SQLite catalogue from the upstream Wiktionary dump.
2. Run `python3 export_app_dataset.py` (adjust paths at the top of the script).
3. Recompute `compressedBytes`, `rawBytes`, `compressedSha256`, `rawSha256` and
   update `dataVersion` / `generatedAt` in `manifest.json`.
4. Commit both files to `main`. Existing installations compare `dataVersion` and
   download the new archive only when it changes.

The app verifies the compressed and raw SHA-256 checksums before activating a
downloaded dataset. A failed download never replaces the last working cache.
