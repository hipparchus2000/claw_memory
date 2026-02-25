#!/usr/bin/env python3
"""
SQLite Memory Prototype for OpenClaw
Implements indexed memory storage for faster search and retrieval
"""

import sqlite3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

class SQLiteMemorySystem:
    """SQLite-based memory system for AI assistant"""
    
    def __init__(self, db_path="/home/openclaw/.openclaw/workspace/memory/memory.db"):
        """Initialize SQLite memory database"""
        self.db_path = db_path
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Initialize database schema"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Create memories table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_id TEXT NOT NULL,
            memory_type TEXT NOT NULL,  -- 'thought', 'insight', 'decision', 'event', 'knowledge'
            content TEXT NOT NULL,
            category TEXT,
            tags TEXT,  -- JSON array of tags
            importance INTEGER DEFAULT 1,  -- 1-5 scale
            access_count INTEGER DEFAULT 0,
            last_accessed TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create indexes for faster search
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_type ON memories(user_id, memory_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON memories(category)')
        
        # Create full-text search virtual table
        cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts 
        USING fts5(content, tags, content='memories', content_rowid='id')
        ''')
        
        self.conn.commit()
        print(f"SQLite memory database initialized at {self.db_path}")
    
    def store_memory(self, user_id, memory_type, content, category=None, tags=None, importance=1):
        """Store a memory with indexing"""
        timestamp = datetime.now(timezone.utc).isoformat()
        tags_json = json.dumps(tags) if tags else '[]'
        
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO memories (timestamp, user_id, memory_type, content, category, tags, importance)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, user_id, memory_type, content, category, tags_json, importance))
        
        memory_id = cursor.lastrowid
        
        # Update full-text search
        cursor.execute('''
        INSERT INTO memories_fts (rowid, content, tags)
        VALUES (?, ?, ?)
        ''', (memory_id, content, tags_json))
        
        self.conn.commit()
        return memory_id
    
    def search_memories(self, user_id=None, query=None, memory_type=None, 
                       category=None, limit=10, offset=0):
        """Search memories with various filters"""
        cursor = self.conn.cursor()
        
        if query:
            # Use full-text search for content queries
            cursor.execute('''
            SELECT m.*
            FROM memories m
            JOIN memories_fts fts ON m.id = fts.rowid
            WHERE memories_fts MATCH ?
            AND (? IS NULL OR m.user_id = ?)
            AND (? IS NULL OR m.memory_type = ?)
            ORDER BY rank
            LIMIT ? OFFSET ?
            ''', (query, user_id, user_id, memory_type, memory_type, limit, offset))
        else:
            # Regular filtered search
            conditions = []
            params = []
            
            if user_id:
                conditions.append("user_id = ?")
                params.append(user_id)
            if memory_type:
                conditions.append("memory_type = ?")
                params.append(memory_type)
            if category:
                conditions.append("category = ?")
                params.append(category)
            
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            params.extend([limit, offset])
            
            cursor.execute(f'''
            SELECT * FROM memories
            WHERE {where_clause}
            ORDER BY timestamp DESC, importance DESC
            LIMIT ? OFFSET ?
            ''', params)
        
        columns = [desc[0] for desc in cursor.description]
        results = []
        for row in cursor.fetchall():
            result = dict(zip(columns, row))
            if 'tags' in result and result['tags']:
                result['tags'] = json.loads(result['tags'])
            results.append(result)
        
        return results
    
    def get_memory_stats(self, user_id=None):
        """Get memory statistics"""
        cursor = self.conn.cursor()
        
        if user_id:
            cursor.execute('''
            SELECT 
                memory_type,
                COUNT(*) as count,
                AVG(importance) as avg_importance,
                SUM(access_count) as total_accesses
            FROM memories
            WHERE user_id = ?
            GROUP BY memory_type
            ''', (user_id,))
        else:
            cursor.execute('''
            SELECT 
                user_id,
                memory_type,
                COUNT(*) as count,
                AVG(importance) as avg_importance,
                SUM(access_count) as total_accesses
            FROM memories
            GROUP BY user_id, memory_type
            ''')
        
        return cursor.fetchall()
    
    def import_from_files(self, file_paths):
        """Import memories from existing text files"""
        imported = 0
        for file_path in file_paths:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Extract metadata from filename/path
                    filename = os.path.basename(file_path)
                    if 'thought' in filename:
                        memory_type = 'thought'
                    elif 'memory' in filename:
                        memory_type = 'memory'
                    else:
                        memory_type = 'knowledge'
                    
                    # Store in database
                    self.store_memory(
                        user_id='system',
                        memory_type=memory_type,
                        content=content,
                        category='imported',
                        tags=['import', filename],
                        importance=2
                    )
                    imported += 1
        
        return imported
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

def test_sqlite_memory():
    """Test the SQLite memory system"""
    print("=== Testing SQLite Memory System ===")
    
    # Initialize system
    memory = SQLiteMemorySystem("/tmp/test_memory.db")
    
    # Store some test memories
    print("\n1. Storing test memories...")
    memory.store_memory(
        user_id="jeff",
        memory_type="thought",
        content="AI assistants should evolve from reactive tools to proactive partners.",
        category="evolution",
        tags=["ai", "evolution", "proactive"],
        importance=5
    )
    
    memory.store_memory(
        user_id="jeff",
        memory_type="insight",
        content="Memory partitioning enables multi-relationship AI without boundary violations.",
        category="architecture",
        tags=["memory", "architecture", "relationships"],
        importance=4
    )
    
    memory.store_memory(
        user_id="system",
        memory_type="knowledge",
        content="SQLite provides fast indexed search for memory systems.",
        category="technology",
        tags=["sqlite", "database", "search"],
        importance=3
    )
    
    # Search memories
    print("\n2. Searching memories...")
    results = memory.search_memories(user_id="jeff", query="memory partitioning")
    print(f"Found {len(results)} results for 'memory partitioning':")
    for r in results:
        print(f"  - {r['memory_type']}: {r['content'][:50]}...")
    
    # Get statistics
    print("\n3. Memory statistics:")
    stats = memory.get_memory_stats("jeff")
    for stat in stats:
        print(f"  - {stat[0]}: {stat[1]} memories, avg importance: {stat[2]:.1f}")
    
    # Cleanup
    memory.close()
    os.remove("/tmp/test_memory.db")
    print("\n=== Test completed successfully ===")

if __name__ == "__main__":
    test_sqlite_memory()