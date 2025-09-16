# Getting Started

## Quick Setup

Get cc-boilerplate running in minutes using the modern synchronization system.

### Prerequisites

- **[Astral UV](https://docs.astral.sh/uv/)** - Python package manager
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** - AI coding assistant
- **Git** 2.20+ with subtree support
- **jq** - JSON manipulation tool

### Modern Installation (Recommended)

Use the new boilerplate synchronization system:

```bash
# 1. Initialize cc-boilerplate in new/existing project
curl -sSL https://raw.githubusercontent.com/neilinger/cc-boilerplate/main/scripts/init-boilerplate.sh | bash

# 2. Build initial configurations
scripts/build-config.sh

# 3. Start Claude Code
claude-code .
```

### Traditional Installation

Alternative setup for direct cloning:

```bash
# 1. Clone this boilerplate
git clone <your-repo-url>
cd cc-boilerplate

# 2. Run setup script
./setup.sh

# 3. Start Claude Code
claude-code .
```

## Configuration

### Synchronization System

The modern setup creates a three-layer configuration:

- **`.claude/boilerplate/`** - Core boilerplate files (git subtree)
- **`.claude/project/`** - Your project customizations
- **Generated files** - CLAUDE.md, settings.json (merged configurations)

### Environment Setup

Both installation methods create:

- **`.env`** - Your personal configuration (API keys, user name)
- **`.mcp.json`** - MCP server configuration (if using ElevenLabs)
- **`.boilerplate-version`** - Version tracking (synchronization system only)

See `.env.sample` for all available configuration options.

## Next Steps

### If Using Synchronization System

1. **Customize Instructions**: Edit `.claude/project/CLAUDE.project.md` with domain-specific rules
2. **Configure Settings**: Modify `.claude/project/settings.project.json` for custom permissions
3. **Build Configurations**: Run `scripts/build-config.sh` after changes
4. **Stay Updated**: Use `scripts/update-boilerplate.sh` to pull improvements

### General Next Steps

1. **Review Documentation**: Check out [Development Workflow](development.md)
2. **Explore Security**: Learn about [Security Features](security.md)
3. **Test TTS**: Try the audio notification system
4. **Create Agents**: Use the meta-agent to generate custom agents
5. **Read Sync Guide**: See [Synchronization Guide](../SYNCHRONIZATION.md) for advanced workflow

For detailed guidance, see our [complete documentation index](../../README.md#documentation).
