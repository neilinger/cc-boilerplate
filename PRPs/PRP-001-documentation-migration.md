# PRP-001: Documentation Migration - UPPERCASE to kebab-case Structure

name: "PRP-001: Documentation Migration - UPPERCASE to kebab-case Structure"
description: |
  Implement the documentation standards established in adr-004 by migrating
  existing UPPERCASE files to kebab-case convention and establishing proper
  cross-referencing structure.

---

## Goal

**Feature Goal**: Migrate all documentation to follow kebab-case naming convention with proper cross-referencing structure

**Deliverable**: Reorganized documentation structure following adr-004 standards with updated README navigation

**Success Definition**:

- All docs follow kebab-case naming (lowercase-hyphen format)
- README.md has complete documentation index
- No broken internal links
- No duplicate content

## User Persona

**Target User**: Contributors and maintainers of cc-boilerplate project

**Use Case**: Finding and navigating project documentation efficiently

**User Journey**:

1. Land on README.md
2. See clear documentation sections  
3. Follow links to specific guides
4. Find information without duplication or confusion

**Pain Points Addressed**:

- Confusion from mixed UPPERCASE/lowercase naming
- Can't find docs due to poor navigation
- Duplicate information across files

## Why

- **Consistency**: Follow [Google Developer Documentation Standards](https://developers.google.com/style/filenames) using kebab-case (lowercase-hyphen format)
- **Discoverability**: Clear navigation structure from README following [CommonMark standard](https://commonmark.org/) and [Google's Markdown style guide](https://google.github.io/styleguide/docguide/style.html)
- **Maintainability**: Single source of truth for each topic
- **KISS/YAGNI Compliance**: Focus on improving existing docs vs creating new ones
- **Based on**: Architectural decision in [adr-004](../docs/adr/adr-004-documentation-standards.md) (Documentation Standards)

## What

Reorganize existing documentation files to match the structure defined in [adr-004](../docs/adr/adr-004-documentation-standards.md).

### Success Criteria

- [ ] All UPPERCASE files renamed to kebab-case convention
- [ ] Documentation organized into logical directory structure
- [ ] README.md updated with complete documentation index
- [ ] All internal links updated and verified working
- [ ] No content duplication between files
- [ ] Governance guidelines added to prevent future drift

## All Needed Context

### Current Documentation Issues

- UPPERCASE files: BRANCH_PROTECTION.md, DEVELOPMENT.md, SECURITY.md, TROUBLESHOOTING.md, REFERENCE.md
- No clear navigation from README.md
- Overlapping content between files
- Missing cross-references

### Architecture Decision

- Based on [adr-004: Documentation Standards and Organization](../docs/adr/adr-004-documentation-standards.md)
- Focus: kebab-case naming, logical structure, cross-referencing

### Target Structure (from adr-004)

```text
docs/
├── adr/                    # Architecture Decision Records  
│   └── adr-*.md           # Numbered ADRs (kebab-case)
├── guides/                 # How-to guides
│   ├── development.md      # Development workflow
│   ├── testing.md          # Testing guide  
│   ├── security.md         # Security practices
│   └── branch-protection.md # Branch protection setup
├── reference/              # API and technical reference
│   └── hooks-api.md        # Hook system reference
└── troubleshooting.md      # Common issues and fixes
```

### Dependencies

- Git operations for file moves/renames
- README.md editing capabilities
- Link validation tools (manual review)

## Implementation Steps

### Phase 1: File Renaming and Moving

#### Step 1.1: Create directory structure

```bash
mkdir -p docs/guides docs/reference
```

#### Step 1.2: Rename and move UPPERCASE files

```bash
# Move and rename files using git to preserve history
git mv docs/BRANCH_PROTECTION.md docs/guides/branch-protection.md
git mv docs/DEVELOPMENT.md docs/guides/development.md  
git mv docs/SECURITY.md docs/guides/security.md
git mv docs/TROUBLESHOOTING.md docs/troubleshooting.md
git mv docs/REFERENCE.md docs/reference/index.md
```

#### Step 1.3: Update ADR filenames (if needed)

Verify ADR files follow `ADR-XXX-title.md` kebab-case pattern (currently they seem correct)

### Phase 2: Content Consolidation

#### Step 2.1: Review for duplicate content

- Compare guides/development.md with other files
- Check for overlapping security content
- Identify redundant troubleshooting info

#### Step 2.2: Consolidate overlapping content

- Keep single source of truth per topic
- Add cross-references instead of duplication
- Update content to reference other sections

#### Step 2.3: Content quality check

- Ensure all content is current and accurate
- Remove outdated information
- Standardize formatting and style

### Phase 3: Navigation Structure

#### Step 3.1: Update README.md

Add comprehensive documentation section:

```markdown
## Documentation

### Quick Start
- [Setup Guide](setup.md) - Get cc-boilerplate running
- [Development Workflow](docs/guides/development.md) - Contributing guidelines

### Core Guides  
- [Security Features](docs/guides/security.md) - Security hooks and validation
- [Testing Strategy](docs/guides/testing.md) - Comprehensive testing approach
- [Branch Protection](docs/guides/branch-protection.md) - Repository protection setup

### Reference
- [Hooks API](docs/reference/hooks-api.md) - Technical hook system reference
- [Troubleshooting](docs/troubleshooting.md) - Common issues and fixes

### Architecture  
- [All ADRs](docs/adr/) - Architecture decision records
- [adr-001: Branching Strategy](docs/adr/adr-001-branching-strategy.md)
- [adr-004: Documentation Standards](docs/adr/adr-004-documentation-standards.md)
- [adr-005: ADR/PRP Separation](docs/adr/adr-005-adr-prp-separation.md)
```

#### Step 3.2: Update all internal links

- Search for links to old UPPERCASE filenames
- Update to new lowercase paths
- Test all links manually or with link checker

#### Step 3.3: Add cross-references in docs

- Add "Related Documents" sections
- Link between related guides
- Reference ADRs from implementation guides

### Phase 4: Governance Implementation

#### Step 4.1: Update guides/development.md

Add documentation guidelines section:

```markdown
## Documentation Guidelines

### File Naming
- Use kebab-case: `user-guide.md` not `USER_GUIDE.md` ([Google style](https://developers.google.com/style/filenames))
- Exception: Standard files (README.md, LICENSE)

### Structure
- Guides go in `docs/guides/`
- Reference material in `docs/reference/`  
- ADRs in `docs/adr/`

### Before Adding New Docs
1. Check if existing doc can be improved instead
2. Ensure proper cross-referencing
3. Update README.md navigation
4. Follow single-source-of-truth principle

### Review Checklist
- [ ] Follows naming convention
- [ ] Added to README navigation
- [ ] Cross-referenced appropriately  
- [ ] No content duplication
```

#### Step 4.2: Create documentation maintenance checklist

For future PRs involving documentation changes.

## Validation Steps

### Link Validation

1. Clone fresh repository
2. Check all links from README.md work
3. Verify internal cross-references  
4. Test that moved files don't break external references

### Content Validation  

1. Ensure no content was lost during moves
2. Verify consolidated content maintains all information
3. Check that examples and code snippets still work

### Structure Validation

1. Confirm directory structure matches adr-004
2. Verify all files follow naming convention
3. Test navigation flow from README

## Success Metrics

- **Technical**: 0 broken internal links
- **Structure**: 100% files follow kebab-case naming convention  
- **Navigation**: Complete documentation index in README
- **Governance**: Development guide includes documentation standards
- **Quality**: No duplicate content between files

## Rollback Plan

If issues arise:

1. Git revert the file moves (preserves history)
2. Restore original README.md
3. Document lessons learned
4. Create revised PRP with fixes

## Notes

- Use `git mv` to preserve file history during renames
- Test links manually as this is a one-time migration
- Focus on improving existing content vs adding new docs
- This PRP implements the architectural decision in [adr-004](../docs/adr/adr-004-documentation-standards.md)

## Timeline

- **Phase 1** (File moves): 1-2 hours
- **Phase 2** (Content consolidation): 2-3 hours  
- **Phase 3** (Navigation): 1-2 hours
- **Phase 4** (Governance): 1 hour
- **Validation**: 1 hour

**Total estimated effort**: 6-9 hours

This PRP provides the tactical implementation of the strategic documentation standards decision captured in [adr-004](../docs/adr/adr-004-documentation-standards.md).
