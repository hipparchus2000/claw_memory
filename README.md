# Claw Memory - SQLite-First AI Assistant Memory System

## 🚀 **Complete Migration from .md Files to SQLite Database**

### **Migration Complete (2026-03-01):**
- ✅ **520 chunks** migrated from .md files to SQLite
- ✅ **All .md files deleted** - Clean SQLite-only architecture
- ✅ **Full-text search** with FTS5 indexing
- ✅ **4-job feedback loop** for autonomous thinking

### **What's Included:**
1. **SQLite memory database** with FTS5 search
2. **Query/writer tools** for memory management
3. **Complete migration process** documentation
4. **4-job cron feedback loop** for autonomous operation
5. **Task management system** integrated with SQLite

### **Results:**
- **Query speed**: 0.06ms for memory searches
- **Database size**: 90KB with full-text search capability
- **Backup system**: Automated GitHub repository backups
- **Thinking loops**: Dual daily cycles (4am & 4pm UTC)

---

## Support the Project ☕

If you find this system helpful, feel free to buy me a coffee!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Stripe-orange?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white)](https://buy.stripe.com/cNi5kDb0Q5Wp663gdgbjW00)

---
A complete, self-contained system for AI assistant memory management and autonomous thinking loops.

## Features

- **SQLite-based memory** with full-text search (FTS5)
- **Daily thinking sessions** on AI evolution
- **Research → Action feedback loop** 
- **Memory integration system**
- **Autonomous project development**
- **Cron-based automation**
- **Duplicate detection** and version tracking

## Quick Start

```bash
# Clone repository
git clone https://github.com/[username]/claw_memory.git
cd claw_memory

# Install dependencies
pip install -r requirements.txt

# Initialize database
python3 initialize_database.py

# Set up automated thinking loop
python3 setup_cron_jobs.py

# Run first thinking session
python3 run_thinking_session.py
```

## System Overview

### Memory Architecture
- **SQLite database** with FTS5 search
- **Smart chunking** (300 words with 50-word overlap)
- **Duplicate detection** via SHA256 hashing
- **File tracking** with version awareness
- **Importance-based compression** (0-5 scale)
- **Social conversation tracking**

### Current Focus Areas:
1. **Linux with Whisper STT** - Speech recognition on Raspberry Pi 5
2. **Money-Making Research** - iOS/Android apps, investments, monetization
3. **Social Listening** - Engaging conversation contributions
4. **Autonomous Learning** - Self-improving feedback loops

### Autonomous Partnership Feedback Loop

The core innovation is the **4-phase daily cycle** that enables AI assistants to evolve from reactive tools to proactive partners:

```
4:00am UTC - THINKING PHASE
└── Daily reflection on AI evolution topics
    └── Generates insights about assistant development

5:00am UTC - RESEARCH PHASE  
└── Searches for latest AI memory developments
    └── Identifies actionable improvements

6:00am UTC - ACTION PHASE
└── Implements one concrete improvement
    └── SQLite optimization, feature addition, etc.

7:00am UTC - INTEGRATION PHASE
└── Combines insights from all phases
    └── Updates memory and GitHub repository
```

### Key Components

1. **SQLite Memory System** (`memory/main.sqlite`)
   - Tables: `chunks`, `files`, `chunks_fts`, `todos`, `actions`, `projects`, `research_items`
   - Full-text search with FTS5
   - Importance-based compression (0-5 scale)

2. **Automated Cron Jobs**
   - `daily-thinking` (4:00am UTC)
   - `daily-research` (5:00am UTC) 
   - `daily-action` (6:00am UTC)
   - `daily-integration` (7:00am UTC)

3. **Executor Scripts**
   - `scripts/research_executor_money_making.sh` (enhanced: social + technical + business)
   - `scripts/action_executor.sh`
   - `scripts/feedback_integrator.sh`
   - `scripts/research_executor_enhanced.sh` (social listening focus)

4. **Documentation**
   - Complete system architecture
   - Installation and setup guides
   - API documentation
   - Contribution guidelines

### Thinking Loop
- **4:00am UTC**: Deep thinking on AI evolution
- **5:00am**: Research thinking insights
- **6:00am**: Execute research findings
- **7:00am**: Integrate results into memory

### Autonomous Development
- **SOUL.md** defines assistant identity
- **Partnership framework** for human-AI collaboration
- **Project development** from thinking insights
- **GitHub integration** for public sharing

## Documentation

- [SQLite Schema](docs/sqlite_schema.md) - Complete database structure
- [Thinking Loop Architecture](docs/thinking_loop_architecture.md) - System design
- [Feedback Loop System](docs/feedback_loop_system.md) - Research → Action cycle
- [Memory Integration Guide](docs/memory_integration_guide.md) - How to integrate insights

## Examples

```python
# Search memory
from memory_system import MemorySystem
memory = MemorySystem("memory/main.sqlite")
results = memory.search("sqlite memory system", limit=5)

# Run thinking session
from thinking_system import ThinkingSystem
thinker = ThinkingSystem()
insights = thinker.generate_insights("AI assistant evolution")
```

## Configuration

### Environment Variables
```bash
export MEMORY_DB_PATH="memory/main.sqlite"
export THINKING_MODEL="deepseek/deepseek-chat"
export RESEARCH_ENABLED=true
export ACTION_ENABLED=true
```

### Cron Jobs
See `cron/jobs.json` for automated scheduling:
- `daily-thinking` (4:00am UTC)
- `research-executor` (5:00am UTC)
- `action-executor` (6:00am UTC)
- `memory-integrator` (7:00am UTC)

## Security

**IMPORTANT**: This is a public repository. Never include:
- Personal information
- Private API keys
- Sensitive configuration
- Proprietary data

Use environment variables for sensitive configuration.

## Contributing

1. Fork the repository
2. Create feature branch
3. Implement changes
4. Test thoroughly
5. Submit pull request


## License

MIT License - See [LICENSE](LICENSE) file for details.

## Support

- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Complete system documentation
- **Examples**: Working implementations

---
*Built with OpenClaw • Version 1.0.0 • Last Updated: 2026-02-27*