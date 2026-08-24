# Ferheng+ Dictionary Data

Ferheng+ is a Kurmancî-centered multilingual dictionary. Each entry is a Kurmancî headword and may contain up to three verified translations per target language: Türkçe (`tr`), English (`en`), Deutsch (`de`), Soranî (`ckb`) and Zazakî (`zza`). Lekî (`lki`) and Southern Kurdish (`sdh`) are excluded from the application data model.

The canonical detail model is based on structured `ku.wiktionary.org` / MediaWiki content. It preserves definitions, examples, pronunciation, grammatical forms, gender metadata, etymology and resolvable inline links so that users can move from one word to another inside a definition. FreeDict is used only as a supplemental translation source. The Android application downloads a verified gzip SQLite package from a GitHub Release; the database is not embedded in the APK.

## Current package

The current manifest is available at [`manifest.json`](./manifest.json). The v1.2.0 release asset is `ferheng_remote.db.gz`.

- **Room schema:** v3
- **Room identity hash:** `dfb9e345547fa7fb813ab302c82fbbd5`
- **Kurmancî entries:** 136,021
- **Translation rows:** 261,418
- **Entries with gender metadata:** 2,289
- **Inline relations with resolved targets:** 15,235
- **Maximum translations per target language:** 3
- **Maximum translations per entry:** 15
- **Primary source:** [ku.wiktionary.org](https://ku.wiktionary.org/)
- **Supplemental source:** [FreeDict](https://freedict.org/)

## Verification

The package is checked before publication for Room schema compatibility, Kurmancî-only entries, target-language validity, empty records, duplicate translations, FTS integrity, character-folded search, and resolvable relation targets. The public Android-facing source labels are intentionally limited to Wiktionary and FreeDict.

The privacy policy is available at [`PRIVACY_POLICY.md`](./PRIVACY_POLICY.md). It is a product-specific working draft and should be reviewed by qualified legal counsel before use as a final legal notice.
