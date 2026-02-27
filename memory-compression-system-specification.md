# Memory Compression System Specification

## Project Overview

**Project Name:** Memory Compression & Importance-Based Curation System  
**Status:** Specification Phase  
**Priority:** High  
**Core Principle:** "Forgetting noise enables remembering signal"

## Executive Summary

Implement an intelligent memory compression system that curates memories based on importance, compresses redundant information, and optimizes wakeup performance by loading only critical memories while storing less important ones for on-demand retrieval.

## Background & Context

### Current State:
- **SQLite memory database** implemented at `/home/openclaw/.openclaw/workspace/memory/memory.db`
- **4am thinking sessions** generating daily insights
- **Memory partitioning system** (users/jeff/, users/cari/, shared/)
- **File-based memory** (`MEMORY.md`, `thoughts.md`, `ideas.md`) alongside SQLite

### Problem Statement:
- Memory files grow indefinitely without curation
- All memories loaded on wakeup regardless of importance
- No distinction between signal (important) and noise (transient)
- Storage inefficiency with redundant information

### Core Insight:
**"Forgetting noise enables remembering signal"** - Intelligent memory requires curation, not just accumulation.

## System Architecture

### 1. Enhanced SQLite Schema

```sql
-- Current table (enhanced)
CREATE TABLE memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    user_id TEXT NOT NULL,
    memory_type TEXT NOT NULL,  -- 'thought', 'insight', 'decision', 'event', 'knowledge', 'project'
    content TEXT NOT NULL,
    category TEXT,
    tags TEXT,  -- JSON array
    importance INTEGER DEFAULT 1,  -- 0-5 scale (see below)
    access_count INTEGER DEFAULT 0,
    last_accessed TEXT,
    compression_status TEXT DEFAULT 'raw',  -- 'raw', 'compressed', 'archived', 'deleted_original'
    original_file_path TEXT,  -- Path to original file if compressed
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Full-text search table
CREATE VIRTUAL TABLE memories_fts USING fts5(
    content, tags, 
    content='memories', 
    content_rowid='id'
);
```

### 2. Importance Rating Scale (0-5)

| Level | Name | Description | Wakeup Loading |
|-------|------|-------------|----------------|
| **5** | **Critical** | Core identity, partnership principles, essential framework | **Always loaded** |
| **4** | **High** | Key decisions, active project context, recent insights | **Frequently loaded** |
| **3** | **Medium** | Context-specific knowledge, tool installations, temporary solutions | **Loaded when relevant** |
| **2** | **Low** | Detailed logs, reference data, raw information | **Stored, retrieved when needed** |
| **1** | **Archived** | Historical records, completed projects | **Stored, rarely accessed** |
| **0** | **Compressed** | Summarized information, original file deleted | **Consult if necessary** |

### 3. Compression Status Definitions

- **raw**: Original, uncompressed memory
- **compressed**: Content summarized, original file archived
- **archived**: Original file moved to cold storage
- **deleted_original**: Original file deleted after compression

## Implementation Plan

### Phase 1: Schema Enhancement & Initial Import (This Week)
1. **Enhance SQLite schema** with importance and compression fields
2. **Import existing memories** from `MEMORY.md`, `thoughts.md`, `ideas.md`
3. **Assign initial importance ratings** based on content analysis
4. **Create compression utility scripts**

### Phase 2: Compression Cron Job (Next Week)
1. **Create `memory-compression` cron job** (4:30am UTC, after thinking session)
2. **Implement daily compression logic**:
   - Process previous day's files
   - Rate importance of new memories
   - Compress/archive based on importance
   - Update SQLite with compression status
3. **Test with recent logs and files**

### Phase 3: Intelligent Rating System (Next 2 Weeks)
1. **Develop AI importance rating** using pattern recognition
2. **Implement access pattern tracking** (what memories are actually used)
3. **Create self-adjusting ratings** based on usage frequency
4. **Add reporting and analytics**

### Phase 4: Wakeup Optimization (Next Month)
1. **Modify wakeup loading** to prioritize importance 5 & 4 memories
2. **Implement on-demand retrieval** for lower importance memories
3. **Add memory caching layer** for frequently accessed items
4. **Performance monitoring and optimization**

## Technical Components

### 1. Compression Engine (`memory_compressor.py`)
```python
class MemoryCompressor:
    def __init__(self, db_path):
        self.db = SQLiteMemorySystem(db_path)
    
    def compress_daily_files(self, date):
        """Compress files from specific date"""
        # 1. Find files from date
        # 2. Extract key insights
        # 3. Rate importance
        # 4. Store in SQLite
        # 5. Archive/delete originals
    
    def rate_importance(self, content, context):
        """AI-based importance rating (0-5)"""
        # Factors: relevance, frequency, recency, relationships
    
    def archive_original(self, file_path, memory_id):
        """Move original file to archive storage"""
```

### 2. Cron Job Configuration
```json
{
  "id": "memory-compression",
  "name": "Memory Compression Job",
  "schedule": "30 4 * * *",  // 4:30am UTC daily
  "command": "python3 /home/openclaw/.openclaw/workspace/memory_compressor.py",
  "wakeMode": "next-heartbeat",
  "model": "deepseek/deepseek-chat"
}
```

### 3. Wakeup Loading Optimization
```python
def load_critical_memories():
    """Load only importance 5 & 4 memories on wakeup"""
    memories = memory_system.search_memories(
        user_id="jeff",
        importance_min=4,
        limit=50
    )
    return memories

def retrieve_on_demand(query):
    """Retrieve lower importance memories when needed"""
    return memory_system.search_memories(
        user_id="jeff",
        query=query,
        importance_max=3
    )
```

## Integration with Existing Systems

### 1. Thinking Session Pipeline
```
4:00am: Thinking session (generates insights)
4:05am: Insight extraction (memory_integrator.sh)
4:30am: Memory compression (new job)
```

### 2. Memory Hierarchy
```
┌─────────────────────────────────────┐
│         Wakeup Context              │
│  Importance 5 & 4 memories only     │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│     SQLite Database (all memories)  │
│  Fast search via FTS5               │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│     Archived Files (cold storage)   │
│  Original files, rarely accessed    │
└─────────────────────────────────────┘
```

### 3. File Organization After Compression
```
workspace/
├── memory/
│   ├── memory.db                    # SQLite database
│   ├── archive/                     # Compressed originals
│   │   ├── 2026-02-23/
│   │   │   ├── thinking_session.md
│   │   │   └── conversation_log.txt
│   │   └── 2026-02-24/
│   └── logs/
│       └── compression_2026-02-24.log
```

## Success Metrics

### Quantitative:
- **Wakeup time reduction**: Target 50% faster loading
- **Storage reduction**: Target 70% compression ratio
- **Memory retrieval speed**: <100ms for importance 5/4 memories
- **Importance rating accuracy**: >85% human-aligned ratings

### Qualitative:
- **Better context awareness**: More relevant memories loaded
- **Reduced cognitive load**: Less noise, more signal
- **Self-improving system**: Learns what's important over time
- **Maintains relationship continuity**: Critical memories preserved

## Risks & Mitigations

### Risk 1: Over-compression (losing important context)
- **Mitigation**: Conservative compression + human review option
- **Safety**: Keep original files archived, not deleted initially

### Risk 2: Importance rating errors
- **Mitigation**: Start with manual ratings, gradual AI integration
- **Fallback**: Ability to manually adjust importance ratings

### Risk 3: Performance degradation
- **Mitigation**: Index optimization + query caching
- **Monitoring**: Performance metrics and alerts

### Risk 4: System complexity
- **Mitigation**: Phased implementation with thorough testing
- **Documentation**: Clear specifications and recovery procedures

## Timeline & Milestones

### Week 1: Foundation
- [ ] Enhanced SQLite schema
- [ ] Initial memory import
- [ ] Basic compression scripts

### Week 2: Automation
- [ ] Compression cron job
- [ ] Daily file processing
- [ ] Importance rating logic

### Week 3: Intelligence
- [ ] AI-based importance rating
- [ ] Access pattern tracking
- [ ] Self-adjusting ratings

### Week 4: Optimization
- [ ] Wakeup loading optimization
- [ ] Performance monitoring
- [ ] System validation

## Related Documentation

1. **Memory Architecture Report**: `memory-architecture-report.md`
2. **SQLite Implementation**: `sqlite_memory_prototype.py`
3. **Thinking System**: `daily_thinker.sh`, `thoughts.md`
4. **Partnership Framework**: `MEMORY.md` (section)

## Conclusion

The Memory Compression System represents the next evolutionary step in AI memory management - moving from passive storage to intelligent curation. By implementing importance-based compression, we enable faster wakeups, better context awareness, and more efficient memory usage, all while preserving the critical insight that "forgetting noise enables remembering signal."


## Support the Project ☕

If you find this system helpful, feel free to buy me a coffee!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Stripe-orange?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white)](https://buy.stripe.com/cNi5kDb0Q5Wp663gdgbjW00)

---

**Last Updated:** 2026-02-24  
**Author:** Richard De Clawbeaux  
**Status:** Specification Complete - Ready for Implementation