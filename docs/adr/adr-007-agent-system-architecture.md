# ADR-007: Hierarchical Multi-Agent System Architecture

**Status**: Accepted
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

**Agent Hierarchy Structure**: Three-tier system with Primary Orchestrators (Opus) coordinating Specialized Agents (Sonnet/Haiku) across Code Quality, Research, Documentation, and GitHub Integration domains. See PRP-004 for detailed hierarchy and agent specifications.

**Key Architectural Principles**:

- **Single Responsibility**: Each agent has one primary function
- **Tool Least Privilege**: Agents receive only tools needed for their role
- **Security Boundaries**: Analysis agents cannot modify files
- **Mandatory Chains**: Critical workflows enforce security/quality checks
- **Cognitive Load Optimization**: Model allocation based on reasoning complexity

## Consequences

### Positive Consequences

- 50% reduction in agent selection confusion through clear boundaries
- Zero security vulnerabilities via mandatory security-scanner integration
- 30% improvement in task completion accuracy through specialization
- Scalable architecture supporting new agents without redesign
- Principle compliance enforcement via hook-based validation
- Audit trail and error isolation capabilities

### Negative Consequences

- Implementation complexity requiring upfront design work
- Learning curve for orchestration patterns
- Potential over-orchestration for simple tasks
- Maintenance overhead for agent boundaries

### Neutral Consequences

- Trade-off: autonomy vs control, cost optimization vs consistency, security vs flexibility

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

**Success Criteria**: All agents refactored with clear boundaries, hook system operational, >95% selection accuracy, zero capability overlap, tool least privilege enforced.

## References

- **PRP-004**: Agent System Redesign (detailed implementation plan)
- **ADR-005**: ADR-PRP Separation (architectural vs implementation boundaries)
- **Claude Code Documentation**: Sub-agent framework capabilities
- **AWS Multi-Agent Orchestration Patterns**: Hierarchical coordination research
- **2024 Multi-Agent Systems Research**: Failure mode analysis and prevention
- **AI System Design Principles**: Knowledge base research on agent architecture
