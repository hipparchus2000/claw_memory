# Claw Memory - AI Assistant Memory & Thinking System

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