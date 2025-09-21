# Project Overview: CC-Boilerplate - Strategic Claude Code Accelerator

## Purpose

CC-Boilerplate is a comprehensive Claude Code acceleration framework that transforms development workflows through:
- **Hierarchical Multi-Agent System**: 32 specialized agents with autonomous coordination
- **Security-First Architecture**: Mandatory validation chains and comprehensive protection
- **Boilerplate Synchronization**: Three-layer configuration system for graceful updates
- **KISS/YAGNI Principles**: Simplest solutions that work, build only what's needed now

## Tech Stack

- **Primary Language**: Python 3.12+ with modern tooling (uv, ruff)
- **Agent Architecture**: Hierarchical orchestration with cognitive load-based model allocation
- **Security System**: Comprehensive hook-based validation with 30+ rm pattern protection
- **Integration**: Claude Code CLI, ElevenLabs TTS, serena-mcp semantic coding, GitHub workflows
- **Synchronization**: Git subtree-based boilerplate delivery system

## Current Architecture (v1.5.0+)

### Hierarchical Agent System (32 Total)
- **Orchestrators (2)**: workflow-orchestrator, security-orchestrator
- **Specialists (27)**: Domain experts (python-pro, react-expert, aws-expert, etc.)
- **Analyzers (3)**: code-reviewer, test-coverage-analyzer, work-completion-summary

### Security Architecture
- **Pre-tool validation**: Blocks dangerous commands before execution
- **Mandatory security chains**: All code modifications trigger security validation
- **Progressive enforcement**: Three-tier security levels (strict/moderate/permissive)
- **Environmental protection**: .env access blocking, path traversal prevention

### Synchronization System
- **Base Layer**: Core boilerplate templates in `boilerplate/` (git subtree)
- **Project Layer**: Domain customizations in `.claude/project/`
- **Merged Layer**: Generated configurations (CLAUDE.md, settings.json)

## Key Differentiators

### Agent-First Development
- **Autonomous coordination**: Agents select and delegate to other agents
- **Security-enforced**: Cannot bypass mandatory validation chains
- **Cognitive optimization**: Model allocation matches task complexity
- **Progressive complexity**: Simple tasks → manual, complex → orchestrated

### Documentation-Driven Architecture
- **ADRs**: Architectural decisions with clear rationale
- **PRPs**: Product requirements with automatic context discovery
- **Spec-Kit Integration**: Structured implementation planning
- **Living documentation**: Self-updating through semantic analysis

### Production-Ready Features
- **Release Flow branching**: Clear development → staging → production path
- **Comprehensive testing**: Security-critical → feature reliability → full validation
- **CI/CD integration**: Branch-specific validation with progressive complexity
- **Badge-driven status**: Real-time project health indicators

## Architecture Benefits

- **Scalability**: Add new agents without system redesign
- **Maintainability**: Clear separation of concerns and single-source-of-truth
- **Security**: Multiple validation layers prevent dangerous operations
- **Flexibility**: Customizable per project while maintaining core integrity
- **Evolution**: Graceful updates through synchronization system