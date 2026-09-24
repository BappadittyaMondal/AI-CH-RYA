"""
Production Database Schema & Migration Architecture (§4, §5, §11, §26)
Provides relational and vector database schemas for PostgreSQL (with pgvector)
and SQLite (for local embedded development and testing).
"""

from typing import Dict, Any, List
import sqlite3


POSTGRES_PGVECTOR_DDL = """
-- PostgreSQL + pgvector Production Schema for AI ĀCHĀRYA
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 1. Canonical Texts Catalog (§4 Ontology)
CREATE TABLE IF NOT EXISTS canonical_texts (
    text_id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    text_type VARCHAR(64) NOT NULL,
    authority_rank INT NOT NULL,
    tradition VARCHAR(128),
    sakha_recension VARCHAR(128),
    is_mukhya BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 2. Verses & Chunks with pgvector embeddings (§11 Hybrid RAG)
CREATE TABLE IF NOT EXISTS verses (
    canonical_id VARCHAR(128) PRIMARY KEY,
    text_id VARCHAR(64) REFERENCES canonical_texts(text_id) ON DELETE CASCADE,
    chapter VARCHAR(32) NOT NULL,
    verse VARCHAR(32) NOT NULL,
    sanskrit_deva TEXT NOT NULL,
    iast TEXT NOT NULL,
    bengali TEXT,
    padaccheda JSONB NOT NULL DEFAULT '[]'::jsonb,
    meaning_summary TEXT NOT NULL,
    state VARCHAR(32) NOT NULL DEFAULT 'A — CANONICAL',
    is_superseded BOOLEAN DEFAULT FALSE,
    embedding vector(1536),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_verses_lookup ON verses(text_id, chapter, verse);
CREATE INDEX IF NOT EXISTS idx_verses_state ON verses(state);

-- 3. Commentaries & Hermeneutical Lineages (§12)
CREATE TABLE IF NOT EXISTS commentaries (
    commentary_id VARCHAR(128) PRIMARY KEY,
    verse_id VARCHAR(128) REFERENCES verses(canonical_id) ON DELETE CASCADE,
    commentator VARCHAR(128) NOT NULL,
    sampradaya VARCHAR(128) NOT NULL,
    textual_basis VARCHAR(255),
    core_claim TEXT NOT NULL,
    underlying_assumption TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_commentaries_verse ON commentaries(verse_id);
CREATE INDEX IF NOT EXISTS idx_commentaries_sampradaya ON commentaries(sampradaya);

-- 4. Atomic Claims Store (§15 Claim Engine)
CREATE TABLE IF NOT EXISTS atomic_claims (
    claim_id VARCHAR(64) PRIMARY KEY,
    claim_text TEXT NOT NULL,
    claim_type VARCHAR(64) NOT NULL,
    source_title VARCHAR(255) NOT NULL,
    source_url TEXT,
    evidence_nature VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'unverified',
    related_canonical_id VARCHAR(128),
    permanent_knowledge BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 5. Auditable Knowledge Version Lifecycle (§26)
CREATE TABLE IF NOT EXISTS audit_events (
    event_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id VARCHAR(128) NOT NULL,
    from_state VARCHAR(32) NOT NULL,
    to_state VARCHAR(32) NOT NULL,
    actor VARCHAR(128) NOT NULL,
    rationale TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
"""

SQLITE_LOCAL_DDL = """
-- SQLite Embedded Schema for Local Testing
CREATE TABLE IF NOT EXISTS canonical_texts (
    text_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    text_type TEXT NOT NULL,
    authority_rank INTEGER NOT NULL,
    tradition TEXT,
    sakha_recension TEXT,
    is_mukhya INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS verses (
    canonical_id TEXT PRIMARY KEY,
    text_id TEXT REFERENCES canonical_texts(text_id),
    chapter TEXT NOT NULL,
    verse TEXT NOT NULL,
    sanskrit_deva TEXT NOT NULL,
    iast TEXT NOT NULL,
    bengali TEXT,
    padaccheda TEXT NOT NULL DEFAULT '[]',
    meaning_summary TEXT NOT NULL,
    state TEXT NOT NULL DEFAULT 'A — CANONICAL',
    is_superseded INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_verses_lookup ON verses(text_id, chapter, verse);

CREATE TABLE IF NOT EXISTS commentaries (
    commentary_id TEXT PRIMARY KEY,
    verse_id TEXT REFERENCES verses(canonical_id),
    commentator TEXT NOT NULL,
    sampradaya TEXT NOT NULL,
    textual_basis TEXT,
    core_claim TEXT NOT NULL,
    underlying_assumption TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS atomic_claims (
    claim_id TEXT PRIMARY KEY,
    claim_text TEXT NOT NULL,
    claim_type TEXT NOT NULL,
    source_title TEXT NOT NULL,
    source_url TEXT,
    evidence_nature TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'unverified',
    related_canonical_id TEXT,
    permanent_knowledge INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_events (
    event_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL,
    from_state TEXT NOT NULL,
    to_state TEXT NOT NULL,
    actor TEXT NOT NULL,
    rationale TEXT NOT NULL,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def generate_ddl(dialect: str = "postgresql") -> str:
    """Returns production DDL for selected database dialect."""
    if dialect.lower() in ["postgres", "postgresql", "pg"]:
        return POSTGRES_PGVECTOR_DDL.strip()
    return SQLITE_LOCAL_DDL.strip()


def init_sqlite_memory_db() -> sqlite3.Connection:
    """Initializes in-memory SQLite database for schema integrity validation."""
    conn = sqlite3.connect(":memory:")
    conn.executescript(SQLITE_LOCAL_DDL)
    conn.commit()
    return conn
