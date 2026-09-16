# Ferheng+ Dictionary Data

Single source: [ku.wiktionary.org](https://ku.wiktionary.org/wiki/Destp%C3%AAk)
via the [kaikki.org kuwiktionary wiktextract](https://kaikki.org/kuwiktionary/rawdata.html) (CC BY-SA 4.0).

**Older packages (v1.0.0-v2.4.0) were deleted.** This tag is the only published dataset.

Each search result is **one Wiktionary lemma page**. Turkish / English / German pages keep numbered Kurdish senses under a single heading.

Inflected *form-of* records are aliases of the lemma, not separate cards.
**ferheng.org, FreeDict and Apertium are not mixed in.**

## Current package — v2.5.0

| Pack | File | Use |
|---|---|---|
| Android Room v4 | `ferheng_remote.db.gz` | Existing Android app (KU entries only) |
| Web lemma pack | `ferheng_web.db.gz` | Web app + Wiktionary-style grouping (KU/TR/EN/DE lemmas) |

### Lemma counts (web pack)

| Language | Lemmas |
|---|---:|
| Kurmancî | 119,926 |
| Tirkî | 67,726 |
| English | 65,577 |
| Deutsch | 28,319 |
| **Total** | **281,548** |

Android pack: 119,926 Kurmancî lemmas, 260,916 TR/EN/DE translations.

Rebuild:

```
python3 scripts/rebuild-ku-wiktionary.py --src kuwiki.jsonl.gz --out ferheng.db
python3 scripts/export-room-pack.py --src ferheng.db --out ferheng_remote.db
```

## Policy

- One ku.wiktionary lemma page per search result.
- Reverse lookup (TR/EN/DE → KU) uses the foreign-language page on ku.wiktionary.
- No secondary dictionary rows.
