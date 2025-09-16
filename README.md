# CC-Boilerplate

[![CI/CD Status](https://github.com/USERNAME/cc-boilerplate/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/USERNAME/cc-boilerplate/actions/workflows/ci-cd.yml)
[![Security Tests](https://img.shields.io/badge/security-passing-brightgreen)](https://github.com/USERNAME/cc-boilerplate/actions)
[![Test Coverage](https://img.shields.io/badge/coverage-60%25-yellow)](https://github.com/USERNAME/cc-boilerplate/actions)
[![Hooks](https://img.shields.io/badge/hooks-8-blue)](#-all-8-claude-code-hooks)
[![Agents](https://img.shields.io/badge/agents-10-purple)](#-essential-agents)
[![Commands](https://img.shields.io/badge/commands-5-cyan)](#-claude-commands-5-total)
[![Output Styles](https://img.shields.io/badge/styles-9-orange)](#-9-output-styles)
[![Release](https://img.shields.io/github/v/release/USERNAME/cc-boilerplate?include_prereleases)](https://github.com/USERNAME/cc-boilerplate/releases)

Claude Code boilerplate with essential hooks, agents, and security features.

## Prerequisites

- **[Astral UV](https://docs.astral.sh/uv/)** - Python package manager
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** - AI coding assistant

## Setup in Claude Code

If you're already working in Claude Code (the primary use case), use this quick setup:

### Quick Start Prompt

Copy this exact prompt into Claude Code:

```
start with latest tag of neilinger/cc-boilerplate repository as skeleton for this project. then guide me through whats next.
```

### Modern Setup (Recommended - PRP-003 Synchronization)

Use the new boilerplate synchronization system for seamless updates:

```bash
# 1. Initialize cc-boilerplate in new/existing project
curl -sSL https://raw.githubusercontent.com/neilinger/cc-boilerplate/main/scripts/init-boilerplate.sh | bash

# 2. Build configurations
scripts/build-config.sh

# 3. Customize for your domain
vim .claude/project/CLAUDE.project.md     # Domain-specific instructions
vim .claude/project/settings.project.json # Custom settings

# 4. Update from upstream (anytime)
scripts/update-boilerplate.sh
```

### Manual Setup Steps

Alternatively, follow these steps manually:

```bash
# 1. Initialize and import boilerplate
git init
git remote add boilerplate https://github.com/neilinger/cc-boilerplate.git
git fetch boilerplate
git checkout v1.1.0 -- .

# 2. Configure for your project
git remote remove boilerplate
git remote add origin https://github.com/username/your-project.git

# 3. Setup configuration (NOTE: setup.sh works inside Claude Code)
cp .mcp.json.sample .mcp.json
mkdir -p logs output
touch logs/.gitkeep output/.gitkeep

# 4. Create .env manually (do NOT copy .env.sample directly)
# IMPORTANT: Create .env with your actual API keys or empty values
# Never use the placeholder strings from .env.sample

# 5. Customize project
# Update PROJECT_NAME in README.md and pyproject.toml
# Update project name throughout the codebase

# 6. Initial commit
git add .
git commit -m "Initial commit from cc-boilerplate"
git push -u origin main
```

### ⚠️ Important Notes

- **Never copy `.env.sample` to `.env` directly** - this breaks Claude with placeholder API keys
- **Create `.env` manually** with your actual keys or empty values: `ANTHROPIC_API_KEY=""`
- **The `./setup.sh` script works inside Claude Code** (detects the environment automatically)
- **Customize project name** in README.md and pyproject.toml before committing

## Traditional Setup (Outside Claude Code)

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
**🔧 Development Tools**: serena-mcp semantic coding for intelligent codebase analysis
**🔊 Smart TTS**: Multi-provider fallback (ElevenLabs → OpenAI → pyttsx3)
**📝 Session Management**: Context-aware hooks and logging

## Key Components

### 🤖 Meta-Agent: Core Automation Engine

The `meta-agent` is the heart of this boilerplate - it automatically creates new specialized agents from natural language descriptions. Simply ask Claude to create an agent and it will:

- Fetch latest Claude Code documentation
- Generate complete agent configuration files
- Set appropriate tools, colors, and delegation rules
- Write ready-to-use `.md` files to `.claude/agents/`

### 🎨 Workflow-Optimized Output Styles (9 Total)

Different development phases need different information formats:

- **GenUI**: Automatically generates and opens HTML documents for visual workflows
- **TTS Summary**: Audio feedback for long-running operations
- **JSON/YAML/HTML Structured**: Machine-parseable outputs for automation
- **Markdown Focused**: Clean readable formats for documentation
- **Bullet Points**: Concise list-based information
- **Table-Based**: Structured tabular data presentation
- **Ultra-Concise**: Minimal, essential information only

### 🔧 Development Infrastructure

- **`.serena/`**: serena-mcp semantic coding tools with project memories and intelligent code analysis
- **`scripts/`**: KISS/YAGNI-compliant validation tools (PRP validation, boilerplate synchronization)
- **`tests/`**: Security-focused testing of critical hook functionality
- **`boilerplate/`**: Layered configuration system with git subtree for graceful updates

## Boilerplate Synchronization System (PRP-003)

The cc-boilerplate now supports graceful updates while preserving project customizations:

### Three-Layer Configuration

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Base Layer     │    │  Project Layer   │    │  Merged Layer   │
│                 │    │                  │    │                 │
│ Boilerplate     │ +  │ Customizations   │ =  │ Final Config    │
│ Templates       │    │ (.claude/project)│    │ (Generated)     │
│ (.claude/       │    │                  │    │                 │
│  boilerplate)   │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**Key Benefits**:
- **Graceful Updates**: Pull boilerplate improvements without losing customizations
- **Project Customization**: Add domain-specific instructions and settings
- **Version Tracking**: Know exactly which boilerplate version you're using
- **Conflict Resolution**: Automatic backup and rollback capabilities

**See**: [Synchronization Guide](docs/SYNCHRONIZATION.md) for complete workflow documentation

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
├── .serena/            # serena-mcp semantic coding & project memory
├── boilerplate/        # Core boilerplate templates and git subtree
│   ├── .claude/        # Base configuration templates
│   ├── templates/      # Mergeable template files
│   └── scripts/        # Synchronization utilities
├── PRPs/               # Product Requirements Process templates
├── scripts/            # Validation utilities (KISS/YAGNI)
│   ├── init-boilerplate.sh    # Initialize synchronization
│   ├── update-boilerplate.sh  # Pull boilerplate updates
│   └── build-config.sh        # Merge configurations
├── tests/              # Security-critical functionality tests
│   └── medium_priority/ # Feature reliability tests
├── examples/           # Sample project implementations
│   └── sample-project/ # Complete synchronization example
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

## 🔒 All 8 Claude Code Hooks

Security-first hooks that execute in sequence:

- **[user_prompt_submit](/.claude/hooks/user_prompt_submit.py)** - Input validation and preprocessing
- **[pre_tool_use](/.claude/hooks/pre_tool_use.py)** - Security validation (CRITICAL - blocks dangerous commands)
- **[post_tool_use](/.claude/hooks/post_tool_use.py)** - Logging and post-execution processing
- **[notification](/.claude/hooks/notification.py)** - TTS alerts and notifications
- **[stop](/.claude/hooks/stop.py)** - Session completion handling
- **[subagent_stop](/.claude/hooks/subagent_stop.py)** - Agent completion processing
- **[pre_compact](/.claude/hooks/pre_compact.py)** - Backup before conversation compaction
- **[session_start](/.claude/hooks/session_start.py)** - Context loading and initialization

## 🤖 Essential Agents

Specialized agents for different development workflows:

- **[meta-agent](/.claude/agents/meta-agent.md)** - Generate new specialized agents from descriptions
- **[smart-doc-generator](/.claude/agents/smart-doc-generator.md)** - Comprehensive documentation generation
- **[engineer-code-reviewer](/.claude/agents/engineer-code-reviewer.md)** - Security and quality code reviews
- **[test-automator](/.claude/agents/test-automator.md)** - Automated test suite creation
- **[test-coverage-analyzer](/.claude/agents/test-coverage-analyzer.md)** - Test coverage analysis and gap identification
- **[work-completion-summary](/.claude/agents/work-completion-summary.md)** - Audio summaries for long operations
- **[llm-ai-agents-and-eng-research](/.claude/agents/llm-ai-agents-and-eng-research.md)** - AI/ML research and analysis
- **[technical.researcher](/.claude/agents/technical.researcher.md)** - Deep technical research and documentation
- **[github-checker](/.claude/agents/github-checker.md)** - GitHub repository analysis and validation
- **[adr-creator](/.claude/agents/adr-creator.md)** - Architectural Decision Record generation

## 🎯 Claude Commands (5 Total)

Specialized commands for common development tasks:

- **[cook](/.claude/commands/cook.md)** - Run multiple agent tasks in parallel for rapid development
- **[prime](/.claude/commands/prime.md)** - Load project context for new agent sessions
- **[prime_tts](/.claude/commands/prime_tts.md)** - Initialize Text-to-Speech system
- **[question](/.claude/commands/question.md)** - Structured questioning for requirements gathering
- **[update_status_line](/.claude/commands/update_status_line.md)** - Update dynamic terminal status displays

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
- **[Serena MCP Integration](docs/reference/serena-mcp.md)** - Semantic coding tools
- **[TTS System](docs/reference/tts-system.md)** - Audio notification system
- **[Synchronization Guide](docs/SYNCHRONIZATION.md)** - Boilerplate update workflow

### Troubleshooting

- **[Common Issues](docs/troubleshooting.md)** - Solutions to frequent problems
- **[Synchronization Issues](docs/SYNCHRONIZATION.md#troubleshooting)** - Boilerplate update problems

### Architecture Decisions

- **[ADR Index](docs/adr/README.md)** - All architectural decision records
- **[ADR-001: Branching Strategy](docs/adr/adr-001-branching-strategy.md)**
- **[ADR-002: CI/CD Pipeline](docs/adr/adr-002-cicd-pipeline.md)**
- **[ADR-003: Testing Strategy](docs/adr/adr-003-testing-strategy.md)**
- **[ADR-004: Documentation Standards](docs/adr/adr-004-documentation-standards.md)**
- **[ADR-005: ADR/PRP Separation](docs/adr/adr-005-adr-prp-separation.md)**
- **[ADR-006: Issue Management Process](docs/adr/adr-006-issue-management-process.md)**

## 🎨 9 Output Styles

Workflow-optimized formatting for different development phases:

- **[genui.md](/.claude/output-styles/genui.md)** - Automatically generates and opens HTML documents for visual workflows
- **[tts-summary.md](/.claude/output-styles/tts-summary.md)** - Audio feedback for long-running operations
- **[json-structured.md](/.claude/output-styles/json-structured.md)** - Machine-parseable JSON outputs for automation
- **[yaml-structured.md](/.claude/output-styles/yaml-structured.md)** - YAML format for configuration and data
- **[html-structured.md](/.claude/output-styles/html-structured.md)** - Structured HTML for rich displays
- **[markdown-focused.md](/.claude/output-styles/markdown-focused.md)** - Clean readable markdown for documentation
- **[bullet-points.md](/.claude/output-styles/bullet-points.md)** - Concise list-based information
- **[table-based.md](/.claude/output-styles/table-based.md)** - Structured tabular data presentation
- **[ultra-concise.md](/.claude/output-styles/ultra-concise.md)** - Minimal, essential information only

## Usage

1. Run `./setup.sh` to configure
2. Start with `claude-code .`
3. Use meta-agent to create custom agents
4. See `CLAUDE.md` for KISS/YAGNI principles
