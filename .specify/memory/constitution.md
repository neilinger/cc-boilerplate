<!--
Sync Impact Report - Constitution Update
========================================
Version change: 1.1.0 → 1.2.0
Modified principles:
- Added V. Test-Driven Development (TDD) - New principle from CLAUDE.md workflow
- Enhanced IV. Validation-Driven Development - Added PRP structure requirement
- Enhanced Development Workflow - Strengthened TDD implementation process
- Added ADR/PRP separation guidance from ADR-005
Added sections:
- Test-Driven Development principle
- ADR vs PRP Guidelines section
- Design Rules section from CLAUDE.md
Removed sections: None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md (Constitution Check aligns)
- ✅ .specify/templates/spec-template.md (No changes needed)
- ✅ .specify/templates/tasks-template.md (TDD ordering already implemented)
Follow-up TODOs: None
-->

# CC-Boilerplate Constitution

## Core Principles

### I. KISS/YAGNI Supremacy (NON-NEGOTIABLE)

**KISS – Keep It Simple, Stupid**: Use the easiest way that works. Fewer parts. Short words. Short functions. If you can't explain code in one breath, simplify it.

**YAGNI – You Aren't Gonna Need It**: Don't build extra stuff "just in case." Build it only when someone actually needs it now. Kill all "nice to have" features.

**Validation Protocol**: Every step must be challenged against KISS/YAGNI with 95%+ certainty. Being "nice" by not challenging ideas wastes time and money.

**Design Rules (think like toy blocks)**:
- One function = one job. Keep it short and clear.
- Prefer simple data (numbers, strings, lists, dicts) over fancy patterns.
- Name things so a child can guess what they do.
- Avoid clever tricks. Clear beats clever.
- No general frameworks, layers, or abstractions until they're truly needed.

### II. Security-First Architecture (MANDATORY)

**Hierarchical Security Boundaries**: All security-sensitive code changes must follow the mandatory security chain: code-reviewer → security-orchestrator → security-scanner.

**Tool Least Privilege**: Agents receive only tools needed for their role. Security violations are blocked and escalated. The security chain is NON-NEGOTIABLE for code safety.

**Protection Systems**: 30+ rm patterns blocked, environment protection, real-time validation before every tool execution.

### III. Hierarchical Agent Orchestration (ADR-007)

**Dynamic Agent Discovery Protocol**: This project has 100+ specialized agents. DO NOT rely on static lists. Use workflow-orchestrator IMMEDIATELY for agent discovery. The orchestrator dynamically scans and selects from ALL available agents.

**Mandatory Orchestration Rules**:

- Complex multi-step tasks (3+ steps) MUST use workflow-orchestrator
- Feature implementations requiring multiple domains MUST use orchestration
- Cross-cutting concerns spanning multiple agents MUST use coordination
- When uncertain about agent selection, invoke workflow-orchestrator for dynamic discovery

**Cognitive Load Optimization (ADR-008)**: Model allocation based on reasoning complexity following three-tier system:
- **Haiku**: Simple tasks, ≤3 tools, low cognitive load (github-checker, work-completion-summary)
- **Sonnet**: Standard complexity, 4-7 tools, medium cognitive load (most specialists/analyzers)
- **Opus**: High complexity, orchestration, coordination tasks (workflow-orchestrator, meta-agent)

**Agent Boundaries Enforcement**:
- Analyzers: Read-only, cannot modify files, hand off to action agents
- Specialists: Domain-restricted tools only, single responsibility
- Orchestrators: Full coordination capabilities, coordinate but don't execute
- Meta-agent: Creates new agents but hands off to workflow-orchestrator

### IV. Validation-Driven Development

**Harsh Validation is Kindness**: Challenge every complexity against value add. Show certainty percentage - kill anything <95% certain.

**Sequential Thinking**: Use sequential thinking to challenge every step against KISS/YAGNI. Reason every step explicitly.

**PRP Structure**: When requests lack clear scope, suggest PRP structure to prevent scope creep. Use workflow-orchestrator or direct planning for clarification.

### V. Test-Driven Development (TDD)

**Tests Before Implementation**: Write the test that will verify achievement of the goal BEFORE writing implementation code. Tests must fail initially to prove they work.

**Red-Green-Refactor Cycle**:
1. Write failing test (RED)
2. Write minimal code to pass (GREEN)
3. Refactor while keeping tests green (REFACTOR)

**TDD Enforcement**: Tasks template MUST order tests before implementation. Contract tests generated before endpoints. All entities require model tests before business logic.

**Coverage Requirements**: All critical paths must have test coverage. Use test-coverage-analyzer for gap identification.

## ADR vs PRP Guidelines

### When to use ADR (Architecture Decision Record)

- Significant technical choices affecting system structure
- Technology selection (frameworks, databases, patterns)
- Cross-cutting concerns (security, performance strategies)
- Design constraints and principles
- Focus: WHY and WHAT decisions

### When to use PRP (Product Requirements Process)

- Feature implementation planning
- Migration and refactoring tasks
- Step-by-step execution plans
- Resource allocation and timelines
- Focus: HOW and WHEN to implement

### MANDATORY: Keep them separate

- ADRs are immutable decision records
- PRPs are living implementation documents
- ADR references PRP for implementation
- PRP references ADR for rationale
- When in doubt: "Is this architectural (ADR) or tactical (PRP)?"

## Security Requirements

**Tool Restrictions**: Analyzers are read-only and cannot modify files. Specialists have domain-restricted tools only. Orchestrators have full coordination capabilities.

**Command Protection**: Comprehensive rm -rf protection, environment variable access blocking, dangerous command detection with real-time validation.

**Security Levels**: Three levels (strict, moderate, permissive) with configurable protection based on project needs.

## Development Workflow

**Critical Agent Selection Failures to Avoid**:
- Documentation request → NOT using smart-doc-generator
- Code review request → NOT using code-reviewer
- Test creation → NOT using test-automator
- Complex feature → NOT using workflow-orchestrator
- Security code → NOT using mandatory security chain
- Architecture decision → NOT using adr-creator
- Technical research → NOT using technical-researcher
- Multi-step workflow → Trying to do manually instead of orchestration

**Implementation Process**:

1. Say the goal in one short sentence
2. Write the test that will verify achievement of this goal
3. Pick the simplest path
4. Make a tiny plan (3 steps max)
5. Build the smallest piece that solves today's need
6. Test with one tiny example
7. Show the result and test
8. Stop - don't add features unless asked

**Quality Gates**: TTS notification system, session management hooks, GitHub Claude review integration with comprehensive validation options.

## Governance

**Constitutional Supremacy**: This constitution supersedes all other practices. Amendments require documentation in ADR format with approval and migration plan.

**Compliance Verification**: All PRs/reviews must verify compliance with KISS/YAGNI principles, agent architecture boundaries, security requirements, and TDD practices.

**Drift Prevention**: Hook-based validation prevents drift through soft warnings. Agent descriptions and boundaries must stay current with architecture compliance.

**Development Guidance**: Use CLAUDE.md for runtime development guidance. This constitution provides the immutable foundation; CLAUDE.md provides tactical implementation details.

**Version**: 1.2.0 | **Ratified**: 2025-01-19 | **Last Amended**: 2025-01-20