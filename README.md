# Ferheng+ Data

This repository publishes the downloadable dictionary package used by Ferheng+ Android.

The dataset is **Kurmancî / Northern Kurdish centered**. Each entry has a Kurmancî headword and verified translations into Turkish, English, German, Sorani and Zazaki. Leki and Southern Kurdish (`lki`, `sdh`) are excluded. The merger keeps at most three translations per target language and at most fifteen translations per entry.

The Android application reads [`manifest.json`](./manifest.json), downloads the versioned gzip asset from the GitHub Release, verifies the compressed SHA-256, decompresses the SQLite database, verifies the uncompressed SHA-256, size and Room identity hash, and only then installs it.

The package contains 136,926 Kurmancî entries, 238,677 translations and Room schema identity hash `fa304dcdc2f42557b84b04352c89c70f`.

## Sources

The merged records preserve provenance from [Tirsik](https://tirsik.net/), [Ferheng.org](https://ferheng.org/), [ku.wiktionary.org](https://ku.wiktionary.org/wiki), [FreeDict](https://freedict.org/), [Vate Ferheng](https://ferheng.vate.com.tr/) and [Tatoeba](https://tatoeba.org/).
