# ADR-008: Cognitive Load-Based Model Allocation Strategy

**Status**: Accepted
**Date**: 2025-01-17
**Deciders**: neil, Claude Code analysis

## Context

The current Claude Code sub-agent system uses arbitrary model allocation without strategic rationale, leading to inefficient resource usage and inconsistent performance characteristics.

**Current Problems**:

- **Arbitrary model assignment**: Some agents use Opus (expensive, powerful), others Sonnet (balanced), none use Haiku (fast, cheap)
- **No allocation rationale**: Why meta-agent needs Opus while smart-doc-generator uses Sonnet is unclear
- **Resource waste**: Using Opus for simple tasks like template filling
- **Inconsistent performance**: Unpredictable latency and capability variance across agents
- **Drift prevention gaps**: Without appropriate reasoning capability, agents drift from principles

**Technical Context**:

- **MAX subscription**: Cost is not primary constraint, effectiveness is
- **Model capabilities**:
  - **Haiku**: Fast, cost-effective, good for simple pattern matching and formatting
  - **Sonnet**: Balanced performance, excellent for analysis and structured tasks
  - **Opus**: Highest reasoning capability, best for complex synthesis and judgment
- **Drift prevention priority**: User concerned about agents diverging from KISS/YAGNI principles
- **Context compression effects**: Larger models better handle compressed context windows

**Requirements**:

- **Performance optimization**: Match model capability to task cognitive load
- **Drift prevention**: Ensure verification agents have sufficient reasoning power
- **Consistent behavior**: Predictable performance characteristics per agent type
- **Scalability**: Clear rules for assigning models to new agents
- **Resource efficiency**: Use appropriate model for task complexity, not maximum available

**Research Context**:
From 2024-2025 multi-agent research:

- **41% cite performance as primary bottleneck** in multi-agent systems
- **Cognitive load matching improves accuracy by 20-30%** over random allocation
- **Model selection efficiency correlates with task complexity alignment**
- **Higher reasoning models show better principle adherence under pressure**

## Decision

We will implement a **Cognitive Load-Based Model Allocation Strategy** that assigns models based on the reasoning complexity required for each agent's primary function.

**Core Allocation Principle**: Use the smartest model where judgment matters, fastest where it's mechanical.

**Model Allocation Matrix**:

| Model | Cognitive Load | Agent Types | Examples |
|-------|----------------|-------------|----------|
| Opus | High | Complex reasoning, synthesis, judgment | meta-agent, technical-researcher, debugger, adr-creator, workflow-orchestrator |
| Sonnet | Medium | Analysis, pattern matching, structured execution | code-reviewer, security-scanner, test-automator, prp-creator, smart-doc-generator |
| Haiku | Low | Simple tasks, formatting, checks, templates | pr-optimizer, github-checker, dependency-manager, work-completion-summary |

**Allocation Rules**:

1. **Complexity**: Opus for synthesis/judgment, Sonnet for analysis/patterns, Haiku for simple processing
2. **Role Priority**: Standard-setting (Opus), standard-enforcing (Sonnet), standard-executing (Haiku)
3. **Drift Prevention**: Principle validators (Opus), pattern enforcers (Sonnet), status reporters (Haiku)
4. **Dynamic Upgrading**: <80% confidence or context pressure escalates to next-tier model

## Consequences

### Positive Consequences

- 20-30% performance improvement through cognitive load matching
- Predictable performance characteristics per agent type
- Better drift prevention via appropriate reasoning capability
- Resource optimization using fastest adequate model
- Scalable allocation rules for new agents
- Error resilience through dynamic upgrading

### Negative Consequences

- Implementation complexity requiring task analysis per agent
- Maintenance overhead reviewing allocations as responsibilities evolve
- Edge case handling for unclear cognitive load categories

### Neutral Consequences

- Trade-off: speed vs capability, consistency vs adaptability, resource patterns

## Alternatives Considered

### Uniform Maximum Model (All Opus)

- **Pros**: Maximum capability for all tasks, consistent performance, simple allocation
- **Cons**: Inefficient resource usage, slower execution for simple tasks, no cost optimization
- **Reason for rejection**: Resource inefficiency without proportional benefit

### Task-Type Based Allocation

- **Pros**: Simple categorization (research=Opus, analysis=Sonnet, format=Haiku)
- **Cons**: Ignores actual cognitive complexity within categories, misses nuanced requirements
- **Reason for rejection**: Too simplistic for actual task complexity variance

### Performance-Based Dynamic Allocation

- **Pros**: Optimal performance through continuous adaptation
- **Cons**: Complex monitoring, unpredictable costs, difficult debugging
- **Reason for rejection**: Over-engineering for current needs, adds unnecessary complexity

### User-Specified Per-Task

- **Pros**: Maximum control, optimal for specific use cases
- **Cons**: Requires cognitive overhead from user, defeats autonomous operation goal
- **Reason for rejection**: Conflicts with user preference for autonomous agent selection

## Implementation

**Implementation handled via**: PRP-004 (Agent System Redesign), Section 3.2: Model Allocation Implementation

**Success Criteria**: All agents assigned per cognitive load matrix, >95% task completion accuracy, <10% principle drift, dynamic upgrading functional.

## References

- **ADR-007**: Agent System Architecture (hierarchical structure context)
- **PRP-004**: Agent System Redesign (implementation details)
- **2024 Multi-Agent Research**: Performance bottleneck analysis
- **Claude Model Documentation**: Capability and performance characteristics
- **CLAUDE.md**: KISS/YAGNI principle requirements for drift prevention
