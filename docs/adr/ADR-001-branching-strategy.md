# ADR-001: Release/Feature Branching Strategy

**Status**: Accepted
**Date**: 2025-01-09
**Deciders**: Neil (Project Owner)

## Context

The cc-boilerplate project needed a structured branching strategy to manage development workflow for a Claude Code enhancement toolkit. Key factors influencing this decision:

- **Project Nature**: Development toolkit with security-critical components (hooks that can block dangerous commands)
- **Release Stability**: Need controlled releases to prevent breaking users' Claude Code setups
- **Solo Development**: Initially single developer, but designed for potential team expansion
- **User Base**: Other developers who depend on stable, tested releases
- **CI/CD Efficiency**: Need to minimize GitHub Actions costs while maintaining quality

Existing situation:
- Currently using feature/prp-functionality and release/v1.0.0 branches
- Main branch exists but workflow was not formally defined
- No documented process for contributing or releasing

## Decision

Adopt a **Release Flow** branching strategy with three branch types:

1. **main branch**: Production-ready code, protected, deployment source
2. **release/vX.X.X branches**: Release preparation, stabilization, and testing
3. **feature/feature-name branches**: Development work, experimentation

### Workflow Process:
```
feature/new-feature → release/v1.1.0 → main
                                    ↓
                               Tagged Release (v1.1.0)
```

### Branch Rules:
- **feature/** branches merge into current release branch
- **release/** branches merge into main after stabilization
- **main** branch only accepts merges from release branches
- Hot fixes create new release branches from main

## Consequences

### Positive Consequences
- **Controlled Releases**: All changes go through release branch stabilization
- **Parallel Development**: Multiple features can be developed simultaneously
- **Quality Gates**: Release branches allow comprehensive testing before production
- **Clear History**: Linear main branch history with clear release points
- **Flexibility**: Can maintain multiple release branches if needed
- **CI/CD Optimization**: Different testing strategies per branch type

### Negative Consequences
- **Additional Complexity**: More complex than simple main-branch workflow
- **Merge Overhead**: Extra merge steps from feature → release → main
- **Branch Management**: Need to manage and clean up old branches
- **Learning Curve**: Contributors need to understand the workflow
- **Release Coordination**: Need to coordinate when to cut release branches

### Neutral Consequences
- **Branch Naming Convention**: Standardized but must be followed consistently
- **PR Strategy**: Requires different PR approaches for different branch types

## Alternatives Considered

### GitHub Flow (main + feature branches)
- **Pros**: Simpler workflow, continuous deployment friendly
- **Cons**: No release stabilization period, harder to coordinate releases
- **Reason for rejection**: Too risky for a toolkit that affects other developers' environments

### Git Flow (main/develop/feature/release/hotfix)
- **Pros**: Well-established pattern, comprehensive workflow
- **Cons**: Overly complex for current team size, develop branch adds confusion
- **Reason for rejection**: Too heavy for solo/small team development

### Trunk-Based Development
- **Pros**: Simplest possible workflow, encourages small changes
- **Cons**: Requires very high test automation, not suitable for release cycles
- **Reason for rejection**: Doesn't match the need for stable release points

## Implementation Notes

### Branch Protection Rules:
- **main**: Require PR reviews, require status checks, restrict pushes
- **release/**: Require basic validation, allow force pushes for stabilization
- **feature/**: No restrictions (development freedom)

### Naming Conventions:
- **Release branches**: `release/v1.2.3` (semantic versioning)
- **Feature branches**: `feature/descriptive-name` or `feature/issue-123`
- **Hot fix branches**: `hotfix/v1.2.4` (if needed)

### Timeline:
- Implement branch protection rules immediately
- Document workflow for contributors
- Update CI/CD to match branch strategy
- Clean up any existing non-conforming branches

## References

- [Git Flow vs GitHub Flow](https://lucamezzalira.com/2014/03/10/git-flow-vs-github-flow/)
- [Release Flow at Microsoft](https://docs.microsoft.com/en-us/azure/devops/learn/devops-at-microsoft/release-flow)
- [Semantic Versioning](https://semver.org/)
- Related ADRs: ADR-002 (CI/CD Pipeline), ADR-003 (Testing Strategy)