#!/usr/bin/env python3
"""
FTS5 Session Search — Inspired by Hermes Agent's full-text search.
Creates a SQLite database with FTS5 index over all memory files and
provides search capabilities across session history.

Supports: keyword search, phrase search, boolean operators, filtered search.
"""

import os
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/wls/.openclaw/workspace-lisa"))
MEMORY_DIR = WORKSPACE / "memory"
DB_PATH = WORKSPACE / "memory" / "index" / "sessions.db"

def get_db():
    """Get or create the SQLite database with FTS5."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(DB_PATH))
    db.execute("PRAGMA journal_mode=WAL")
    _init_schema(db)
    return db

def _init_schema(db):
    """Initialize database schema with FTS5."""
    db.executescript("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            title TEXT,
            category TEXT,
            source TEXT DEFAULT 'memory',
            indexed_at REAL NOT NULL,
            content_hash TEXT,
            UNIQUE(path, content_hash)
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(
            title,
            content
        );

        CREATE INDEX IF NOT EXISTS idx_documents_path ON documents(path);
        CREATE INDEX IF NOT EXISTS idx_documents_category ON documents(category);
    """)

    # Create FTS triggers
    db.executescript("""
        -- FTS sync is handled manually in code (not via triggers) to avoid schema issues
        -- with content= sync mode requiring content table column
    """)

def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def index_memory_files():
    """Index all memory/*.md files into the FTS5 database."""
    db = get_db()
    indexed = 0
    skipped = 0

    if not MEMORY_DIR.exists():
        return {"indexed": 0, "skipped": 0}

    for md_file in MEMORY_DIR.glob("*.md"):
        if md_file.name == "nudge_state.json":
            continue
        content = md_file.read_text(errors="replace")
        if not content.strip():
            continue

        chash = content_hash(content)
        path = str(md_file.relative_to(WORKSPACE))

        # Check if already indexed with same hash
        existing = db.execute(
            "SELECT id FROM documents WHERE path=? AND content_hash=?",
            (path, chash)
        ).fetchone()

        if existing:
            skipped += 1
            continue

        # Remove old version if path exists with different hash
        db.execute("DELETE FROM documents WHERE path=?", (path,))

        # Determine category
        category = "daily" if md_file.stem.startswith("20") else "other"

        db.execute(
            "INSERT INTO documents (path, title, category, indexed_at, content_hash) VALUES (?, ?, ?, ?, ?)",
            (path, md_file.stem, category, datetime.now().timestamp(), chash)
        )

        # Insert into FTS5
        db.execute("INSERT INTO docs_fts(title, content) VALUES (?, ?)", (md_file.stem, content))
        indexed += 1

    db.commit()
    db.close()
    return {"indexed": indexed, "skipped": skipped}

def search(query: str, category: str = None, limit: int = 10):
    """Search across all indexed documents using FTS5."""
    db = get_db()

    # Sanitize query for FTS5
    safe_query = _sanitize_fts5(query)

    if category:
        sql = """
            SELECT d.path, d.title, d.category, snippet(docs_fts, 1, '>>>', '<<<', '...', 30) as snippet
            FROM docs_fts f
            JOIN documents d ON d.title = f.title
            WHERE docs_fts MATCH ? AND d.category = ?
            ORDER BY rank
            LIMIT ?
        """
        results = db.execute(sql, (safe_query, category, limit)).fetchall()
    else:
        sql = """
            SELECT d.path, d.title, d.category, snippet(docs_fts, 1, '>>>', '<<<', '...', 30) as snippet
            FROM docs_fts f
            JOIN documents d ON d.title = f.title
            WHERE docs_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """
        results = db.execute(sql, (safe_query, limit)).fetchall()

    db.close()
    return [
        {"path": r[0], "title": r[1], "category": r[2], "snippet": r[3]}
        for r in results
    ]

def _sanitize_fts5(query: str) -> str:
    """Sanitize user input for FTS5 query syntax."""
    import re
    # Remove dangerous characters
    query = re.sub(r'[^\w\s"\'*ANDORNOT-]', '', query)
    # Balance quotes
    if query.count('"') % 2 != 0:
        query = query.rstrip('"') + '"'
    # Remove dangling operators
    query = re.sub(r'\b(AND|OR|NOT)\s*$', '', query)
    if not query.strip():
        return '"*"'
    return query

def get_stats():
    """Get index statistics."""
    db = get_db()
    total_docs = db.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    categories = db.execute(
        "SELECT category, COUNT(*) FROM documents GROUP BY category"
    ).fetchall()
    db.close()
    return {"total_documents": total_docs, "categories": dict(categories)}

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Search mode
        query = " ".join(sys.argv[1:])
        print(f"🔍 Searching: {query}")
        results = search(query)
        if results:
            for r in results:
                print(f"\n📄 {r['title']} ({r['category']})")
                print(f"   Path: {r['path']}")
                print(f"   {r['snippet']}")
        else:
            print("No results found.")
    else:
        # Index mode
        print("📚 Indexing memory files...")
        result = index_memory_files()
        stats = get_stats()
        print(f"✅ Indexed: {result['indexed']} new, {result['skipped']} unchanged")
        print(f"📊 Total: {stats['total_documents']} documents")
        for cat, count in stats['categories'].items():
            print(f"   {cat}: {count}")