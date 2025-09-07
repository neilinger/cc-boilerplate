# Getting Started

## Quick Setup

Get cc-boilerplate running in minutes.

### Prerequisites

- **[Astral UV](https://docs.astral.sh/uv/)** - Python package manager
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** - AI coding assistant
- **Git** - Version control

### Installation

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

The setup script creates:

- **`.env`** - Your personal configuration (API keys, user name)
- **`.mcp.json`** - MCP server configuration (if using ElevenLabs)

See `.env.sample` for all available configuration options.

## Next Steps

1. **Review Documentation**: Check out [Development Workflow](development.md)
2. **Explore Security**: Learn about [Security Features](security.md)
3. **Test TTS**: Try the audio notification system
4. **Create Agents**: Use the meta-agent to generate custom agents

For detailed guidance, see our [complete documentation index](../../README.md#documentation).
