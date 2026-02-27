# SQLite Memory Database Schema

## Support the Project ☕

If you find this system helpful, feel free to buy me a coffee!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Stripe-orange?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white)](https://buy.stripe.com/cNi5kDb0Q5Wp663gdgbjW00)

---

## Database Location

- **Path**: `/home/openclaw/.openclaw/memory/main.sqlite`
- **Size**: ~68KB (as of 2026-02-27)
- **Purpose**: Indexed memory storage with full-text search

## Table Structure

### 1. `chunks` - Text Chunks Table
Primary table for storing text chunks with metadata.

```sql
CREATE TABLE chunks (
    id TEXT PRIMARY KEY,                    -- Unique chunk identifier (file_hash:chunk_index)
    path TEXT NOT NULL,                     -- Source file path
    source TEXT NOT NULL DEFAULT 'memory',  -- Source category (core_memory_smart, memory_version:*, etc.)
    start_line INTEGER NOT NULL,            -- Starting word position in original file
    end_line INTEGER NOT NULL,              -- Ending word position in original file
    hash TEXT NOT NULL,                     -- SHA256 hash of chunk text (for duplicate detection)
    model TEXT NOT NULL,                    -- Embedding model used (or placeholder)
    text TEXT NOT NULL,                     -- Chunk content (~107 words average)
    embedding TEXT NOT NULL,                -- Vector embedding (empty string if not embedded)
    updated_at INTEGER NOT NULL             -- Last update timestamp (milliseconds)
);
```

**Indexes:**
- `idx_chunks_source` ON chunks(source)
- `idx_chunks_path` ON chunks(path)
- `hash` column used for duplicate detection

### 2. `chunks_fts` - Full-Text Search Virtual Table
FTS5 virtual table for fast text search.

```sql
CREATE VIRTUAL TABLE chunks_fts USING fts5(
    text,              -- Searchable text content
    id UNINDEXED,      -- Chunk identifier (not searchable)
    path UNINDEXED,    -- File path (not searchable)
    source UNINDEXED,  -- Source category (not searchable)
    model UNINDEXED,   -- Model name (not searchable)
    start_line UNINDEXED,  -- Start position (not searchable)
    end_line UNINDEXED     -- End position (not searchable)
);
```

**Supporting FTS5 Tables:**
- `chunks_fts_config` - FTS5 configuration
- `chunks_fts_content` - Content storage
- `chunks_fts_data` - Data storage
- `chunks_fts_docsize` - Document sizes
- `chunks_fts_idx` - Index data

### 3. `files` - File Tracking Table
Tracks source files and their metadata.

```sql
CREATE TABLE files (
    path TEXT PRIMARY KEY,                  -- Full file path
    source TEXT NOT NULL DEFAULT 'memory',  -- Source category
    hash TEXT NOT NULL,                     -- SHA256 hash of entire file
    mtime INTEGER NOT NULL,                 -- Last modification time (milliseconds)
    size INTEGER NOT NULL                   -- File size in bytes
);
```

### 4. `embedding_cache` - Vector Embedding Cache
For caching embeddings to avoid recomputation.

```sql
CREATE TABLE embedding_cache (
    provider TEXT NOT NULL,      -- Embedding provider (e.g., 'openai', 'cohere')
    model TEXT NOT NULL,         -- Model name (e.g., 'text-embedding-ada-002')
    provider_key TEXT NOT NULL,  -- Provider-specific key/version
    hash TEXT NOT NULL,          -- Hash of text that was embedded
    embedding TEXT NOT NULL,     -- Vector embedding (JSON or binary)
    dims INTEGER,                -- Embedding dimensions
    updated_at INTEGER NOT NULL, -- Last update timestamp
    PRIMARY KEY (provider, model, provider_key, hash)
);
```

### 5. `meta` - System Metadata Table
Stores system configuration and metadata.

```sql
CREATE TABLE meta (
    key TEXT PRIMARY KEY,   -- Metadata key
    value TEXT NOT NULL     -- JSON-encoded value
);
```

**Current meta entry:**
```json
{
  "model": "fts-only",
  "provider": "none", 
  "providerKey": "b2f409223dd1bd19cedee3332de54748a5f323765d4cdcbbb29295199cfde125",
  "sources": ["memory"],
  "chunkTokens": 400,
  "chunkOverlap": 80
}
```

## Chunking Strategy

### Parameters:
- **Target chunk size**: ~300 words
- **Overlap**: 50 words between chunks
- **Boundary awareness**: Respects paragraph and section breaks

### Smart Chunking Algorithm:
1. **Split by markdown headers** (`#`, `##`, `###`)
2. **Respect paragraph boundaries** (double newlines)
3. **Handle large paragraphs** (split if > target size)
4. **Maintain overlap** for context continuity
5. **Hash-based duplicate detection** across all chunks

### Chunk Statistics (as of 2026-02-27):
- **Total chunks**: 109
- **Average words per chunk**: 107
- **Minimum words**: 3
- **Maximum words**: 1000
- **Duplicate chunks skipped**: 6

## Import Process

### 1. File Processing:
```python
def import_file(filepath, source_category):
    # 1. Read file content
    # 2. Calculate file hash (SHA256)
    # 3. Check if file already imported with same hash
    # 4. Delete old chunks if file changed
    # 5. Create smart chunks
    # 6. Insert chunks with duplicate detection
    # 7. Update file tracking
```

### 2. Duplicate Detection:
- **Chunk-level deduplication**: Compare SHA256 hashes
- **Cross-file detection**: Same text in different files = single chunk
- **Storage efficiency**: Avoid storing identical content multiple times

### 3. FTS Index Maintenance:
```sql
-- Clear and rebuild FTS index
DELETE FROM chunks_fts;
INSERT INTO chunks_fts (text, id, path, source, model, start_line, end_line)
SELECT text, id, path, source, model, start_line, end_line
FROM chunks;
```

## Search Capabilities

### Full-Text Search:
```sql
-- Basic search
SELECT * FROM chunks_fts WHERE chunks_fts MATCH 'sqlite memory';

-- Search with snippet highlighting
SELECT snippet(chunks_fts, 0, '[', ']', '...', 2) as snippet
FROM chunks_fts
WHERE chunks_fts MATCH 'partnership framework';
```

### Source Filtering:
```sql
-- Search within specific source
SELECT * FROM chunks_fts 
WHERE chunks_fts MATCH 'thinking' 
  AND source = 'core_memory_smart';
```

### Combined Queries:
```sql
-- Search with multiple terms
SELECT * FROM chunks_fts 
WHERE chunks_fts MATCH 'sqlite AND memory AND NOT private';
```

## Current Content (2026-02-27)

### Sources in Database:
1. **core_memory_smart** (87 chunks) - Current memory files with smart chunking
2. **core_memory** (4 chunks) - Legacy imports
3. **memory_integration** (7 chunks) - Integration summaries
4. **memory_version:*** (13 chunks) - Historical MEMORY.md versions

### File Types:
- **MEMORY.md**: 59 chunks (current + historical versions)
- **journal.md**: 26 chunks
- **ideas.md**: 12 chunks
- **thoughts.md**: 8 chunks
- **Other**: 4 chunks

## Usage Examples

### Python Interface:
```python
import sqlite3

class MemoryDatabase:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
    
    def search(self, query, limit=10):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT path, snippet(chunks_fts, 0, '[', ']', '...', 2) as snippet
            FROM chunks_fts
            WHERE chunks_fts MATCH ?
            LIMIT ?
        """, (query, limit))
        return cursor.fetchall()
    
    def get_chunk(self, chunk_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM chunks WHERE id = ?", (chunk_id,))
        return cursor.fetchone()
```

### Command Line:
```bash
# Search from command line
sqlite3 /home/openclaw/.openclaw/memory/main.sqlite \
  "SELECT snippet(chunks_fts, 0, '[', ']', '...', 1) FROM chunks_fts WHERE chunks_fts MATCH 'sqlite' LIMIT 3;"
```

## Future Extensions

### 1. Embedding Integration:
- Add vector embeddings to `embedding_cache` table
- Implement hybrid search (FTS + vector similarity)
- Support multiple embedding models

### 2. Todo/Action System:
- Add `todos`, `actions`, `projects` tables
- Integrate with thinking → research → action feedback loop
- Priority-based task management

### 3. Advanced Features:
- Temporal indexing (time-based queries)
- Relationship mapping between chunks
- Importance scoring (0-5 scale)
- Compression status tracking

## Maintenance

### Regular Tasks:
1. **Import new content** from .md files
2. **Update FTS index** after imports
3. **Check for duplicates** during import
4. **Backup database** periodically
5. **Monitor performance** and optimize queries

### Backup Strategy:
```bash
# Simple backup
cp /home/openclaw/.openclaw/memory/main.sqlite \
   /home/openclaw/.openclaw/memory/backups/main_$(date +%Y%m%d).sqlite
```


---
*Last Updated: 2026-02-27*
*Schema Version: 1.0*
*Database: /home/openclaw/.openclaw/memory/main.sqlite*