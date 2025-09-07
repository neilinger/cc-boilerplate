# API Reference

## Table of Contents

- [Hook API Reference](#hook-api-reference)
- [Agent API Reference](#agent-api-reference)
- [Utility API Reference](#utility-api-reference)
- [Output Style Reference](#output-style-reference)
- [Configuration API](#configuration-api)

## Hook API Reference

The CC-Boilerplate includes all 8 Claude Code hooks with security-focused enhancements.

### Hook Execution Order

```
1. user_prompt_submit    → Pre-process user input
2. pre_tool_use         → Security validation before tool execution
3. post_tool_use        → Post-processing and logging
4. notification         → Custom notifications with TTS
5. stop                 → Task completion handling
6. subagent_stop        → Subagent completion announcements
7. pre_compact          → Transcript backup before compaction
8. session_start        → Development context loading
```

### 1. user_prompt_submit.py

**Purpose**: Pre-processes user prompts with validation and logging.

**Parameters**:

- `prompt`: User input prompt (string)
- `--logging-level`: Log verbosity (`debug`, `info`, `warn`, `error`)

**Exit Codes**:

- `0`: Success, continue processing
- `1`: Validation failed, block prompt
- `2`: System error

**Usage Example**:

```bash
echo '{"prompt": "Hello Claude"}' | uv run .claude/hooks/user_prompt_submit.py
```

**Features**:

- Input sanitization and validation
- Prompt logging with session context
- User configuration loading

### 2. pre_tool_use.py

**Purpose**: Security validation before tool execution. **SECURITY CRITICAL**.

**Parameters**:

- `tool_name`: Name of tool being executed
- `parameters`: Tool parameters (JSON object)
- `--security-level`: Validation strictness (`strict`, `moderate`, `permissive`)

**Exit Codes**:

- `0`: Safe to proceed
- `1`: **BLOCKED** - Dangerous command detected
- `2`: Validation error

**Dangerous Command Detection**: For complete security patterns and protection details, see [Security Guide](../guides/security.md#blocked-commands).

**Usage Example**:

```bash
echo '{"tool_name": "bash", "parameters": {"command": "rm -rf /"}}' | \
  uv run .claude/hooks/pre_tool_use.py
# Exit code: 1 (BLOCKED)
```

**Security Features**: For detailed security validation features, see [Security Guide](../guides/security.md#threat-protection).

### 3. post_tool_use.py

**Purpose**: Post-execution logging and transcript processing.

**Parameters**:

- `tool_name`: Executed tool name
- `result`: Tool execution result (JSON)
- `--transcript-format`: Output format (`json`, `markdown`)

**Exit Codes**:

- `0`: Success
- `1`: Logging failed
- `2`: Transcript processing error

**Features**:

- Execution result logging
- Transcript format conversion
- Performance timing
- Error tracking

### 4. notification.py

**Purpose**: Intelligent notifications with TTS provider fallback.

**Parameters**:

- `message`: Notification message
- `--tts-provider`: Force specific provider (`elevenlabs`, `openai`, `pyttsx3`)
- `--voice`: Voice selection (provider-specific)
- `--no-audio`: Disable audio output

**TTS Provider Fallback Logic**: For complete TTS provider configuration and fallback details, see [TTS System Reference](../reference/tts-system.md#fallback-logic).

**Usage Example**:

```bash
echo '{"message": "Task completed successfully"}' | \
  uv run .claude/hooks/notification.py --tts-provider elevenlabs
```

**Features**: For comprehensive TTS features and configuration, see [TTS System Reference](../reference/tts-system.md#system-overview).

### 5. stop.py

**Purpose**: Task completion handling with AI-generated summaries.

**Parameters**:

- `session_data`: Session context (JSON)
- `--summary-style`: Summary format (`concise`, `detailed`, `technical`)
- `--generate-audio`: Create audio summary

**Features**:

- AI-generated completion messages
- Session context integration
- Audio summary generation
- Task outcome classification

### 6. subagent_stop.py

**Purpose**: Subagent completion announcements and handoffs.

**Parameters**:

- `subagent_name`: Name of completed subagent
- `subagent_result`: Result data from subagent
- `--handoff-mode`: Next action (`return`, `continue`, `delegate`)

**Features**:

- Subagent result processing
- Context handoff management
- Multi-agent workflow coordination

### 7. pre_compact.py

**Purpose**: Transcript backup before conversation compaction.

**Parameters**:

- `transcript_data`: Full conversation transcript
- `--backup-location`: Storage location (`local`, `cloud`)
- `--compression`: Backup compression (`none`, `gzip`, `lz4`)

**Features**:

- Automatic transcript archiving
- Configurable backup strategies
- Compression and storage optimization
- Recovery procedures

### 8. session_start.py

**Purpose**: Development context loading and session initialization.

**Parameters**:

- `project_path`: Current project directory
- `--context-level`: Context depth (`minimal`, `standard`, `comprehensive`)
- `--load-history`: Load previous session data

**Features**:

- Project context detection
- Git integration and status loading
- Previous session restoration
- Development environment setup

## Agent API Reference

The CC-Boilerplate includes 8 specialized agents with distinct capabilities.

### Core Agents

#### 1. meta-agent

**Purpose**: Generates new Claude Code agents from descriptions.

**Tools**: `Write`, `WebFetch`, `mcp__firecrawl-mcp__firecrawl_scrape`, `MultiEdit`

**Usage Pattern**:

```
user: "Create an agent that reviews pull requests for security issues"
assistant: [Uses meta-agent to generate new PR security review agent]
```

**Capabilities**:

- Agent configuration file generation
- Tool selection and optimization
- Best practice integration
- Template customization

#### 2. engineer-code-reviewer

**Purpose**: Automated code quality and security reviews.

**Tools**: Universal access (`*`)

**Review Categories**:

- **Security**: Vulnerability detection, dangerous patterns
- **Quality**: Code style, best practices, maintainability
- **Performance**: Optimization opportunities, bottlenecks
- **Architecture**: Design patterns, structure analysis

**Usage Example**:

```python
# Automatically triggered after code changes
def review_criteria():
    return {
        "security": ["injection", "xss", "auth", "secrets"],
        "quality": ["complexity", "duplication", "naming"],
        "performance": ["algorithms", "memory", "io"]
    }
```

#### 3. work-completion-summary

**Purpose**: Audio task summaries via TTS.

**Tools**: `Bash`, `mcp__ElevenLabs__text_to_speech`, `mcp__ElevenLabs__play_audio`

**Usage Pattern**:

```
user: "tts summary"
assistant: [Generates concise audio summary of completed work]
```

**Features**:

- Context-aware summarization
- Multi-language support
- Voice customization
- Automatic playback

#### 4. llm-ai-agents-and-eng-research

**Purpose**: AI/ML research and trend analysis specialist.

**Tools**: `Bash`, `mcp__firecrawl-mcp__firecrawl_search`, `WebFetch`

**Research Areas**:

- LLM developments and releases
- AI agent architectures
- Engineering best practices
- Technology trend analysis

### Specialized Agents

#### 5. test-automator

**Purpose**: Comprehensive test suite creation and automation.

**Tools**: Universal access (`*`)

**Test Categories**:

```python
test_types = {
    "unit": "Individual component testing",
    "integration": "Component interaction testing",
    "e2e": "End-to-end workflow testing",
    "security": "Security validation testing",
    "performance": "Load and stress testing"
}
```

#### 6. technical-researcher

**Purpose**: In-depth technical research and analysis.

**Tools**: Universal access (`*`)

**Research Capabilities**:

- Framework evaluation and comparison
- Security vulnerability analysis
- Performance optimization strategies
- Architecture decision support

#### 7. test-coverage-analyzer

**Purpose**: Test coverage gap analysis and recommendations.

**Tools**: `Read`, `Grep`, `Glob`, `Bash`, `MultiEdit`

**Analysis Output**:

```python
coverage_report = {
    "current_coverage": "60%",
    "critical_gaps": ["security validation", "error handling"],
    "recommendations": ["Add integration tests", "Improve edge case coverage"]
}
```

#### 8. smart-doc-generator

**Purpose**: Comprehensive documentation generation.

**Tools**: `Read`, `Glob`, `Grep`, `LS`, `Write`, `MultiEdit`

**Documentation Types**:

- API documentation
- Architecture overviews
- User guides and tutorials
- Inline code comments

## Utility API Reference

### TTS Provider System

For comprehensive TTS provider documentation including:

- Individual provider setup and configuration
- Parameter details and usage examples
- Voice selection and customization options
- Performance characteristics and troubleshooting

See [TTS System Reference](../reference/tts-system.md).

### LLM Utility System

#### Anthropic LLM (`anth.py`)

**Capabilities**:

- Claude model integration
- Context management
- Response streaming
- Function calling

#### OpenAI LLM (`oai.py`)

**Capabilities**:

- GPT model integration
- Chat completion
- Function calling
- Token optimization

#### Ollama LLM (`ollama.py`)

**Capabilities**:

- Local model execution
- Custom model support
- Offline operation
- Resource management

## Output Style Reference

### Available Styles

1. **genui** - Beautiful HTML generation with embedded styling
2. **table-based** - Organized markdown tables
3. **tts-summary** - Audio feedback via TTS
4. **yaml-structured** - YAML configuration format
5. **bullet-points** - Clean nested lists
6. **ultra-concise** - Minimal words, maximum speed
7. **html-structured** - Semantic HTML5
8. **markdown-focused** - Rich markdown features

### Style Selection

```json
{
  "style": "tts-summary",
  "parameters": {
    "voice_provider": "elevenlabs",
    "summary_length": "concise",
    "include_audio": true
  }
}
```

## Configuration API

### Settings.json Structure

```json
{
  "hooks": {
    "user_prompt_submit": {"enabled": true, "logging": "info"},
    "pre_tool_use": {"enabled": true, "security_level": "strict"},
    "notification": {"enabled": true, "default_tts": "elevenlabs"}
  },
  "agents": {
    "meta-agent": {"auto_generate": true},
    "engineer-code-reviewer": {"auto_review": false}
  },
  "security": {
    "dangerous_commands": true,
    "env_file_protection": true,
    "path_traversal_check": true
  }
}
```

### Environment Variables

```bash
# TTS Providers
ELEVENLABS_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# LLM Providers
ANTHROPIC_API_KEY=your_key_here
OLLAMA_HOST=http://localhost:11434

# User Configuration
USER_NAME=Neil
TTS_DEFAULT_PROVIDER=elevenlabs
LOG_LEVEL=info
```

## Error Handling

### Common Exit Codes

For detailed exit codes and error handling, see [Hooks API Reference](../reference/hooks-api.md#exit-codes-and-error-handling).

### Error Response Format

```json
{
  "error": true,
  "code": 1,
  "message": "Dangerous command detected",
  "details": {
    "command": "rm -rf /",
    "pattern_matched": "rm.*-rf",
    "safety_level": "critical"
  },
  "timestamp": "2025-01-09T12:00:00Z"
}
```

## Performance Characteristics

### Hook Execution Times

| Hook | Typical Duration | Max Timeout |
|------|------------------|-------------|
| user_prompt_submit | <100ms | 5s |
| pre_tool_use | <200ms | 3s |
| post_tool_use | <150ms | 5s |
| notification | 1-3s | 30s |
| stop | <500ms | 10s |
| subagent_stop | <300ms | 5s |
| pre_compact | 1-5s | 60s |
| session_start | <1s | 10s |

### TTS Provider Performance

| Provider | Latency | Quality | Offline |
|----------|---------|---------|---------|
| ElevenLabs | 2-5s | Excellent | No |
| OpenAI | 1-3s | Very Good | No |
| pyttsx3 | <1s | Good | Yes |

## Security Considerations

### Critical Security Features

1. **Dangerous Command Detection**: Prevents destructive rm operations
2. **Environment Protection**: Blocks .env file access attempts
3. **Path Traversal Prevention**: Validates file path access
4. **Input Sanitization**: Cleanses user input for security
5. **API Key Protection**: Prevents accidental key exposure

### Security Best Practices

For comprehensive security configuration and best practices, see [Security Guide](../guides/security.md).

This API reference provides complete documentation for integrating and extending the CC-Boilerplate system while maintaining security and reliability.
