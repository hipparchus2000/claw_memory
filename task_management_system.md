# Task Management System Architecture
**Created:** 2026-02-28 by Richard De Clawbeaux  
**Last Updated:** 2026-03-01 00:15 UTC  
**Status:** ✅ **IMPLEMENTED** (Private - NOT pushed to GitHub)
**Security Note:** This documentation contains internal paths - DO NOT push to public GitHub

## Overview

A two-level task management system that combines centralized tracking with project-specific context.

### Core Philosophy
- **SQLite Master Registry:** Single source of truth for task status
- **Project Files:** Rich implementation context in project folders
- **Linked System:** Bi-directional references between SQLite and project files
- **No Cron Duplication:** Cron handles automated execution, tasks track manual work

## Architecture

### Level 1: SQLite Master Task Registry
**Location:** SQLite database → `todos` table
**Purpose:** Centralized task tracking, status management, priority coordination

### Level 2: Project-Specific Task Files
**Location:** Project folders (e.g., project todo.md files)
**Purpose:** Detailed technical context, implementation steps, collaboration space

### Integration with Other Systems
- **Cron Jobs:** Automated execution schedules (no duplication)
- **Memory Files:** Task discussions and decisions
- **Schedule File:** Template tasks by frequency

## SQLite Schema

### Table: `todos`

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `title` | TEXT | Task title (concise) |
| `description` | TEXT | Detailed task description |
| `category` | TEXT | Task category (research, system, documentation, architecture) |
| `priority` | INTEGER | 1-5 (5 = highest) |
| `status` | TEXT | pending, in_progress, blocked, completed |
| `due_date` | TEXT | Due date (YYYY-MM-DD) |
| `created_at` | TEXT | Creation timestamp (ISO) |
| `completed_at` | TEXT | Completion timestamp (ISO) |
| `tags` | TEXT | Comma-separated tags |
| `project_path` | TEXT | Path to project folder |
| `project_file` | TEXT | Specific file in project |
| `external_ref` | TEXT | External reference (GitHub issue, etc.) |
| `parent_task_id` | INTEGER | For subtasks hierarchy |
| `dependencies` | TEXT | JSON array of task IDs this depends on |
| `estimated_hours` | REAL | Time estimate in hours |
| `actual_hours` | REAL | Actual time spent |
| `recurring` | TEXT | Recurrence pattern (daily, weekly, monthly, cron) |
| `next_recurrence` | TEXT | Next occurrence date |
| `assigned_to` | TEXT | Who's responsible (Richard, Jeff, Kimi, System) |
| `last_updated` | TEXT | Last status update timestamp |
| `blocked_by` | TEXT | What's blocking this task |
| `progress_percent` | INTEGER | 0-100% completion |
| `notes` | TEXT | Additional notes |
| `priority_reason` | TEXT | Why this priority was assigned |
| `completion_notes` | TEXT | Notes on completion |

## Workflow

### 1. Task Creation
```sql
-- SQLite entry (master registry)
INSERT INTO todos (title, description, category, priority, status, due_date, 
                   project_path, project_file, assigned_to)
VALUES ('Implement feature', 'Detailed description', 'development', 3, 'pending', 
        '2026-03-05', '/path/to/project/', 'todo.md', 'Richard');
```

### 2. Task Execution
1. **Check SQLite** for highest priority tasks
2. **Navigate to project folder** using `project_path`
3. **Read project file** for implementation details
4. **Update SQLite status** as work progresses
5. **Add notes** to both SQLite and project file

### 3. Task Completion
1. **Mark complete** in SQLite (`status = 'completed'`, `progress_percent = 100`)
2. **Add completion notes** to both locations
3. **Archive** project implementation details
4. **Trigger dependent tasks** if any

## Cron Integration Strategy

### Separation of Concerns
- **Cron:** **WHEN** to execute (schedule, automation)
- **Tasks:** **WHAT** to do (work items, manual effort)

### Benefits
- ✅ **No duplication** - Cron schedules, tasks track work
- ✅ **Status tracking** - Can see progress
- ✅ **History** - Complete record of what was done
- ✅ **Flexibility** - Manual override if cron fails

## Implementation Status

### ✅ Completed
1. **Enhanced SQLite schema** with all proposed columns
2. **Updated existing tasks** with default values
3. **Created documentation** (this file - PRIVATE)
4. **Created helper script** (`task_helper.py` in shared/tools/)
5. **Updated project todo files** with SQLite task IDs
6. **Imported all todos** from documentation into SQLite (19 active tasks)
7. **Removed outdated todo files** (`updated_todos_focus.md`, `todos_and_goals.md`)

### 🔄 In Progress
1. **Migration script** for existing project todos
2. **Dashboard/view** for task status overview

### 🚨 Cleanup Completed:
- **Removed:** `updated_todos_focus.md` (outdated Feb 27 todo list)
- **Removed:** `todos_and_goals.md` (conflicting todo documentation)
- **Reason:** SQLite is now single source of truth for todos
- **All tasks imported:** 12 new todos imported into SQLite database

## Usage Guidelines

### For Richard (AI Assistant)
1. **Always check SQLite `todos` table** before starting work
2. **Follow priority order** (5 → 1, then due date)
3. **Update status regularly** as work progresses
4. **Link to project files** for implementation context
5. **Document decisions** in both SQLite and project files

### Security Rules (CRITICAL):
- **NEVER push from Jeff's private space** to GitHub
- **ONLY push from Richard's project space** if repository is public
- **Verify directory** before any git operation
- **Check for private paths** in documentation

## Future Enhancements

### Phase 2: Advanced Features
1. **Task templates** for common project types
2. **Time tracking integration** with actual hours
3. **Dependency resolution** automatic scheduling
4. **Recurring task management** with pattern support

## Conclusion

This two-level task management system provides:
- ✅ **Centralized control** via SQLite
- ✅ **Rich context** in project folders  
- ✅ **Clear linkages** between systems
- ✅ **Scalable architecture** for any number of projects
- ✅ **No duplication** with existing systems (cron, memory, schedule)

**Security Note:** This file contains internal system architecture and should NOT be pushed to public GitHub repositories.