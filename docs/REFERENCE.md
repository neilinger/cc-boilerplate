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

Blocks dangerous commands:
- `rm -rf` patterns (30+ variations)
- `.env` file access 
- Path traversal (`../`, system paths)

Test: `echo '{"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}' | uv run .claude/hooks/pre_tool_use.py`

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

**ElevenLabs**: Premium quality, 29 languages, requires API key  
**OpenAI**: Good quality, 6 voices, requires API key  
**pyttsx3**: Local system TTS, always available  

Configuration in `.env`:
```
TTS_DEFAULT_PROVIDER=elevenlabs
ELEVENLABS_API_KEY=your_key
OPENAI_API_KEY=your_key
```

## Security Levels

**strict** - Block all dangerous patterns (production)  
**moderate** - Warn and block (development)  
**permissive** - Warn only (testing)  

Set: `SECURITY_LEVEL=strict`

## Testing

```bash
# All tests
python tests/run_all_tests.py

# Security only
python tests/test_safety_hooks.py

# TTS only
python tests/test_tts_providers.py
```

Test categories:
- 🔴 Security (always run)
- 🟡 Features (release branches)  
- 🟢 Extended (manual)

## Configuration

### .env essentials:
```
USER_NAME=YourName
TTS_DEFAULT_PROVIDER=elevenlabs
ELEVENLABS_API_KEY=your_key
SECURITY_LEVEL=strict
```

### Hook settings (.claude/settings.json):
```json
{
  "hooks": {
    "pre_tool_use": {"enabled": true, "security_level": "strict"},
    "notification": {"enabled": true, "default_tts": "elevenlabs"}
  }
}
```

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