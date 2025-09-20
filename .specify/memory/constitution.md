# CC-Boilerplate Constitution

## Core Principles

### I. KISS/YAGNI Supremacy (NON-NEGOTIABLE)
**KISS – Keep It Simple, Stupid**: Use the easiest way that works. Fewer parts. Short words. Short functions. If you can't explain code in one breath, simplify it.

**YAGNI – You Aren't Gonna Need It**: Don't build extra stuff "just in case." Build it only when someone actually needs it now. Kill all "nice to have" features.

**Validation Protocol**: Every step must be challenged against KISS/YAGNI with 95%+ certainty. Being "nice" by not challenging ideas wastes time and money.

### II. Security-First Architecture (MANDATORY)
**Hierarchical Security Boundaries**: All security-sensitive code changes must follow the mandatory security chain: code-reviewer → security-orchestrator → security-scanner.

**Tool Least Privilege**: Agents receive only tools needed for their role. Security violations are blocked and escalated. The security chain is NON-NEGOTIABLE for code safety.

**Protection Systems**: 30+ rm patterns blocked, environment protection, real-time validation before every tool execution.

### III. Hierarchical Agent Orchestration (ADR-007)
**Autonomous Agent Selection**: Use workflow-orchestrator for complex multi-step tasks, domain specialists for focused work, analyzers for read-only analysis.

**Cognitive Load Optimization**: Model allocation based on reasoning complexity (Haiku→Sonnet→Opus) following ADR-008 principles.

**Mandatory Orchestration**: Tasks involving 3+ distinct steps require workflow-orchestrator coordination. No manual routing for complex workflows.

### IV. Validation-Driven Development
**Harsh Validation is Kindness**: Challenge every complexity against value add. Show certainty percentage - kill anything <95% certain.

**Sequential Thinking**: Use sequential thinking to challenge every step against KISS/YAGNI. Reason every step explicitly.

**PRP Structure**: When requests lack clear scope, suggest PRP structure to prevent scope creep.

### V. Architecture Compliance (ADR-007/008)
**Agent Boundaries**: Single responsibility per agent, clear tool restrictions, mandatory security chains, no capability overlap.

**Principle Compliance**: Run `./.claude/hooks/check-agents.sh` to validate architecture compliance. Tool allocation follows least privilege principle.

**Documentation Standards**: ADRs for architectural decisions (WHY/WHAT), PRPs for implementation planning (HOW/WHEN). Keep them separate.

## Security Requirements

**Tool Restrictions**: Analyzers are read-only and cannot modify files. Specialists have domain-restricted tools only. Orchestrators have full coordination capabilities.

**Command Protection**: Comprehensive rm -rf protection, environment variable access blocking, dangerous command detection with real-time validation.

**Security Levels**: Three levels (strict, moderate, permissive) with configurable protection based on project needs.

## Development Workflow

**Agent Selection Protocol**: Follow the decision tree in CLAUDE.md exactly. Security-critical operations require mandatory security chain. Complex multi-step tasks use workflow-orchestrator.

**Implementation Process**:
1. Say the goal in one short sentence
2. Pick the simplest path
3. Make a tiny plan (3 steps max)
4. Build the smallest piece that solves today's need
5. Test with one tiny example
6. Show the result and test
7. Stop - don't add features unless asked

**Quality Gates**: TTS notification system, session management hooks, GitHub Claude review integration with comprehensive validation options.

## Governance

**Constitutional Supremacy**: This constitution supersedes all other practices. Amendments require documentation in ADR format with approval and migration plan.

**Compliance Verification**: All PRs/reviews must verify compliance with KISS/YAGNI principles, agent architecture boundaries, and security requirements.

**Drift Prevention**: Hook-based validation prevents drift through soft warnings. Agent descriptions and boundaries must stay current with architecture compliance.

**Development Guidance**: Use CLAUDE.md for runtime development guidance. This constitution provides the immutable foundation; CLAUDE.md provides tactical implementation details.

**Version**: 1.0.0 | **Ratified**: 2025-01-19 | **Last Amended**: 2025-01-19