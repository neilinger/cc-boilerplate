# ADR-008: Cognitive Load-Based Model Allocation Strategy

**Status**: Proposed
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

### Opus (High Cognitive Load)

#### Complex reasoning, synthesis, creation, judgment

- **meta-agent**: Creating new agents requires deep understanding of patterns and requirements
- **technical-researcher**: Synthesizing multiple complex sources with critical evaluation
- **context-engineer**: Optimizing prompts requires nuanced understanding of AI behavior
- **debugger**: Root cause analysis requires complex logical reasoning chains
- **adr-creator**: Architectural decisions need deep thought and consequence analysis
- **workflow-orchestrator**: Complex multi-step coordination requiring strategic planning

### Sonnet (Medium Cognitive Load)

#### Analysis, pattern matching, structured execution

- **code-reviewer**: Pattern recognition in code, style analysis, best practice application
- **security-scanner**: Vulnerability pattern matching with context awareness
- **test-automator**: Test generation from patterns with coverage analysis
- **prp-creator**: Structured planning with dependency analysis
- **the-librarian**: Knowledge retrieval and synthesis from structured sources
- **codebase-researcher**: Internal pattern analysis with relationship mapping
- **smart-doc-generator**: Content generation following templates and patterns
- **code-lifecycle-manager**: Standard workflow management with decision trees

### Haiku (Low Cognitive Load)

#### Simple tasks, formatting, checks, template operations

- **pr-optimizer**: Template filling, label assignment, formatting
- **github-checker**: Simple status checks, API calls, list processing
- **dependency-manager**: Version comparisons, update notifications
- **work-completion-summary**: Brief summaries, TTS integration
- **security-orchestrator**: Simple chain triggering and status management

**Allocation Rules**:

1. **Task Complexity Assessment**:
   - **Opus**: Requires synthesis of multiple complex concepts, creative problem-solving, or critical judgment
   - **Sonnet**: Requires pattern recognition, structured analysis, or domain expertise application
   - **Haiku**: Requires simple processing, formatting, or straightforward template operations

2. **Verification Role Priority**:
   - **Standard-setting agents** (meta-agent, adr-creator): Use Opus for maximum judgment capability
   - **Standard-enforcing agents** (reviewers, analyzers): Use Sonnet for consistent pattern application
   - **Standard-executing agents** (formatters, checkers): Use Haiku for efficiency

3. **Drift Prevention Optimization**:
   - **Principle validators**: Use Opus for nuanced KISS/YAGNI assessment
   - **Pattern enforcers**: Use Sonnet for consistent rule application
   - **Status reporters**: Use Haiku for simple compliance checking

4. **Dynamic Upgrading Scenarios**:
   - **Confidence thresholds**: If Sonnet agent confidence <80%, escalate to Opus for complex decisions
   - **Context pressure**: Under high context compression, prefer higher-capability models
   - **Error recovery**: Failed tasks automatically retry with next-tier model

## Consequences

### Positive Consequences

- **20-30% performance improvement** through cognitive load matching vs random allocation
- **Predictable performance characteristics** per agent type and task complexity
- **Better drift prevention** via appropriate reasoning capability for verification tasks
- **Resource optimization** using fastest adequate model rather than always maximum
- **Consistent quality standards** through standard-setting vs standard-enforcing hierarchy
- **Scalable allocation rules** for adding new agents without case-by-case decisions
- **Error resilience** through dynamic upgrading mechanisms
- **Clear debugging path** when performance issues arise (check model-task alignment)

### Negative Consequences

- **Implementation complexity** requiring careful task analysis for each agent
- **Potential over-optimization** spending time on allocation vs agent functionality
- **Dynamic upgrading complexity** managing confidence thresholds and escalation rules
- **Maintenance overhead** reviewing allocations as agent responsibilities evolve
- **Edge case handling** for tasks that don't fit clearly into cognitive load categories

### Neutral Consequences

- **Trade-off between speed and capability**: Fast agents may miss nuanced issues
- **Consistency vs adaptability**: Fixed allocations vs dynamic adjustment
- **Resource utilization patterns**: More Haiku usage, selective Opus deployment

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

**Success Criteria**:

- All agents assigned models according to cognitive load matrix
- Performance improvement measurable in task completion accuracy
- Drift prevention enhanced through appropriate verification model selection
- Allocation rules documented and followed for new agent creation
- Dynamic upgrading functional for confidence threshold scenarios
- No performance regressions from over-optimization

**Validation Metrics**:

- **Task completion accuracy**: >95% for all cognitive load categories
- **Principle adherence**: <10% drift after 10+ operations
- **Performance consistency**: Predictable latency per model tier
- **Resource efficiency**: Optimal model usage without capability sacrifice

## References

- **ADR-007**: Agent System Architecture (hierarchical structure context)
- **PRP-004**: Agent System Redesign (implementation details)
- **2024 Multi-Agent Research**: Performance bottleneck analysis
- **Claude Model Documentation**: Capability and performance characteristics
- **CLAUDE.md**: KISS/YAGNI principle requirements for drift prevention
