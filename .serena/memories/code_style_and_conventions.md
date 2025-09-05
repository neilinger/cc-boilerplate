# Code Style and Conventions

## Core Principles (from CLAUDE.md)
- **KISS (Keep It Simple, Stupid)**: Use the easiest way that works. Fewer parts. Short words. Short functions.
- **YAGNI (You Aren't Gonna Need It)**: Don't build extra stuff "just in case." Build it only when someone actually needs it now.

## Design Rules
- One function = one job. Keep it short and clear.
- Prefer simple data (numbers, strings, lists, dicts) over fancy patterns.
- Name things so a child can guess what they do.
- Names should explain "what" not "how" (getUserById not fetchUserFromDatabase).
- Avoid clever tricks. Clear beats clever.
- No general frameworks, layers, or abstractions until they're truly needed.

## Python Conventions
- Uses UV script headers with embedded dependencies
- Type hints not consistently used but should be added
- Error handling with graceful degradation (silent failures for non-critical operations)
- JSON for data persistence and logging
- Pathlib for file operations
- Subprocess for external tool execution

## File Organization
- `.claude/hooks/` - Hook implementations as UV single-file scripts
- `.claude/agents/` - Sub-agent configurations (YAML frontmatter + markdown)
- `.claude/output-styles/` - Response formatting configurations
- `.claude/status_lines/` - Terminal status displays
- `logs/` - JSON logs of all hook executions