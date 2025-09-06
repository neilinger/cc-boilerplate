# ADR-002: Branch-Specific CI/CD Pipeline

**Status**: Accepted
**Date**: 2025-01-09
**Deciders**: Neil (Project Owner)

## Context

Following the adoption of Release Flow branching strategy (ADR-001), we needed a CI/CD pipeline that:

- **Matches Branch Purpose**: Different branches serve different purposes and need different validation levels
- **Resource Efficiency**: Minimize GitHub Actions costs while maintaining quality
- **Fast Feedback**: Developers need quick feedback on feature branches
- **Release Quality**: Release branches need comprehensive validation
- **Security First**: Safety hooks (dangerous command detection) are security-critical

Current situation:
- Comprehensive test suite exists (60% coverage) with priority-based organization
- Tests include security-critical safety hooks and integration testing
- No CI/CD automation currently in place
- Manual testing is time-consuming and inconsistent

Constraints:
- GitHub Actions has cost implications for excessive usage
- Some tests (TTS providers) may fail without API keys
- Test suite can take 5-10 minutes for full execution
- Solo developer needs efficient workflow

## Decision

Implement a **branch-specific CI/CD pipeline** with different test strategies based on branch type:

### Feature Branches (`feature/**`)
**Purpose**: Fast feedback for development
**Strategy**: Security-critical tests only (~2-3 minutes)
```yaml
on:
  push:
    branches: ['feature/**']
```
**Tests**:
- Safety hooks (dangerous command detection) - CRITICAL
- Basic PRP edge case validation - CRITICAL  
- Hook integration smoke tests - ESSENTIAL

### Release Branches (`release/**`)
**Purpose**: Comprehensive validation before production
**Strategy**: Full test suite (~5-7 minutes)
```yaml
on:
  push:
    branches: ['release/**']
  pull_request:
    branches: ['release/**']
```
**Tests**:
- Complete security test suite
- Full hook integration testing
- TTS provider testing (allow failures)
- Coverage reporting
- Release preparation validation

### Main Branch
**Purpose**: Final validation and deployment
**Strategy**: Full validation + deployment tasks (~3-5 minutes)
```yaml
on:
  push:
    branches: [main]
```
**Tasks**:
- Full test suite validation
- Automated semantic version tagging
- Release artifact creation
- Badge status updates

### Pull Requests to Main
**Purpose**: Final gate before production
**Strategy**: Enhanced validation (~7-10 minutes)
```yaml
on:
  pull_request:
    branches: [main]
```
**Tests**:
- Everything from release branch validation
- Additional security scanning
- Dependency vulnerability checks
- Release notes validation

## Consequences

### Positive Consequences
- **Fast Development Feedback**: Feature branches get 2-3 minute validation
- **Resource Efficient**: ~15-20 CI minutes total per feature completion
- **Quality Assurance**: Release branches get comprehensive testing
- **Security First**: Critical security tests run on every branch
- **Clear Separation**: Different concerns tested at appropriate times
- **Cost Control**: Minimal GitHub Actions usage while maintaining quality

### Negative Consequences
- **Workflow Complexity**: Developers need to understand branch-specific behavior
- **Configuration Maintenance**: Multiple workflow configurations to maintain
- **False Security**: Feature branches might pass but fail on release branch
- **Documentation Overhead**: Need clear docs on what gets tested when
- **Merge Conflicts**: Different test requirements might cause confusion

### Neutral Consequences
- **Badge Strategy**: Need branch-specific badges to show appropriate status
- **Test Organization**: Existing test structure works well for this approach
- **Caching Strategy**: UV dependency caching needed for efficiency

## Alternatives Considered

### Uniform Testing (Same tests on all branches)
- **Pros**: Simple to understand, consistent behavior
- **Cons**: Slow feedback on feature branches, wasteful of CI resources
- **Reason for rejection**: 5-10 minutes feedback is too slow for development

### No CI/CD on Feature Branches
- **Pros**: Minimal resource usage, fast development
- **Cons**: Security issues not caught early, poor developer experience
- **Reason for rejection**: Security tests are too critical to skip

### Matrix Testing Across Branches
- **Pros**: Comprehensive testing, multiple Python versions
- **Cons**: Expensive in CI resources, overkill for current needs
- **Reason for rejection**: Solo development doesn't justify matrix complexity

### External CI Services (Travis, CircleCI)
- **Pros**: Potentially different pricing models
- **Cons**: Additional complexity, GitHub Actions integration better
- **Reason for rejection**: GitHub Actions is simpler and well-integrated

## Implementation Notes

### Workflow Structure:
```yaml
name: CC-Boilerplate CI/CD
on:
  push:
    branches: ['feature/**', 'release/**', 'main']
  pull_request:
    branches: ['main', 'release/**']

jobs:
  security-tests:
    if: contains(github.ref, 'feature/')
    # Fast security-critical tests only
    
  comprehensive-tests:
    if: contains(github.ref, 'release/') || github.ref == 'refs/heads/main'
    # Full test suite
    
  production-deployment:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    # Tagging and release tasks
```

### Resource Optimization:
- **Caching**: UV dependencies cached across runs
- **Parallel Jobs**: Security and feature tests run in parallel where possible
- **Conditional Execution**: Jobs only run when relevant
- **Timeout Management**: Reasonable timeouts to prevent hanging builds

### Test Categories:
- **Security Critical** (Always run): Safety hooks, dangerous command detection
- **Integration** (Release+): Hook pipeline, PRP validation  
- **Features** (Release only): TTS providers, status lines
- **Extended** (PR to main): Security scanning, dependency checks

### Badge Integration:
- Main badge shows main branch status
- Security badge shows latest security test status
- Coverage badge from latest release branch run
- Custom badges for hook count and other metrics

## References

- ADR-001: Branching Strategy (provides context for branch types)
- ADR-003: Testing Strategy (defines test priorities)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Astral UV GitHub Action](https://github.com/astral-sh/setup-uv)
- [Branch-specific workflows](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onpushpull_requestbranchestags)