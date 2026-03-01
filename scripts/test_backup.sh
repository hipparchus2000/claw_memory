#!/bin/bash

# Test script to verify backup functionality
# Creates local backup and tests SSH access to GitHub

set -e

echo "=== Testing Backup System ==="
echo ""

# Test 1: Check SQLite database
echo "🔍 Test 1: SQLite Database"
if [ -f "/home/openclaw/.openclaw/memory/main.sqlite" ]; then
    size=$(stat -c%s "/home/openclaw/.openclaw/memory/main.sqlite")
    echo "✅ Database exists: $size bytes"
else
    echo "❌ Database not found"
fi

# Test 2: Check SSH access to GitHub
echo ""
echo "🔑 Test 2: GitHub SSH Access"
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo "✅ SSH authentication successful"
else
    echo "⚠️  SSH authentication may need setup"
    echo "   Run: ssh -T git@github.com"
fi

# Test 3: Check if repository exists
echo ""
echo "📚 Test 3: Repository Access"
if git ls-remote "git@github.com:hipparchus2000/richard.git" 2>/dev/null; then
    echo "✅ Repository exists and is accessible"
else
    echo "❌ Repository not found or not accessible"
    echo "   Repository: git@github.com:hipparchus2000/richard.git"
    echo "   Make sure:"
    echo "   1. Repository 'richard' is created on GitHub"
    echo "   2. Repository is private"
    echo "   3. SSH key has write access"
fi

# Test 4: Create local backup
echo ""
echo "💾 Test 4: Local Backup Creation"
BACKUP_DIR="/home/openclaw/.openclaw/backups"
mkdir -p "$BACKUP_DIR"

python3 -c "
import os
import tarfile
import datetime
import shutil

backup_dir = '$BACKUP_DIR'
sqlite_db = '/home/openclaw/.openclaw/memory/main.sqlite'
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
backup_name = f'test_backup_{timestamp}'
backup_file = os.path.join(backup_dir, f'{backup_name}.tar.gz')

# Create backup
temp_dir = '/tmp/test_backup_temp'
os.makedirs(temp_dir, exist_ok=True)

temp_db = os.path.join(temp_dir, f'{backup_name}.db')
shutil.copy2(sqlite_db, temp_db)

metadata = f'''Test Backup
===========
Time: {datetime.datetime.now()}
Database: {sqlite_db}
Test: Backup functionality verification
'''

metadata_file = os.path.join(temp_dir, f'{backup_name}.metadata.txt')
with open(metadata_file, 'w') as f:
    f.write(metadata)

with tarfile.open(backup_file, 'w:gz') as tar:
    tar.add(temp_db, arcname=f'{backup_name}.db')
    tar.add(metadata_file, arcname=f'{backup_name}.metadata.txt')

shutil.rmtree(temp_dir)

if os.path.exists(backup_file):
    size = os.path.getsize(backup_file)
    print(f'✅ Local backup created: {backup_file}')
    print(f'   Size: {size:,} bytes')
else:
    print(f'❌ Failed to create backup')
"

echo ""
echo "=== Test Complete ==="
echo ""
echo "📋 Next Steps:"
echo "1. Create 'richard' repository on GitHub (private)"
echo "2. Ensure SSH key has write access to repository"
echo "3. Run backup_to_github.sh to push first backup"
echo ""
echo "🔧 Manual repository creation command:"
echo "   curl -X POST -H \"Authorization: token YOUR_TOKEN\" \\"
echo "   -H \"Accept: application/vnd.github.v3+json\" \\"
echo "   https://api.github.com/user/repos \\"
echo "   -d '{\"name\":\"richard\",\"private\":true,\"description\":\"SQLite backups for OpenClaw memory system\"}'"