name: "prp-003: Boilerplate Synchronization System"
description: |
  Implement a layered configuration system with git subtree to enable graceful boilerplate updates
  while preserving project customizations

---

# prp-003: Boilerplate Synchronization System

## Status

Status: PROPOSED
Status_Date: 2025-01-13
Status_Note: Ready for implementation

## Goal

**Feature Goal**: Implement a layered configuration system that allows cc-boilerplate to be merged into existing projects and updated gracefully without losing customizations.

**Deliverable**: A set of shell scripts and restructured directory layout that enables bidirectional synchronization between cc-boilerplate and derived projects.

**Success Definition**: Users can initialize boilerplate in new/existing projects, pull updates without conflicts, and maintain project-specific customizations seamlessly.

## User Persona

**Target User**: Developer using cc-boilerplate as foundation for Claude Code projects

**Use Case**: Maintaining multiple projects based on cc-boilerplate while keeping them synchronized with upstream improvements

**User Journey**:

1. Initialize cc-boilerplate in new or existing project
2. Customize configurations for project needs
3. Pull cc-boilerplate updates without losing customizations
4. Optionally contribute improvements back to cc-boilerplate

**Pain Points Addressed**:

- Manual merge conflicts with CLAUDE.md, .pre-commit-config.yaml, .claude/ files
- Project-specific PRPs getting mixed with boilerplate
- No clear separation between base and custom configurations
- Difficult to track which version of boilerplate is used

## Why

- Enables "re-apply gracefully" workflow for boilerplate updates
- Follows KISS principle with git subtree (simpler than submodules)
- Clear separation between boilerplate and project-specific code
- Supports semantic versioning already implemented in cc-boilerplate
- Enables feedback loop from derived projects back to boilerplate

## What

A three-layer configuration system with automated merging:

- **Base Layer**: Core boilerplate files from cc-boilerplate (immutable)
- **Project Layer**: Project-specific customizations (preserved)
- **Merged Layer**: Auto-generated final configuration (gitignored)

### Success Criteria

- [ ] Restructured cc-boilerplate with clear boilerplate/project separation
- [ ] Three shell scripts: init-boilerplate.sh, update-boilerplate.sh, build-config.sh
- [ ] Template files for CLAUDE.md and settings.json with merge markers
- [ ] Version tracking via .boilerplate-version file
- [ ] Documentation for the synchronization workflow
- [ ] Successful test with sample project

## All Needed Context

### Context Completeness Check

_This PRP contains all file paths, command patterns, and implementation details needed for successful implementation without prior knowledge of the codebase._

### Documentation & References

```yaml
- url: https://manpages.debian.org/testing/git-man/git-subtree.1.en.html
  why: Official git-subtree documentation for command syntax
  critical: Use --squash flag for all operations to maintain clean history

- url: https://gist.github.com/SKempin/b7857a6ff6bddb05717cc17a44091202
  why: Real-world git subtree workflow examples
  pattern: git subtree add/pull commands with --prefix and --squash

- url: https://github.com/crazed/b5448baeb204eb816eb9
  why: jq patterns for JSON deep merging
  critical: Arrays are replaced by default, use reduce for deep merge

- url: https://mikefarah.gitbook.io/yq/operators/multiply-merge
  why: yq operators for YAML merging
  critical: Use *+ operator to append arrays instead of replacing

- file: .claude/settings.json
  why: Current settings structure to understand merge requirements
  pattern: JSON with nested objects, arrays of permissions and hooks
  gotcha: $CLAUDE_PROJECT_DIR variable must be preserved

- file: CLAUDE.md
  why: Current instruction structure needing section-based merging
  pattern: Markdown with headers and code blocks
  gotcha: Contains both universal and project-specific instructions

- file: docs/adr/adr-001-branching-strategy.md
  why: Semantic versioning and release workflow already in place
  pattern: Release branches with v.X.X.X tags

- file: setup.sh
  why: Existing setup script patterns for OS detection and tool checking
  pattern: Uses command -v for tool detection, mktemp for safe file ops

- docfile: PRPs/ai_docs/git-subtree-implementation.md
  why: Detailed git subtree commands and conflict resolution strategies
  section: Squash mode operations
```

### Current Codebase tree

```bash
.
├── .claude/
│   ├── agents/
│   ├── commands/
│   ├── hooks/
│   ├── output-styles/
│   ├── status_lines/
│   ├── settings.json
│   └── settings.local.json
├── PRPs/
│   ├── prp-001-documentation-migration.md
│   ├── prp-002-github-maintenance-check.md
│   └── templates/
├── docs/
│   └── adr/
├── scripts/
├── tests/
├── CLAUDE.md
├── setup.sh
├── .pre-commit-config.yaml
└── pyproject.toml
```

### Desired Codebase tree with files to be added

```bash
.
├── boilerplate/                          # NEW: Core boilerplate files
│   ├── .claude/
│   │   ├── agents/
│   │   ├── commands/
│   │   ├── hooks/
│   │   ├── output-styles/
│   │   ├── status_lines/
│   │   └── settings.template.json       # Template with merge markers
│   ├── templates/
│   │   ├── CLAUDE.template.md          # Template with section markers
│   │   └── .pre-commit-config.template.yaml
│   └── .boilerplate-manifest.json      # List of syncable files
├── scripts/
│   ├── init-boilerplate.sh             # NEW: Initialize in projects
│   ├── update-boilerplate.sh           # NEW: Pull updates
│   └── build-config.sh                 # NEW: Merge configurations
├── examples/
│   └── sample-project/                 # NEW: Example implementation
│       ├── .claude/
│       │   ├── boilerplate/            # Subtree from cc-boilerplate
│       │   └── project/                # Project customizations
│       └── .boilerplate-version
└── docs/
    └── SYNCHRONIZATION.md               # NEW: User documentation
```

### Known Gotchas of our codebase & Library Quirks

```bash
# CRITICAL: Git subtree is in contrib/, not core git
# May need: git subtree || git-subtree (hyphenated on some systems)

# CRITICAL: Date command differs between macOS and Linux
# macOS: date -v-30d
# Linux: date -d '30 days ago'
# Use: date -u +%Y%m%d_%H%M%S for portable timestamps

# CRITICAL: jq array merging replaces by default
# Must use: jq -s 'reduce .[] as $item ({}; . * $item)' for deep merge

# CRITICAL: Shell portability
# Use #!/usr/bin/env bash not #!/bin/bash
# Use [[ ]] for conditionals (bash-specific but more reliable)
# Use command -v not which or type
```

## Implementation Blueprint

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: CREATE boilerplate/ directory structure
  - IMPLEMENT: Move .claude/, templates to boilerplate/
  - CREATE: boilerplate/.boilerplate-manifest.json listing all files
  - PRESERVE: Keep copies in root for backward compatibility initially
  - PLACEMENT: Top-level boilerplate/ directory
  - NAMING: Maintain exact subdirectory structure inside boilerplate/

Task 2: CREATE boilerplate/templates/CLAUDE.template.md
  - IMPLEMENT: Template with section markers for merging
  - FOLLOW pattern: Use HTML comments for markers
  - ADD markers: <!-- BEGIN BOILERPLATE -->, <!-- END BOILERPLATE -->
  - ADD markers: <!-- BEGIN PROJECT -->, <!-- END PROJECT -->
  - PLACEMENT: boilerplate/templates/CLAUDE.template.md

Task 3: CREATE boilerplate/.claude/settings.template.json
  - IMPLEMENT: Base settings with merge points
  - ADD structure: Separate base permissions, hooks, and configs
  - USE placeholder: __PROJECT_CUSTOM__ for injection points
  - PRESERVE: $CLAUDE_PROJECT_DIR variable references
  - PLACEMENT: boilerplate/.claude/settings.template.json

Task 4: CREATE scripts/init-boilerplate.sh
  - IMPLEMENT: Initialize boilerplate in new/existing projects
  - ADD: OS detection using OSTYPE (Darwin/Linux)
  - ADD: Tool checking with command -v for git, jq
  - ADD: Git subtree add command with --squash
  - ADD: Initial build-config.sh execution
  - FOLLOW pattern: setup.sh for error handling and colors
  - PLACEMENT: scripts/init-boilerplate.sh

Task 5: CREATE scripts/update-boilerplate.sh
  - IMPLEMENT: Pull updates from cc-boilerplate
  - ADD: Version checking from .boilerplate-version
  - ADD: Backup current configurations before update
  - ADD: Git subtree pull with --squash
  - ADD: Automatic build-config.sh execution
  - ADD: Rollback on failure using trap
  - PLACEMENT: scripts/update-boilerplate.sh

Task 6: CREATE scripts/build-config.sh
  - IMPLEMENT: Merge base + project configurations
  - ADD: JSON merging with jq for settings files
  - ADD: Markdown section merging for CLAUDE.md
  - ADD: YAML merging with yq if available (fallback to manual)
  - ADD: Validation of merged output
  - FOLLOW pattern: Use mktemp for atomic file operations
  - PLACEMENT: scripts/build-config.sh

Task 7: CREATE .boilerplate-manifest.json
  - IMPLEMENT: JSON listing of all boilerplate files
  - STRUCTURE: {"files": [...], "version": "1.0.0", "merge_strategy": {...}}
  - ADD: Merge strategy per file type (replace/merge/append)
  - PLACEMENT: boilerplate/.boilerplate-manifest.json

Task 8: CREATE examples/sample-project/
  - IMPLEMENT: Complete example of integrated boilerplate
  - ADD: .boilerplate-version file with version tracking
  - ADD: Project-specific customizations in .claude/project/
  - ADD: README showing the workflow
  - PLACEMENT: examples/sample-project/

Task 9: CREATE docs/SYNCHRONIZATION.md
  - IMPLEMENT: Complete user documentation
  - ADD: Installation instructions
  - ADD: Update workflow
  - ADD: Troubleshooting section
  - ADD: Migration guide from current structure
  - PLACEMENT: docs/SYNCHRONIZATION.md

Task 10: MODIFY .gitignore
  - ADD: .claude/build/ to ignore generated files
  - ADD: CLAUDE.md if it becomes generated
  - ADD: *.backup.* for backup files
  - PRESERVE: Existing ignore patterns
```

### Implementation Patterns & Key Details

```bash
# Shell script header pattern (all scripts)
#!/usr/bin/env bash
set -euo pipefail

# Color setup (from Homebrew patterns)
setup_colors() {
    if [[ -t 1 ]] && command -v tput >/dev/null 2>&1; then
        RED=$(tput setaf 1)
        GREEN=$(tput setaf 2)
        BLUE=$(tput setaf 4)
        BOLD=$(tput bold)
        RESET=$(tput sgr0)
    else
        RED="" GREEN="" BLUE="" BOLD="" RESET=""
    fi
}

# OS detection pattern
detect_os() {
    case "$OSTYPE" in
        darwin*) OS="macOS" ;;
        linux*)  OS="Linux" ;;
        *)       abort "Unsupported OS: $OSTYPE" ;;
    esac
}

# Git subtree add pattern (init-boilerplate.sh)
git remote add -f cc-boilerplate https://github.com/user/cc-boilerplate.git
git subtree add --prefix=.claude/boilerplate cc-boilerplate main --squash

# Git subtree pull pattern (update-boilerplate.sh)
git fetch cc-boilerplate main
git subtree pull --prefix=.claude/boilerplate cc-boilerplate main --squash

# JSON merge pattern with jq (build-config.sh)
jq -s '.[0] * .[1]' base.json project.json > merged.json

# Markdown merge pattern (build-config.sh)
merge_markdown() {
    local base="$1" project="$2" output="$3"
    # Extract sections using sed/awk based on markers
    # Combine preserving project sections
}

# Atomic file replacement pattern
safe_replace() {
    local target="$1" content="$2"
    local tmpfile=$(mktemp "${target}.tmp.XXXXXX")
    echo "$content" > "$tmpfile"
    mv "$tmpfile" "$target"
}
```

### Integration Points

```yaml
VERSION_TRACKING:
  - file: .boilerplate-version
  - format: {"version": "1.0.0", "commit": "abc123", "date": "2024-01-15"}
  - update: After each successful pull

BACKWARDS_COMPATIBILITY:
  - maintain: Symlinks from root to boilerplate/ initially
  - deprecate: After 2 minor versions
  - document: Migration path in SYNCHRONIZATION.md

CI/CD:
  - add to: .github/workflows/
  - test: Initialization and update scripts
  - validate: Merged configurations
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Validate shell scripts
shellcheck scripts/*.sh

# Check file permissions
ls -la scripts/*.sh | grep -E '^-rwxr-xr-x'

# Validate JSON files
jq empty boilerplate/.boilerplate-manifest.json
jq empty boilerplate/.claude/settings.template.json

# Expected: Zero errors, all scripts executable
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test init script in temporary directory
TMPDIR=$(mktemp -d)
cd "$TMPDIR"
git init
../../scripts/init-boilerplate.sh
test -d .claude/boilerplate || echo "FAIL: boilerplate not created"
test -f .boilerplate-version || echo "FAIL: version file not created"
cd -
rm -rf "$TMPDIR"

# Test build-config script
./scripts/build-config.sh --dry-run
test -f CLAUDE.md || echo "FAIL: CLAUDE.md not generated"
test -f .claude/settings.json || echo "FAIL: settings.json not generated"

# Test update script (requires existing setup)
./scripts/update-boilerplate.sh --dry-run
```

### Level 3: Integration Testing (System Validation)

```bash
# Full workflow test
cd examples/sample-project

# Initialize
../../scripts/init-boilerplate.sh

# Add customization
echo "# Project Specific" >> CLAUDE.project.md

# Build configs
../../scripts/build-config.sh

# Verify merge
grep "Project Specific" CLAUDE.md || echo "FAIL: Custom content not merged"

# Simulate update
git tag v1.0.1 # In cc-boilerplate
../../scripts/update-boilerplate.sh

# Verify version
grep '"version": "1.0.1"' .boilerplate-version || echo "FAIL: Version not updated"
```

### Level 4: Creative & Domain-Specific Validation

```bash
# Test conflict resolution
# Create intentional conflict
echo "conflict" > .claude/boilerplate/test.txt
git add . && git commit -m "Local change"
# In cc-boilerplate
echo "different" > boilerplate/test.txt
git add . && git commit -m "Upstream change"

# Run update - should handle gracefully
./scripts/update-boilerplate.sh
# Verify backup exists
ls .claude/boilerplate.backup.* || echo "FAIL: No backup created"

# Test OS compatibility
docker run -it ubuntu:latest bash -c "cd /project && ./scripts/init-boilerplate.sh"
docker run -it alpine:latest sh -c "cd /project && ./scripts/init-boilerplate.sh"

# Performance test with large configs
time ./scripts/build-config.sh

# Test rollback mechanism
./scripts/update-boilerplate.sh --simulate-failure
# Verify state restored
```

## Final Validation Checklist

### Technical Validation

- [ ] All 4 validation levels completed successfully
- [ ] Shell scripts pass shellcheck
- [ ] JSON/YAML files valid
- [ ] Git subtree operations work correctly
- [ ] Merge operations preserve customizations

### Feature Validation

- [ ] Can initialize in new project
- [ ] Can initialize in existing project
- [ ] Updates pull without conflicts
- [ ] Customizations preserved after update
- [ ] Version tracking accurate
- [ ] Rollback works on failure

### Code Quality Validation

- [ ] Scripts follow shell best practices
- [ ] Error handling comprehensive
- [ ] Atomic file operations used
- [ ] Clear user feedback provided
- [ ] Documentation complete

### Documentation & Deployment

- [ ] SYNCHRONIZATION.md complete with examples
- [ ] Migration guide from current structure
- [ ] Examples demonstrate all workflows
- [ ] README.md updated with new structure

---

## Anti-Patterns to Avoid

- ❌ Don't use git submodules - more complex than subtree
- ❌ Don't modify files in .claude/boilerplate/ directly
- ❌ Don't skip --squash flag - causes history pollution
- ❌ Don't use which or type - use command -v
- ❌ Don't hardcode paths - use relative or configurable
- ❌ Don't ignore OS differences - test on both macOS and Linux
