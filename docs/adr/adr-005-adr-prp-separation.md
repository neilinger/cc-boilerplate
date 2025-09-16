# adr-005: ADR vs PRP Separation of Concerns

**Status**: Accepted
**Date**: 2025-01-09
**Deciders**: Neil (Project Owner)

## Context

While implementing adr-004 (Documentation Standards), we discovered scope confusion between Architecture Decision Records (ADRs) and Product Requirements Process (PRPs). The original adr-004 included detailed migration plans, which violates the principle of separation of concerns.

Research into ADR best practices revealed that:

- ADRs should focus on **strategic architectural decisions** (WHY & WHAT)
- Implementation details should be handled by separate artifacts (HOW & WHEN)
- ADRs are **immutable decision records**, not living implementation documents
- Migration plans are **operational/tactical**, not architectural

This confusion leads to:

- **Scope Creep**: ADRs becoming implementation plans
- **Maintenance Issues**: Implementation details changing after ADR approval
- **Poor Boundaries**: Unclear when to use ADR vs PRP
- **KISS/YAGNI Violations**: Over-documenting architectural decisions

## Decision

Establish clear separation of concerns between ADRs and PRPs:

### Architecture Decision Records (ADRs)

**Purpose**: Document significant architectural and technical decisions

**Scope**:

- Technology choices (frameworks, databases, patterns)
- System structure decisions (microservices, monolith, API design)
- Cross-cutting concerns (security strategies, performance approaches)
- Non-functional requirements (scalability, availability)

**Focus**: WHY and WHAT

- Context: What problem are we solving?
- Decision: What choice did we make?
- Consequences: What are the implications?
- Alternatives: What else did we consider?

**Characteristics**:

- **Immutable**: Once approved, ADRs don't change (only status updates)
- **Strategic**: Focus on architectural significance
- **Concise**: 1-2 pages, 5-minute read
- **Decision-focused**: Not implementation-focused

### Product Requirements Process (PRPs)

**Purpose**: Define and plan tactical implementation work

**Scope**:

- Feature implementation planning
- Migration and refactoring tasks
- Step-by-step execution plans
- Resource allocation and timelines

**Focus**: HOW and WHEN

- Goal: What specific deliverable?
- Context: What information is needed?
- Implementation: How will it be built?
- Success Criteria: How do we validate completion?

**Characteristics**:

- **Living Documents**: Can be updated during implementation
- **Tactical**: Focus on execution details
- **Comprehensive**: Include all implementation context
- **Delivery-focused**: Emphasis on concrete outcomes

### Cross-referencing Standards

- **ADR → PRP**: "Implementation handled via prp-XXX"
- **PRP → ADR**: "Based on architectural decision adr-XXX"
- **Clear Handoff**: ADR establishes decision, PRP executes it

### Naming Conventions

**ADRs**: `adr-XXX-decision-title.md`

- XXX is a 3-digit sequence number (001, 002, 003...)
- decision-title describes the architectural decision

**PRPs**: `prp-XXX-feature-name.md`

- XXX is a 3-digit sequence number (001, 002, 003...)
- feature-name is a kebab-case description of the feature goal
- Examples: `prp-001-documentation-migration.md`, `prp-002-github-maintenance-check.md`

## Consequences

### Positive Consequences

- **Clear Boundaries**: Teams know when to use ADR vs PRP
- **Focused Documentation**: Each pattern serves its purpose
- **Reduced Scope Creep**: ADRs stay architectural, PRPs stay tactical
- **Better Maintenance**: Implementation changes don't affect decision records
- **KISS Compliance**: Each document has single responsibility

### Negative Consequences

- **Learning Curve**: Team must understand both patterns
- **Coordination Overhead**: Need to cross-reference between ADRs and PRPs
- **More Documents**: Two artifacts instead of one comprehensive document

### Neutral Consequences

- **Template Updates**: Need templates and tooling for both patterns
- **Process Changes**: Team workflow must accommodate both patterns

## Implementation Guidelines

### When to Create an ADR

- Making technology choices with system-wide impact
- Establishing architectural patterns or constraints
- Resolving trade-offs between architectural alternatives
- Documenting decisions that affect multiple teams/services
- **Trigger**: When the decision has architectural significance

### When to Create a PRP

- Planning feature implementation
- Organizing migration or refactoring work
- Coordinating complex deliveries
- **Trigger**: When you need to plan HOW to implement something

### Boundary Examples

| Scenario | ADR | PRP |
|----------|-----|-----|
| Choose React vs Angular | ✅ | ❌ |
| Plan React component migration | ❌ | ✅ |
| Decide on microservice pattern | ✅ | ❌ |
| Implement user authentication service | ❌ | ✅ |
| Establish API versioning strategy | ✅ | ❌ |
| Migrate API from v1 to v2 | ❌ | ✅ |

### Cross-referencing Pattern

```markdown
# In ADR
## Implementation
This decision will be implemented via prp-XXX (link when created).

# In PRP
## Context
This PRP implements the architectural decision documented in adr-XXX.
```

## Alternatives Considered

### Single Document Pattern

- **Pros**: Everything in one place
- **Cons**: Scope confusion, maintenance issues, violates SRP
- **Rejected**: Research shows clear separation is best practice

### Wiki-style Linking

- **Pros**: Easy cross-referencing
- **Cons**: Breaks version control, separates docs from code
- **Rejected**: Documentation should live with code

### Issue/Ticket-based Planning

- **Pros**: Integrated with development workflow
- **Cons**: Poor discoverability, limited structure
- **Rejected**: Need structured approach for complex decisions

## References

- [AWS ADR Best Practices](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)
- [GitHub ADR Examples](https://github.com/joelparkerhenderson/architecture-decision-record)
- [ADR Process - AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- Related ADRs: adr-001 (Branching), adr-004 (Documentation Standards)
- Implementation PRP: prp-001 (Documentation Migration)
