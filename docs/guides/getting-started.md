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

# 2. Configure your project (API keys, project name, TTS)
./setup.sh

# 3. Start Claude Code and test
claude .
# Test with: /code-quality
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

- **`.claude/boilerplate/`** - Core boilerplate files (agents, hooks, templates)
- **`.claude/project/`** - Your project customizations
- **Project root** - setup.sh, .env.sample, .mcp.json.sample (for configuration)
- **Generated files** - CLAUDE.md, settings.json (merged configurations)

**Important**: Always run `./setup.sh` from your project root, not from inside `.claude/boilerplate/`.

### Environment Setup

Both installation methods create:

- **`.env`** - Your personal configuration (API keys, user name)
- **`.mcp.json`** - MCP server configuration (if using ElevenLabs)
- **`.boilerplate-version`** - Version tracking (synchronization system only)

See `.env.sample` for all available configuration options.

## Hierarchical Agent System (Phase 1)

cc-boilerplate now includes a sophisticated multi-agent system with **32 specialized agents** (expanded from 17) designed to handle complex development workflows through intelligent orchestration.

### Agent Categories

#### 🎯 **Orchestrators** - Coordinate Complex Workflows
- **workflow-orchestrator**: Multi-step task coordination and agent management
- **security-orchestrator**: Mandatory security validation chains

#### 🔍 **Analyzers** - Read-Only Analysis and Handoff
- **code-reviewer**: Code quality analysis (hands off to security-orchestrator)
- **test-coverage-analyzer**: Coverage gaps and test quality assessment
- **work-completion-summary**: Task summaries and TTS announcements

#### 🛠️ **Specialists** - Domain Expertise (27 agents)

**Core Development:**
- **smart-doc-generator**: Documentation creation, README files, API docs
- **test-automator**: Test creation, coverage improvement, automation setup
- **adr-creator**: Architectural decisions and technology choices
- **technical-researcher**: In-depth research and framework evaluation
- **debugger**: Root cause analysis and complex debugging

**Language & Framework Experts (New in Phase 1):**
- **python-pro**: Python 3.12+ with modern tooling (uv, ruff, FastAPI)
- **typescript-pro**: Advanced TypeScript, generics, enterprise patterns
- **react-expert**: React 19+, Next.js 15+, performance optimization
- **nextjs-expert**: Next.js App Router, SSR/SSG, full-stack patterns
- **graphql-architect**: Federation, schema design, performance

**Infrastructure & Cloud:**
- **aws-expert**: AWS architecture, IaC, cost optimization, Well-Architected
- **docker-expert**: Containerization, K8s, security, performance
- **postgres-expert**: PostgreSQL optimization, advanced features, scaling
- **api-architect**: RESTful/GraphQL APIs, microservices, service boundaries
- **performance-optimizer**: System optimization, profiling, load testing

**Operations & Management:**
- **pr-optimizer**: PR creation, GitHub workflow automation
- **dependency-manager**: Dependency updates, security alerts, packages
- **github-checker**: Repository maintenance, issue management
- **security-scanner**: Vulnerability scanning, OWASP compliance
- **context-engineer**: Context optimization, prompt improvement

### Using the Agent System

#### For Complex Tasks → Use workflow-orchestrator

```bash
# Example: Implementing authentication system
workflow-orchestrator "Implement user authentication with tests and documentation"
```

The workflow-orchestrator automatically:
- Coordinates multiple specialists (code, tests, docs, security)
- Ensures security validation chains are triggered
- Manages dependencies between tasks
- Provides progress tracking via TodoWrite

#### For Domain-Specific Work → Use Specialists

```bash
# Documentation tasks
smart-doc-generator "Create API documentation for user endpoints"

# Testing tasks
test-automator "Add comprehensive test coverage for authentication"

# Technical research
technical-researcher "Evaluate authentication libraries for FastAPI"

# Cloud infrastructure
aws-expert "Design scalable deployment architecture on AWS"

# Code debugging
debugger "Investigate performance bottleneck in user query"
```

#### Security Chain (Mandatory)

All security-sensitive code changes follow the mandatory chain:
```
code-reviewer → security-orchestrator → (validation complete)
```

This ensures comprehensive security validation before code changes.

### Git Operations Enhancement

#### Smart Commit with Agent Integration

```bash
# Context-aware commits with Release Flow support
/git-ops:smart-commit "Additional commit instructions"
```

Features:
- Analyzes changes and suggests conventional commit format
- Runs local security validation automatically
- Provides GitHub review options for comprehensive validation
- Supports Release Flow workflow integration

#### Release Flow Navigation

```bash
# Guided release process following ADR-001
/git-ops:start-release-journey
```

The journey guide:
- Auto-detects current workflow state
- Provides step-by-step guidance for proper Release Flow
- Handles feature/* → release/* → main workflow
- Includes emergency procedures and cleanup options

### Agent Compliance Validation

Validate agent architecture compliance:

```bash
# Quick compliance check
./scripts/agent-validation/check-agents.sh

# Verbose compliance analysis
./scripts/agent-validation/check-agents.sh --verbose
```

The compliance checker ensures:
- Agent architecture follows ADR-007 (Hierarchical Multi-Agent Architecture)
- Tool permissions respect security boundaries
- Cognitive load model allocation is correct
- All agents maintain proper metadata format

## Next Steps

### If Using Synchronization System

1. **Customize Instructions**: Edit `.claude/project/CLAUDE.project.md` with domain-specific rules
2. **Configure Settings**: Modify `.claude/project/settings.project.json` for custom permissions
3. **Build Configurations**: Run `scripts/build-config.sh` after changes
4. **Stay Updated**: Use `scripts/update-boilerplate.sh` to pull improvements

### Agent System Onboarding

1. **Start with workflow-orchestrator**: Try a complex task to see orchestration in action
2. **Explore specialists**: Use domain experts for specific technology tasks
3. **Practice git-ops**: Use smart-commit and start-release-journey commands
4. **Validate compliance**: Run agent compliance checks during development
5. **Security-first**: Always ensure security chains are triggered for sensitive code

### General Next Steps

1. **Review Documentation**: Check out [Development Workflow](development.md)
2. **Explore Security**: Learn about [Security Features](security.md)
3. **Test TTS**: Try the audio notification system
4. **Read Agent System**: See [Agent System Reference](../reference/agent-system.md)
5. **Read Sync Guide**: See [Synchronization Guide](../SYNCHRONIZATION.md) for advanced workflow

For detailed guidance, see our [complete documentation index](../../README.md#documentation).
