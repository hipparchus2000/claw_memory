#!/usr/bin/env python3
"""
Memory Compressor - Cron job for daily memory compression
Runs at 4:30am UTC, after the 4am thinking session
"""

import sqlite3
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

class DailyMemoryCompressor:
    """Daily compression job for memory optimization"""
    
    def __init__(self, db_path="/home/openclaw/.openclaw/workspace/memory/memory.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.today = datetime.now(timezone.utc).date()
        self.yesterday = self.today - timedelta(days=1)
        
    def compress_yesterday_files(self):
        """Find and compress files from yesterday"""
        print(f"Compressing files from {self.yesterday}")
        
        # Look for yesterday's files in workspace
        workspace_path = "/home/openclaw/.openclaw/workspace"
        compressed_count = 0
        
        # Common patterns for daily files
        file_patterns = [
            f"*{self.yesterday.strftime('%Y-%m-%d')}*",
            f"*{self.yesterday.strftime('%Y%m%d')}*",
            "today_thoughts*.md",
            "daily_*.log",
            "security/logs/*.log"
        ]
        
        for pattern in file_patterns:
            try:
                for file_path in Path(workspace_path).glob(pattern):
                    if file_path.is_file():
                        compressed = self.compress_file(file_path)
                        if compressed:
                            compressed_count += 1
            except Exception as e:
                print(f"Error processing pattern {pattern}: {e}")
        
        return compressed_count
    
    def compress_file(self, file_path):
        """Compress a single file into memory database"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Skip if already compressed
            self.cursor.execute('''
            SELECT COUNT(*) FROM memories WHERE original_file_path = ?
            ''', (str(file_path),))
            if self.cursor.fetchone()[0] > 0:
                print(f"  Already compressed: {file_path.name}")
                return False
            
            # Determine importance based on file type and content
            importance = self.rate_file_importance(file_path, content)
            
            # Extract metadata
            memory_type = self.determine_memory_type(file_path)
            category = self.determine_category(content)
            tags = self.extract_tags(content)
            
            # Store compressed memory
            self.cursor.execute('''
            INSERT INTO memories (
                timestamp, user_id, memory_type, content, category,
                tags, importance, compression_status, original_file_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now(timezone.utc).isoformat(),
                "jeff",
                memory_type,
                content[:2000],  # Compress to first 2000 chars
                category,
                json.dumps(tags),
                importance,
                "compressed",
                str(file_path)
            ))
            
            memory_id = self.cursor.lastrowid
            
            # Update FTS
            self.cursor.execute('''
            INSERT INTO memories_fts (rowid, content, tags)
            VALUES (?, ?, ?)
            ''', (memory_id, content[:2000], json.dumps(tags)))
            
            print(f"  Compressed: {file_path.name} -> importance {importance}")
            return True
            
        except Exception as e:
            print(f"  Error compressing {file_path}: {e}")
            return False
    
    def rate_file_importance(self, file_path, content):
        """Rate file importance (0-5)"""
        importance = 2  # Default
        
        # Boost based on file type
        filename = file_path.name.lower()
        if 'memory' in filename or 'MEMORY' in filename:
            importance = 5
        elif 'thought' in filename:
            importance = 4
        elif 'idea' in filename:
            importance = 4
        elif 'specification' in filename or 'design' in filename:
            importance = 4
        elif 'journal' in filename:
            importance = 3
        elif 'log' in filename:
            importance = 1  # Logs are low importance
        
        # Adjust based on content
        content_lower = content.lower()
        if any(word in content_lower for word in ['critical', 'essential', 'core', 'principle']):
            importance = min(5, importance + 1)
        if any(word in content_lower for word in ['error', 'failed', 'warning']):
            importance = max(1, importance - 1)  # Errors might be important
        
        return importance
    
    def determine_memory_type(self, file_path):
        """Determine memory type from filename"""
        filename = file_path.name.lower()
        if 'thought' in filename:
            return 'thought'
        elif 'idea' in filename:
            return 'idea'
        elif 'memory' in filename:
            return 'memory'
        elif 'journal' in filename:
            return 'journal'
        elif 'log' in filename:
            return 'log'
        elif 'specification' in filename or 'design' in filename:
            return 'specification'
        else:
            return 'document'
    
    def determine_category(self, content):
        """Determine category from content"""
        content_lower = content.lower()
        if any(word in content_lower for word in ['sqlite', 'database', 'python', 'code']):
            return 'technology'
        elif any(word in content_lower for word in ['memory', 'remember', 'forget', 'compression']):
            return 'memory'
        elif any(word in content_lower for word in ['ai', 'assistant', 'evolution', 'thinking']):
            return 'ai-evolution'
        elif any(word in content_lower for word in ['project', 'implementation', 'phase']):
            return 'project'
        else:
            return 'general'
    
    def extract_tags(self, content):
        """Extract tags from content"""
        tags = []
        content_lower = content.lower()
        
        tag_patterns = {
            'compression': ['compress', 'curation', 'importance'],
            'memory': ['memory', 'remember', 'forget'],
            'sqlite': ['sqlite', 'database'],
            'ai': ['ai', 'artificial intelligence'],
            'collaboration': ['collaboration', 'partnership'],
            'thinking': ['think', 'reflection', 'insight'],
            'cron': ['cron', 'schedule', 'job'],
            'project': ['project', 'implementation']
        }
        
        for tag, patterns in tag_patterns.items():
            for pattern in patterns:
                if pattern in content_lower:
                    tags.append(tag)
                    break
        
        return list(set(tags))
    
    def update_access_patterns(self):
        """Update access count for frequently accessed memories"""
        # Simple implementation: increment access count for memories accessed today
        # In future, this could be more sophisticated
        self.cursor.execute('''
        UPDATE memories 
        SET access_count = access_count + 1,
            last_accessed = ?
        WHERE id IN (
            SELECT id FROM memories 
            WHERE importance >= 4 
            ORDER BY RANDOM() 
            LIMIT 5
        )
        ''', (datetime.now(timezone.utc).isoformat(),))
        
        updated = self.cursor.rowcount
        print(f"Updated access patterns for {updated} memories")
    
    def generate_compression_report(self):
        """Generate report of compression activity"""
        self.cursor.execute('''
        SELECT 
            COUNT(*) as total_memories,
            COUNT(CASE WHEN compression_status = 'compressed' THEN 1 END) as compressed_count,
            COUNT(CASE WHEN importance >= 4 THEN 1 END) as critical_count,
            AVG(importance) as avg_importance
        FROM memories
        ''')
        
        stats = self.cursor.fetchone()
        
        report = f"""
        === Memory Compression Report ===
        Date: {self.today}
        
        Database Statistics:
        - Total memories: {stats[0]}
        - Compressed memories: {stats[1]}
        - Critical memories (importance >= 4): {stats[2]}
        - Average importance: {stats[3]:.1f}
        
        Compression Principle:
        "Forgetting noise enables remembering signal"
        
        Next scheduled compression: Tomorrow 4:30am UTC
        """
        
        return report
    
    def run_daily_compression(self):
        """Run full daily compression routine"""
        print("=" * 60)
        print(f"Daily Memory Compression - {self.today}")
        print("=" * 60)
        
        # Step 1: Compress yesterday's files
        print("\n1. Compressing yesterday's files...")
        compressed = self.compress_yesterday_files()
        print(f"   Compressed {compressed} files")
        
        # Step 2: Update access patterns
        print("\n2. Updating access patterns...")
        self.update_access_patterns()
        
        # Step 3: Generate report
        print("\n3. Generating compression report...")
        report = self.generate_compression_report()
        print(report)
        
        # Step 4: Commit changes
        self.conn.commit()
        print(f"\n4. Changes committed to database")
        
        # Step 5: Cleanup (optional - in future phases)
        # self.cleanup_old_files()
        
        return compressed
    
    def cleanup(self):
        """Cleanup database connection"""
        self.conn.close()

def main():
    """Main function for cron job execution"""
    print("Starting memory compression job...")
    
    try:
        compressor = DailyMemoryCompressor()
        compressed_count = compressor.run_daily_compression()
        compressor.cleanup()
        
        # Return success code
        sys.exit(0 if compressed_count >= 0 else 1)
        
    except Exception as e:
        print(f"Error in compression job: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()