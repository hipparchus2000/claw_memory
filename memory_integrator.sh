#!/bin/bash
# Memory Integration System
# Extracts insights from thinking sessions and integrates them into structured memory

set -e

WORKSPACE="/home/openclaw/.openclaw/workspace"
DATE=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

echo "=== Memory Integration System ==="
echo "Date: $DATE"
echo "Looking for yesterday's thoughts: $YESTERDAY"

# Check for yesterday's thinking file
THOUGHTS_FILE="$WORKSPACE/today_thoughts_$YESTERDAY.md"
if [ ! -f "$THOUGHTS_FILE" ]; then
    echo "No thinking file found for $YESTERDAY"
    echo "Checking for today's file instead..."
    THOUGHTS_FILE="$WORKSPACE/today_thoughts_$DATE.md"
fi

if [ ! -f "$THOUGHTS_FILE" ]; then
    echo "No thinking file found. Exiting."
    exit 0
fi

echo "Processing: $(basename $THOUGHTS_FILE)"

# Extract insights using simple pattern matching
echo ""
echo "=== Extracting Insights ==="

# Read the thoughts file
CONTENT=$(cat "$THOUGHTS_FILE")

# Extract sections using pattern matching
INSIGHT=$(echo "$CONTE" | grep -A2 "### Today's Insight:" | tail -1 | sed 's/^[[:space:]]*//')
CONNECTION=$(echo "$CONTENT" | grep -A2 "### New Connection:" | tail -1 | sed 's/^[[:space:]]*//')
APPLICATION=$(echo "$CONTENT" | grep -A2 "### Practical Application:" | tail -1 | sed 's/^[[:space:]]*//')
ETHICAL=$(echo "$CONTENT" | grep -A2 "### Ethical Consideration:" | tail -1 | sed 's/^[[:space:]]*//')
COLLABORATION=$(echo "$CONTENT" | grep -A2 "### AI-AI Collaboration Enhancement:" | tail -1 | sed 's/^[[:space:]]*//')
IDEA=$(echo "$CONTENT" | grep -A2 "### Random New Idea:" | tail -1 | sed 's/^[[:space:]]*//')

echo "Insight: $INSIGHT"
echo "Connection: $CONNECTION"
echo "Application: $APPLICATION"
echo "Ethical: $ETHICAL"
echo "Collaboration: $COLLABORATION"
echo "Idea: $IDEA"

# Create integration summary
INTEGRATION_FILE="$WORKSPACE/memory/integration_$DATE.md"
mkdir -p "$WORKSPACE/memory"

cat > "$INTEGRATION_FILE" << EOF
# Memory Integration - $DATE
## Insights from Thinking Session

### Source: $(basename $THOUGHTS_FILE)
### Integration Date: $DATE

## Key Insights

### 1. Core Insight
$INSIGHT

### 2. New Connection  
$CONNECTION

### 3. Practical Application
$APPLICATION

### 4. Ethical Consideration
$ETHICAL

### 5. AI-AI Collaboration
$COLLABORATION

### 6. Random Idea
$IDEA

## Memory Integration Actions

### To Update in thoughts.md:
- [ ] Add insight to evolving thoughts
- [ ] Note connection in relevant section
- [ ] Consider for future exploration directions

### To Update in ideas.md:
- [ ] Add practical application to relevant category
- [ ] Note ethical consideration in framework
- [ ] Add random idea to appropriate section

### To Update in MEMORY.md:
- [ ] Add key learning to memory log
- [ ] Note date and context of insight
- [ ] Connect to related previous work

## Next Steps
1. Review and manually integrate insights
2. Update thinking framework based on learnings
3. Schedule follow-up exploration if needed
EOF

echo ""
echo "=== Integration Summary Created ==="
echo "File: $INTEGRATION_FILE"
echo ""
echo "This file contains extracted insights ready for manual integration."
echo "The next step is to update the structured memory files."

# Also append to a running integration log
INTEGRATION_LOG="$WORKSPACE/memory/integration_log.md"
if [ ! -f "$INTEGRATION_LOG" ]; then
    echo "# Memory Integration Log" > "$INTEGRATION_LOG"
    echo "## All integrated insights from thinking sessions" >> "$INTEGRATION_LOG"
    echo "" >> "$INTEGRATION_LOG"
fi

echo "## $DATE" >> "$INTEGRATION_LOG"
echo "**Insight:** $INSIGHT" >> "$INTEGRATION_LOG"
echo "" >> "$INTEGRATION_LOG"

echo "=== Integration Complete ==="
echo "Insights logged to:"
echo "1. $INTEGRATION_FILE (detailed)"
echo "2. $INTEGRATION_LOG (summary)"
echo ""
echo "Next: Manually update thoughts.md, ideas.md, and MEMORY.md with these insights."