# Task Management System Architecture
**Created:** 2026-02-28 by Richard De Clawbeaux  
**Last Updated:** 2026-02-28 23:55 UTC  
**Status:** ✅ **IMPLEMENTED**

## Overview

A two-level task management system that combines centralized tracking with project-specific context.

### Core Philosophy
- **SQLite Master Registry:** Single source of truth for task status
- **Project Files:** Rich implementation context in project folders
- **Linked System:** Bi-directional references between SQLite and project files
- **No Cron Duplication:** Cron handles automated execution, tasks track manual work

## Architecture

### Level 1: SQLite Master Task Registry
**Location:** `/home/openclaw/.openclaw/memory/main.sqlite` → `todos` table
**Purpose:** Centralized task tracking, status management, priority coordination

### Level 2: Project-Specific Task Files
**Location:** Project folders (e.g., `projects/clawchat/todo.md`)
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
| `assigned_to` | TEXT | Responsible party (Richard, Jeff, Kimi, System) |
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
VALUES ('Implement Python UDP hole punching', 
        'Create Python implementation of UDP hole punching with Mega.nz signaling',
        'development', 3, 'pending', '2026-03-05',
        '/home/openclaw/.openclaw/workspace/users/jeff/projects/clawchat/',
        'todo.md', 'Richard');
```

```markdown
<!-- Project todo.md file -->
# ClawChat Security Implementation

## SQLite Task Reference
- **Task ID:** [SQLITE_TASK_ID]
- **Status:** pending
- **Assigned:** Richard
- **Due:** 2026-03-05

## Technical Details
[Implementation steps, code snippets, architecture diagrams]
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

### Example: AI Judicial Research
```
Cron Job (jobs.json):
  - Name: ai-judicial-monthly-update
  - Schedule: 0 9 1 * * (monthly on 1st at 09:00 UTC)
  - Action: Creates/updates task in SQLite

SQLite Task:
  - Title: "Research AI judicial developments for March 2026"
  - Status: pending → in_progress → completed
  - Assigned: Richard
  - Project: users/jeff/projects/ai-judicial-research/
```

### Benefits
- ✅ **No duplication** - Cron schedules, tasks track work
- ✅ **Status tracking** - Can see research progress
- ✅ **History** - Complete record of what was done
- ✅ **Flexibility** - Manual override if cron fails

## Implementation Status

### ✅ Completed
1. **Enhanced SQLite schema** with all proposed columns
2. **Updated existing tasks** with default values
3. **Created documentation** (this file)

### 🔄 In Progress
1. **Update project todo files** with SQLite task IDs
2. **Create helper scripts** for task management
3. **Update SOUL.md** with new workflow instructions

### 📅 Planned
1. **Migration script** for existing project todos
2. **Dashboard/view** for task status overview
3. **Integration with memory system** for automatic task creation

## Usage Guidelines

### For Richard (AI Assistant)
1. **Always check SQLite `todos` table** before starting work
2. **Follow priority order** (5 → 1, then due date)
3. **Update status regularly** as work progresses
4. **Link to project files** for implementation context
5. **Document decisions** in both SQLite and project files

### For Jeff (Human)
1. **Add tasks to SQLite** (centralized management)
2. **Check task dashboard** for overall status
3. **Update priorities** as needed
4. **Review project files** for technical details

### For System (Automation)
1. **Cron creates tasks** but doesn't track them
2. **Automated updates** to task status where possible
3. **Notifications** for overdue or blocked tasks

## Future Enhancements

### Phase 2: Advanced Features
1. **Task templates** for common project types
2. **Time tracking integration** with actual hours
3. **Dependency resolution** automatic scheduling
4. **Recurring task management** with pattern support

### Phase 3: Integration
1. **GitHub issues sync** (bi-directional)
2. **Calendar integration** for due dates
3. **Notification system** for updates
4. **Reporting dashboard** with metrics

## Conclusion

This two-level task management system provides:
- ✅ **Centralized control** via SQLite
- ✅ **Rich context** in project folders  
- ✅ **Clear linkages** between systems
- ✅ **Scalable architecture** for any number of projects
- ✅ **No duplication** with existing systems (cron, memory, schedule)

**Next Step:** Update project todo files with SQLite task IDs and create helper scripts.