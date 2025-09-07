# Reference

Essential API and system information.

## Hooks

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

## Agents

**meta-agent** - Generate new agents
**engineer-code-reviewer** - Code/security review
**work-completion-summary** - Audio summaries
**llm-ai-agents-and-eng-research** - AI research
**test-automator** - Generate test suites
**technical-researcher** - Technical analysis
**test-coverage-analyzer** - Coverage analysis
**smart-doc-generator** - Documentation

## TTS System

Provider fallback: ElevenLabs → OpenAI → pyttsx3

For complete TTS system documentation including provider comparison, configuration, and troubleshooting, see [TTS System Reference](../reference/tts-system.md).

## Security Levels

**strict** - Block all dangerous patterns (production)
**moderate** - Warn and block (development)
**permissive** - Warn only (testing)

Set: `SECURITY_LEVEL=strict`

## Testing

For comprehensive testing strategy, commands, and categories, see [Testing Guide](../guides/testing.md).

Quick commands:

- All tests: `python tests/run_all_tests.py`
- Security only: `python tests/test_safety_hooks.py`

## Configuration

### Configuration

For detailed configuration including .env setup, hook settings, and environment variables, see:

- [Development Guide](../guides/development.md) for development configuration
- [TTS System Reference](../reference/tts-system.md) for TTS configuration
- [Security Guide](../guides/security.md) for security configuration

## Architecture

```
User Input → user_prompt_submit → pre_tool_use (security) → Tool Execution
                                       ↓ (if blocked)
                                   Block + Log
```

## Common Issues

**Permission denied**: `chmod +x .claude/hooks/*.py`
**No TTS**: Check API keys or use pyttsx3
**Commands blocked**: Review security patterns
**Import errors**: Run `uv sync`
