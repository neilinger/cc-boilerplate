# adr-003: Priority-Based Testing Strategy

**Status**: Accepted
**Date**: 2025-01-09
**Deciders**: Neil (Project Owner)

## Context

Following the implementation of comprehensive test coverage (from ~15% to ~60%), we needed a testing strategy that balances security, reliability, and resource efficiency for the cc-boilerplate project.

Key factors influencing this decision:

- **Security Critical Components**: Safety hooks prevent dangerous commands (rm -rf protection)
- **Limited Resources**: Solo developer with GitHub Actions cost considerations
- **KISS/YAGNI Principles**: Simple, focused testing without over-engineering
- **CI/CD Integration**: Must align with branch-specific pipeline strategy (adr-002)
- **Development Velocity**: Fast feedback on critical issues, comprehensive validation on releases

Current situation:

- Test coverage increased from 15% to 60% across critical components
- Test suite includes 4 priority-based test categories
- Execution time ranges from <10 seconds (safety) to <60 seconds (TTS)
- No formal testing strategy or priority definition documented

Constraints:

- Limited development time for test maintenance
- API-dependent tests (TTS providers) may fail without keys
- GitHub Actions cost optimization required
- Security tests must never be skipped

## Decision

Implement a **priority-based testing strategy** with four distinct test categories executed based on context and branch type:

### Test Priority Categories

| Priority | Purpose | Execution | Timeout | Tests | Success Criteria |
|----------|---------|-----------|---------|-------|------------------|
| 🔴 High | Security critical | All branches, CI/CD mandatory | <30s | Safety hooks, hook integration, PRP security | 100% pass rate |
| 🟡 Medium | Feature reliability | Release+, main, PR to main | <90s | TTS providers, integration, performance | 95% pass rate |
| 🟢 Low | Extended validation | Release only, manual | <180s | External deps, config, load testing | Best effort |
| 🔵 Manual | UX validation | Major releases, manual | As needed | E2E workflows, docs, acceptance | Manual sign-off |

## Consequences

### Positive Consequences

- **Clear Priorities**: Everyone knows what tests matter most in each context
- **Resource Efficiency**: High-priority tests run fast (<30s) for quick feedback
- **Security First**: Critical security tests never skipped regardless of context
- **Flexible Execution**: Different test suites for different branch strategies
- **Cost Control**: Expensive tests only run when necessary (release branches)
- **Quality Assurance**: Comprehensive validation where it matters most

### Negative Consequences

- **Strategy Complexity**: Developers must understand when tests run
- **Maintenance Overhead**: Four different test categories to maintain
- **False Confidence**: Feature branches might pass high-priority but fail medium-priority
- **Documentation Burden**: Must document what gets tested in each context
- **Workflow Dependencies**: Strategy tied to specific branching model

### Neutral Consequences

- **Test Organization**: Requires reorganizing existing tests by priority
- **CI/CD Configuration**: Must align with branch-specific pipeline strategy
- **Badge Strategy**: Different badges needed for different test categories

## Alternatives Considered

### Uniform Testing (Same tests everywhere)

- **Pros**: Simple to understand, consistent behavior across contexts
- **Cons**: Slow feedback (5-10 min), wasteful of CI resources, poor developer experience
- **Reason for rejection**: 10-minute test feedback is unacceptable for development velocity

### No Automated Testing

- **Pros**: No CI costs, maximum development speed
- **Cons**: Security vulnerabilities undetected, manual testing inconsistent, poor quality
- **Reason for rejection**: Security-critical components require automated validation

### Test Everything Always

- **Pros**: Maximum coverage and confidence in all contexts
- **Cons**: Extremely expensive in CI resources, slow development feedback
- **Reason for rejection**: Over-engineering for solo development, violates YAGNI principles

### Risk-Based Testing Only

- **Pros**: Focus on highest-risk components only
- **Cons**: Feature reliability suffers, hard to define "risk" consistently
- **Reason for rejection**: Doesn't address user experience and feature quality needs

## Implementation Notes

### Implementation Details

**Test Execution**: See [Testing Guide](../guides/testing.md#how-to-run-different-test-suites) for current commands.

**CI/CD Integration**: Feature branches (High only), Release branches (High + Medium), Main (All automated + manual), PR to main (Extended validation).

**Test Organization**: `tests/` directory with priority-based subdirectories: `high_priority/`, `medium_priority/`, `low_priority/`, plus `run_all_tests.py` orchestrator.

**Failure Response**: High priority blocks merges, Medium priority allows merge with approval, Low priority logs for improvement.

**Coverage Targets**: High (95%), Medium (80%), Low (60%), Overall system (75%).

## References

- adr-001: Branching Strategy (defines when tests run on which branches)
- adr-002: CI/CD Pipeline (defines test execution contexts)
- [Testing Guide](../guides/testing.md) (detailed test documentation)
- [KISS/YAGNI Principles](https://en.wikipedia.org/wiki/KISS_principle)
- [Priority-Based Testing](https://www.satisfice.com/download/test-strategy-primer)
- [Security Testing Best Practices](https://owasp.org/www-project-web-security-testing-guide/)
