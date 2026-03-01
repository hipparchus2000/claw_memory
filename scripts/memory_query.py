#!/usr/bin/env python3
"""
SQLite Memory Query Tool
Replaces MEMORY.md file access with SQLite queries
"""

import sqlite3
import sys

DB_PATH = "/home/openclaw/.openclaw/memory/main.sqlite"

def query_memory(search_term=None, source=None, limit=10):
    """Query memory chunks from SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if search_term:
        # Use FTS for full-text search
        cursor.execute('''
            SELECT snippet(chunks_fts, 0, '[', ']', '...', 2) as snippet,
                   source, path
            FROM chunks_fts
            WHERE chunks_fts MATCH ?
            LIMIT ?
        ''', (search_term, limit))
    else:
        # Simple query
        query = "SELECT * FROM chunks WHERE 1=1"
        params = []
        
        if source:
            query += " AND source = ?"
            params.append(source)
        
        query += " ORDER BY updated_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
    
    results = cursor.fetchall()
    conn.close()
    return results

def show_todos(status=None, priority=None):
    """Show todos from SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT * FROM todos WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status)
    
    if priority:
        query += " AND priority = ?"
        params.append(priority)
    
    query += " ORDER BY priority DESC, due_date ASC"
    
    cursor.execute(query, params)
    todos = cursor.fetchall()
    conn.close()
    return todos

def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python3 memory_query.py [command] [options]")
        print("\nCommands:")
        print("  search [term] - Search memory (full-text)")
        print("  recent [N] - Show recent memory entries")
        print("  todos [status] [priority] - Show todos")
        print("  stats - Show database statistics")
        return
    
    command = sys.argv[1]
    
    if command == "search":
        term = sys.argv[2] if len(sys.argv) > 2 else ""
        results = query_memory(search_term=term, limit=5)
        
        print(f'🔍 Search results for "{term}":')
        for i, row in enumerate(results, 1):
            if 'snippet' in row.keys():
                print(f'{i}. {row["snippet"]}')
                print(f'   Source: {row["source"]} | Path: {row["path"]}')
            else:
                print(f'{i}. {row["text"][:100]}...')
                print(f'   Source: {row["source"]} | Lines: {row["start_line"]}-{row["end_line"]}')
            print()
    
    elif command == "recent":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        results = query_memory(limit=limit)
        
        print(f'📝 Recent memory entries ({limit} most recent):')
        for i, row in enumerate(results, 1):
            print(f'{i}. {row["text"][:80]}...')
            print(f'   Source: {row["source"]} | Updated: {row["updated_at"][:19]}')
            print()
    
    elif command == "todos":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        priority = int(sys.argv[3]) if len(sys.argv) > 3 else None
        
        todos = show_todos(status, priority)
        
        print('📋 Todos:')
        for todo in todos:
            status_emoji = '🟡' if todo['status'] == 'in_progress' else '🔴' if todo['status'] == 'pending' else '⏸️'
            priority_stars = '⭐' * todo['priority']
            print(f'{status_emoji} {todo["id"]}. {todo["title"][:50]}...')
            print(f'   {priority_stars} Priority {todo["priority"]} | Due: {todo["due_date"]} | Status: {todo["status"]}')
            print()
    
    elif command == "stats":
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM chunks')
        chunks = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM todos WHERE status != "completed"')
        active_todos = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM memories')
        memories = cursor.fetchone()[0]
        
        cursor.execute('SELECT source, COUNT(*) FROM chunks GROUP BY source')
        sources = cursor.fetchall()
        
        print('📊 SQLite Memory Database Statistics:')
        print(f'  Total chunks: {chunks}')
        print(f'  Active todos: {active_todos}')
        print(f'  Memory entries: {memories}')
        print(f'  Sources:')
        for source, count in sources:
            print(f'    - {source}: {count} chunks')
        
        conn.close()
    
    else:
        print(f"Unknown command: {command}")
        print("Use: search, recent, todos, stats")

if __name__ == "__main__":
    main()