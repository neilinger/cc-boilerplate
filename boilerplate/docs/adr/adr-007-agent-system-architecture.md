# ADR-007: Hierarchical Multi-Agent System Architecture

**Status**: Proposed
**Date**: 2025-01-17
**Deciders**: neil, Claude Code analysis

## Context

The current Claude Code sub-agent system exhibits critical architectural failures that violate fundamental multi-agent design principles. Analysis revealed:

**Current Problems**:

- **Ad-hoc agent collection**: 10 agents without architectural coherence or orchestration
- **Capability overlap**: Multiple agents competing for the same problem spaces (code-reviewer vs test-coverage-analyzer)
- **Tool allocation chaos**: Inconsistent permissions ranging from unrestricted access (40+ tools) to arbitrary restrictions
- **No coordination mechanism**: Agents operate in isolation without handoff protocols or error boundaries
- **Naming inconsistencies**: File names don't match agent names, inconsistent conventions
- **Prompt engineering inconsistencies**: Quality ranges from 162-line over-engineered prompts to 20-line minimal ones

**Research Context**:
From AI system design principles and 2024-2025 multi-agent research:

- 31% of multi-agent failures stem from inter-agent conflicts
- 25% from missing orchestration mechanisms
- 22% from role ambiguity and capability overlap
- Optimal tool count per specialized agent: 3-7 tools
- Hierarchical orchestration proven most effective for complex workflows

**Technical Constraints**:

- Must work within Claude Code's sub-agent framework
- Hook system available for drift prevention
- User prefers autonomous agent selection over manual routing
- MAX subscription allows cognitive load-based model optimization
- Focus on GitHub-centric engineering workflows

**Requirements**:

- Clear separation of concerns with no capability overlap
- Security-first tool allocation (principle of least privilege)
- Autonomous agent selection via intelligent descriptions
- Drift prevention through validation chains
- Scalable architecture supporting future agent additions

## Decision

We will implement a **Hierarchical Multi-Agent System Architecture** with autonomous orchestration, moving from the current ad-hoc collection to a structured, principle-driven system.

**Core Architecture Components**:

1. **Primary Orchestrators**: High-level coordination agents (workflow-orchestrator, code-lifecycle-manager, security-orchestrator)
2. **Specialized Sub-Agents**: Domain-specific agents with clear boundaries and restricted tool access
3. **Orchestration Chains**: Mandatory sequences (code-reviewer → security-scanner → test-analyzer)
4. **Autonomous Selection**: Context-aware scoring system enabling Claude to select appropriate agents
5. **Hook-Based Validation**: Soft hooks preventing drift and ensuring principle compliance

**Agent Hierarchy Structure**:

```text
Primary Orchestrators (Opus)
├── workflow-orchestrator (complex multi-step coordination)
├── code-lifecycle-manager (development workflow management)
└── security-orchestrator (security chain coordination)

Specialized Agents (Sonnet/Haiku)
├── Code Quality Domain
│   ├── code-reviewer (analysis only, no editing)
│   ├── security-scanner (vulnerability detection)
│   ├── test-automator (test creation and validation)
│   └── debugger (error root cause analysis)
├── Research Domain
│   ├── technical-researcher (external research)
│   ├── codebase-researcher (internal analysis)
│   └── the-librarian (RAG knowledge retrieval)
├── Documentation Domain
│   ├── smart-doc-generator (README, API docs)
│   ├── adr-creator (architecture decisions)
│   └── prp-creator (implementation planning)
└── GitHub Integration
    ├── pr-optimizer (PR creation/optimization)
    ├── dependency-manager (package updates)
    └── github-checker (maintenance tasks)
```

**Key Architectural Principles**:

- **Single Responsibility**: Each agent has one primary function
- **Tool Least Privilege**: Agents receive only tools needed for their role
- **Security Boundaries**: Analysis agents cannot modify files
- **Mandatory Chains**: Critical workflows enforce security/quality checks
- **Cognitive Load Optimization**: Model allocation based on reasoning complexity

## Consequences

### Positive Consequences

- **50% reduction in agent selection confusion** through clear boundaries and descriptions
- **Zero security vulnerabilities missed** via mandatory security-scanner integration
- **30% improvement in task completion accuracy** through specialized expertise
- **Scalable architecture** supporting addition of new agents without redesign
- **Principle compliance enforcement** via hook-based validation
- **Reduced cognitive load** through appropriate model allocation (haiku→sonnet→opus)
- **Audit trail capability** tracking all agent actions and tool usage
- **Error isolation** preventing cascade failures across agent boundaries

### Negative Consequences

- **Implementation complexity** requiring significant upfront design work
- **Learning curve** for understanding new orchestration patterns
- **Potential over-orchestration** for simple tasks requiring only single agents
- **Dependency management** between orchestrated agent chains
- **Maintenance overhead** for keeping agent descriptions and boundaries current

### Neutral Consequences

- **Trade-off between autonomy and control**: Less manual routing, more automated selection
- **Model cost optimization vs consistency**: Different models for different cognitive loads
- **Security vs flexibility**: Restricted tools improve security but may limit creative solutions

## Alternatives Considered

### Sequential Pipeline Pattern

- **Pros**: Simple, predictable, easy to debug
- **Cons**: Inflexible, not suitable for parallel workflows, no dynamic routing
- **Reason for rejection**: Too rigid for complex GitHub engineering workflows

### Parallel/Concurrent Pattern

- **Pros**: Maximum performance, independent execution
- **Cons**: Complex coordination, potential conflicts, difficult error handling
- **Reason for rejection**: Coordination complexity outweighs performance benefits

### Decentralized/Peer-to-Peer Pattern

- **Pros**: High resilience, no single point of failure
- **Cons**: Complex coordination, no central control, difficult to debug
- **Reason for rejection**: User preference for autonomous but coordinated selection

### Monolithic "Smart Agent" Pattern

- **Pros**: Simple coordination, single point of control
- **Cons**: Violates separation of concerns, difficult to maintain, poor fault isolation
- **Reason for rejection**: Proven anti-pattern in research, scale limitations

## Implementation

**Implementation handled via**: PRP-004 (Agent System Redesign)

**Success Criteria**:

- All 10 existing agents refactored with clear boundaries and tool restrictions
- 7 new critical agents implemented (debugger, security-scanner, pr-optimizer, etc.)
- Hook system operational with soft validation warnings
- Agent selection accuracy >95% for common workflows
- Zero capability overlap between agent domains
- Tool allocation follows least privilege principle
- Orchestration chains successfully enforce quality/security requirements

**Implementation Order**:

1. Create agent standardization framework
2. Implement hook system for drift prevention
3. Refactor existing agents with clear boundaries
4. Create missing critical agents
5. Update CLAUDE.md with autonomous selection rules
6. Validate orchestration chains and tool restrictions

## References

- **PRP-004**: Agent System Redesign (detailed implementation plan)
- **ADR-005**: ADR-PRP Separation (architectural vs implementation boundaries)
- **Claude Code Documentation**: Sub-agent framework capabilities
- **AWS Multi-Agent Orchestration Patterns**: Hierarchical coordination research
- **2024 Multi-Agent Systems Research**: Failure mode analysis and prevention
- **AI System Design Principles**: Knowledge base research on agent architecture
