# CC-Boilerplate

[![CI/CD Status](https://github.com/USERNAME/cc-boilerplate/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/USERNAME/cc-boilerplate/actions/workflows/ci-cd.yml)
[![Security Tests](https://img.shields.io/badge/security-passing-brightgreen)](https://github.com/USERNAME/cc-boilerplate/actions)
[![Test Coverage](https://img.shields.io/badge/coverage-60%25-yellow)](https://github.com/USERNAME/cc-boilerplate/actions)
[![Hooks](https://img.shields.io/badge/hooks-8-blue)](#-all-8-claude-code-hooks)
[![Agents](https://img.shields.io/badge/agents-32-purple)](#-hierarchical-agent-system)
[![Commands](https://img.shields.io/badge/commands-7-cyan)](#-claude-commands-7-total)
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

### For Existing Projects (Recommended)

Add cc-boilerplate to your existing project. **Choose your preferred method**:

#### Option 1: One-Liner (Fastest)
```bash
# Single command setup - works in any existing project
curl -sSL https://raw.githubusercontent.com/neilinger/cc-boilerplate/main/scripts/init-boilerplate.sh | bash
```

#### Option 2: GitHub CLI (Most Reliable)
```bash
# Alternative if curl fails - uses GitHub CLI
gh repo clone neilinger/cc-boilerplate temp-boilerplate
./temp-boilerplate/scripts/init-boilerplate.sh
rm -rf temp-boilerplate
```

This will:
- ✅ Detect your existing project structure
- ✅ Add cc-boilerplate without conflicts
- ✅ Preserve your existing files
- ✅ Create project-specific customization area
- ✅ Build merged configurations

**Verify installation worked:**
```bash
# Quick test - should show cc-boilerplate components
ls -la .claude/
ls -la scripts/
```

**Then customize for your domain:**
```bash
# Edit project-specific instructions
vim .claude/project/CLAUDE.project.md

# Edit custom settings
vim .claude/project/settings.project.json

# Rebuild when you make changes
scripts/build-config.sh

# Check for updates periodically
scripts/update-boilerplate.sh --dry-run
```

### For New Projects

**Option 1: One-Liner**
```bash
# 1. Create your project
git init my-project && cd my-project

# 2. Add cc-boilerplate
curl -sSL https://raw.githubusercontent.com/neilinger/cc-boilerplate/main/scripts/init-boilerplate.sh | bash

# 3. Start building!
```

**Option 2: GitHub CLI (Alternative)**
```bash
# 1. Create your project
git init my-project && cd my-project

# 2. Add cc-boilerplate (GitHub CLI method)
gh repo clone neilinger/cc-boilerplate temp-boilerplate
./temp-boilerplate/scripts/init-boilerplate.sh
rm -rf temp-boilerplate

# 3. Start building!
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

**🛡️ Security**: Comprehensive `rm -rf` protection with role-based tool permissions and mandatory security chains
**🤖 Hierarchical Orchestration**: ADR-007 compliant multi-agent system with autonomous coordination
**🔗 Agent Chains**: Mandatory security workflows (code-reviewer → security-orchestrator → security-scanner)
**🧠 Cognitive Load Optimization**: Model allocation based on task complexity (haiku→sonnet→opus)
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

## 🤖 Hierarchical Agent System

Implements ADR-007 (Hierarchical Multi-Agent Architecture) with autonomous orchestration and security-first tool allocation:

### Primary Orchestrators (Opus Models)
- **[workflow-orchestrator](/.claude/agents/orchestrators/workflow-orchestrator.md)** - Complex multi-step coordination and feature implementation
- **[security-orchestrator](/.claude/agents/orchestrators/security-orchestrator.md)** - Security validation chain coordination

### Specialized Agents (Sonnet/Opus Models)
- **[meta-agent](/.claude/agents/meta-agent.md)** - Generate new specialized agents with external repository discovery
- **[smart-doc-generator](/.claude/agents/specialists/smart-doc-generator.md)** - Comprehensive documentation generation
- **[test-automator](/.claude/agents/specialists/test-automator.md)** - Automated test suite creation
- **[debugger](/.claude/agents/specialists/debugger.md)** - Root cause analysis and fix implementation
- **[security-scanner](/.claude/agents/specialists/security-scanner.md)** - OWASP vulnerability detection
- **[technical-researcher](/.claude/agents/specialists/technical-researcher.md)** - Deep technical research and analysis
- **[adr-creator](/.claude/agents/specialists/adr-creator.md)** - Architectural Decision Record generation
- **[pr-optimizer](/.claude/agents/specialists/pr-optimizer.md)** - GitHub PR optimization and management
- **[dependency-manager](/.claude/agents/specialists/dependency-manager.md)** - Package management and security updates
- **[context-engineer](/.claude/agents/specialists/context-engineer.md)** - Context window and prompt optimization
- **[ai-engineering-researcher](/.claude/agents/specialists/ai-engineering-researcher.md)** - AI/ML research specialist

#### New Specialist Agents (Phase 1 Implementation)
- **[api-architect](/.claude/agents/specialists/api-architect.md)** - RESTful/GraphQL API design and implementation
- **[aws-expert](/.claude/agents/specialists/aws-expert.md)** - AWS cloud services and infrastructure
- **[docker-expert](/.claude/agents/specialists/docker-expert.md)** - Containerization and orchestration
- **[postgres-expert](/.claude/agents/specialists/postgres-expert.md)** - Database design and optimization
- **[react-expert](/.claude/agents/specialists/react-expert.md)** - React development and best practices
- **[nextjs-expert](/.claude/agents/specialists/nextjs-expert.md)** - Next.js applications and optimization
- **[typescript-pro](/.claude/agents/specialists/typescript-pro.md)** - TypeScript development and type safety
- **[python-pro](/.claude/agents/specialists/python-pro.md)** - Python development and ecosystem tools
- **[graphql-architect](/.claude/agents/specialists/graphql-architect.md)** - GraphQL schema design and implementation
- **[performance-optimizer](/.claude/agents/specialists/performance-optimizer.md)** - Application performance and optimization

### Analysis Agents (Sonnet/Haiku Models)
- **[code-reviewer](/.claude/agents/analyzers/code-reviewer.md)** - Security and quality code reviews (read-only)
- **[test-coverage-analyzer](/.claude/agents/analyzers/test-coverage-analyzer.md)** - Test coverage analysis and gap identification
- **[work-completion-summary](/.claude/agents/analyzers/work-completion-summary.md)** - Audio summaries for long operations
- **[github-checker](/.claude/agents/specialists/github-checker.md)** - GitHub repository analysis and validation

### Agent Selection Protocol

**Always use workflow-orchestrator for:**
- Feature implementations requiring multiple domains (code + tests + docs + security)
- Cross-cutting concerns spanning multiple agents
- Complex workflows requiring coordination
- Any task involving 3+ distinct steps

**Mandatory security chain integration:**
- ANY code modification touching security boundaries
- The security chain is NON-NEGOTIABLE: code-reviewer → security-orchestrator → security-scanner

**Agent architecture compliance**: Run `./claude/hooks/check-agents.sh --verbose` for validation

## 🎯 Claude Commands (7 Total)

Specialized commands for common development tasks:

- **[cook](/.claude/commands/cook.md)** - Run multiple agent tasks in parallel for rapid development
- **[prime](/.claude/commands/prime.md)** - Load project context for new agent sessions
- **[prime_tts](/.claude/commands/prime_tts.md)** - Initialize Text-to-Speech system
- **[question](/.claude/commands/question.md)** - Structured questioning for requirements gathering
- **[update_status_line](/.claude/commands/update_status_line.md)** - Update dynamic terminal status displays

### Git Operations Commands
- **[git-ops:smart-commit](/.claude/commands/git-ops/smart-commit.md)** - Context-aware commit creation with Release Flow support
- **[git-ops:start-release-journey](/.claude/commands/git-ops/start-release-journey.md)** - Guide engineers through proper Release Flow process ("This is the way")

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
- **[Agent System Reference](docs/reference/agent-system.md)** - Hierarchical orchestration guide
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
- **[ADR-007: Hierarchical Multi-Agent Architecture](docs/adr/adr-007-agent-system-architecture.md)**
- **[ADR-008: Cognitive Load Model Allocation](docs/adr/adr-008-cognitive-load-model-allocation.md)**

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
