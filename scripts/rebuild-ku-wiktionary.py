#!/usr/bin/env python3
"""Rebuild Ferheng+ from ku.wiktionary.org only (kaikki.org wiktextract).

One Wiktionary lemma page = one search result. Turkish/English/German pages
keep their numbered Kurdish senses under a single heading.
Inflected form-of records become aliases, not separate cards.
No ferheng.org / FreeDict / Apertium rows.
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sqlite3
import unicodedata
from collections import defaultdict
from pathlib import Path

LANGS = {"ku", "tr", "en", "de"}
SPACE = re.compile(r"\s+")
PAREN = re.compile(r"\s*\([^)]*\)")
SPLIT = re.compile(r"\s*[,;|/]\s*")
POS_MAP = {
    "noun": "Navder",
    "verb": "Leker",
    "adj": "Rengder",
    "adv": "Hoker",
    "name": "Nav",
    "phrase": "Hevok",
    "proverb": "Gotin",
    "prep": "Dacek",
    "pron": "Cinav",
    "num": "Hejmar",
    "prefix": "Pesgir",
    "suffix": "Pasgir",
    "abbrev": "Kurtenav",
    "conj": "Giredek",
    "unknown": "",
}

def norm(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "").strip().lower()
    value = "".join(ch for ch in unicodedata.normalize("NFD", value) if unicodedata.category(ch) != "Mn")
    return SPACE.sub(" ", value.replace("\u0131", "i").replace("\u0130", "i")).strip()

def lemma(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "").strip()
    return SPACE.sub(" ", value).strip(" \t-\u2013,;")

def map_pos(raw: str, title: str = "") -> str:
    token = (raw or "").lower()
    if token in POS_MAP and POS_MAP[token]:
        return POS_MAP[token]
    title = unicodedata.normalize("NFC", title or "").strip()
    return title or (raw or "").capitalize() or "\u2014"

def is_form_of(obj: dict) -> bool:
    tags = set(obj.get("tags") or [])
    if "form-of" in tags or "inflection-of" in tags:
        return True
    for sense in obj.get("senses") or []:
        stags = set(sense.get("tags") or [])
        if "form-of" in stags or "inflection-of" in stags or sense.get("form_of"):
            return True
    return False

def gender_of(obj: dict):
    tags = set(obj.get("tags") or [])
    if "feminine" in tags:
        return "me"
    if "masculine" in tags:
        return "ner"
    return None

def ku_parts(gloss: str) -> list:
    cleaned = PAREN.sub("", gloss or "")
    out = []
    seen = set()
    for part in SPLIT.split(cleaned):
        item = lemma(part)
        key = norm(item)
        if not item or not key or len(item) > 60 or key in seen:
            continue
        if not re.search(r"[A-Za-z]", item):
            continue
        seen.add(key)
        out.append(item)
    return out

def form_targets(obj: dict) -> list:
    found = []
    for sense in obj.get("senses") or []:
        for item in sense.get("form_of") or []:
            word = lemma(str(item.get("word") or item.get("title") or ""))
            if word:
                found.append(word)
        for item in sense.get("alt_of") or []:
            word = lemma(str(item.get("word") or ""))
            if word:
                found.append(word)
    return found

class Lemma:
    def __init__(self, headword: str, lang: str) -> None:
        self.headword = headword
        self.lang = lang
        self.pos = []
        self.gender = None
        self.etymology = ""
        self.senses = []
        self.examples = []
        self.translations = defaultdict(list)
        self.forms = []
        self.pronunciations = []
        self.relations = []
        self.source_url = f"https://ku.wiktionary.org/wiki/{headword.replace(' ', '_')}"
    def add_pos(self, pos: str) -> None:
        if pos and pos not in self.pos and pos != "\u2014":
            self.pos.append(pos)
    def add_translation(self, lang: str, value: str) -> None:
        if lang not in LANGS:
            return
        item = lemma(value)
        key = norm(item)
        if not item or not key:
            return
        existing = {norm(x) for x in self.translations[lang]}
        if key not in existing:
            self.translations[lang].append(item)

def ingest(path: Path):
    lemmas = {}
    aliases = []
    scanned = 0
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            scanned += 1
            obj = json.loads(line)
            lang = str(obj.get("lang_code") or "")
            if lang not in LANGS:
                continue
            word = lemma(str(obj.get("word") or ""))
            if not word or len(word) > 80:
                continue
            key = (norm(word), lang)
            if not key[0]:
                continue
            if is_form_of(obj):
                for target in form_targets(obj):
                    aliases.append((word, lang, target, str(obj.get("pos") or "form")))
                continue
            entry = lemmas.get(key)
            if entry is None:
                entry = Lemma(word, lang)
                lemmas[key] = entry
            entry.add_pos(map_pos(str(obj.get("pos") or ""), str(obj.get("pos_title") or "")))
            if not entry.gender:
                entry.gender = gender_of(obj)
            etym = " ".join(str(x) for x in (obj.get("etymology_texts") or []) if x)
            if etym and len(etym) > len(entry.etymology):
                entry.etymology = etym[:2000]
            pos_label = entry.pos[-1] if entry.pos else ""
            for sense in obj.get("senses") or []:
                glosses = [lemma(str(g)) for g in (sense.get("glosses") or []) if lemma(str(g))]
                if not glosses:
                    continue
                definition = glosses[0]
                ordinal = len(entry.senses) + 1
                entry.senses.append((ordinal, pos_label, definition))
                if lang != "ku":
                    for part in ku_parts(definition):
                        entry.add_translation("ku", part)
                for example in sense.get("examples") or []:
                    text = lemma(str(example.get("text") or ""))
                    if not text:
                        continue
                    trans = lemma(str(example.get("translation") or ""))
                    entry.examples.append((ordinal, text, trans))
            for row in obj.get("translations") or []:
                code = str(row.get("lang_code") or "")
                if code in LANGS and code != lang:
                    entry.add_translation(code, str(row.get("word") or ""))
            for row in obj.get("forms") or []:
                form = lemma(str(row.get("form") or row.get("word") or ""))
                if form and norm(form) != key[0]:
                    kind = ",".join(row.get("tags") or []) or "form"
                    entry.forms.append((kind, form))
            for sound in obj.get("sounds") or []:
                ipa = lemma(str(sound.get("ipa") or sound.get("other") or ""))
                if ipa:
                    entry.pronunciations.append(("ipa", ipa))
            for rel_type, field in (("synonym", "synonyms"), ("derived", "derived"), ("related", "related")):
                for row in obj.get(field) or []:
                    target = lemma(str(row.get("word") or row.get("title") or ""))
                    if target:
                        entry.relations.append((rel_type, target))
    print(json.dumps({"scanned": scanned, "lemmas": len(lemmas), "aliases": len(aliases)}))
    return lemmas, aliases

SCHEMA = """
PRAGMA journal_mode=OFF;
PRAGMA synchronous=OFF;
PRAGMA temp_store=MEMORY;
PRAGMA foreign_keys=OFF;
DROP TABLE IF EXISTS entries_normalized_fts;
DROP TABLE IF EXISTS translations_normalized_fts;
DROP TABLE IF EXISTS relations;
DROP TABLE IF EXISTS pronunciations;
DROP TABLE IF EXISTS forms;
DROP TABLE IF EXISTS examples;
DROP TABLE IF EXISTS translations;
DROP TABLE IF EXISTS senses;
DROP TABLE IF EXISTS entries;
DROP TABLE IF EXISTS meta;
CREATE TABLE entries (
  id INTEGER PRIMARY KEY,
  headword TEXT NOT NULL,
  headword_normalized TEXT NOT NULL,
  language_code TEXT NOT NULL,
  dialect TEXT,
  script TEXT,
  part_of_speech TEXT,
  gender TEXT,
  etymology TEXT,
  source TEXT NOT NULL,
  source_url TEXT NOT NULL
);
CREATE INDEX idx_entries_lang_head ON entries(language_code, headword_normalized);
CREATE TABLE senses (
  id INTEGER PRIMARY KEY,
  entry_id INTEGER NOT NULL,
  ordinal INTEGER NOT NULL,
  section TEXT,
  definition TEXT NOT NULL
);
CREATE TABLE examples (
  id INTEGER PRIMARY KEY,
  entry_id INTEGER NOT NULL,
  sense_ordinal INTEGER,
  text TEXT NOT NULL,
  translation TEXT
);
CREATE TABLE translations (
  id INTEGER PRIMARY KEY,
  entry_id INTEGER NOT NULL,
  language_code TEXT NOT NULL,
  translation TEXT NOT NULL,
  translation_normalized TEXT NOT NULL,
  source TEXT NOT NULL
);
CREATE INDEX idx_translations_normalized ON translations(language_code, translation_normalized);
CREATE TABLE forms (
  id INTEGER PRIMARY KEY,
  entry_id INTEGER NOT NULL,
  kind TEXT,
  value TEXT NOT NULL,
  value_normalized TEXT NOT NULL
);
CREATE INDEX idx_forms_value ON forms(value_normalized);
CREATE TABLE pronunciations (
  id INTEGER PRIMARY KEY,
  entry_id INTEGER NOT NULL,
  system TEXT,
  value TEXT
);
CREATE TABLE relations (
  id INTEGER PRIMARY KEY,
  entry_id INTEGER NOT NULL,
  relation_type TEXT NOT NULL,
  target_title TEXT NOT NULL,
  target_title_normalized TEXT NOT NULL,
  target_entry_id INTEGER
);
CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
"""

def write_db(lemmas, aliases, dest: Path):
    if dest.exists():
        dest.unlink()
    db = sqlite3.connect(dest)
    db.executescript(SCHEMA)
    lookup = {}
    eid = 0
    n_sense = n_ex = n_tr = n_form = 0
    for (nword, lang), entry in lemmas.items():
        if not entry.senses and not any(entry.translations.values()):
            continue
        eid += 1
        lookup[(nword, lang)] = eid
        db.execute(
            "INSERT INTO entries(id, headword, headword_normalized, language_code, dialect, script, part_of_speech, gender, etymology, source, source_url) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (eid, entry.headword, nword, lang, None, None, " \u00b7 ".join(entry.pos) or "\u2014", entry.gender, entry.etymology, "ku.wiktionary.org", entry.source_url),
        )
        for ordinal, section, definition in entry.senses:
            db.execute("INSERT INTO senses(entry_id, ordinal, section, definition) VALUES (?,?,?,?)", (eid, ordinal, section, definition))
            n_sense += 1
        for ordinal, text, trans in entry.examples[:12]:
            db.execute("INSERT INTO examples(entry_id, sense_ordinal, text, translation) VALUES (?,?,?,?)", (eid, ordinal, text, trans or None))
            n_ex += 1
        for tlang, values in entry.translations.items():
            for value in values:
                db.execute("INSERT INTO translations(entry_id, language_code, translation, translation_normalized, source) VALUES (?,?,?,?,?)", (eid, tlang, value, norm(value), "ku.wiktionary.org"))
                n_tr += 1
        seen_forms = {nword}
        for kind, value in entry.forms:
            vn = norm(value)
            if not vn or vn in seen_forms:
                continue
            seen_forms.add(vn)
            db.execute("INSERT INTO forms(entry_id, kind, value, value_normalized) VALUES (?,?,?,?)", (eid, kind, value, vn))
            n_form += 1
        seen_ipa = set()
        for system, value in entry.pronunciations:
            if value in seen_ipa:
                continue
            seen_ipa.add(value)
            db.execute("INSERT INTO pronunciations(entry_id, system, value) VALUES (?,?,?)", (eid, system, value))
        seen_rel = set()
        for rel_type, target in entry.relations:
            tn = norm(target)
            rel_key = (rel_type, tn)
            if not tn or rel_key in seen_rel:
                continue
            seen_rel.add(rel_key)
            db.execute("INSERT INTO relations(entry_id, relation_type, target_title, target_title_normalized, target_entry_id) VALUES (?,?,?,?,?)", (eid, rel_type, target, tn, None))
    for form, lang, target, kind in aliases:
        parent = lookup.get((norm(target), lang))
        if not parent:
            continue
        vn = norm(form)
        if not vn:
            continue
        db.execute("INSERT INTO forms(entry_id, kind, value, value_normalized) VALUES (?,?,?,?)", (parent, kind or "form-of", form, vn))
        n_form += 1
    db.execute("CREATE VIRTUAL TABLE entries_normalized_fts USING fts5(headword_normalized, content='entries', content_rowid='id')")
    db.execute("CREATE VIRTUAL TABLE translations_normalized_fts USING fts5(translation_normalized, content='translations', content_rowid='id')")
    db.execute("INSERT INTO entries_normalized_fts(entries_normalized_fts) VALUES('rebuild')")
    db.execute("INSERT INTO translations_normalized_fts(translations_normalized_fts) VALUES('rebuild')")
    db.execute("INSERT INTO meta(key, value) VALUES('data_version','2026091702')")
    db.execute("INSERT INTO meta(key, value) VALUES('source','ku.wiktionary.org')")
    db.commit()
    stats = {"entries": eid, "senses": n_sense, "examples": n_ex, "translations": n_tr, "forms": n_form, "by_lang": dict(db.execute("SELECT language_code, COUNT(*) FROM entries GROUP BY 1"))}
    db.close()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    return stats

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", default="/tmp/enrich/kuwiki.jsonl.gz")
    parser.add_argument("--out", default="ferheng.db")
    args = parser.parse_args()
    src = Path(args.src)
    if not src.exists():
        raise SystemExit(f"missing dump: {src}")
    lemmas, aliases = ingest(src)
    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".tmp.db")
    write_db(lemmas, aliases, tmp)
    os.replace(tmp, dest)
    print("wrote", dest, dest.stat().st_size)

if __name__ == "__main__":
    main()
