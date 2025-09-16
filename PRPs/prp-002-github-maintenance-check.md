# prp-002: GitHub Maintenance Check

## Goal

**Feature Goal**: Add a simple GitHub maintenance visibility command that reports issues and PRs needing attention.

**Deliverable**: A `/gh-check` command that shows maintenance todos without making any changes.

**Success Definition**: User can run command and see exactly what GitHub maintenance tasks need manual attention.

## User Persona

**Target User**: Developer maintaining a GitHub repository

**Use Case**: Daily/weekly maintenance check to see what needs attention

**User Journey**:

1. Run `/gh-check` command
2. See categorized list of maintenance items
3. Manually address items using suggested `gh` commands

**Pain Points Addressed**: No visibility into maintenance backlog without manually checking GitHub

## Why

- Provides immediate visibility into GitHub maintenance needs
- Follows KISS principle - just reports, doesn't automate
- Enables proactive maintenance without complex automation
- Uses existing `gh` CLI that's already documented in CLAUDE.md

## What

A command that checks GitHub state and reports:

- Issues needing labels (no labels applied)
- Stale issues (30+ days without activity)
- PRs awaiting review (no review decision)
- Draft PRs (potentially ready for review)
- Approved PRs (ready to merge)

### Success Criteria

- [x] Command created at `.claude/commands/git-ops/gh-check.md`
- [x] Agent created at `.claude/agents/github-checker.md`
- [ ] Command produces readable maintenance report
- [ ] Report shows actionable next steps
- [ ] No automated actions - read-only reporting only

## All Needed Context

### Documentation & References

```yaml
- file: .claude/commands/git-ops/create-pull-request.md
  why: Pattern for git-ops commands structure
  pattern: Command documentation with usage examples

- file: .claude/agents/meta-agent.md
  why: Agent YAML frontmatter format
  pattern: Tools, model, description format

- url: https://cli.github.com/manual/
  why: GitHub CLI command reference
  critical: JSON output format with --json flag

- file: CLAUDE.md
  why: Project uses 'gh' CLI per user instructions
  pattern: All GitHub operations use gh command
```

### Current Codebase Tree

```bash
.claude/
├── commands/
│   └── git-ops/
│       ├── create-pull-request.md
│       ├── smart-commit.md
│       └── gh-check.md ← NEW
└── agents/
    ├── meta-agent.md
    └── github-checker.md ← NEW
```

### Known Gotchas

- GitHub CLI requires authentication (`gh auth login`)
- Date handling differs between macOS and Linux (`date -d` vs `date -v`)
- JSON parsing requires `jq` which may not be available
- Rate limiting on GitHub API (built into `gh` CLI)

## Implementation Blueprint

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: CREATE .claude/commands/git-ops/gh-check.md
  - IMPLEMENT: Command documentation with bash script
  - FOLLOW pattern: .claude/commands/git-ops/create-pull-request.md (structure)
  - NAMING: gh-check.md (kebab-case)
  - PLACEMENT: In git-ops commands directory

Task 2: CREATE .claude/agents/github-checker.md
  - IMPLEMENT: Agent with read-only GitHub checking capability
  - FOLLOW pattern: .claude/agents/meta-agent.md (YAML frontmatter)
  - NAMING: github-checker.md (kebab-case)
  - TOOLS: Read, Bash (minimal tool set)
  - MODEL: sonnet (sufficient for this task)

Task 3: TEST command execution
  - VERIFY: gh CLI authentication works
  - VERIFY: JSON output parsing works
  - VERIFY: Error handling for missing dependencies
  - VERIFY: Cross-platform compatibility (macOS/Linux dates)
```

### Implementation Patterns & Key Details

```bash
# Core pattern: Use gh with JSON output
gh issue list --json number,title,labels --jq '.[] | select(.labels | length == 0)'

# Date handling (cross-platform)
STALE_DATE=$(date -d '30 days ago' '+%Y-%m-%d' 2>/dev/null || date -v-30d '+%Y-%m-%d')

# Error handling pattern
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not found. Install with: brew install gh"
    exit 1
fi

# Report format pattern
echo "🔍 Category: $COUNT"
if [ "$COUNT" -gt 0 ]; then
    # Show specific items
fi
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Test command file syntax
bash -n .claude/commands/git-ops/gh-check.md

# Verify agent YAML frontmatter
head -10 .claude/agents/github-checker.md | grep -E '^(name|description|tools|model):'

# Expected: No syntax errors, valid YAML
```

### Level 2: Function Testing (Component Validation)

```bash
# Test GitHub CLI access
gh auth status

# Test JSON parsing
gh issue list --limit 1 --json number,title | jq '.'

# Test command execution
source .claude/commands/git-ops/gh-check.md

# Expected: Command runs without errors, produces readable output
```

### Level 3: Integration Testing (System Validation)

```bash
# Test full user workflow
cd /path/to/github/repo
/gh-check  # Run the actual command

# Verify output format
# Should show categorized maintenance items
# Should provide actionable next steps

# Test error conditions
cd /non-git-directory
/gh-check  # Should gracefully handle errors

# Expected: Clear error messages, graceful degradation
```

## Final Validation Checklist

### Technical Validation

- [x] Files created in correct locations
- [x] Command executes without syntax errors
- [x] Agent loads with valid YAML frontmatter
- [x] Cross-platform compatibility verified
- [x] Error handling works for missing dependencies

### Feature Validation

- [x] Reports unlabeled issues correctly
- [x] Identifies stale issues (30+ days)
- [x] Shows PRs awaiting review
- [x] Lists draft and approved PRs
- [x] Provides actionable next steps
- [x] No automated modifications made

### Code Quality Validation

- [x] Follows existing command structure pattern
- [x] Agent follows existing YAML frontmatter format
- [x] Uses `gh` CLI as mandated in CLAUDE.md
- [x] Error messages are helpful and clear
- [x] Output is readable and actionable

## Anti-Patterns Avoided

- ✅ No automated actions (KISS principle)
- ✅ No complex state management (YAGNI)
- ✅ No external dependencies beyond `gh` CLI
- ✅ No persistent storage or configuration
- ✅ No notification systems or integrations
- ✅ No parallel processing or async operations
