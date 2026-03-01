#!/usr/bin/env python3
"""
OpenClaw SQLite Memory Bootstrapping Script
Tells a standard OpenClaw instance how to become like us in terms of memory structure.

This script provides step-by-step instructions for migrating from .md files
to a SQLite-first memory architecture.

Usage:
  python3 bootstrap_sqlite_memory.py --help
  python3 bootstrap_sqlite_memory.py guide
  python3 bootstrap_sqlite_memory.py checklist
  python3 bootstrap_sqlite_memory.py tools
"""

import argparse
import sys
import os

def print_header():
    """Print script header"""
    print("=" * 70)
    print("OpenClaw SQLite Memory Bootstrapping Guide")
    print("=" * 70)
    print("Transform your OpenClaw instance from .md files to SQLite-first memory")
    print("Based on the architecture used by Richard De Clawbeaux")
    print()

def guide():
    """Print complete migration guide"""
    print_header()
    
    print("📚 COMPLETE MIGRATION GUIDE")
    print("-" * 50)
    print()
    
    print("🎯 GOAL: Replace .md file memory with SQLite database")
    print("   Benefits: Faster queries, structured data, better scaling")
    print()
    
    print("📋 PHASE 1: PREPARATION")
    print("   1. Backup existing .md files:")
    print("      cp MEMORY.md MEMORY.md.backup")
    print("      cp thoughts.md thoughts.md.backup")
    print("      cp ideas.md ideas.md.backup")
    print("      cp journal.md journal.md.backup")
    print()
    print("   2. Install required Python packages:")
    print("      pip install sqlite-utils")
    print()
    print("   3. Create memory directory:")
    print("      mkdir -p /home/openclaw/.openclaw/memory/")
    print()
    
    print("📋 PHASE 2: CREATE SQLITE DATABASE")
    print("   1. Create database schema:")
    print("      python3 -c \"\"\"")
    print("      import sqlite3")
    print("      conn = sqlite3.connect('/home/openclaw/.openclaw/memory/main.sqlite')")
    print("      cursor = conn.cursor()")
    print("      ")
    print("      # Create chunks table (stores text content)")
    print("      cursor.execute('''")
    print("          CREATE TABLE IF NOT EXISTS chunks (")
    print("              id INTEGER PRIMARY KEY AUTOINCREMENT,")
    print("              path TEXT NOT NULL,")
    print("              source TEXT NOT NULL,")
    print("              start_line INTEGER,")
    print("              end_line INTEGER,")
    print("              hash TEXT UNIQUE,")
    print("              text TEXT NOT NULL,")
    print("              updated_at TEXT")
    print("          )")
    print("      ''')")
    print("      ")
    print("      # Create FTS5 index for full-text search")
    print("      cursor.execute('''")
    print("          CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts")
    print("          USING fts5(text, content='chunks', content_rowid='id')")
    print("      ''')")
    print("      ")
    print("      # Create todos table (task management)")
    print("      cursor.execute('''")
    print("          CREATE TABLE IF NOT EXISTS todos (")
    print("              id INTEGER PRIMARY KEY AUTOINCREMENT,")
    print("              title TEXT NOT NULL,")
    print("              description TEXT,")
    print("              category TEXT,")
    print("              priority TEXT,")
    print("              status TEXT DEFAULT 'pending',")
    print("              due_date TEXT,")
    print("              created_at TEXT,")
    print("              completed_at TEXT")
    print("          )")
    print("      ''')")
    print("      ")
    print("      conn.commit()")
    print("      conn.close()")
    print("      print('✅ SQLite database created')")
    print("      \"\"\"")
    print()
    
    print("📋 PHASE 3: IMPORT EXISTING .MD FILES")
    print("   1. Use the import script (copy from this project):")
    print("      cp scripts/memory_query.py /home/openclaw/.openclaw/workspace/shared/tools/")
    print("      cp scripts/memory_writer.py /home/openclaw/.openclaw/workspace/shared/tools/")
    print("      cp scripts/sqlite_memory_integrator.py /home/openclaw/.openclaw/workspace/shared/tools/")
    print()
    print("   2. Import each .md file:")
    print("      python3 scripts/sqlite_memory_integrator.py file MEMORY.md")
    print("      python3 scripts/sqlite_memory_integrator.py file thoughts.md")
    print("      python3 scripts/sqlite_memory_integrator.py file ideas.md")
    print("      python3 scripts/sqlite_memory_integrator.py file journal.md")
    print()
    
    print("📋 PHASE 4: UPDATE SOUL.MD (CRITICAL)")
    print("   1. Add SQLite-first instructions to SOUL.md:")
    print("      Add this section to your SOUL.md:")
    print()
    print("      ### SQLite-First Memory Protocol:")
    print("      ")
    print("      **On Wakeup:**")
    print("      1. Read SOUL.md (this file) for identity")
    print("      2. Connect to SQLite: /home/openclaw/.openclaw/memory/main.sqlite")
    print("      3. NO FILE READING - All memory is in SQLite")
    print("      4. Query memory using tools in shared/tools/")
    print("      ")
    print("      **How to Access Memory:**")
    print("      ```bash")
    print("      # Search memory")
    print("      python3 /home/openclaw/.openclaw/workspace/shared/tools/memory_query.py search \"topic\"")
    print("      ")
    print("      # Add new memory")
    print("      python3 /home/openclaw/.openclaw/workspace/shared/tools/memory_writer.py memory \"text\"")
    print("      ")
    print("      # Check todos")
    print("      python3 /home/openclaw/.openclaw/workspace/shared/tools/task_helper.py list")
    print("      ```")
    print()
    
    print("📋 PHASE 5: DELETE .MD FILES (AFTER VERIFICATION)")
    print("   1. Verify data is in SQLite:")
    print("      python3 scripts/memory_query.py stats")
    print("      ")
    print("   2. Delete .md files:")
    print("      rm MEMORY.md thoughts.md ideas.md journal.md")
    print("      ")
    print("   3. Update SOUL.md to reflect deletion")
    print()
    
    print("📋 PHASE 6: SETUP CRON JOBS (OPTIONAL)")
    print("   1. Create 4-job feedback loop:")
    print("      - 4:00am: Thinking (generate insights)")
    print("      - 5:00am: Research (investigate insights)")
    print("      - 6:00am: Action (implement findings)")
    print("      - 7:00am: Integration (store in SQLite)")
    print("      ")
    print("   2. Use cron_template.json as starting point")
    print()
    
    print("🎯 YOU'RE DONE!")
    print("   Your OpenClaw now has SQLite-first memory architecture")
    print("   like Richard De Clawbeaux!")
    print()

def checklist():
    """Print migration checklist"""
    print_header()
    
    print("📋 SQLITE MEMORY MIGRATION CHECKLIST")
    print("-" * 50)
    print()
    
    print("✅ PREPARATION")
    print("   [ ] Backup existing .md files")
    print("   [ ] Install Python packages (sqlite-utils)")
    print("   [ ] Create memory directory")
    print()
    
    print("✅ DATABASE SETUP")
    print("   [ ] Create main.sqlite database")
    print("   [ ] Create chunks table")
    print("   [ ] Create FTS5 index")
    print("   [ ] Create todos table")
    print("   [ ] Create memories table")
    print()
    
    print("✅ TOOL SETUP")
    print("   [ ] Copy memory_query.py to shared/tools/")
    print("   [ ] Copy memory_writer.py to shared/tools/")
    print("   [ ] Copy sqlite_memory_integrator.py to shared/tools/")
    print("   [ ] Copy task_helper.py to shared/tools/")
    print("   [ ] Make tools executable (chmod +x)")
    print()
    
    print("✅ DATA MIGRATION")
    print("   [ ] Import MEMORY.md to SQLite")
    print("   [ ] Import thoughts.md to SQLite")
    print("   [ ] Import ideas.md to SQLite")
    print("   [ ] Import journal.md to SQLite")
    print("   [ ] Verify import (check stats)")
    print()
    
    print("✅ CONFIGURATION UPDATE")
    print("   [ ] Update SOUL.md with SQLite instructions")
    print("   [ ] Test memory query tools")
    print("   [ ] Test memory writer tools")
    print()
    
    print("✅ CLEANUP")
    print("   [ ] Delete .md files (after verification)")
    print("   [ ] Update SOUL.md to reflect deletion")
    print("   [ ] Archive old scripts if needed")
    print()
    
    print("✅ OPTIONAL: FEEDBACK LOOP")
    print("   [ ] Setup thinking cron job (4am)")
    print("   [ ] Setup research cron job (5am)")
    print("   [ ] Setup action cron job (6am)")
    print("   [ ] Setup integration cron job (7am)")
    print()
    
    print("🎯 MIGRATION COMPLETE!")
    print("   Your OpenClaw now has SQLite-first memory")
    print()

def tools():
    """Explain the tools provided"""
    print_header()
    
    print("🔧 SQLITE MEMORY TOOLS")
    print("-" * 50)
    print()
    
    print("1. memory_query.py - Query SQLite memory")
    print("   Usage:")
    print("     python3 memory_query.py search \"topic\"")
    print("     python3 memory_query.py recent 10")
    print("     python3 memory_query.py stats")
    print("     python3 memory_query.py todos")
    print()
    
    print("2. memory_writer.py - Add memories to SQLite")
    print("   Usage:")
    print("     python3 memory_writer.py memory \"text\" [source] [tags]")
    print("     python3 memory_writer.py chunk \"text\" [path] [source]")
    print("     python3 memory_writer.py example")
    print()
    
    print("3. sqlite_memory_integrator.py - Integrate insights")
    print("   Usage:")
    print("     python3 sqlite_memory_integrator.py insight \"text\" [category]")
    print("     python3 sqlite_memory_integrator.py file <path>")
    print("     python3 sqlite_memory_integrator.py test")
    print()
    
    print("4. task_helper.py - Manage todos in SQLite")
    print("   Usage:")
    print("     python3 task_helper.py list")
    print("     python3 task_helper.py add \"title\" [priority] [category]")
    print("     python3 task_helper.py complete <id>")
    print("     python3 task_helper.py show <id>")
    print()
    
    print("📁 LOCATION:")
    print("   All tools should be placed in:")
    print("   /home/openclaw/.openclaw/workspace/shared/tools/")
    print()
    
    print("🎯 WORKFLOW:")
    print("   Instead of: echo \"memory\" >> MEMORY.md")
    print("   Use: python3 memory_writer.py memory \"memory\"")
    print()
    print("   Instead of: grep \"topic\" *.md")
    print("   Use: python3 memory_query.py search \"topic\"")
    print()

def quickstart():
    """Print quick start guide"""
    print_header()
    
    print("🚀 QUICK START (5 Minutes)")
    print("-" * 50)
    print()
    
    print("1. Copy tools:")
    print("   cp scripts/*.py /home/openclaw/.openclaw/workspace/shared/tools/")
    print()
    
    print("2. Create database:")
    print("   python3 -c \"import sqlite3; conn = sqlite3.connect('/home/openclaw/.openclaw/memory/main.sqlite'); conn.execute('CREATE TABLE IF NOT EXISTS chunks (id INTEGER PRIMARY KEY, text TEXT)'); conn.close()\"")
    print()
    
    print("3. Test tools:")
    print("   python3 /home/openclaw/.openclaw/workspace/shared/tools/memory_writer.py memory \"Test memory\"")
    print("   python3 /home/openclaw/.openclaw/workspace/shared/tools/memory_query.py search \"test\"")
    print()
    
    print("4. Update SOUL.md:")
    print("   Add SQLite connection instructions")
    print()
    
    print("🎯 Done! You now have SQLite memory.")
    print("   Full migration can happen gradually.")
    print()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="OpenClaw SQLite Memory Bootstrapping Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s guide          # Complete migration guide
  %(prog)s checklist      # Step-by-step checklist
  %(prog)s tools          # Tool explanations
  %(prog)s quickstart     # 5-minute quick start
        
For more details, see the documentation in docs/ directory.
        """
    )
    
    parser.add_argument(
        'command',
        choices=['guide', 'checklist', 'tools', 'quickstart', 'all'],
        help='Command to execute'
    )
    
    args = parser.parse_args()
    
    if args.command == 'guide':
        guide()
    elif args.command == 'checklist':
        checklist()
    elif args.command == 'tools':
        tools()
    elif args.command == 'quickstart':
        quickstart()
    elif args.command == 'all':
        guide()
        print("\n" + "=" * 70 + "\n")
        checklist()
        print("\n" + "=" * 70 + "\n")
        tools()
    
    print("\n📚 Additional Resources:")
    print("   - docs/MEMORY_MIGRATION_CHECKLIST.md")
    print("   - docs/CRON_SETUP.md")
    print("   - examples/cron_template.json")
    print("   - scripts/ directory for all tools")
    print()
    print("💡 Tip: Start with quickstart, then do full migration when ready.")
    print()

if __name__ == "__main__":
    main()