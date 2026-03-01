#!/usr/bin/env python3
"""
SQLite Memory Integrator Tool
Replaces memory_integrator.sh - integrates insights into SQLite database
"""

import sqlite3
import datetime
import sys
import os

DB_PATH = "/home/openclaw/.openclaw/memory/main.sqlite"

def integrate_insight(insight_text, source="integration", category="insight", importance=4):
    """Integrate an insight into SQLite memory"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.datetime.now().isoformat()
    
    # Add to memories table
    cursor.execute('''
        INSERT INTO memories 
        (timestamp, source, content_type, content, tags, importance, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        now,
        source,
        'insight',
        insight_text,
        f'integration,{category}',
        importance,
        now,
        now
    ))
    
    # Also add as chunk for searchability
    import hashlib
    chunk_hash = hashlib.sha256(insight_text.encode()).hexdigest()
    
    cursor.execute('''
        INSERT OR IGNORE INTO chunks 
        (path, source, start_line, end_line, hash, text, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        'integration',
        'insight',
        1,
        1,
        chunk_hash,
        insight_text,
        now
    ))
    
    memory_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ Insight integrated with ID: {memory_id}")
    return memory_id

def integrate_from_file(file_path):
    """Integrate insights from a thinking file"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return 0
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Simple extraction - in reality would use NLP
    insights = []
    lines = content.split('\n')
    
    # Look for key insights (simplified)
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in ['insight:', 'key finding:', 'important:', 'conclusion:', 'learned:']):
            insights.append(line.strip())
        elif line.strip().startswith('## ') or line.strip().startswith('### '):
            insights.append(line.strip())
    
    if not insights:
        # Take first 3 non-empty lines as insights
        insights = [line.strip() for line in lines if line.strip()][:3]
    
    integrated = 0
    for insight in insights:
        if insight and len(insight) > 10:  # Minimum length
            integrate_insight(insight, source="thinking_file", category="daily")
            integrated += 1
    
    print(f"✅ Integrated {integrated} insights from {file_path}")
    return integrated

def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python3 sqlite_memory_integrator.py [command]")
        print("\nCommands:")
        print("  insight \"text\" [category] - Integrate single insight")
        print("  file <path> - Integrate insights from file")
        print("  test - Test integration")
        return
    
    command = sys.argv[1]
    
    if command == "insight":
        if len(sys.argv) < 3:
            print("Usage: insight \"text\" [category]")
            return
        
        text = sys.argv[2]
        category = sys.argv[3] if len(sys.argv) > 3 else "general"
        integrate_insight(text, category=category)
    
    elif command == "file":
        if len(sys.argv) < 3:
            print("Usage: file <path>")
            return
        
        file_path = sys.argv[2]
        integrate_from_file(file_path)
    
    elif command == "test":
        # Test integration
        test_insight = "Test insight: SQLite memory integration system working"
        integrate_insight(test_insight, source="test", category="system")
        print("✅ Test integration complete")
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()