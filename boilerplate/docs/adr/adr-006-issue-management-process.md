# ADR-006: Issue Management Process

**Status**: Accepted
**Date**: 2025-09-07
**Deciders**: Neil (Project Owner)

## Context

The cc-boilerplate project has received its first GitHub issues from users, exposing the need for a systematic approach to handle bug reports, feature requests, and documentation gaps. Key factors influencing this decision:

- **First User Feedback**: 4 GitHub issues raised covering bugs (#5, #6), documentation (#7), and enhancement (#8)
- **Project Principles**: Must align with KISS/YAGNI principles to avoid over-engineering
- **Existing Workflow**: ADR-001 defines Release Flow branching strategy but lacks issue-specific guidance
- **Solo Development**: Initially single developer but designed for potential contributors
- **User Impact**: Need to prioritize fixes that block user adoption versus nice-to-have features
- **YAGNI Validation**: Enhancements require evaluation against "needed now" criteria

Current situation:

- No documented issue triage process
- No severity/priority classification system
- Unclear when to create separate branches per issue vs grouped fixes
- No integration between issue management and Release Flow strategy

## Decision

Adopt a **three-level issue classification system** integrated with the existing Release Flow branching strategy:

### Issue Classification

1. **🔴 blocking**: Breaks core functionality, prevents project usage
   - Examples: Setup failures, API key problems, broken installation
   - Response: Fix immediately, highest priority

2. **🟡 important**: Affects user experience, should fix soon
   - Examples: Documentation gaps, usability issues, minor bugs
   - Response: Fix in current development cycle

3. **🟢 enhancement**: New features, evaluate against YAGNI
   - Examples: New tools, workflow improvements, convenience features
   - Response: Challenge with YAGNI - only implement if needed NOW

### Branch Strategy Integration

**For Blocking Issues on Production:**

- Create `hotfix/issue-X` branches from `main`
- Direct merge to `main` after testing
- Cherry-pick to current release branch if needed

**For Development Issues (blocking/important):**

- Use Release Flow: group related issues in single `feature/*` branch
- Follow existing feature → release → main workflow

**For Enhancement Issues:**

- Individual `feature/*` branches for isolation
- Easier to defer, modify, or rollback if not needed

### Process Guidelines

**Group issues when**: Same files/severity, <500 lines, ship together logically
**Separate issues when**: Different severity levels, unrelated functionality, >500 lines

**Workflow**: Label with severity → Apply YAGNI test → Create branch → Reference issues → Use GitHub native features

## Consequences

### Positive Consequences

- **Clear Prioritization**: Three levels provide obvious action priority
- **YAGNI Enforcement**: Enhancements must justify immediate need
- **Workflow Integration**: Builds on existing Release Flow rather than replacing it
- **Contributor Clarity**: Clear guidelines for when to branch vs group
- **GitHub Native**: Uses platform features, no additional tooling overhead
- **KISS Compliance**: Simple enough to explain in one breath

### Negative Consequences

- **Learning Curve**: Contributors need to understand severity levels
- **Decision Overhead**: Must evaluate each issue for classification
- **Grouping Complexity**: Deciding when to group vs separate requires judgment
- **Branch Management**: More branches than simple "fix everything in main"

### Neutral Consequences

- **Label Maintenance**: Need to create and maintain GitHub labels
- **Process Evolution**: May need refinement as project scales
- **Documentation**: Requires updating contributing guidelines

## Alternatives Considered

### Enterprise Bug Triage (4 severity + 4 priority levels)

- **Pros**: Comprehensive classification, industry standard
- **Cons**: Over-engineering for project size, violates KISS principle
- **Reason for rejection**: Too complex for solo/small team development

### GitHub Flow (no severity levels)

- **Pros**: Minimal process overhead, very simple
- **Cons**: No guidance for prioritization, treats all issues equally
- **Reason for rejection**: Doesn't help prioritize blocking vs nice-to-have issues

### One Branch Per Issue

- **Pros**: Complete isolation, easier to track individual changes
- **Cons**: Branch proliferation, merge overhead for related fixes
- **Reason for rejection**: Violates KISS for related small fixes

### Traditional Kanban Board

- **Pros**: Visual workflow, detailed status tracking
- **Cons**: External tooling, overhead for small project
- **Reason for rejection**: GitHub issues provide sufficient tracking

## Implementation

**Implementation handled via**: Direct implementation in this feature branch (demonstrates process in action)

**Success Criteria**:

- All 4 current issues resolved using new process
- GitHub labels configured and applied
- Process documented and tested
- Integration with Release Flow validated

## References

- ADR-001: Branching Strategy (Release Flow)
- ADR-005: ADR/PRP Separation
- Industry research on bug severity best practices
- GitHub Issues documentation and labeling guidelines
- Current issues #5, #6, #7, #8 as test cases
