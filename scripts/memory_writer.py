#!/usr/bin/env python3
"""
SQLite Memory Writer Tool
Add new memories to SQLite database (replaces .md file editing)
"""

import sqlite3
import datetime
import sys

DB_PATH = "/home/openclaw/.openclaw/memory/main.sqlite"

def add_memory(text, source="manual", tags=None, importance=3):
    """Add a new memory entry to SQLite"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.datetime.now().isoformat()
    
    cursor.execute('''
        INSERT INTO memories 
        (timestamp, source, content_type, content, tags, importance, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        now,
        source,
        'text',
        text,
        tags,
        importance,
        now,
        now
    ))
    
    memory_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ Memory added with ID: {memory_id}")
    return memory_id

def add_chunk(text, path="manual", source="user", start_line=1, end_line=1):
    """Add a text chunk to SQLite (for structured content)"""
    import hashlib
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.datetime.now().isoformat()
    chunk_hash = hashlib.sha256(text.encode()).hexdigest()
    
    cursor.execute('''
        INSERT OR IGNORE INTO chunks 
        (path, source, start_line, end_line, hash, text, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        path,
        source,
        start_line,
        end_line,
        chunk_hash,
        text,
        now
    ))
    
    chunk_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    if chunk_id:
        print(f"✅ Chunk added with ID: {chunk_id}")
    else:
        print("⚠️ Chunk already exists (duplicate hash)")
    
    return chunk_id

def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python3 memory_writer.py [command] [options]")
        print("\nCommands:")
        print("  memory \"text\" [source] [tags] - Add memory entry")
        print("  chunk \"text\" [path] [source] - Add text chunk")
        print("  example - Show examples")
        return
    
    command = sys.argv[1]
    
    if command == "memory":
        if len(sys.argv) < 3:
            print("Usage: memory \"text\" [source] [tags]")
            return
        
        text = sys.argv[2]
        source = sys.argv[3] if len(sys.argv) > 3 else "manual"
        tags = sys.argv[4] if len(sys.argv) > 4 else None
        
        add_memory(text, source, tags)
    
    elif command == "chunk":
        if len(sys.argv) < 3:
            print("Usage: chunk \"text\" [path] [source]")
            return
        
        text = sys.argv[2]
        path = sys.argv[3] if len(sys.argv) > 3 else "manual"
        source = sys.argv[4] if len(sys.argv) > 4 else "user"
        
        add_chunk(text, path, source)
    
    elif command == "example":
        print("Example commands:")
        print('  python3 memory_writer.py memory "Learned about SQLite migration today" learning sqlite,migration')
        print('  python3 memory_writer.py chunk "## New Insight 2026-03-01" insights.md daily')
        print('\nCommon sources: daily, learning, decision, insight, conversation')
        print('Common paths: insights.md, decisions.md, learnings.md, manual')
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()