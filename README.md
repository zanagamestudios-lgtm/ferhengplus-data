# Ferheng+ Dictionary Data

Ferheng+ is a **Kurmancî-centered dictionary**. Every production entry is a Kurmancî (`ku`) headword. Target-language values are stored separately and are limited to at most three values per selected target language: Türkçe (`tr`), English (`en`), Deutsch (`de`), Soranî (`ckb`) and Zazakî (`zza`). Lekî (`lki`), Southern Kurdish (`sdh`) and all non-Kurmancî source sections are excluded from the production package.

The sole canonical source is [ku.wiktionary.org](https://ku.wiktionary.org/wiki/Destp%C3%AAk), accessed through the [MediaWiki Action API](https://www.mediawiki.org/wiki/API:Action_API). The detail model preserves the page’s structured meaning: senses, examples, pronunciation, grammatical forms, gender metadata, etymology and resolvable inline links. Translation subpages such as `/Werger` are treated as part of the same ku.wiktionary source, and only the five application target languages are retained. No FreeDict, Vate, Ferheng.org, Tirsik, Tatoeba, reverse dictionary merge or user bridge is included in this package.

The Android application downloads a verified gzip SQLite package from a GitHub Release. The dictionary database is not embedded in the APK.

## Current package

The current manifest is available at [`manifest.json`](./manifest.json). The v1.3.1 release asset is `ferheng_remote.db.gz`.

| Field | Value |
|---|---:|
| Room schema | v3 |
| Room identity hash | `dfb9e345547fa7fb813ab302c82fbbd5` |
| Kurmancî entries | 4,263 |
| Sense rows | 5,895 |
| Translation rows | 7,592 |
| Example rows | 634 |
| Form rows | 2,887 |
| Pronunciation rows | 1,574 |
| Relation rows | 22,392 |
| Entries with gender metadata | 2,241 |
| Source snapshots | 1 (`wiktionary.org`) |
| Maximum translations per target language | 3 |
| Maximum translations per entry | 15 |
| Canonical source | [ku.wiktionary.org Destpêk](https://ku.wiktionary.org/wiki/Destp%C3%AAk) |

## Verification

The package is checked for Room schema compatibility, `ku`-only entries, the allowed target-language set, source purity, empty records, duplicate translations, FTS integrity, character-folded search, and resolvable relation targets. The app displays the active target-language card first on a word detail page; Kurmancî definitions and other structured fields follow below it.

The privacy policy is available at [`PRIVACY_POLICY.md`](./PRIVACY_POLICY.md). It is a product-specific working draft and should be reviewed by qualified legal counsel before use as a final legal notice.
