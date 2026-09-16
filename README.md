# Ferheng+ Dictionary Data

Ferheng+ is a **Kurmancî-centered dictionary** sourced **only** from [ku.wiktionary.org](https://ku.wiktionary.org/wiki/Destp%C3%AAk).

Each search result is **one Wiktionary lemma page**. Turkish / English / German pages keep their numbered Kurdish senses under a single heading — the same structure as on Wiktionary:

```
içmek
1. vexwarin, noşîn, noştin, aşaftin
2. kişandin (ji bo cixare û wekî wê)
3. vexwarin (ji bo mêtînê)
4. vexwarin (ji bo vexwarina alkolê)
```

Inflected *form-of* records are aliases of the lemma, not separate cards.
**ferheng.org, FreeDict and Apertium are not mixed in.**

The extract is the official [kaikki.org kuwiktionary wiktextract](https://kaikki.org/kuwiktionary/rawdata.html) (CC BY-SA 4.0).

## Current packages

| Package | Tag | Use |
|---|---|---|
| Android Room v4 (`ferheng_remote.db.gz`) | [v2.3.0](https://github.com/zanagamestudios-lgtm/ferhengplus-data/releases/tag/v2.3.0) | Existing Android app |
| Lemma pack (`ferheng_web.db.gz`) | [v2.4.0](https://github.com/zanagamestudios-lgtm/ferhengplus-data/releases/tag/v2.4.0) | Web app + Wiktionary-style grouping |

### v2.4.0 lemma pack

| Field | Value |
|---|---:|
| Kurmancî lemmas | 119,926 |
| Tirkî lemmas | 67,726 |
| English lemmas | 65,577 |
| Deutsch lemmas | 28,319 |
| Total lemmas | 281,548 |
| Senses | 350,576 |
| Translation rows | 641,974 |
| Source | ku.wiktionary.org only |

Rebuild:

```
python3 scripts/rebuild-ku-wiktionary.py \
  --src kuwiki.jsonl.gz \
  --out ferheng.db
```

The GitHub Action `.github/workflows/build-ku-wiktionary.yml` downloads the wiktextract dump and publishes `ferheng_web.db.gz` as release **v2.4.0**.

## Policy

- One ku.wiktionary lemma page per search result.
- Reverse lookup (TR/EN/DE → KU) uses the foreign-language page on ku.wiktionary, not a scatter of Kurdish headwords.
- No secondary dictionary rows.
