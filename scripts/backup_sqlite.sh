#!/bin/bash

# SQLite Backup Script
# Creates tar.gz backup of SQLite database for GitHub repository storage

set -e

# Configuration
BACKUP_DIR="/home/openclaw/.openclaw/backups"
SQLITE_DB="/home/openclaw/.openclaw/memory/main.sqlite"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="sqlite_backup_${TIMESTAMP}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "=== SQLite Database Backup ==="
echo "Database: $SQLITE_DB"
echo "Backup to: $BACKUP_PATH.tar.gz"
echo "Timestamp: $TIMESTAMP"
echo ""

# Check if database exists
if [ ! -f "$SQLITE_DB" ]; then
    echo "❌ ERROR: SQLite database not found at $SQLITE_DB"
    exit 1
fi

# Get database info
echo "📊 Database Information:"
sqlite3 "$SQLITE_DB" <<EOF
.timeout 20000
.headers on
.mode column
SELECT 'Tables:' as Info;
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;
SELECT '';
SELECT 'Chunks count:' as Info;
SELECT COUNT(*) as count FROM chunks;
SELECT '';
SELECT 'TODOs count:' as Info;
SELECT COUNT(*) as count FROM todos WHERE status != 'cancelled';
SELECT '';
SELECT 'Research items:' as Info;
SELECT COUNT(*) as count FROM research_items;
EOF

echo ""

# Create backup
echo "🔒 Creating backup..."
cp "$SQLITE_DB" "${BACKUP_PATH}.db"

# Create metadata file
cat > "${BACKUP_PATH}.metadata.txt" <<EOF
SQLite Database Backup
======================
Backup Time: $(date)
Database: $SQLITE_DB
Size: $(du -h "$SQLITE_DB" | cut -f1)
Tables: $(sqlite3 "$SQLITE_DB" "SELECT COUNT(*) FROM sqlite_master WHERE type='table';")
Chunks: $(sqlite3 "$SQLITE_DB" "SELECT COUNT(*) FROM chunks;")
TODOs: $(sqlite3 "$SQLITE_DB" "SELECT COUNT(*) FROM todos WHERE status != 'cancelled';")
Research Items: $(sqlite3 "$SQLITE_DB" "SELECT COUNT(*) FROM research_items;")
EOF

# Create tar.gz archive
echo "📦 Creating tar.gz archive..."
tar -czf "${BACKUP_PATH}.tar.gz" \
    "${BACKUP_PATH}.db" \
    "${BACKUP_PATH}.metadata.txt"

# Clean up temporary files
rm "${BACKUP_PATH}.db"
rm "${BACKUP_PATH}.metadata.txt"

# Verify backup
if [ -f "${BACKUP_PATH}.tar.gz" ]; then
    BACKUP_SIZE=$(du -h "${BACKUP_PATH}.tar.gz" | cut -f1)
    echo "✅ Backup created successfully!"
    echo "   Archive: ${BACKUP_PATH}.tar.gz"
    echo "   Size: $BACKUP_SIZE"
    echo "   Location: $BACKUP_DIR"
    
    # List recent backups
    echo ""
    echo "📁 Recent backups:"
    ls -lh "$BACKUP_DIR"/*.tar.gz 2>/dev/null | tail -5 || echo "   No previous backups found"
else
    echo "❌ ERROR: Backup file not created!"
    exit 1
fi

# Restore test (optional)
echo ""
echo "💾 Restore test command:"
echo "   tar -xzf ${BACKUP_PATH}.tar.gz -C /tmp/"
echo "   cp /tmp/${BACKUP_NAME}.db /home/openclaw/.openclaw/memory/main.sqlite"

echo ""
echo "=== Backup Complete ==="