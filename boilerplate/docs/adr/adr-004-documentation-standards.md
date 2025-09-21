# adr-004: Documentation Standards and Organization

**Status**: Accepted
**Date**: 2025-01-09
**Deciders**: Neil (Project Owner)

## Context

The cc-boilerplate project's documentation has grown organically without consistent standards, leading to:

- **Naming Inconsistency**: Mix of UPPERCASE and lowercase files violating conventions
- **No Cross-referencing**: Documentation exists in isolation without proper linking
- **Duplicate Content**: Multiple files covering similar topics
- **KISS/YAGNI Violation**: Creating new docs instead of improving existing ones
- **Poor Discoverability**: Users can't easily find relevant documentation

Current issues identified:

- UPPERCASE files in docs/ (BRANCH_PROTECTION.md, DEVELOPMENT.md, etc.)
- No documentation index or navigation structure
- Overlapping content between multiple files
- Documentation created without clear governance

## Decision

Adopt consistent documentation standards following KISS/YAGNI principles:

### File Naming Convention

- **Use lowercase with hyphens**: `branch-protection.md` not `BRANCH_PROTECTION.md`
- **Exception**: Standard files (README.md, LICENSE, CHANGELOG.md)
- **Rationale**: Follows industry conventions, improves consistency

### Documentation Structure

**Directories**: `docs/adr/` (ADRs), `docs/guides/` (how-tos), `docs/reference/` (API docs), `troubleshooting.md` (common issues)

### Documentation Principles

1. **Modify Before Create**: Always improve existing docs before creating new ones
2. **Single Source of Truth**: One authoritative location per topic
3. **Cross-reference Everything**: All docs must be linked from README.md
4. **Keep It Simple**: Short, focused documents over comprehensive tomes
5. **Just-in-Time Documentation**: Document only what's actively used

### Content Guidelines

- **Title Case for Headings**: Use "Branch Protection Setup" not "BRANCH PROTECTION SETUP"
- **Lowercase Filenames**: Use `branch-protection.md` not `BRANCH_PROTECTION.md`
- **Clear Hierarchy**: Main README links to category docs, which link to specifics
- **No Duplication**: If content exists elsewhere, link to it instead

## Consequences

### Positive Consequences

- **Improved Discoverability**: Clear navigation from README to all docs
- **Consistent Experience**: Predictable naming and structure
- **Reduced Maintenance**: Less duplicate content to keep synchronized
- **KISS Compliance**: Simpler documentation structure
- **Better Onboarding**: New contributors can find information easily

### Negative Consequences

- **Migration Effort**: Need to rename and reorganize existing docs
- **Breaking Links**: External references to old filenames will break
- **Learning Curve**: Contributors must learn the conventions

### Neutral Consequences

- **Enforcement Needed**: Requires review process or automation
- **Regular Cleanup**: Periodic review to prevent documentation drift

## Implementation

Brief reorganization to establish consistent documentation architecture.

**Implementation handled via**: PRP-001 (Documentation Migration)

**Success Criteria**:

- All documentation follows naming conventions
- Clear navigation structure from README
- No duplicate content across files
- Established governance prevents future drift

## Alternatives Considered

### Keep Current Structure

- **Pros**: No migration effort
- **Cons**: Continues confusion, violates conventions
- **Rejected**: Technical debt will compound

### Automated Documentation Generation

- **Pros**: Always up-to-date
- **Cons**: Complex setup, violates YAGNI
- **Rejected**: Over-engineering for current needs

### Wiki-style Documentation

- **Pros**: Easy editing, rich linking
- **Cons**: Separate from code, harder to version
- **Rejected**: Documentation should live with code

## References

- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Write the Docs - Documentation Guide](https://www.writethedocs.org/guide/)
- Related ADRs: adr-001 (Branching), adr-002 (CI/CD), adr-003 (Testing), adr-005 (ADR/PRP Separation)
- Implementation PRP: PRP-001 (Documentation Migration)
- KISS/YAGNI principles in CLAUDE.md
