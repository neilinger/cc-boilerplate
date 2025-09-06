# CC-Boilerplate

[![CI/CD Status](https://github.com/USERNAME/cc-boilerplate/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/USERNAME/cc-boilerplate/actions/workflows/ci-cd.yml)
[![Security Tests](https://img.shields.io/badge/security-passing-brightgreen)](https://github.com/USERNAME/cc-boilerplate/actions)
[![Test Coverage](https://img.shields.io/badge/coverage-60%25-yellow)](https://github.com/USERNAME/cc-boilerplate/actions)
[![Hooks](https://img.shields.io/badge/hooks-8-blue)](#-all-8-claude-code-hooks)
[![Agents](https://img.shields.io/badge/agents-4-purple)](#-essential-agents)
[![Output Styles](https://img.shields.io/badge/styles-8-orange)](#-8-output-styles)
[![Release](https://img.shields.io/github/v/release/USERNAME/cc-boilerplate?include_prereleases)](https://github.com/USERNAME/cc-boilerplate/releases)

Claude Code boilerplate with hooks, agents, and output styles pre-configured for rapid project setup.

## Prerequisites

- **[Astral UV](https://docs.astral.sh/uv/)** - Python package manager
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** - AI coding assistant

## Quick Start

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

## What's Included

### 🪝 All 8 Claude Code Hooks
- **UserPromptSubmit** - Pre-process prompts, logging, validation
- **PreToolUse** - Security validation (blocks `rm -rf`, `.env` access)  
- **PostToolUse** - Post-execution logging and transcript conversion
- **Notification** - Custom notifications with optional TTS
- **Stop** - Completion handling with AI-generated messages
- **SubagentStop** - Subagent completion announcements
- **PreCompact** - Transcript backup before compaction
- **SessionStart** - Development context loading

### 🤖 Essential Agents
- **meta-agent** - Generate new agents from descriptions
- **engineer-code-reviewer** - Automated code quality checks  
- **work-completion-summary** - Audio task summaries via TTS
- **llm-ai-agents-and-eng-research** - AI/LLM research specialist

### 🎨 8 Output Styles
- **genui** - Beautiful HTML generation with embedded styling
- **table-based** - Organized markdown tables  
- **tts-summary** - Audio feedback via ElevenLabs TTS
- **yaml-structured** - YAML configuration format
- **bullet-points** - Clean nested lists
- **ultra-concise** - Minimal words, maximum speed
- **html-structured** - Semantic HTML5
- **markdown-focused** - Rich markdown features

### 📊 4 Dynamic Status Lines  
Real-time terminal displays with session context, git info, and agent names.

## Project Structure

```
cc-boilerplate/
├── .claude/
│   ├── agents/         # 4 essential agents
│   ├── hooks/          # All 8 hooks + utilities
│   ├── output-styles/  # 8 response formatting styles
│   ├── status_lines/   # 4 dynamic status displays
│   └── settings.json   # Hook and permission configuration
├── logs/               # Hook execution logs (JSON)
├── output/             # Generated files output
├── .env.sample         # Configuration template
├── .mcp.json.sample    # MCP server template  
├── CLAUDE.md           # KISS/YAGNI development principles
└── setup.sh            # Project setup script
```

## Key Features

- **Security-First** - Comprehensive command validation and blocking
- **Intelligent TTS** - Multi-provider audio feedback (ElevenLabs → OpenAI → pyttsx3)  
- **Session Management** - Agent naming and context persistence
- **UV Single-File Scripts** - Self-contained hooks with embedded dependencies
- **Zero Dependencies** - No virtual environment management needed

## 🛡️ Security Features

CC-Boilerplate implements **production-grade security** with multi-layered protection:

### Dangerous Command Protection
- **30+ rm patterns** detected and blocked (prevents `rm -rf /` disasters)
- **Path traversal prevention** blocks access to system files
- **Command injection filtering** prevents malicious command chains
- **Real-time validation** before every tool execution

### Environment Protection
- **.env file access blocking** prevents accidental API key exposure
- **Sensitive data protection** with pattern-based detection
- **Audit logging** of all security events and blocks

### Security Levels
- **Strict** (Production): Maximum protection, blocks all dangerous patterns
- **Moderate** (Development): Balanced protection with warnings
- **Permissive** (Testing): Warnings only for development freedom

```bash
# Example: This command would be BLOCKED by safety hooks
user: "Clean up the system with rm -rf /"
claude: 🚫 BLOCKED - Dangerous command detected by safety hooks
```

## 🔊 TTS System Architecture

**Multi-Provider Intelligence** with automatic fallback ensures audio is always available:

### Provider Hierarchy
1. **ElevenLabs** (Premium) - Professional AI voices, 29 languages, custom training
2. **OpenAI** (High Quality) - Fast API, 6 voices, excellent reliability  
3. **pyttsx3** (Local Fallback) - System TTS, offline, always available

### Smart Fallback Logic
```
ElevenLabs API → Network Error → OpenAI API → Success ✅
OpenAI API → Invalid Key → pyttsx3 Local → Success ✅
All Providers → Unavailable → Silent Mode → Continue
```

### Configuration
```bash
# .env configuration
TTS_DEFAULT_PROVIDER=elevenlabs
ELEVENLABS_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

## 🤖 Agent System

**8 Specialized Agents** enhance Claude Code with domain expertise:

### Meta-System Agents
- **meta-agent**: Generate new agents from descriptions
- **test-automator**: Create comprehensive test suites automatically
- **test-coverage-analyzer**: Analyze gaps and improve coverage

### Code Quality Agents  
- **engineer-code-reviewer**: Automated security and quality reviews
- **technical-researcher**: Deep technical research and analysis

### Documentation & Communication
- **smart-doc-generator**: Generate comprehensive documentation
- **work-completion-summary**: Audio task summaries with TTS
- **llm-ai-agents-and-eng-research**: AI/ML research specialist

### Usage Examples
```
user: "Create tests for my authentication system"
claude: [Uses test-automator agent to generate comprehensive test suite]

user: "Review this code for security vulnerabilities"  
claude: [Uses engineer-code-reviewer for security analysis]

user: "Generate full documentation for this project"
claude: [Uses smart-doc-generator for complete documentation]
```

## 📊 Testing & Quality Assurance

**Priority-Based Testing** with 60% coverage across critical components:

### Test Categories
- **🔴 High Priority (Security Critical)**: Safety hooks, dangerous command detection
- **🟡 Medium Priority (Feature Reliability)**: TTS providers, integration testing
- **🟢 Low Priority (Extended Validation)**: Performance, edge cases

### CI/CD Pipeline
- **Feature branches**: Fast security validation (~30s)
- **Release branches**: Comprehensive testing (~5-7min)  
- **Main branch**: Full validation + deployment (~3-5min)

### Running Tests
```bash
# Run all tests with reporting
python tests/run_all_tests.py

# Run security-critical tests only
python tests/test_safety_hooks.py

# Run TTS integration tests
python tests/test_tts_providers.py
```

## 📚 Comprehensive Documentation

**Professional Documentation Suite** following industry best practices:

### User Documentation
- **[Getting Started](docs/GETTING_STARTED.md)** - Complete setup guide
- **[API Reference](docs/API.md)** - Comprehensive API documentation
- **[TTS System](docs/TTS_SYSTEM.md)** - TTS provider configuration and usage

### Security & Architecture
- **[Security Guide](docs/SECURITY.md)** - Threat model and protection details
- **[Architecture](docs/ARCHITECTURE.md)** - System design and component relationships  
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Problem resolution guide

### Development
- **[Development Workflow](docs/DEVELOPMENT.md)** - Day-to-day development process
- **[Branch Protection](docs/BRANCH_PROTECTION.md)** - GitHub setup instructions
- **[ADR Documentation](docs/adr/)** - Architecture Decision Records

## Customization

- **Add new hooks**: Place in `.claude/hooks/`
- **Create agents**: Use `/agents` command or meta-agent  
- **Define output styles**: Add to `.claude/output-styles/`
- **Configure permissions**: Edit `.claude/settings.json`

## Development Principles  

See **`CLAUDE.md`** for KISS/YAGNI principles that guide this project's architecture.

## Next Steps

1. Review and customize `.env` configuration
2. Explore the pre-configured hooks and agents
3. Start building your project with Claude Code's enhanced capabilities
4. Use the meta-agent to create specialized agents for your domain