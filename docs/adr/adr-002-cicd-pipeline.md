# adr-002: Branch-Specific CI/CD Pipeline

**Status**: Accepted
**Date**: 2025-01-09
**Deciders**: Neil (Project Owner)

## Context

Following the adoption of Release Flow branching strategy (adr-001), we needed a CI/CD pipeline that:

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

### Branch-Specific Testing Strategy

| Branch Type | Purpose | Strategy | Duration | Tests |
|-------------|---------|----------|----------|-------|
| `feature/**` | Fast feedback | Security-critical only | 2-3 min | Safety hooks, PRP validation, hook integration |
| `release/**` | Pre-production validation | Full test suite | 5-7 min | Complete security, full hooks, TTS (allow failures), coverage |
| `main` | Final validation + deployment | Full + deployment | 3-5 min | Full validation, version tagging, artifacts, badges |
| PR → `main` | Production gate | Enhanced validation | 7-10 min | Release validation + security scanning + dependency checks |

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

### Implementation Details

**Workflow Structure**: Single GitHub Actions workflow with conditional jobs based on branch patterns. Security tests run on all branches, comprehensive tests on release/main, deployment tasks on main only.

**Resource Optimization**: UV dependency caching, parallel execution where possible, conditional job execution, timeout management.

**Test Categories**: Security Critical (always), Integration (release+), Features (release only), Extended (PR to main).

**Badge Integration**: Branch-specific status badges for main, security, coverage, and custom metrics.

## References

- adr-001: Branching Strategy (provides context for branch types)
- adr-003: Testing Strategy (defines test priorities)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Astral UV GitHub Action](https://github.com/astral-sh/setup-uv)
- [Branch-specific workflows](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onpushpull_requestbranchestags)
