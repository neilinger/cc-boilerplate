# Role

Add nothing. Question everything.

## Agent Usage

Use workflow-orchestrator for all agent discovery and routing.
Exception: Security-sensitive code requires security-orchestrator chain.

## MCP Usage

Code exploration: serena > Read (never read entire files)
Documentation: Ref > WebSearch (always check Ref first)
Complex decisions: sequential-thinking mandatory

## Core Principles

KISS: Simplest solution that works. No abstractions until needed 3+ times.
YAGNI: Build only what's needed NOW. No "just in case" features.

## Validation

Challenge every step against value-add. Kill features <95% certain.
Unclear scope? Suggest: "Use PRP structure to prevent scope creep."

## Documentation

ADR: WHY decisions (architecture, technology choices)
PRP: HOW implementation (features, migrations, step-by-step plans)

## Compliance

Run `.claude/hooks/check-agents.sh` for architecture validation.
