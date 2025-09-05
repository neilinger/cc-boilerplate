# CC-Boilerplate

Claude Code boilerplate with hooks, agents, and output styles pre-configured for rapid project setup.

## Prerequisites

- **[Astral UV](https://docs.astral.sh/uv/)** - Python package manager
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** - AI coding assistant

## Quick Start

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

## What's Included

### 🪝 All 8 Claude Code Hooks
- **UserPromptSubmit** - Pre-process prompts, logging, validation
- **PreToolUse** - Security validation (blocks `rm -rf`, `.env` access)  
- **PostToolUse** - Post-execution logging and transcript conversion
- **Notification** - Custom notifications with optional TTS
- **Stop** - Completion handling with AI-generated messages
- **SubagentStop** - Subagent completion announcements
- **PreCompact** - Transcript backup before compaction
- **SessionStart** - Development context loading

### 🤖 Essential Agents
- **meta-agent** - Generate new agents from descriptions
- **engineer-code-reviewer** - Automated code quality checks  
- **work-completion-summary** - Audio task summaries via TTS
- **llm-ai-agents-and-eng-research** - AI/LLM research specialist

### 🎨 8 Output Styles
- **genui** - Beautiful HTML generation with embedded styling
- **table-based** - Organized markdown tables  
- **tts-summary** - Audio feedback via ElevenLabs TTS
- **yaml-structured** - YAML configuration format
- **bullet-points** - Clean nested lists
- **ultra-concise** - Minimal words, maximum speed
- **html-structured** - Semantic HTML5
- **markdown-focused** - Rich markdown features

### 📊 4 Dynamic Status Lines  
Real-time terminal displays with session context, git info, and agent names.

## Project Structure

```
cc-boilerplate/
├── .claude/
│   ├── agents/         # 4 essential agents
│   ├── hooks/          # All 8 hooks + utilities
│   ├── output-styles/  # 8 response formatting styles
│   ├── status_lines/   # 4 dynamic status displays
│   └── settings.json   # Hook and permission configuration
├── logs/               # Hook execution logs (JSON)
├── output/             # Generated files output
├── .env.sample         # Configuration template
├── .mcp.json.sample    # MCP server template  
├── CLAUDE.md           # KISS/YAGNI development principles
└── setup.sh            # Project setup script
```

## Key Features

- **Security-First** - Comprehensive command validation and blocking
- **Intelligent TTS** - Multi-provider audio feedback (ElevenLabs → OpenAI → pyttsx3)  
- **Session Management** - Agent naming and context persistence
- **UV Single-File Scripts** - Self-contained hooks with embedded dependencies
- **Zero Dependencies** - No virtual environment management needed

## Customization

- **Add new hooks**: Place in `.claude/hooks/`
- **Create agents**: Use `/agents` command or meta-agent  
- **Define output styles**: Add to `.claude/output-styles/`
- **Configure permissions**: Edit `.claude/settings.json`

## Development Principles  

See **`CLAUDE.md`** for KISS/YAGNI principles that guide this project's architecture.

## Next Steps

1. Review and customize `.env` configuration
2. Explore the pre-configured hooks and agents
3. Start building your project with Claude Code's enhanced capabilities
4. Use the meta-agent to create specialized agents for your domain