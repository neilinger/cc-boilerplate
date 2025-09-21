# CC-Boilerplate Code Style and Conventions

## Architectural Principles
- **KISS (Keep It Simple, Stupid)** - Avoid over-engineering
- **YAGNI (You Aren't Gonna Need It)** - Don't build unnecessary features
- **Security-first** - All code modifications must pass security chains
- **Zero dependencies** - Python standard library only

## Code Organization
- **File-based storage** - Everything in git repository
- **Cross-platform compatibility** - Works on macOS, Linux, Windows
- **Standard library only** - No external dependencies in pyproject.toml
- **UV single-file scripts** - Self-contained executable scripts

## Agent System Conventions
- **Hierarchical delegation** - Always use workflow-orchestrator for complex tasks
- **Cognitive load optimization** - Model allocation based on task complexity
- **Security chain compliance** - code-reviewer → security-orchestrator → security-scanner
- **Role-based permissions** - Agent-specific tool access boundaries

## File Structure Conventions
```
.claude/
├── agents/         # Hierarchical agent system (100+ agents)
├── commands/       # Claude commands (7 total)
├── hooks/          # All 8 Claude Code hooks
├── output-styles/  # 9 workflow-optimized formats
└── settings.json   # Permissions and configuration

specs/              # PRP specifications
PRPs/              # Product Requirements Process templates
scripts/           # Validation and sync utilities
tests/             # Security-focused testing
```

## Documentation Standards
- **ADR** (Architecture Decision Records) - WHY decisions
- **PRP** (Product Requirements Process) - HOW implementation
- **No proactive documentation** - Only create docs when explicitly requested
- **Security documentation** - Mandatory for all security-sensitive features

## Quality Standards
- **Behavioral consistency** - LLM-as-Judge validation
- **CEO role adherence** - Delegation patterns and contrarian discipline
- **Non-blocking quality gates** - Validate without stopping velocity
- **95% detection accuracy** - For behavioral regression testing