# Reference

Essential API and system information.

## Hooks (8 Total)

8 hooks execute in sequence. Exit codes: 0=continue, 1=block, 2=error.

**user_prompt_submit** - Input validation
**pre_tool_use** - Security validation (CRITICAL)
**post_tool_use** - Logging
**notification** - TTS alerts
**stop** - Completion handling
**subagent_stop** - Agent completion
**pre_compact** - Backup before compaction
**session_start** - Context loading

### Security Hook (pre_tool_use)

Blocks dangerous commands. For complete security patterns and testing details, see [Security Guide](../guides/security.md).

Quick test: `echo '{"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}' | uv run .claude/hooks/pre_tool_use.py`

## Hierarchical Agent System (32 Total)

**Orchestrators (2)**:
- **workflow-orchestrator** - Complex multi-step coordination
- **security-orchestrator** - Mandatory security validation chains

**Specialists (27)**: Domain expertise including python-pro, typescript-pro, react-expert, nextjs-expert, aws-expert, docker-expert, postgres-expert, api-architect, performance-optimizer, and 18 more

**Analyzers (3)**:
- **code-reviewer** - Security and quality analysis
- **test-coverage-analyzer** - Coverage analysis
- **work-completion-summary** - Audio summaries

For complete agent documentation, see [Agent System Reference](agent-system.md).

## Commands (7 Total)

**cook** - Run multiple agent tasks in parallel for rapid development
**prime** - Load project context for new agent sessions
**prime_tts** - Initialize Text-to-Speech system
**question** - Structured questioning for requirements gathering
**update_status_line** - Update dynamic terminal status displays
**git-ops:smart-commit** - Context-aware commit creation with Release Flow support
**git-ops:start-release-journey** - Guide engineers through proper Release Flow process

## Serena MCP Integration

Semantic coding tools for intelligent codebase analysis and manipulation.

**Key Features:**

- Symbol-based navigation and code understanding
- Project memory system for architectural knowledge
- Token-efficient code reading and manipulation
- Pattern-based search with structure awareness

For complete serena-mcp documentation including setup, usage patterns, and best practices, see [Serena MCP Reference](serena-mcp.md).

## TTS System

Provider fallback: ElevenLabs → OpenAI → pyttsx3

For complete TTS system documentation including provider comparison, configuration, and troubleshooting, see [TTS System Reference](../reference/tts-system.md).

## Security Levels

**strict** - Block all dangerous patterns (production)
**moderate** - Warn and block (development)
**permissive** - Warn only (testing)

Set: `SECURITY_LEVEL=strict`

## Testing & Validation

**3-Tier Testing Architecture:**

- **High Priority (Security Critical)**: Safety hooks, dangerous command detection
- **Medium Priority (Feature Reliability)**: TTS providers, integration testing
- **Infrastructure**: Comprehensive test runners and validation

For comprehensive testing strategy, commands, and categories, see [Testing Guide](../guides/testing.md).

Quick commands:

- All tests: `python tests/run_all_tests.py`
- Security only: `python tests/test_safety_hooks.py`
- Hook integration: `python tests/test_hook_integration.py`

## Boilerplate Synchronization System

Three-layer configuration system for graceful boilerplate updates:

**Base Layer**: Core boilerplate files (git subtree)
**Project Layer**: Domain-specific customizations
**Merged Layer**: Auto-generated final configuration

### Synchronization Commands

**init-boilerplate.sh** - Initialize synchronization system in projects
**update-boilerplate.sh** - Pull boilerplate updates without losing customizations
**build-config.sh** - Merge base templates with project customizations

For complete synchronization workflow, see [Synchronization Guide](../SYNCHRONIZATION.md).

## PRP Status Management

PRPs (Product Requirements Process) include lifecycle tracking to prevent documentation drift:

| Status | Description | Set By |
|--------|-------------|--------|
| **PROPOSED** | Idea documented, not started | `/prp:create` |
| **IN_PROGRESS** | Being implemented | `/prp:execute` |
| **COMPLETED** | Finished and reviewed | `/prp:review` |
| **OBSOLETE** | No longer relevant | Manual update |

## Configuration

For detailed configuration including .env setup, hook settings, and environment variables, see:

- [Development Guide](../guides/development.md) for development configuration
- [TTS System Reference](tts-system.md) for TTS configuration
- [Security Guide](../guides/security.md) for security configuration
- [Serena MCP Reference](serena-mcp.md) for semantic coding configuration
- [Synchronization Guide](../SYNCHRONIZATION.md) for boilerplate sync configuration

## Architecture

```text
User Input → user_prompt_submit → pre_tool_use (security) → Tool Execution
                                       ↓ (if blocked)
                                   Block + Log
```

## Common Issues

**Permission denied**: `chmod +x .claude/hooks/*.py`
**No TTS**: Check API keys or use pyttsx3
**Commands blocked**: Review security patterns
**Import errors**: Run `uv sync`
