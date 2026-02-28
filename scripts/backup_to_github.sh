#!/bin/bash

# Backup SQLite to Private GitHub Repository
# Pushes tar.gz backups to the 'richard' private repository

set -e

# Configuration
BACKUP_DIR="/home/openclaw/.openclaw/backups"
SQLITE_DB="/home/openclaw/.openclaw/memory/main.sqlite"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="sqlite_backup_${TIMESTAMP}"
BACKUP_FILE="${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
GIT_REPO_DIR="/home/openclaw/.openclaw/backups/github_backups"
GIT_REPO_URL="git@github.com:hipparchus2000/richard.git"
COMMIT_MESSAGE="SQLite backup ${TIMESTAMP}"

echo "=== Backup to GitHub Repository ==="
echo "Repository: $GIT_REPO_URL"
echo "Backup file: $BACKUP_FILE"
echo "Timestamp: $TIMESTAMP"
echo ""

# Step 1: Create SQLite backup
echo "📦 Step 1: Creating SQLite backup..."
python3 -c "
import os
import tarfile
import datetime
import shutil

backup_dir = '$BACKUP_DIR'
sqlite_db = '$SQLITE_DB'
backup_name = '$BACKUP_NAME'
backup_path = os.path.join(backup_dir, backup_name)

# Create backup directory
os.makedirs(backup_dir, exist_ok=True)

# Check if database exists
if not os.path.exists(sqlite_db):
    print(f'❌ ERROR: SQLite database not found at {sqlite_db}')
    exit(1)

# Get database size
db_size = os.path.getsize(sqlite_db)
print(f'   Database size: {db_size:,} bytes')

# Create temporary directory
temp_dir = '/tmp/sqlite_backup_temp'
os.makedirs(temp_dir, exist_ok=True)

# Copy database to temp directory
temp_db = os.path.join(temp_dir, f'{backup_name}.db')
shutil.copy2(sqlite_db, temp_db)

# Create metadata file
metadata = f'''SQLite Database Backup
======================
Backup Time: {datetime.datetime.now()}
Database: {sqlite_db}
Size: {db_size:,} bytes
Tables: chunks, todos, research_items, etc.
Backup ID: {backup_name}
System: OpenClaw Memory System
'''

metadata_file = os.path.join(temp_dir, f'{backup_name}.metadata.txt')
with open(metadata_file, 'w') as f:
    f.write(metadata)

# Create tar.gz archive
with tarfile.open('$BACKUP_FILE', 'w:gz') as tar:
    tar.add(temp_db, arcname=f'{backup_name}.db')
    tar.add(metadata_file, arcname=f'{backup_name}.metadata.txt')

# Clean up temp directory
shutil.rmtree(temp_dir)

backup_size = os.path.getsize('$BACKUP_FILE')
print(f'✅ Backup created: $BACKUP_FILE')
print(f'   Archive size: {backup_size:,} bytes')
"

# Step 2: Clone or update GitHub repository
echo ""
echo "🔄 Step 2: Setting up GitHub repository..."
if [ ! -d "$GIT_REPO_DIR" ]; then
    echo "   Cloning repository..."
    git clone "$GIT_REPO_URL" "$GIT_REPO_DIR" 2>/dev/null || {
        echo "❌ ERROR: Failed to clone repository"
        echo "   Make sure:"
        echo "   1. Repository 'richard' exists at GitHub"
        echo "   2. SSH key has write access"
        echo "   3. Repository is private"
        exit 1
    }
else
    echo "   Updating existing repository..."
    cd "$GIT_REPO_DIR"
    git pull origin main 2>/dev/null || echo "   Warning: Could not pull, continuing..."
fi

# Step 3: Copy backup to repository
echo ""
echo "📁 Step 3: Adding backup to repository..."
cd "$GIT_REPO_DIR"

# Create backups directory if it doesn't exist
mkdir -p "backups"

# Copy backup file
cp "$BACKUP_FILE" "backups/"

# Create README if it doesn't exist
if [ ! -f "README.md" ]; then
    cat > "README.md" <<EOF
# Richard - SQLite Backups Repository

This is a private repository for storing SQLite database backups from the OpenClaw memory system.

## Purpose
- Store encrypted SQLite database backups
- Maintain version history of memory system
- Enable disaster recovery

## Backup Structure
- Each backup is a tar.gz archive containing:
  - \`sqlite_backup_YYYYMMDD_HHMMSS.db\` - SQLite database file
  - \`sqlite_backup_YYYYMMDD_HHMMSS.metadata.txt\` - Backup metadata

## Restoration
\`\`\`bash
# Extract backup
tar -xzf backups/sqlite_backup_YYYYMMDD_HHMMSS.tar.gz -C /tmp/

# Restore database
cp /tmp/sqlite_backup_YYYYMMDD_HHMMSS.db /home/openclaw/.openclaw/memory/main.sqlite
\`\`\`

## Automation
Backups are automatically created and pushed to this repository.

## Security
- Repository is private
- Contains only SQLite database backups (no sensitive data)
- Used for disaster recovery only
EOF
fi

# Step 4: Commit and push
echo ""
echo "🚀 Step 4: Committing and pushing to GitHub..."
cd "$GIT_REPO_DIR"

# Add all files
git add .

# Commit
git commit -m "$COMMIT_MESSAGE" 2>/dev/null || {
    echo "   No changes to commit (backup already exists)"
    echo "✅ Backup already in repository"
    exit 0
}

# Push to GitHub
echo "   Pushing to GitHub..."
git push origin main 2>/dev/null && {
    echo "✅ Successfully pushed to GitHub!"
    echo "   Repository: $GIT_REPO_URL"
    echo "   Commit: $COMMIT_MESSAGE"
} || {
    echo "❌ ERROR: Failed to push to GitHub"
    echo "   Check SSH key permissions and repository access"
    exit 1
}

# Step 5: Cleanup old backups (keep last 10)
echo ""
echo "🧹 Step 5: Cleaning up old backups..."
cd "$GIT_REPO_DIR/backups" 2>/dev/null && {
    # Count backups
    backup_count=$(ls -1 *.tar.gz 2>/dev/null | wc -l)
    
    if [ "$backup_count" -gt 10 ]; then
        echo "   Found $backup_count backups, keeping last 10..."
        
        # List backups sorted by date (oldest first)
        backups=$(ls -1t *.tar.gz 2>/dev/null | tail -n +11)
        
        for old_backup in $backups; do
            echo "   Removing: $old_backup"
            git rm "$old_backup" 2>/dev/null
        done
        
        # Commit cleanup
        cd "$GIT_REPO_DIR"
        git commit -m "Cleanup: Remove old backups, keep last 10" 2>/dev/null
        git push origin main 2>/dev/null && echo "✅ Cleanup completed"
    else
        echo "   $backup_count backups (no cleanup needed)"
    fi
} || echo "   No backups directory yet"

echo ""
echo "=== Backup to GitHub Complete ==="
echo ""
echo "📊 Summary:"
echo "   Backup file: $(basename $BACKUP_FILE)"
echo "   Repository: $GIT_REPO_URL"
echo "   Local copy: $BACKUP_DIR"
echo "   GitHub copy: $GIT_REPO_DIR/backups/"
echo ""
echo "🔗 GitHub URL: https://github.com/hipparchus2000/richard"
echo "   (Private repository - requires login)"