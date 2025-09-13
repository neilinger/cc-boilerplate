# CC-Boilerplate

[![CI/CD Status](https://github.com/USERNAME/cc-boilerplate/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/USERNAME/cc-boilerplate/actions/workflows/ci-cd.yml)
[![Security Tests](https://img.shields.io/badge/security-passing-brightgreen)](https://github.com/USERNAME/cc-boilerplate/actions)
[![Test Coverage](https://img.shields.io/badge/coverage-60%25-yellow)](https://github.com/USERNAME/cc-boilerplate/actions)
[![Hooks](https://img.shields.io/badge/hooks-8-blue)](#-all-8-claude-code-hooks)
[![Agents](https://img.shields.io/badge/agents-4-purple)](#-essential-agents)
[![Output Styles](https://img.shields.io/badge/styles-8-orange)](#-8-output-styles)
[![Release](https://img.shields.io/github/v/release/USERNAME/cc-boilerplate?include_prereleases)](https://github.com/USERNAME/cc-boilerplate/releases)

Claude Code boilerplate with essential hooks, agents, and security features.

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

## Core Features

**🛡️ Security**: Comprehensive `rm -rf` protection with 30+ dangerous command patterns
**🤖 Agent Automation**: Meta-agent creates new specialized agents from descriptions
**🎨 Workflow Styles**: Output formats optimized for different development phases
**🔧 Development Tools**: serena-mcp integration for boilerplate maintenance
**🔊 Smart TTS**: Multi-provider fallback (ElevenLabs → OpenAI → pyttsx3)
**📝 Session Management**: Context-aware hooks and logging

## Key Components

### 🤖 Meta-Agent: Core Automation Engine

The `meta-agent` is the heart of this boilerplate - it automatically creates new specialized agents from natural language descriptions. Simply ask Claude to create an agent and it will:

- Fetch latest Claude Code documentation
- Generate complete agent configuration files
- Set appropriate tools, colors, and delegation rules
- Write ready-to-use `.md` files to `.claude/agents/`

### 🎨 Workflow-Optimized Output Styles

Different development phases need different information formats:

- **GenUI**: Automatically generates and opens HTML documents for visual workflows
- **TTS Summary**: Audio feedback for long-running operations
- **JSON Structured**: Machine-parseable outputs for automation
- **Markdown/Bullet Points**: Clean readable formats for documentation

### 🔧 Development Infrastructure

- **`.serena/`**: serena-mcp tooling for maintaining and evolving this boilerplate itself
- **`scripts/`**: KISS/YAGNI-compliant validation tools (PRP validation, etc.)
- **`tests/`**: Security-focused testing of critical hook functionality

## PRP Status Management

PRPs (Product Requirements Process) now include lifecycle tracking to prevent documentation drift:

| Status | Description | Set By |
|--------|-------------|--------|
| **PROPOSED** | Idea documented, not started | `/prp:create` |
| **IN_PROGRESS** | Being implemented | `/prp:execute` |
| **COMPLETED** | Finished and reviewed | `/prp:review` |
| **OBSOLETE** | No longer relevant | Manual update |

The pre-commit hook will warn (but not block) if you're committing PRPs with IN_PROGRESS status, helping prevent incomplete work from appearing finished.

## Project Structure

```
cc-boilerplate/
├── .claude/
│   ├── agents/         # Meta-agent + specialized agents
│   ├── commands/       # Claude commands including PRP lifecycle
│   ├── hooks/          # Security, TTS, session management
│   ├── output-styles/  # Workflow-specific formatting
│   ├── status_lines/   # Dynamic terminal displays
│   └── settings.json   # Permissions and configuration
├── .serena/            # serena-mcp development tooling
├── PRPs/               # Product Requirements Process templates
├── scripts/            # Validation utilities (KISS/YAGNI)
├── tests/              # Security-critical functionality tests
├── CLAUDE.md           # KISS/YAGNI development principles
└── setup.sh            # Project setup script
```

## Core

- Security-first command validation
- Multi-provider TTS (ElevenLabs → OpenAI → pyttsx3)
- UV single-file scripts
- Zero dependency management

## Security

**30+ rm patterns blocked** - Prevents `rm -rf /` disasters
**Environment protection** - Blocks `.env` access
**Real-time validation** - Before every tool execution

**Security levels**: strict, moderate, permissive

```bash
user: "rm -rf /"
claude: 🚫 BLOCKED - Dangerous command
```

## TTS

**Provider fallback**: ElevenLabs → OpenAI → pyttsx3

```bash
# .env
TTS_DEFAULT_PROVIDER=elevenlabs
ELEVENLABS_API_KEY=key
OPENAI_API_KEY=key
```

## Agents

- **meta-agent** - Generate new agents
- **test-automator** - Create test suites
- **code-reviewer** - Security and quality reviews
- **technical-researcher** - Research analysis
- **smart-doc-generator** - Documentation
- **work-completion-summary** - Audio summaries
- **test-coverage-analyzer** - Coverage gaps
- **llm-research** - AI/ML developments

## Testing

**🔴 High Priority (Security Critical)**: Safety hooks, dangerous command detection
**🟡 Medium Priority (Feature Reliability)**: TTS providers, integration testing
**🔧 Test Infrastructure**: Comprehensive runner with priority-based execution

```bash
# All tests with detailed reporting
python tests/run_all_tests.py

# Security-critical tests only
python tests/test_safety_hooks.py

# Hook integration testing
python tests/test_hook_integration.py
```

**Full testing documentation**: See [Testing Guide](docs/guides/testing.md) for comprehensive coverage details, security testing approach, and troubleshooting guide.

## Documentation

### Quick Start

- **[Getting Started](docs/guides/getting-started.md)** - Installation and initial setup
- **[Development Workflow](docs/guides/development.md)** - Daily development process

### Guides

- **[Architecture Overview](docs/guides/architecture.md)** - System design and components
- **[Security Features](docs/guides/security.md)** - Safety hooks and protection
- **[Branch Protection](docs/guides/branch-protection.md)** - Repository protection setup
- **[Testing Guide](docs/guides/testing.md)** - 3-tier testing architecture and workflows

### Reference

- **[API Reference](docs/reference/api.md)** - Complete API documentation
- **[System Reference](docs/reference/index.md)** - Essential system information
- **[TTS System](docs/reference/tts-system.md)** - Audio notification system

### Troubleshooting

- **[Common Issues](docs/troubleshooting.md)** - Solutions to frequent problems

### Architecture Decisions

- **[ADR Index](docs/adr/README.md)** - All architectural decision records
- **[ADR-001: Branching Strategy](docs/adr/adr-001-branching-strategy.md)**
- **[ADR-002: CI/CD Pipeline](docs/adr/adr-002-cicd-pipeline.md)**
- **[ADR-003: Testing Strategy](docs/adr/adr-003-testing-strategy.md)**
- **[ADR-004: Documentation Standards](docs/adr/adr-004-documentation-standards.md)**
- **[ADR-005: ADR/PRP Separation](docs/adr/adr-005-adr-prp-separation.md)**

## Usage

1. Run `./setup.sh` to configure
2. Start with `claude-code .`
3. Use meta-agent to create custom agents
4. See `CLAUDE.md` for KISS/YAGNI principles
