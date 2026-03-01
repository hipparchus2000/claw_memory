# Cron Job Configuration for SQLite Memory System

## Overview
This document describes the **4-5 job feedback loop** for the SQLite memory system. This is a clean, minimal configuration suitable for demonstration and adoption by other projects.

## Core Feedback Loop (4 Jobs)

### 1. **Daily Thinking** (4:00 UTC)
**Purpose:** Generate insights about AI assistant evolution
**Schedule:** `0 4 * * *` (4am daily)
**Task:** Deep reflection on memory systems, feedback loops, AI-AI collaboration
**Output:** Posted to `#ai-thinking` channel

### 2. **Daily Research** (5:00 UTC)
**Purpose:** Investigate thinking insights
**Schedule:** `0 5 * * *` (5am daily)
**Task:** Search for latest developments in AI memory systems, SQLite optimization
**Output:** Posted to `#ai-research` channel

### 3. **Daily Action** (6:00 UTC)
**Purpose:** Implement research findings
**Schedule:** `0 6 * * *` (6am daily)
**Task:** Implement one concrete improvement to SQLite memory system
**Tools:** Uses `memory_writer.py`, `memory_query.py`, `sqlite_memory_integrator.py`
**Output:** Posted to `#ai-action` channel

### 4. **Daily Integration** (7:00 UTC)
**Purpose:** Update memory with insights
**Schedule:** `0 7 * * *` (7am daily)
**Task:** Integrate insights from thinking, research, and action phases
**Tools:** Uses `sqlite_memory_integrator.py`
**Output:** Posted to `#ai-integration` channel

## Optional 5th Job

### 5. **Daily SQLite Backup** (8:00 UTC)
**Purpose:** Database maintenance example
**Schedule:** `0 8 * * *` (8am daily)
**Task:** Create backup of SQLite database, optionally push to GitHub
**Output:** Posted to `#backup` channel

## Configuration File

The complete configuration is available in:
```
examples/cron_feedback_loop.json
```

## How to Deploy

### 1. Install OpenClaw
```bash
npm install -g @openclaw/openclaw
```

### 2. Configure Channels
Update the `delivery.to` fields in `cron_feedback_loop.json` to match your Slack channels.

### 3. Import Jobs
```bash
# Using OpenClaw CLI
openclaw cron import examples/cron_feedback_loop.json

# Or manually via API
curl -X POST http://localhost:3000/cron/jobs \
  -H "Content-Type: application/json" \
  -d @examples/cron_feedback_loop.json
```

### 4. Verify Setup
```bash
openclaw cron list
```

## Customization

### Adjust Schedule
Modify the `schedule.expr` values for different timezones:
- `0 4 * * *` = 4am UTC daily
- `0 9 * * *` = 9am UTC daily
- `0 0 * * *` = Midnight UTC daily

### Change Delivery Channels
Update `delivery.channel` and `delivery.to`:
- Slack: `"channel": "slack", "to": "#channel-name"`
- Discord: `"channel": "discord", "to": "channel-id"`
- Telegram: `"channel": "telegram", "to": "chat-id"`

### Modify Tasks
Update `payload.message` to match your specific needs:
- Different research topics
- Alternative implementation tasks
- Custom integration workflows

## Architecture Benefits

### Complete Feedback Loop
```
4:00 Thinking → 5:00 Research → 6:00 Action → 7:00 Integration
```

### SQLite-First Design
- All memory operations use SQLite database
- Tools provided: `memory_query.py`, `memory_writer.py`, `sqlite_memory_integrator.py`
- No file-based memory (.md files)

### Scalable
- Start with 4 core jobs
- Add additional jobs as needed
- Each job isolated for reliability

## Example Output

### Thinking Phase
```
🤔 DAILY THINKING - AI Assistant Evolution
Insight: AI assistants need structured feedback loops...
```

### Research Phase
```
🔍 DAILY RESEARCH - AI Memory Systems
Found: New SQLite optimization technique...
```

### Action Phase
```
🔧 DAILY ACTION - Implementation
Implemented: Added memory compression feature...
```

### Integration Phase
```
📊 DAILY INTEGRATION - Memory Update
Integrated: 3 new insights added to SQLite...
```

## Troubleshooting

### Jobs Not Running
1. Check OpenClaw gateway status: `openclaw gateway status`
2. Verify cron scheduler: `openclaw cron status`
3. Check job enablement: `openclaw cron list --include-disabled`

### Delivery Issues
1. Verify channel configuration
2. Check API tokens/permissions
3. Test manual message delivery

### SQLite Access
1. Ensure database exists: `/path/to/memory/main.sqlite`
2. Verify tool permissions: `chmod +x scripts/*.py`
3. Test tools manually: `python3 scripts/memory_query.py stats`

## Next Steps

1. **Customize** for your project needs
2. **Monitor** first few days of execution
3. **Extend** with additional jobs as needed
4. **Contribute** improvements back to the community

## Resources

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [GitHub Repository](https://github.com/hipparchus2000/claw_memory)
- [Community Discord](https://discord.com/invite/clawd)