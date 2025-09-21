# Development Workflow

This document describes the agent-driven development workflow for cc-boilerplate following Release Flow branching strategy, hierarchical multi-agent patterns, and priority-based testing.

## Agent-First Development Overview

CC-Boilerplate now uses a **hierarchical multi-agent system** that enhances rather than complicates development. The system follows KISS/YAGNI principles with proven value:

- **27 specialist agents** for domain expertise (60% increase in coverage)
- **Single workflow-orchestrator** for complex multi-step tasks
- **Mandatory security chain** for all code modifications
- **66% simpler orchestration** than traditional complex systems

## Quick Reference - Agent-Enhanced Workflow

```bash
# Agent-driven feature development
workflow-orchestrator "Implement user authentication with tests and docs"

# Smart commit with context awareness
/git-ops:smart-commit "Additional commit context"

# Guided release process
/git-ops:start-release-journey

# Manual workflow (for simple changes)
git checkout -b feature/your-feature-name
git push origin feature/your-feature-name  # Runs security tests (~30s)
git checkout -b release/v1.1.0
git merge feature/your-feature-name
git push origin release/v1.1.0  # Runs comprehensive tests (~5-7min)
gh pr create --base main --title "Release v1.1.0"  # Runs enhanced tests (~7-10min)
```

## Agent Selection Decision Tree

```text
Is this a complex multi-step task?
├─ YES → Use workflow-orchestrator
└─ NO ↓

Does this involve security-sensitive code?
├─ YES → Mandatory security chain (code-reviewer → security-orchestrator)
└─ NO ↓

Is this domain-specific work?
├─ Documentation → smart-doc-generator
├─ Testing → test-automator
├─ Python → python-pro
├─ TypeScript → typescript-pro
├─ React → react-expert
├─ API Design → api-architect
├─ Research → technical-researcher
├─ Debugging → debugger
├─ Architecture → adr-creator
├─ GitHub ops → pr-optimizer or github-checker
└─ Analysis only → appropriate analyzer

Is this a simple task?
└─ Proceed manually with appropriate tools
```

## Branch Strategy Overview

Our workflow uses **Release Flow** with three branch types:

- **`feature/**`** - Development work, fast security feedback
- **`release/**`** - Stabilization and comprehensive testing
- **`main`** - Production-ready code with deployment automation

## Boilerplate Synchronization

### Development to Deliverable Sync

CC-Boilerplate has a dual structure:
- **Development**: `.claude/`, `docs/adr/`, `PRPs/` (where active development happens)
- **Deliverable**: `boilerplate/` (what gets delivered to users)

**CRITICAL**: After making changes to agents, ADRs, or PRPs, you must sync to the deliverable:

```bash
# Sync development content to boilerplate deliverable
./scripts/sync-to-boilerplate.sh

# Preview what would be synced
./scripts/sync-to-boilerplate.sh --dry-run --verbose

# Sync and commit for release
./scripts/sync-to-boilerplate.sh
git add boilerplate/
git commit -m "sync: update boilerplate with latest development"
```

**What gets synced:**
- `.claude/` → `boilerplate/.claude/` (all agents, configs, hooks)
- `docs/adr/` → `boilerplate/docs/adr/` (Architecture Decision Records)
- `PRPs/` → `boilerplate/PRPs/` (Product Requirements Process)
- `setup.sh`, `.env.sample`, scripts

**Safety features:**
- Creates backup before sync
- Validates sync completeness
- Shows before/after statistics
- Dry-run mode for testing

### When to Sync

**ALWAYS sync before:**
- Creating releases/tags
- Pushing agent changes
- Adding new ADRs or PRPs
- Testing with `init-boilerplate.sh`

**Validation:**
```bash
# Check sync worked
ls boilerplate/.claude/agents/specialists/ | wc -l  # Should be 26+ files
ls boilerplate/docs/adr/*.md | wc -l              # Should be 10+ files
ls boilerplate/PRPs/*.md | wc -l                  # Should be 6+ files
```

## Agent-Driven Development Patterns

### 1. Complex Feature Development (Agent-First)

**Use workflow-orchestrator for multi-step tasks requiring coordination:**

```bash
# Complex feature with multiple domains
workflow-orchestrator "Implement user authentication system with JWT, tests, and documentation"

# The orchestrator will:
# 1. Plan the workflow with TodoWrite
# 2. Coordinate appropriate specialists (python-pro, security-scanner, test-automator)
# 3. Trigger mandatory security chain
# 4. Generate documentation via smart-doc-generator
# 5. Integrate results and validate completion
```

**When to use orchestration:**
- Features requiring 3+ distinct steps
- Cross-cutting concerns (security + performance + documentation)
- Multi-domain work (backend + frontend + database)
- Architecture-impacting changes

### 2. Domain-Specific Development (Specialist-First)

**Use specialist agents for focused domain work:**

```bash
# Python development
python-pro "Optimize the FastAPI route performance using modern Python 3.12 features"

# React development
react-expert "Implement React 19 suspense patterns for the user dashboard"

# Database optimization
postgres-expert "Design efficient indexing strategy for user analytics queries"

# API architecture
api-architect "Design RESTful API boundaries for the notification service"
```

**Available specialists (10 new in Phase 1):**
- **python-pro**: Python 3.12+, FastAPI, modern tooling (uv, ruff)
- **typescript-pro**: Advanced TypeScript, enterprise patterns
- **react-expert**: React 19+, Next.js 15+, performance optimization
- **postgres-expert**: PostgreSQL optimization, advanced features
- **aws-expert**: AWS architecture, IaC, Well-Architected Framework
- **docker-expert**: Containerization, K8s, security, performance
- **performance-optimizer**: System optimization, profiling, load testing
- **api-architect**: RESTful/GraphQL APIs, microservices
- **nextjs-expert**: Next.js App Router, SSR/SSG, full-stack
- **graphql-architect**: Federation, schema design, optimization

### 3. Traditional Feature Development (Manual)

**Purpose**: Simple changes using traditional git workflow with security validation

```bash
# Start from latest main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/descriptive-name
# Examples: feature/fix-typo, feature/update-config

# Make simple changes
# ... edit files ...

# Use smart commit for context-aware commits
/git-ops:smart-commit "Fix configuration bug in TTS provider"
# OR manual commit with security validation
git add .
python tests/test_safety_hooks.py  # Required security check
git commit -m "feat: implement TTS provider fallback"
git push origin feature/descriptive-name
```

### 4. Security-First Patterns (Mandatory)

**ALL code modifications trigger the security chain - this is non-negotiable:**

```text
Security Chain: code-reviewer → security-orchestrator → security-scanner
Result: BLOCK if issues found, PROCEED if validated
```

**Security chain integration examples:**

```bash
# Automatic: Triggered by any agent modifying code
workflow-orchestrator "Add user input validation"  # Security chain runs automatically

# Manual: When working outside agent system
# 1. Make code changes
# 2. Security chain validates automatically on commit/push
# 3. Fix any issues before proceeding
```

**Security boundaries and tool restrictions:**
- **Analyzers**: Read-only access (code-reviewer, security-scanner)
- **Specialists**: Domain-restricted tools only
- **Orchestrators**: Full coordination capabilities
- **All agents**: Respect principle of least privilege

### 5. Git-Ops Integration

**Enhanced git operations with smart commands:**

```bash
# Smart commit - context-aware with Release Flow support
/git-ops:smart-commit "Additional context about the change"
# Features:
# - Analyzes changes and suggests appropriate commit type
# - Runs security validation
# - Offers GitHub review integration
# - Follows conventional commits format

# Guided release process
/git-ops:start-release-journey
# Features:
# - Walks through Release Flow branching
# - Validates branch naming conventions
# - Ensures proper PR targeting
# - Integrates with CI/CD pipeline

# Create context-aware PRs
/git-ops:create-pull-request "Release v1.2.0"
# Features:
# - Auto-detects branch type and targets correctly
# - Follows Release Flow: feature/* → release/* → main
# - Generates comprehensive PR descriptions
# - Enables GitHub Claude review
```

**GitHub Claude Review integration:**

```text
# After creating PR, use comprehensive review
@claude Please review this PR comprehensively for security, KISS/YAGNI compliance, hierarchical agent architecture alignment (ADR-007), and cognitive load model allocation (ADR-008)

# Quick security focus
@claude Review for security vulnerabilities and safety

# Agent architecture compliance
@claude Check adherence to ADR-007 (Hierarchical Multi-Agent Architecture)
```

### 6. Release Preparation

**Purpose**: Stabilize features and run comprehensive validation

```bash
# Create release branch from main
git checkout main
git pull origin main
git checkout -b release/v1.2.0

# Merge completed features
git merge feature/feature-1
git merge feature/feature-2

# Push for comprehensive testing
git push origin release/v1.2.0
```

**CI/CD**: Runs **comprehensive test suite** (~5-7 minutes)

- All security-critical tests
- Feature reliability tests (TTS providers)
- Coverage reporting
- Performance validation

✅ **Success**: Ready for main branch and production
❌ **Failure**: Fix issues in release branch or remove problematic features

### 7. Production Release

**Purpose**: Deploy stable code and create official release

```bash
# Create pull request to main
gh pr create --base main --title "Release v1.2.0" --body "
## Release v1.2.0

### Features
- New TTS provider fallback system
- Enhanced PRP validation
- Improved safety hooks

### Testing
- ✅ Security tests passed
- ✅ Integration tests passed
- ✅ Feature tests passed

### Breaking Changes
- None
"

# After PR approval and merge, automatic deployment runs:
# - Final test validation
# - Semantic version tagging
# - Release artifact creation
# - Badge updates
```

**CI/CD**: Runs **enhanced validation** (~7-10 minutes)

- Complete test suite
- Security scanning
- Dependency vulnerability checks
- Release notes validation

**Deployment**: Automatic on main branch push

- Creates semantic version tag (e.g., v1.2.0-20250109120000)
- Updates repository badges
- Generates release notes

## Testing Strategy

### Test Categories by Branch

| Branch Type | Tests Run | Duration | Purpose |
|-------------|-----------|----------|---------|
| `feature/**` | Security Critical | ~30s | Fast feedback |
| `release/**` | Comprehensive | ~5-7min | Quality assurance |
| PR to `main` | Enhanced | ~7-10min | Final validation |
| `main` push | Full + Deploy | ~3-5min | Production ready |

### Test Priorities

For detailed test categories and execution strategy, see [Testing Guide](testing.md#test-categories-and-priorities).

## Agent-Enhanced Development Best Practices

### Before You Start

1. **Agent System Awareness**: Understand when to use orchestration vs specialists vs manual work
2. **Read ADRs**: Review [docs/adr/](../adr/) for architectural decisions
3. **Check CLAUDE.md**: Follow KISS/YAGNI principles and agent selection protocol
4. **Validate agent compliance**: Run `./scripts/agent-validation/check-agents.sh` to ensure system health
5. **Review test coverage**: Understand what needs testing
6. **Synchronization setup**: If using boilerplate sync, understand [Synchronization Guide](../SYNCHRONIZATION.md)

### During Development

1. **Agent-first approach**: Use appropriate agent for the task complexity
2. **Security chain respect**: Never bypass mandatory security validations
3. **Small, logical commits**: Use `/git-ops:smart-commit` for context-aware commits
4. **Domain expertise**: Leverage specialist agents (python-pro, react-expert, etc.)
5. **Test locally**: Security hooks run automatically, but validate with `python tests/test_safety_hooks.py`
6. **Document decisions**: Use `adr-creator` agent for architectural choices
7. **Sync awareness**: If using boilerplate sync, customize in `.claude/project/` not base files

### Before Release

1. **Agent validation**: Run `./scripts/agent-validation/check-agents.sh --verbose` for comprehensive compliance
2. **Full test run**: Execute `python tests/run_all_tests.py`
3. **Security validation**: Ensure security chain has validated all changes
4. **Documentation sync**: Use `smart-doc-generator` for updates if needed
5. **Manual validation**: Test key user scenarios
6. **Version planning**: Follow semantic versioning

### Documentation Standards

For markdown files (`.md`), the project uses automated linting to ensure quality and consistency.

#### Setup (First Time)

```bash
# Install pre-commit (using UV)
uv pip install pre-commit

# Install git hooks
pre-commit install

# Install VS Code extension (recommended)
# Search for "markdownlint" by David Anson in VS Code Extensions
```

#### Usage

```bash
# Automatic: Runs on every commit (fixes issues automatically)
git commit -m "docs: update API documentation"

# Manual: Check all markdown files
pre-commit run markdownlint --all-files

# Manual: Check specific file
markdownlint docs/reference/api.md --fix
```

#### Standards Enforced

- **File naming**: Use kebab-case (`api-guide.md` not `API_GUIDE.md`)
- **Exceptions**: `README.md`, `LICENSE`, `CHANGELOG.md` keep their standard names
- **Link formatting**: `[Setup Guide](setup-guide.md)` not `[here](setup-guide.md)`
- **Code blocks**: Specify language for syntax highlighting (```python,```bash)
- **Consistent lists**: Use either `*` or `-` throughout document

#### Configuration

Project uses `.markdownlint.json` with pragmatic rules:

- No line length limits (let editors wrap)
- Allow HTML when needed
- Focus on real quality issues, not pedantic formatting

## Repository Structure

```
cc-boilerplate/
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # Branch-specific CI/CD pipeline
├── boilerplate/                # NEW: Core boilerplate templates
│   ├── .claude/                # Base configuration templates
│   ├── templates/              # Mergeable template files
│   └── scripts/                # Synchronization utilities
├── docs/
│   ├── adr/                    # Architecture Decision Records
│   │   ├── adr-001-branching-strategy.md
│   │   ├── adr-002-cicd-pipeline.md
│   │   └── adr-003-testing-strategy.md
│   ├── SYNCHRONIZATION.md      # NEW: Boilerplate sync guide
│   └── development.md          # This file
├── examples/
│   └── sample-project/         # NEW: Synchronization example
├── scripts/
│   ├── init-boilerplate.sh     # NEW: Initialize synchronization
│   ├── update-boilerplate.sh   # NEW: Pull boilerplate updates
│   └── build-config.sh         # NEW: Merge configurations
├── tests/
│   ├── test_safety_hooks.py    # 🔴 Security critical
│   ├── test_hook_integration.py # 🔴 Security critical
│   ├── test_prp_edge_cases.py  # 🔴 Security critical
│   ├── test_tts_providers.py   # 🟡 Feature reliability
│   └── run_all_tests.py        # Test orchestrator
└── [project files...]
```

### Agent Validation and Compliance

**Regular compliance checking ensures system health:**

```bash
# Quick compliance check
./scripts/agent-validation/check-agents.sh

# Detailed analysis with suggestions
./scripts/agent-validation/check-agents.sh --verbose

# What gets validated:
# ✓ Hierarchical agent placement (27 agents organized properly)
# ✓ Tool allocation boundaries (3-7 tools per agent)
# ✓ Model allocation rules (cognitive load matching)
# ✓ Security chain integration
# ✓ Agent configuration integrity
```

**Compliance ensures:**
- **Architecture integrity**: Proper orchestrator → specialist → analyzer hierarchy
- **Security boundaries**: Tool restrictions enforced
- **Performance optimization**: Model allocation matches cognitive load
- **Cost efficiency**: No over-allocation of expensive models

## Common Development Scenarios

### Agent-Driven Scenarios

**Complex Feature Implementation:**
```bash
# Let workflow-orchestrator coordinate everything
workflow-orchestrator "Implement OAuth2 integration with Google, including tests and documentation"
# Result: Full feature with security validation, tests, and docs
```

**Domain-Specific Optimization:**
```bash
# Use appropriate specialist
performance-optimizer "Analyze and optimize database query performance in user analytics"
aws-expert "Design cost-optimized AWS architecture for the new service"
```

**Research and Architecture:**
```bash
# Deep research with recommendations
technical-researcher "Evaluate Next.js 15 App Router vs traditional routing for our use case"
adr-creator "Document decision on microservices vs monolith architecture"
```

### Traditional Scenarios

### Hot Fix (Security-First)

```bash
# Critical bug found in production
git checkout main
git checkout -b hotfix/v1.2.1

# For complex fixes, use debugger agent
debugger "Analyze and fix critical safety hook bypass vulnerability"

# For simple fixes, manual with security validation
# ... make minimal changes ...
/git-ops:smart-commit "Critical security fix"

# Security chain runs automatically - CANNOT be bypassed
# Create PR directly to main (skip release branch for urgency)
/git-ops:create-pull-request "Hotfix v1.2.1 - Critical security fix"

# GitHub review recommended for security fixes
# @claude Review this hotfix for security vulnerabilities and completeness
```

### Multiple Features in Parallel (Agent Coordination)

```bash
# Developer A - Use specialist for domain work
python-pro "Enhance TTS provider with new fallback mechanisms"

# Developer B - Use orchestrator for complex work
workflow-orchestrator "Implement new safety hook system with validation"

# Both features developed with agent assistance
# Security chain validates each feature automatically
# Integration managed by Release Flow
git checkout release/v1.3.0
git merge feature/tts-enhancement
git merge feature/new-hook
```

### Working with Boilerplate Synchronization (Agent-Aware)

```bash
# Update boilerplate while working on feature
git checkout feature/my-feature
scripts/update-boilerplate.sh  # Pulls latest boilerplate improvements
scripts/build-config.sh        # Rebuilds merged configurations

# Validate agent system integrity after sync
./scripts/agent-validation/check-agents.sh

# Test that customizations are preserved
git diff CLAUDE.md             # Should show your domain-specific content
/git-ops:smart-commit "Update boilerplate and rebuild configs"
```

### Failed Release Branch (Debug-Assisted)

```bash
# If release/v1.2.0 tests fail badly
# Use debugger agent for root cause analysis
debugger "Analyze why release/v1.2.0 tests are failing and identify problematic changes"

# Based on analysis, create new release branch
git checkout main
git checkout -b release/v1.2.1  # New release branch

# Cherry-pick only working features
git cherry-pick feature/working-feature
# Skip the broken feature for now

# Document the issue for future reference
adr-creator "Document lessons learned from release/v1.2.0 failure"
```

## Badge System

The README badges reflect current status:

- **CI/CD Status**: Overall workflow health
- **Security Tests**: Safety hook validation status
- **Test Coverage**: Current coverage percentage
- **Hooks/Agents/Styles**: Static count badges
- **Release**: Latest version tag
- **License**: Project license

Update badges by editing the README.md links after repository setup.

## Troubleshooting

### Tests Failing on Feature Branch

- Only security tests run on feature branches
- Focus on safety hooks and dangerous command detection
- Check `.env` access patterns and JSON validation

### Comprehensive Tests Failing on Release

- Review all test categories (security + features)
- TTS provider tests may fail without API keys (acceptable)
- Check test timeout limits and performance

### Enhanced Validation Failing on PR

- Most comprehensive test suite runs
- Security scanning may flag new vulnerabilities
- Dependency checks may find outdated packages
- Manual review may be required

### Deployment Issues

- Check semantic versioning format
- Verify git credentials and permissions
- Review badge update automation
- Validate release notes generation

## Documentation Guidelines

### File Naming

- Use kebab-case: `user-guide.md` not `USER_GUIDE.md` ([Google style](https://developers.google.com/style/filenames))
- Exception: Standard files (README.md, LICENSE)

### Structure

- Guides go in `docs/guides/`
- Reference material in `docs/reference/`
- ADRs in `docs/adr/`

### Before Adding New Docs

1. Check if existing doc can be improved instead
2. Ensure proper cross-referencing
3. Update README.md navigation
4. Follow single-source-of-truth principle

### Review Checklist

- [ ] Follows naming convention
- [ ] Added to README navigation
- [ ] Cross-referenced appropriately
- [ ] No content duplication

## Getting Help

### Agent System Resources

1. **Agent System Reference**: [docs/reference/agent-system.md](../reference/agent-system.md) for complete agent documentation
2. **Agent Selection**: Use the decision tree above or consult [CLAUDE.md](../../CLAUDE.md) for selection protocol
3. **Compliance Validation**: Run `./scripts/agent-validation/check-agents.sh --verbose` for system health
4. **Phase 1 Analysis**: [docs/phase1-agent-system-evolution.md](../phase1-agent-system-evolution.md) for system evolution details

### Traditional Resources

1. **Review ADRs**: [docs/adr/](../adr/) explains architectural decisions
2. **Check test docs**: [Testing Guide](testing.md) for detailed test info
3. **KISS/YAGNI guidance**: [CLAUDE.md](../../CLAUDE.md) for development principles
4. **Create issue**: Use GitHub issues for bugs or enhancement requests

### Quick Agent Examples

```bash
# Documentation help
smart-doc-generator "Update the API documentation for the new endpoints"

# Testing help
test-automator "Create comprehensive tests for the authentication module"

# Research help
technical-researcher "Research best practices for implementing rate limiting in FastAPI"

# Architecture help
adr-creator "Document the decision between Redis and in-memory caching"

# GitHub help
pr-optimizer "Optimize this PR description and validate it follows our standards"
```

Remember: **Agent-enhanced, security first, simplicity always, ship only what's needed now.**
