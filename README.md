# Ferheng+ Dictionary Data

Ferheng+ is a **Kurmancî-centered dictionary**. Every production entry is a Kurmancî (`ku`) language section from the official ku.wiktionary corpus. Target-language values are stored separately and are limited to at most three values per selected target language: Türkçe (`tr`), English (`en`), Deutsch (`de`), Soranî (`ckb`) and Zazakî (`zza`). Lekî (`lki`), Southern Kurdish (`sdh`) and non-Kurmancî source sections are excluded from the entry table.

The sole canonical source is [ku.wiktionary.org](https://ku.wiktionary.org/wiki/Destp%C3%AAk), collected from the official current [Wikimedia ku.wiktionary XML dump](https://dumps.wikimedia.org/kuwiktionary/latest/) and parsed according to the [MediaWiki Action API/page model](https://www.mediawiki.org/wiki/API:Action_API). The dump’s 1,036,065 main-namespace pages were scanned; 227,148 Kurmancî language sections were parsed and 227,145 unique page-language entries were retained after duplicate page-language removal.

Each entry preserves the complete Kurmancî section as raw wikitext and as ordered section records, in addition to structured senses, examples, pronunciation, grammatical forms, gender metadata, etymology, translation values and relations. This means that sections not yet mapped to a dedicated UI card remain available in the mobile detail page rather than being discarded. `/Werger`-style translation content is treated as part of the same ku.wiktionary source. No FreeDict, Vate, Ferheng.org, Tirsik, Tatoeba, reverse dictionary merge or user bridge is included.

The Android application downloads a verified gzip SQLite package from a GitHub Release. The dictionary database is not embedded in the APK.

## Current package

The current manifest is available at [`manifest.json`](./manifest.json). The current release asset is `ferheng_remote.db.gz` in v2.0.0.

| Field | Value |
|---|---:|
| Room schema | v4 |
| Room identity hash | `ea067184c0b040f5509e25a8811a4d4e` |
| Kurmancî entries | 227,145 |
| Sense rows | 251,569 |
| Translation rows | 186,729 |
| Example rows | 6,452 |
| Form rows | 27,380 |
| Pronunciation rows | 33,887 |
| Entry section rows | 576,130 |
| Relation rows | 736,618 |
| Entries with gender metadata | 24,066 |
| Resolved inline links | 630,566 |
| Source snapshots | 1 (`wiktionary.org`) |
| Maximum translations per target language | 3 |
| Maximum translations per entry | 15 |
| Canonical source | [ku.wiktionary.org Destpêk](https://ku.wiktionary.org/wiki/Destp%C3%AAk) |

## Verification

The package is checked for Room schema compatibility, `ku`-only entries, source purity, allowed target-language values, duplicate page-language removal, translation caps, empty section records, FTS integrity, character-folded search and resolvable inline relation targets. The app presents the active target-language card first on a word detail page, followed by the Kurmancî headword and all mapped and unmapped Wiktionary section content.

The privacy policy is available at [`PRIVACY_POLICY.md`](./PRIVACY_POLICY.md). It is a product-specific working draft and should be reviewed by qualified legal counsel before use as a final legal notice.
