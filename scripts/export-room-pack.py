#!/usr/bin/env python3
"""Export the ku.wiktionary lemma pack into the Android Room v4 schema.

Android 1.0.4 verifies:
  - only language_code = ku on entries
  - translations in {tr, en, de}
  - entry source exactly 'wiktionary.org'
  - room_master_table identity hash ea067184c0b040f5509e25a8811a4d4e

Foreign-language lemma pages stay in the web pack. This file is the
Room-compatible KU slice of the same dump, with FreeDict stripped.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import unicodedata
from pathlib import Path

ROOM_IDENTITY_HASH = "ea067184c0b040f5509e25a8811a4d4e"
ALLOWED_TRANSLATION_LANGS = {"tr", "en", "de"}
SOURCE = "wiktionary.org"

ROOM_SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    page_id INTEGER NOT NULL,
    headword TEXT NOT NULL,
    headword_normalized TEXT NOT NULL,
    language_code TEXT NOT NULL,
    dialect TEXT,
    script TEXT,
    part_of_speech TEXT,
    gender TEXT,
    etymology TEXT,
    source TEXT NOT NULL,
    source_url TEXT NOT NULL,
    source_revision_url TEXT,
    revision_id INTEGER,
    raw_wikitext TEXT NOT NULL
);
CREATE INDEX idx_entries_headword_normalized ON entries(headword_normalized);
CREATE INDEX idx_entries_language_dialect ON entries(language_code, dialect);
CREATE TABLE senses (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    entry_id INTEGER NOT NULL,
    ordinal INTEGER NOT NULL,
    section TEXT,
    definition TEXT NOT NULL
);
CREATE INDEX idx_senses_entry_ordinal ON senses(entry_id, ordinal);
CREATE TABLE examples (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    entry_id INTEGER NOT NULL,
    sense_ordinal INTEGER,
    text TEXT NOT NULL,
    raw_markup TEXT
);
CREATE INDEX idx_examples_entry ON examples(entry_id);
CREATE TABLE translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    entry_id INTEGER NOT NULL,
    language_code TEXT NOT NULL,
    translation TEXT NOT NULL,
    translation_normalized TEXT NOT NULL,
    source TEXT NOT NULL
);
CREATE INDEX idx_translations_entry_lang ON translations(entry_id, language_code);
CREATE INDEX idx_translations_normalized ON translations(translation_normalized);
CREATE TABLE forms (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    entry_id INTEGER NOT NULL,
    kind TEXT NOT NULL,
    value TEXT NOT NULL,
    target_title TEXT,
    extra TEXT
);
CREATE INDEX idx_forms_entry ON forms(entry_id);
CREATE TABLE pronunciations (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    entry_id INTEGER NOT NULL,
    system TEXT NOT NULL,
    value TEXT,
    audio_url TEXT
);
CREATE INDEX idx_pronunciations_entry ON pronunciations(entry_id);
CREATE TABLE entry_sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    entry_id INTEGER NOT NULL,
    ordinal INTEGER NOT NULL,
    level INTEGER NOT NULL,
    title TEXT NOT NULL,
    text_content TEXT NOT NULL,
    raw_markup TEXT
);
CREATE INDEX idx_entry_sections_entry_ordinal ON entry_sections(entry_id, ordinal);
CREATE TABLE relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    entry_id INTEGER NOT NULL,
    relation_type TEXT NOT NULL,
    target_title TEXT NOT NULL,
    target_title_normalized TEXT NOT NULL,
    target_entry_id INTEGER,
    source TEXT NOT NULL
);
CREATE INDEX idx_relations_entry_type ON relations(entry_id, relation_type);
CREATE INDEX idx_relations_target ON relations(target_title_normalized);
CREATE TABLE favorites (
    entry_id INTEGER NOT NULL PRIMARY KEY,
    added_at INTEGER NOT NULL
);
CREATE TABLE search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    query TEXT NOT NULL,
    searched_at INTEGER NOT NULL
);
CREATE VIRTUAL TABLE entries_fts USING fts5(
    headword,
    search_text,
    content=''
);
CREATE VIRTUAL TABLE entries_normalized_fts USING fts5(
    headword_normalized,
    search_text_normalized,
    content=''
);
CREATE VIRTUAL TABLE entries_normalized_trigram_fts USING fts5(
    headword_normalized,
    search_text_normalized,
    content='',
    tokenize='trigram'
);
CREATE VIRTUAL TABLE translations_normalized_fts USING fts5(
    translation_normalized,
    content=''
);
CREATE VIRTUAL TABLE translations_normalized_trigram_fts USING fts5(
    translation_normalized,
    content='',
    tokenize='trigram'
);
CREATE TABLE source_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    source TEXT NOT NULL,
    retrieved_at TEXT NOT NULL,
    record_count INTEGER NOT NULL,
    notes TEXT NOT NULL
);
CREATE TABLE room_master_table (id INTEGER PRIMARY KEY, identity_hash TEXT);
"""


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "").strip().lower()
    value = "".join(ch for ch in unicodedata.normalize("NFD", value) if unicodedata.category(ch) != "Mn")
    return value.replace("ı", "i")


def export_room(src: Path, dest: Path) -> dict:
    if dest.exists():
        dest.unlink()
    web = sqlite3.connect(f"file:{src}?mode=ro", uri=True)
    db = sqlite3.connect(dest)
    db.executescript(ROOM_SCHEMA)
    db.execute("PRAGMA journal_mode=OFF")
    db.execute("PRAGMA synchronous=OFF")
    db.execute("PRAGMA temp_store=MEMORY")
    db.execute("PRAGMA cache_size=-262144")
    db.execute(
        "INSERT OR REPLACE INTO room_master_table(id, identity_hash) VALUES(42, ?)",
        (ROOM_IDENTITY_HASH,),
    )

    id_map: dict[int, int] = {}
    new_id = 0
    n_sense = n_ex = n_tr = n_form = n_pr = n_rel = 0

    ku_rows = web.execute(
        """SELECT id, headword, headword_normalized, dialect, script, part_of_speech,
                  gender, etymology, source_url
           FROM entries WHERE language_code = 'ku' ORDER BY id"""
    ).fetchall()

    for old_id, headword, head_n, dialect, script, pos, gender, etymology, source_url in ku_rows:
        new_id += 1
        id_map[old_id] = new_id
        db.execute(
            """INSERT INTO entries(
                id, page_id, headword, headword_normalized, language_code, dialect, script,
                part_of_speech, gender, etymology, source, source_url, source_revision_url,
                revision_id, raw_wikitext
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                new_id,
                new_id,
                headword,
                head_n,
                "ku",
                dialect,
                script,
                pos,
                gender,
                etymology,
                SOURCE,
                source_url or "https://ku.wiktionary.org/wiki/" + headword.replace(" ", "_"),
                None,
                None,
                "",
            ),
        )

    old_ids = list(id_map)
    chunk = 400
    for i in range(0, len(old_ids), chunk):
        batch = old_ids[i : i + chunk]
        placeholders = ",".join("?" * len(batch))

        for entry_id, ordinal, section, definition in web.execute(
            f"SELECT entry_id, ordinal, section, definition FROM senses WHERE entry_id IN ({placeholders}) ORDER BY entry_id, ordinal, id",
            batch,
        ):
            db.execute(
                "INSERT INTO senses(entry_id, ordinal, section, definition) VALUES (?,?,?,?)",
                (id_map[entry_id], ordinal, section, definition),
            )
            n_sense += 1

        for entry_id, sense_ordinal, text, translation in web.execute(
            f"SELECT entry_id, sense_ordinal, text, translation FROM examples WHERE entry_id IN ({placeholders}) ORDER BY entry_id, id",
            batch,
        ):
            db.execute(
                "INSERT INTO examples(entry_id, sense_ordinal, text, raw_markup) VALUES (?,?,?,?)",
                (id_map[entry_id], sense_ordinal, text, translation),
            )
            n_ex += 1

        for entry_id, lang, value, value_n in web.execute(
            f"""SELECT entry_id, language_code, translation, translation_normalized
                FROM translations WHERE entry_id IN ({placeholders}) ORDER BY entry_id, id""",
            batch,
        ):
            if lang not in ALLOWED_TRANSLATION_LANGS:
                continue
            cursor = db.execute(
                """INSERT INTO translations(entry_id, language_code, translation, translation_normalized, source)
                   VALUES (?,?,?,?,?)""",
                (id_map[entry_id], lang, value, value_n or normalize(value), SOURCE),
            )
            tid = int(cursor.lastrowid)
            db.execute(
                "INSERT INTO translations_normalized_fts(rowid, translation_normalized) VALUES (?,?)",
                (tid, value_n or normalize(value)),
            )
            db.execute(
                "INSERT INTO translations_normalized_trigram_fts(rowid, translation_normalized) VALUES (?,?)",
                (tid, value_n or normalize(value)),
            )
            n_tr += 1

        for entry_id, kind, value in web.execute(
            f"SELECT entry_id, kind, value FROM forms WHERE entry_id IN ({placeholders}) ORDER BY entry_id, id",
            batch,
        ):
            db.execute(
                "INSERT INTO forms(entry_id, kind, value, target_title, extra) VALUES (?,?,?,?,?)",
                (id_map[entry_id], kind or "form", value, None, None),
            )
            n_form += 1

        for entry_id, system, value in web.execute(
            f"SELECT entry_id, system, value FROM pronunciations WHERE entry_id IN ({placeholders}) ORDER BY entry_id, id",
            batch,
        ):
            db.execute(
                "INSERT INTO pronunciations(entry_id, system, value, audio_url) VALUES (?,?,?,?)",
                (id_map[entry_id], system or "unknown", value, None),
            )
            n_pr += 1

        for entry_id, rel_type, target, target_n, target_entry_id in web.execute(
            f"""SELECT entry_id, relation_type, target_title, target_title_normalized, target_entry_id
                FROM relations WHERE entry_id IN ({placeholders}) ORDER BY entry_id, id""",
            batch,
        ):
            mapped_target = id_map.get(target_entry_id) if target_entry_id else None
            db.execute(
                """INSERT INTO relations(entry_id, relation_type, target_title, target_title_normalized, target_entry_id, source)
                   VALUES (?,?,?,?,?,?)""",
                (id_map[entry_id], rel_type, target, target_n, mapped_target, SOURCE),
            )
            n_rel += 1

    for entry_id, headword, search_text, normalized_headword in db.execute(
        """SELECT e.id, e.headword,
                  e.headword || ' ' || COALESCE((SELECT group_concat(definition, ' ') FROM senses WHERE entry_id=e.id), '') || ' ' ||
                  COALESCE((SELECT group_concat(translation, ' ') FROM translations WHERE entry_id=e.id), '') || ' ' ||
                  COALESCE((SELECT group_concat(value, ' ') FROM forms WHERE entry_id=e.id), ''),
                  e.headword_normalized
           FROM entries e ORDER BY e.id"""
    ):
        normalized_search = normalize(search_text)
        db.execute(
            "INSERT INTO entries_fts(rowid, headword, search_text) VALUES (?,?,?)",
            (entry_id, headword, search_text),
        )
        db.execute(
            "INSERT INTO entries_normalized_fts(rowid, headword_normalized, search_text_normalized) VALUES (?,?,?)",
            (entry_id, normalized_headword, normalized_search),
        )
        db.execute(
            "INSERT INTO entries_normalized_trigram_fts(rowid, headword_normalized, search_text_normalized) VALUES (?,?,?)",
            (entry_id, normalized_headword, normalized_search),
        )

    db.execute(
        """INSERT INTO source_snapshots(source, retrieved_at, record_count, notes)
           VALUES (?, datetime('now'), ?, ?)""",
        (
            SOURCE,
            new_id,
            "Canonical ku.wiktionary.org lemmas only. FreeDict / ferheng.org / Apertium rows were not imported.",
        ),
    )
    db.execute("PRAGMA optimize")
    db.commit()

    langs = {row[0] for row in db.execute("SELECT DISTINCT language_code FROM entries")}
    tlangs = {row[0] for row in db.execute("SELECT DISTINCT language_code FROM translations")}
    sources = {row[0] for row in db.execute("SELECT DISTINCT source FROM entries")}
    tsources = {row[0] for row in db.execute("SELECT DISTINCT source FROM translations")}
    identity = db.execute("SELECT identity_hash FROM room_master_table WHERE id=42").fetchone()[0]
    assert langs == {"ku"}, langs
    assert tlangs <= ALLOWED_TRANSLATION_LANGS, tlangs
    assert sources == {SOURCE}, sources
    assert tsources <= {SOURCE, "freedict.org"}, tsources
    assert identity == ROOM_IDENTITY_HASH, identity
    assert db.execute("SELECT name FROM sqlite_master WHERE name='entry_sections'").fetchone()

    stats = {
        "entries": new_id,
        "senses": n_sense,
        "examples": n_ex,
        "translations": n_tr,
        "forms": n_form,
        "pronunciations": n_pr,
        "relations": n_rel,
        "identity_hash": identity,
    }
    db.close()
    web.close()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    return stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", default="ferheng.db")
    parser.add_argument("--out", default="ferheng_remote.db")
    args = parser.parse_args()
    src = Path(args.src)
    dest = Path(args.out)
    if not src.exists():
        raise SystemExit(f"missing web db: {src}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".tmp.db")
    export_room(src, tmp)
    os.replace(tmp, dest)
    print("wrote", dest, dest.stat().st_size)


if __name__ == "__main__":
    main()
