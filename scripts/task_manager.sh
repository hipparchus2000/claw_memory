#!/bin/bash

# Task Management System for OpenClaw
# Always consult TODOs for next task, mark completed tasks as complete

set -e

SQLITE_DB="/home/openclaw/.openclaw/memory/main.sqlite"

echo "=== TASK MANAGEMENT SYSTEM ==="
echo ""

# Function to show next task
show_next_task() {
    python3 -c "
import sqlite3
import datetime

conn = sqlite3.connect('$SQLITE_DB')
cursor = conn.cursor()

# Get highest priority pending task
cursor.execute('''
    SELECT title, priority, due_date, description
    FROM todos 
    WHERE status = 'pending'
    ORDER BY priority DESC, due_date
    LIMIT 1
''')

task = cursor.fetchone()

if task:
    title, priority, due_date, description = task
    print('🎯 NEXT TASK:')
    print(f'   Priority: {priority}')
    print(f'   Title: {title}')
    print(f'   Due: {due_date}')
    if description:
        print(f'   Description: {description[:100]}...')
else:
    print('✅ No pending tasks!')

conn.close()
"
}

# Function to mark task complete
mark_complete() {
    local task_title="$1"
    
    python3 -c "
import sqlite3
import datetime

conn = sqlite3.connect('$SQLITE_DB')
cursor = conn.cursor()

cursor.execute('''
    UPDATE todos 
    SET status = 'completed', completed_at = ?
    WHERE title = ? AND status != 'completed'
''', (datetime.datetime.now().isoformat(), '$task_title'))

rows_updated = cursor.rowcount
conn.commit()
conn.close()

if rows_updated > 0:
    print(f'✅ Task marked as COMPLETED: $task_title')
else:
    print(f'⚠️  Task not found or already completed: $task_title')
"
}

# Function to add new task
add_task() {
    local title="$1"
    local description="$2"
    local priority="${3:-3}"
    local due_date="${4:-$(date -d '+7 days' +%Y-%m-%d)}"
    
    python3 -c "
import sqlite3
import datetime

conn = sqlite3.connect('$SQLITE_DB')
cursor = conn.cursor()

cursor.execute('''
    INSERT INTO todos 
    (title, description, priority, due_date, created_at, status)
    VALUES (?, ?, ?, ?, ?, 'pending')
''', ('$title', '$description', $priority, '$due_date', datetime.datetime.now().isoformat()))

conn.commit()
conn.close()

print(f'✅ Task added: $title')
print(f'   Priority: $priority, Due: $due_date')
"
}

# Function to list all tasks
list_tasks() {
    python3 -c "
import sqlite3

conn = sqlite3.connect('$SQLITE_DB')
cursor = conn.cursor()

print('=== ALL TASKS ===')
print('')

# Pending tasks
cursor.execute('''
    SELECT title, priority, due_date, status
    FROM todos 
    WHERE status != 'completed'
    ORDER BY priority DESC, due_date
''')

pending = cursor.fetchall()

if pending:
    print('⏳ PENDING TASKS:')
    for title, priority, due_date, status in pending:
        status_emoji = '🔄' if status == 'in_progress' else '⏳'
        print(f'   $status_emoji [{priority}] $title (due: $due_date)')
else:
    print('✅ No pending tasks')

print('')

# Completed today
cursor.execute('''
    SELECT title, priority
    FROM todos 
    WHERE status = 'completed' 
    AND date(completed_at) = date('now')
    ORDER BY priority DESC
''')

completed = cursor.fetchall()

if completed:
    print('✅ COMPLETED TODAY:')
    for title, priority in completed:
        print(f'   [{priority}] $title')
else:
    print('📝 No tasks completed today')

conn.close()
"
}

# Main logic
case "${1:-show}" in
    "show")
        show_next_task
        ;;
    "complete")
        if [ -z "$2" ]; then
            echo "Usage: $0 complete \"Task Title\""
            exit 1
        fi
        mark_complete "$2"
        ;;
    "add")
        if [ -z "$2" ]; then
            echo "Usage: $0 add \"Task Title\" \"Description\" [priority] [due_date]"
            exit 1
        fi
        add_task "$2" "${3:-}" "${4:-3}" "${5:-}"
        ;;
    "list")
        list_tasks
        ;;
    "help")
        echo "Task Management Commands:"
        echo "  $0 show          - Show next task"
        echo "  $0 complete \"Title\" - Mark task as complete"
        echo "  $0 add \"Title\" \"Desc\" [priority] [due_date] - Add new task"
        echo "  $0 list          - List all tasks"
        echo ""
        echo "Priority: 1 (low) to 5 (critical)"
        echo "Due date: YYYY-MM-DD format"
        ;;
    *)
        show_next_task
        ;;
esac

echo ""
echo "=== SYSTEM READY ==="