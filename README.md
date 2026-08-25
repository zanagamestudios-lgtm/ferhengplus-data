# Ferheng+ Dictionary Data

Ferheng+ is a **Kurmancî-centered dictionary**. Every production entry is a Kurmancî (`ku`) language section from the official ku.wiktionary corpus. The supported target languages are Türkçe (`tr`), English (`en`) and Deutsch (`de`); each target keeps at most three source-native Wiktionary equivalents per entry.

The sole canonical source is [ku.wiktionary.org](https://ku.wiktionary.org/wiki/Destp%C3%AAk), collected from the official current [Wikimedia ku.wiktionary XML dump](https://dumps.wikimedia.org/kuwiktionary/latest/) and parsed according to the [MediaWiki page/revision model](https://www.mediawiki.org/wiki/API:Action_API). The complete Kurmancî language-section scope is retained; no external dictionary, corpus, reverse dictionary merge or user bridge is included.

Each entry preserves structured senses, examples, pronunciation, grammatical forms, gender metadata, etymology, source-native translations, relations and ordered Wiktionary sections. The Android detail page shows the selected direction’s result first, then the Kurmancî headword and mapped Wiktionary information. Unmapped section content remains available as additional Wiktionary sections.

The Android application downloads a verified gzip SQLite package from a GitHub Release. The dictionary database is not embedded in the APK.

## Current package

The current manifest is available at [`manifest.json`](./manifest.json). The current release asset is `ferheng_remote.db.gz` in v2.1.0.

| Field | Value |
|---|---:|
| Room schema | v4 |
| Room identity hash | `ea067184c0b040f5509e25a8811a4d4e` |
| Kurmancî entries | 227,145 |
| Sense rows | 251,569 |
| Translation rows | 186,693 |
| Example rows | 6,452 |
| Form rows | 27,380 |
| Pronunciation rows | 33,887 |
| Entry section rows | 576,130 |
| Relation rows | 736,618 |
| Entries with gender metadata | 24,066 |
| Resolved inline links | 630,566 |
| Supported targets | Türkçe, English, Deutsch |
| Maximum translations per target language | 3 |
| Maximum translations per entry | 9 |
| Canonical source | [ku.wiktionary.org Destpêk](https://ku.wiktionary.org/wiki/Destp%C3%AAk) |

## Verification

The package is checked for Room schema compatibility, `ku`-only entries, source purity, supported target-language values, duplicate page-language removal, translation caps, empty section records, FTS integrity, character-folded search and resolvable inline relation targets. Search supports both directions for the six pairs `KU↔TR`, `KU↔EN` and `KU↔DE`.

The privacy policy is displayed entirely inside the Android application. The app does not redirect the user to the GitHub repository when the privacy policy is opened.
