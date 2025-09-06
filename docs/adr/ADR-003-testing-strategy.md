# ADR-003: Priority-Based Testing Strategy

**Status**: Accepted
**Date**: 2025-01-09
**Deciders**: Neil (Project Owner)

## Context

Following the implementation of comprehensive test coverage (from ~15% to ~60%), we needed a testing strategy that balances security, reliability, and resource efficiency for the cc-boilerplate project.

Key factors influencing this decision:
- **Security Critical Components**: Safety hooks prevent dangerous commands (rm -rf protection)
- **Limited Resources**: Solo developer with GitHub Actions cost considerations
- **KISS/YAGNI Principles**: Simple, focused testing without over-engineering
- **CI/CD Integration**: Must align with branch-specific pipeline strategy (ADR-002)
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

#### 🔴 High Priority (Security Critical - Always Run)
**Purpose**: Prevent security vulnerabilities and system failures
**Execution**: All branches, all contexts, CI/CD mandatory
**Timeout**: <30 seconds total

**Tests**:
- `test_safety_hooks.py` - Dangerous command detection (rm -rf protection)
- `test_hook_integration.py` - Hook pipeline execution and error handling  
- `test_prp_edge_cases.py` - PRP system security validation

**Success Criteria**: 100% pass rate required for any deployment

#### 🟡 Medium Priority (Feature Reliability - Release Testing)
**Purpose**: Validate feature functionality and user experience
**Execution**: Release branches, main branch, PR to main
**Timeout**: <90 seconds total

**Tests**:
- `test_tts_providers.py` - TTS provider fallback and error handling
- Integration tests for status line generation
- Performance benchmarking

**Success Criteria**: 95% pass rate, failures documented but not blocking

#### 🟢 Low Priority (Extended Validation - Release Only)
**Purpose**: Comprehensive system validation and edge case coverage
**Execution**: Release branches only, manual testing
**Timeout**: <180 seconds total

**Tests**:
- External dependency validation (git, gh commands)
- Configuration testing across environments
- Load testing and performance validation

**Success Criteria**: Best effort, failures inform improvement backlog

#### 🔵 Manual Priority (Human Validation)
**Purpose**: User experience and integration validation
**Execution**: Before major releases, manual only
**Timeline**: As needed

**Tests**:
- End-to-end workflow testing
- Documentation accuracy validation
- User acceptance scenarios

**Success Criteria**: Manual sign-off by project maintainer

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

### Test Execution Commands
```bash
# High Priority (Security Critical) - <30s
python3 tests/test_safety_hooks.py
python3 tests/test_hook_integration.py  
python3 tests/test_prp_edge_cases.py

# Medium Priority (Feature Reliability) - <90s
python3 tests/test_tts_providers.py
# Additional feature tests as implemented

# All Tests with Reporting
python3 tests/run_all_tests.py
```

### CI/CD Integration
- **Feature branches**: High priority tests only
- **Release branches**: High + Medium priority tests
- **Main branch**: All automated tests + manual validation
- **PR to main**: Extended validation including security scanning

### Test Organization Structure
```
tests/
├── high_priority/          # Security critical
│   ├── test_safety_hooks.py
│   ├── test_hook_integration.py
│   └── test_prp_edge_cases.py
├── medium_priority/        # Feature reliability  
│   └── test_tts_providers.py
├── low_priority/          # Extended validation
│   └── [future tests]
└── run_all_tests.py       # Orchestrator
```

### Performance Requirements
- **High Priority**: Must complete in <30 seconds total
- **Medium Priority**: Must complete in <90 seconds total
- **Low Priority**: Must complete in <180 seconds total
- **Timeout Handling**: Tests that exceed timeout are automatically failed

### Failure Response Protocol
1. **High Priority Failures**: Block all merges, immediate investigation required
2. **Medium Priority Failures**: Document issue, create tracking ticket, allow merge with approval
3. **Low Priority Failures**: Log for future improvement, does not block development

### Coverage Targets by Priority
- **High Priority**: 95% line coverage minimum
- **Medium Priority**: 80% line coverage target  
- **Low Priority**: 60% line coverage acceptable
- **Overall System**: 75% coverage target across all priorities

## References

- ADR-001: Branching Strategy (defines when tests run on which branches)
- ADR-002: CI/CD Pipeline (defines test execution contexts)
- [Test Coverage Implementation](/tests/README.md) (detailed test documentation)
- [KISS/YAGNI Principles](https://en.wikipedia.org/wiki/KISS_principle)
- [Priority-Based Testing](https://www.satisfice.com/download/test-strategy-primer)
- [Security Testing Best Practices](https://owasp.org/www-project-web-security-testing-guide/)