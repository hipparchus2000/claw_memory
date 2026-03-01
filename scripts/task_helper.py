#!/usr/bin/env python3
"""
Task Management Helper Script
Provides command-line interface to SQLite task system
"""

import sqlite3
import json
import datetime
import sys
from pathlib import Path

DB_PATH = "/home/openclaw/.openclaw/memory/main.sqlite"

class TaskManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    
    def list_tasks(self, status=None, priority=None, category=None):
        """List tasks with optional filters"""
        query = "SELECT * FROM todos WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY priority DESC, due_date ASC, created_at ASC"
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def add_task(self, title, description, category="general", priority=3, 
                 due_date=None, project_path=None, project_file=None,
                 assigned_to="Richard", tags=None):
        """Add a new task to the database"""
        now = datetime.datetime.now().isoformat()
        
        if not due_date:
            due_date = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        
        self.cursor.execute('''
            INSERT INTO todos (title, description, category, priority, status, 
                              due_date, created_at, last_updated, assigned_to,
                              project_path, project_file, tags, progress_percent)
            VALUES (?, ?, ?, ?, 'pending', ?, ?, ?, ?, ?, ?, ?, 0)
        ''', (title, description, category, priority, due_date, now, now, 
              assigned_to, project_path, project_file, tags))
        
        self.conn.commit()
        task_id = self.cursor.lastrowid
        print(f"✅ Task added with ID: {task_id}")
        return task_id
    
    def update_status(self, task_id, status, progress_percent=None, notes=None):
        """Update task status and progress"""
        now = datetime.datetime.now().isoformat()
        
        if status == 'completed':
            self.cursor.execute('''
                UPDATE todos 
                SET status = ?, progress_percent = 100, completed_at = ?, last_updated = ?
                WHERE id = ?
            ''', (status, now, now, task_id))
        else:
            if progress_percent is None:
                # Auto-set progress based on status
                progress_percent = 50 if status == 'in_progress' else 0
            
            self.cursor.execute('''
                UPDATE todos 
                SET status = ?, progress_percent = ?, last_updated = ?
                WHERE id = ?
            ''', (status, progress_percent, now, task_id))
        
        if notes:
            self.cursor.execute('''
                UPDATE todos SET notes = ? WHERE id = ?
            ''', (notes, task_id))
        
        self.conn.commit()
        print(f"✅ Task {task_id} updated to status: {status}")
    
    def show_task(self, task_id):
        """Show detailed information about a task"""
        self.cursor.execute('SELECT * FROM todos WHERE id = ?', (task_id,))
        task = self.cursor.fetchone()
        
        if not task:
            print(f"❌ Task {task_id} not found")
            return None
        
        print(f"\n📋 Task #{task['id']}: {task['title']}")
        print(f"   Status: {task['status']} ({task['progress_percent']}%)")
        print(f"   Priority: {task['priority']}/5 | Due: {task['due_date']}")
        print(f"   Category: {task['category']} | Assigned: {task['assigned_to']}")
        
        if task['project_path']:
            print(f"   Project: {task['project_path']}")
            if task['project_file']:
                print(f"   File: {task['project_file']}")
        
        if task['tags']:
            print(f"   Tags: {task['tags']}")
        
        if task['description']:
            print(f"\n📝 Description:\n   {task['description']}")
        
        if task['notes']:
            print(f"\n📓 Notes:\n   {task['notes']}")
        
        if task['blocked_by']:
            print(f"\n🚫 Blocked by: {task['blocked_by']}")
        
        print(f"\n⏰ Created: {task['created_at']}")
        print(f"   Updated: {task['last_updated']}")
        if task['completed_at']:
            print(f"   Completed: {task['completed_at']}")
        
        return task
    
    def close(self):
        """Close database connection"""
        self.conn.close()

def print_tasks_table(tasks):
    """Print tasks in a formatted table"""
    if not tasks:
        print("No tasks found")
        return
    
    print("\n📋 ACTIVE TASKS")
    print("=" * 80)
    print(f"{'ID':<4} {'Priority':<8} {'Status':<12} {'Due':<12} {'Title':<40}")
    print("-" * 80)
    
    for task in tasks:
        # Status emoji
        status_emoji = {
            'pending': '🔴',
            'in_progress': '🟡',
            'blocked': '⏸️',
            'completed': '✅'
        }.get(task['status'], '❓')
        
        # Priority stars
        priority_stars = '⭐' * task['priority']
        
        print(f"{task['id']:<4} {priority_stars:<8} {status_emoji} {task['status']:<10} "
              f"{task['due_date'] or 'N/A':<12} {task['title'][:37]:<37}...")

def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python3 task_helper.py [command] [options]")
        print("\nCommands:")
        print("  list [status] [priority] [category] - List tasks")
        print("  add \"title\" \"description\" [category] [priority] - Add task")
        print("  update [id] [status] [progress%] - Update task status")
        print("  show [id] - Show task details")
        print("  help - Show this help")
        return
    
    command = sys.argv[1]
    manager = TaskManager()
    
    try:
        if command == "list":
            status = sys.argv[2] if len(sys.argv) > 2 else None
            priority = int(sys.argv[3]) if len(sys.argv) > 3 else None
            category = sys.argv[4] if len(sys.argv) > 4 else None
            
            tasks = manager.list_tasks(status, priority, category)
            print_tasks_table(tasks)
            
            # Show summary
            total = len(tasks)
            completed = sum(1 for t in tasks if t['status'] == 'completed')
            in_progress = sum(1 for t in tasks if t['status'] == 'in_progress')
            pending = sum(1 for t in tasks if t['status'] == 'pending')
            
            print(f"\n📊 Summary: {total} tasks ({completed}✅ {in_progress}🟡 {pending}🔴)")
        
        elif command == "add":
            if len(sys.argv) < 4:
                print("Usage: add \"title\" \"description\" [category] [priority]")
                return
            
            title = sys.argv[2]
            description = sys.argv[3]
            category = sys.argv[4] if len(sys.argv) > 4 else "general"
            priority = int(sys.argv[5]) if len(sys.argv) > 5 else 3
            
            manager.add_task(title, description, category, priority)
        
        elif command == "update":
            if len(sys.argv) < 4:
                print("Usage: update [id] [status] [progress%]")
                return
            
            task_id = int(sys.argv[2])
            status = sys.argv[3]
            progress = int(sys.argv[4]) if len(sys.argv) > 4 else None
            
            manager.update_status(task_id, status, progress)
        
        elif command == "show":
            if len(sys.argv) < 3:
                print("Usage: show [id]")
                return
            
            task_id = int(sys.argv[2])
            manager.show_task(task_id)
        
        elif command == "help":
            print("Task Management System Helper")
            print("\nDatabase:", DB_PATH)
            print("\nAvailable statuses: pending, in_progress, blocked, completed")
            print("Priorities: 1 (lowest) to 5 (highest)")
            print("\nExamples:")
            print("  python3 task_helper.py list")
            print("  python3 task_helper.py list pending")
            print("  python3 task_helper.py add \"Research topic\" \"Detailed description\" research 4")
            print("  python3 task_helper.py update 1 in_progress 50")
            print("  python3 task_helper.py show 1")
        
        else:
            print(f"Unknown command: {command}")
            print("Use 'help' for available commands")
    
    finally:
        manager.close()

if __name__ == "__main__":
    main()