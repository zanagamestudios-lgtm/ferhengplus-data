# Ferheng+ Data

This repository publishes the downloadable dictionary package used by Ferheng+ Android.

The dataset is **Kurmancî / Northern Kurdish centered**. Each entry has a Kurmancî headword and translations into Turkish, English, German, Sorani and Zazaki. Leki and Southern Kurdish (`lki`, `sdh`) are excluded. The cleaned merger keeps at most three unique translations per target language and at most fifteen translations per entry.

The Android application reads [`manifest.json`](./manifest.json), downloads the versioned gzip asset from the GitHub Release, verifies the compressed SHA-256, decompresses the SQLite database, verifies the uncompressed SHA-256, size and Room identity hash, and only then installs it.

The current package contains 136,021 Kurmancî entries and 261,418 translations. Its Room schema identity hash is `fa304dcdc2f42557b84b04352c89c70f`.

## Public source labels

The application displays only [Wiktionary](https://www.wiktionary.org/) and [FreeDict](https://freedict.org/) as public source labels. Raw payloads and source URLs remain internally preserved for data integrity and auditing, but additional source names are not listed in the application’s source description.

## Data quality

The supplied Zazaki corpus was processed as a separate input, normalized, deduplicated and cross-checked in both Zazaki-to-Turkish and Turkish-to-Zazaki directions before accepted translations were added to the Kurmancî-centered records. Empty, technically malformed and uncorroborated records were excluded. The final package enforces the three-translation-per-target-language cap.
