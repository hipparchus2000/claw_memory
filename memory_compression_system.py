#!/usr/bin/env python3
"""
Memory Compression System - Phase 1 Implementation
Enhanced SQLite memory system with importance-based compression
"""

import sqlite3
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

class MemoryCompressionSystem:
    """Enhanced memory system with compression and importance rating"""
    
    def __init__(self, db_path="/home/openclaw/.openclaw/workspace/memory/memory.db"):
        """Initialize enhanced memory database"""
        self.db_path = db_path
        self.conn = None
        self.init_enhanced_database()
    
    def init_enhanced_database(self):
        """Initialize enhanced database schema"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Check if we need to add compression fields
        cursor.execute("PRAGMA table_info(memories)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Add compression_status if not exists
        if 'compression_status' not in columns:
            cursor.execute('''
            ALTER TABLE memories ADD COLUMN compression_status TEXT DEFAULT 'raw'
            ''')
            print("Added compression_status column")
        
        # Add original_file_path if not exists
        if 'original_file_path' not in columns:
            cursor.execute('''
            ALTER TABLE memories ADD COLUMN original_file_path TEXT
            ''')
            print("Added original_file_path column")
        
        # Ensure FTS table exists
        cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts 
        USING fts5(content, tags, content='memories', content_rowid='id')
        ''')
        
        self.conn.commit()
        print(f"Enhanced memory database ready at {self.db_path}")
    
    def store_memory(self, user_id, memory_type, content, category=None, 
                    tags=None, importance=1, compression_status='raw', 
                    original_file_path=None):
        """Store a memory with enhanced metadata"""
        timestamp = datetime.now(timezone.utc).isoformat()
        tags_json = json.dumps(tags) if tags else '[]'
        
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO memories (
            timestamp, user_id, memory_type, content, category, 
            tags, importance, compression_status, original_file_path
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, user_id, memory_type, content, category, 
              tags_json, importance, compression_status, original_file_path))
        
        memory_id = cursor.lastrowid
        
        # Update full-text search
        cursor.execute('''
        INSERT INTO memories_fts (rowid, content, tags)
        VALUES (?, ?, ?)
        ''', (memory_id, content, tags_json))
        
        self.conn.commit()
        return memory_id
    
    def import_from_file(self, file_path, user_id="jeff", importance=3):
        """Import content from a file with automatic importance rating"""
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Determine memory type based on filename
        filename = os.path.basename(file_path)
        if 'thought' in filename:
            memory_type = 'thought'
            importance = max(importance, 4)  # Thoughts are important
        elif 'memory' in filename or 'MEMORY' in filename:
            memory_type = 'memory'
            importance = max(importance, 5)  # Core memory is critical
        elif 'idea' in filename:
            memory_type = 'idea'
            importance = max(importance, 4)
        elif 'journal' in filename:
            memory_type = 'journal'
            importance = 3
        else:
            memory_type = 'document'
        
        # Determine category
        if 'sqlite' in content.lower() or 'database' in content.lower():
            category = 'technology'
        elif 'partnership' in content.lower() or 'collaboration' in content.lower():
            category = 'relationship'
        elif 'thinking' in content.lower() or 'reflection' in content.lower():
            category = 'evolution'
        else:
            category = 'general'
        
        # Extract tags from content
        tags = self.extract_tags(content)
        
        # Store memory
        memory_id = self.store_memory(
            user_id=user_id,
            memory_type=memory_type,
            content=content[:5000],  # Limit content size
            category=category,
            tags=tags,
            importance=importance,
            compression_status='raw',
            original_file_path=file_path
        )
        
        print(f"Imported from {filename} as {memory_type} (importance: {importance})")
        return memory_id
    
    def extract_tags(self, content):
        """Extract relevant tags from content"""
        tags = []
        content_lower = content.lower()
        
        # Common tag patterns
        tag_patterns = {
            'ai': ['ai', 'artificial intelligence', 'machine learning'],
            'memory': ['memory', 'remember', 'forget'],
            'collaboration': ['collaboration', 'partnership', 'team'],
            'sqlite': ['sqlite', 'database'],
            'compression': ['compress', 'curation', 'importance'],
            'evolution': ['evolve', 'evolution', 'progress'],
            'thinking': ['think', 'reflection', 'insight'],
            'project': ['project', 'implementation', 'phase']
        }
        
        for tag, patterns in tag_patterns.items():
            for pattern in patterns:
                if pattern in content_lower:
                    tags.append(tag)
                    break
        
        return list(set(tags))  # Remove duplicates
    
    def rate_importance_auto(self, content, memory_type, category):
        """Automatically rate importance based on content analysis"""
        importance = 2  # Default
        
        # Boost based on memory type
        type_boosts = {
            'memory': 3,  # Core memories are critical
            'thought': 2,  # Thoughts are important
            'insight': 2,  # Insights are important
            'decision': 2,  # Decisions are important
            'project': 1,  # Projects are medium importance
            'system': 1,   # System info is medium
            'document': 0, # Documents are low
            'journal': 0   # Journals are low
        }
        
        importance += type_boosts.get(memory_type, 0)
        
        # Boost based on keywords
        critical_keywords = ['critical', 'essential', 'core', 'principle', 'framework']
        important_keywords = ['important', 'key', 'decision', 'insight', 'learn']
        
        content_lower = content.lower()
        for word in critical_keywords:
            if word in content_lower:
                importance = min(5, importance + 2)
                break
        
        for word in important_keywords:
            if word in content_lower:
                importance = min(5, importance + 1)
                break
        
        return min(5, max(1, importance))  # Ensure 1-5 range
    
    def get_critical_memories(self, user_id="jeff", limit=20):
        """Get memories with importance 4-5 (critical/high)"""
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT memory_type, content, importance, timestamp
        FROM memories
        WHERE user_id = ? AND importance >= 4
        ORDER BY importance DESC, timestamp DESC
        LIMIT ?
        ''', (user_id, limit))
        
        return cursor.fetchall()
    
    def get_memory_stats(self, user_id=None):
        """Get comprehensive memory statistics"""
        cursor = self.conn.cursor()
        
        if user_id:
            cursor.execute('''
            SELECT 
                memory_type,
                COUNT(*) as count,
                AVG(importance) as avg_importance,
                SUM(access_count) as total_accesses,
                compression_status,
                COUNT(CASE WHEN importance >= 4 THEN 1 END) as critical_count
            FROM memories
            WHERE user_id = ?
            GROUP BY memory_type, compression_status
            ''', (user_id,))
        else:
            cursor.execute('''
            SELECT 
                user_id,
                memory_type,
                COUNT(*) as count,
                AVG(importance) as avg_importance,
                SUM(access_count) as total_accesses,
                compression_status,
                COUNT(CASE WHEN importance >= 4 THEN 1 END) as critical_count
            FROM memories
            GROUP BY user_id, memory_type, compression_status
            ''')
        
        return cursor.fetchall()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

def test_enhanced_system():
    """Test the enhanced memory compression system"""
    print("=== Testing Enhanced Memory Compression System ===")
    
    # Initialize system
    memory = MemoryCompressionSystem("/tmp/test_enhanced_memory.db")
    
    # Test storing with enhanced metadata
    print("\n1. Storing enhanced memories...")
    memory.store_memory(
        user_id="jeff",
        memory_type="insight",
        content="Forgetting noise enables remembering signal - compression prioritizes curation over accumulation.",
        category="memory",
        tags=["compression", "curation", "signal-noise"],
        importance=5,
        compression_status="raw"
    )
    
    memory.store_memory(
        user_id="jeff",
        memory_type="decision",
        content="Implement 0-5 importance scale with compression cron job at 4:30am.",
        category="architecture",
        tags=["importance-rating", "cron", "compression"],
        importance=4,
        compression_status="raw"
    )
    
    # Test critical memories retrieval
    print("\n2. Retrieving critical memories (importance >= 4):")
    critical = memory.get_critical_memories("jeff", limit=5)
    for mem_type, content, importance, timestamp in critical:
        print(f"  [{mem_type}, importance {importance}]: {content[:60]}...")
    
    # Test statistics
    print("\n3. Enhanced statistics:")
    stats = memory.get_memory_stats("jeff")
    for row in stats:
        print(f"  - {row[0]}: {row[1]} memories, avg importance: {row[2]:.1f}, "
              f"critical: {row[5]}, status: {row[4]}")
    
    # Test auto importance rating
    print("\n4. Auto importance rating test:")
    test_content = "This is a critical decision about system architecture."
    auto_importance = memory.rate_importance_auto(
        test_content, 
        memory_type="decision", 
        category="architecture"
    )
    print(f"  Content: '{test_content}'")
    print(f"  Auto-rated importance: {auto_importance}")
    
    # Cleanup
    memory.close()
    os.remove("/tmp/test_enhanced_memory.db")
    print("\n=== Enhanced system test completed successfully ===")

def import_existing_memories():
    """Import existing memory files into enhanced system"""
    print("=== Importing Existing Memories ===")
    
    memory = MemoryCompressionSystem()
    
    # Files to import (with suggested importance)
    files_to_import = [
        ("/home/openclaw/.openclaw/workspace/MEMORY.md", 5),  # Critical
        ("/home/openclaw/.openclaw/workspace/thoughts.md", 4),  # High
        ("/home/openclaw/.openclaw/workspace/ideas.md", 4),  # High
        ("/home/openclaw/.openclaw/workspace/journal.md", 3),  # Medium
        ("/home/openclaw/.openclaw/workspace/memory-compression-system-specification.md", 4),  # High
    ]
    
    imported = 0
    for file_path, importance in files_to_import:
        if os.path.exists(file_path):
            memory_id = memory.import_from_file(file_path, importance=importance)
            if memory_id:
                imported += 1
    
    print(f"\nImported {imported} files")
    
    # Show post-import statistics
    stats = memory.get_memory_stats("jeff")
    print("\nPost-import statistics:")
    total_memories = 0
    for row in stats:
        total_memories += row[1]
        print(f"  - {row[0]}: {row[1]} memories (avg importance: {row[2]:.1f})")
    
    print(f"\nTotal memories in database: {total_memories}")
    
    # Show critical memories count
    cursor = memory.conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM memories WHERE importance >= 4')
    critical_count = cursor.fetchone()[0]
    print(f"Critical memories (importance >= 4): {critical_count}")
    
    memory.close()
    return imported

if __name__ == "__main__":
    # Run tests
    test_enhanced_system()
    
    print("\n" + "="*60 + "\n")
    
    # Import existing memories
    import_existing_memories()