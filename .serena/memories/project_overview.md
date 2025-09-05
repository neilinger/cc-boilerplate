# Project Overview: Claude Code Hooks Mastery

## Purpose
This is a comprehensive demonstration project for Claude Code hooks - showing how to add deterministic control over Claude Code's behavior through all 8 hook lifecycle events. It teaches mastery of Claude Code hooks, sub-agents, and advanced features.

## Tech Stack
- **Primary Language**: Python 3.11+
- **Dependency Management**: UV (Astral) single-file scripts
- **Hook Architecture**: UV single-file scripts with embedded dependencies
- **Integration**: Claude Code CLI, ElevenLabs TTS, MCP servers

## Key Features
- Complete hook lifecycle coverage (all 8 events)
- Intelligent TTS system with fallback providers
- Security enhancements and command validation
- Sub-agent configurations and meta-agent
- Custom output styles and status lines
- Session management and agent naming
- Audio feedback and completion summaries

## Architecture Benefits
- **Isolation**: Hook logic separate from main project
- **Portability**: Self-contained scripts with inline dependencies
- **No Virtual Environment Management**: UV handles dependencies automatically
- **Fast Execution**: UV's lightning-fast dependency resolution