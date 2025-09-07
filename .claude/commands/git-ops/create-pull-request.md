# Create Pull Request - Release Flow

Create a well-structured pull request following the Release Flow branching strategy (ADR-001).

## PR Title (if provided)

$ARGUMENTS

## Release Flow Process

Follows the workflow: `feature/* → release/* → main`

### 1. **Branch Type Detection & Validation**

   ```bash
   # Check current branch and determine PR flow
   CURRENT_BRANCH=$(git branch --show-current)
   echo "Current branch: $CURRENT_BRANCH"

   # Validate branch naming convention
   case $CURRENT_BRANCH in
     feature/*)
       echo "✅ Feature branch detected - will target release branch"
       TARGET_TYPE="release"
       ;;
     release/*)
       echo "✅ Release branch detected - will target main"
       TARGET_TYPE="main"
       ;;
     hotfix/*)
       echo "🚨 Hotfix branch detected - will target main"
       TARGET_TYPE="main"
       ;;
     main)
       echo "❌ Cannot create PR from main branch"
       exit 1
       ;;
     *)
       echo "⚠️ Non-standard branch name: $CURRENT_BRANCH"
       echo "Expected: feature/, release/, or hotfix/"
       ;;
   esac
   ```

### 2. **Determine Target Branch**

   ```bash
   if [[ $CURRENT_BRANCH == feature/* ]]; then
     # Find or create appropriate release branch
     echo "Available release branches:"
     git branch -r | grep "origin/release/" || echo "No existing release branches"

     # Suggest version based on changes
     echo "Create release branch? (e.g., release/v1.1.0)"
     read -p "Enter release version or existing release branch: " RELEASE_BRANCH

     if [[ ! $RELEASE_BRANCH == release/* ]]; then
       RELEASE_BRANCH="release/$RELEASE_BRANCH"
     fi

     TARGET_BRANCH="$RELEASE_BRANCH"
   elif [[ $CURRENT_BRANCH == release/* ]] || [[ $CURRENT_BRANCH == hotfix/* ]]; then
     TARGET_BRANCH="main"
   fi

   echo "Target branch: $TARGET_BRANCH"
   ```

### 3. **Review Changes**

   ```bash
   # See what will be included
   git status

   # Show changes since branch point
   if [[ $TARGET_BRANCH == "main" ]]; then
     git diff main...HEAD --stat
     git log --oneline main..HEAD
   else
     # For feature branches, show all changes
     git diff HEAD~$(git rev-list --count HEAD ^main)...HEAD --stat
     git log --oneline main..HEAD
   fi
   ```

### 4. **Create Release Branch (if needed)**

   ```bash
   # Only if targeting a new release branch
   if [[ $CURRENT_BRANCH == feature/* ]] && [[ ! $(git branch -r | grep "origin/$TARGET_BRANCH") ]]; then
     echo "Creating new release branch: $TARGET_BRANCH"
     git checkout -b "$TARGET_BRANCH"
     git push -u origin "$TARGET_BRANCH"

     # Return to feature branch for PR creation
     git checkout "$CURRENT_BRANCH"
   fi
   ```

### 5. **Ensure Branch is Pushed**

   ```bash
   # Ensure current branch is pushed to remote
   git push -u origin HEAD
   ```

### 6. **Validate Commits**

- Commits should be logical and atomic
- Follow conventional commits format:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation
  - `test:` for tests
  - `refactor:` for refactoring
- Follow KISS/YAGNI principles (no unnecessary complexity)
- Include Claude Code attribution per project standards

### 7. **Create PR with Branch-Specific Template**

   ```bash
   # Generate appropriate PR based on branch type
   if [[ $CURRENT_BRANCH == feature/* ]]; then
     # Feature → Release PR
     gh pr create \
       --base "$TARGET_BRANCH" \
       --head "$CURRENT_BRANCH" \
       --title "$ARGUMENTS" \
       --body "$(cat <<'EOF'
## Summary
[Brief description of what this feature implements]

## Changes
- [List key changes]
- [Reference PRP/ADR if applicable]

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation update
- [ ] Testing infrastructure

## Implementation Details
- [Technical details about the implementation]
- [Architecture decisions made]
- [Any dependencies or prerequisites]

## Testing
- [ ] All tests pass locally (`./scripts/run_tests.sh`)
- [ ] Added new tests for new functionality
- [ ] Manual testing completed
- [ ] CI/CD pipeline tests pass

## Documentation
- [ ] Updated relevant documentation
- [ ] Added/updated ADRs if architectural changes
- [ ] README updated if user-facing changes

## Checklist
- [ ] Follows KISS/YAGNI principles
- [ ] Code follows project conventions
- [ ] Self-reviewed the changes
- [ ] No debug code or console.logs
- [ ] Addresses all requirements from PRP (if applicable)

## Related Documents
- PRP: [Link to relevant PRP if applicable]
- ADR: [Link to relevant ADRs]
- Issues: [Link to related issues]

## Additional Context
[Any extra information reviewers should know]
EOF
)"

   elif [[ $CURRENT_BRANCH == release/* ]]; then
     # Release → Main PR
     VERSION=$(echo $CURRENT_BRANCH | sed 's/release\///')
     gh pr create \
       --base "main" \
       --head "$CURRENT_BRANCH" \
       --title "Release $VERSION: $ARGUMENTS" \
       --body "$(cat <<EOF
## Release $VERSION

### 🎯 Major Features
- [List major features in this release]

### 🐛 Bug Fixes
- [List important bug fixes]

### 📋 Included PRs
- [List PRs merged into this release branch]

### ✅ Release Checklist
- [ ] All tests passing (Security Critical, Comprehensive, Enhanced Validation)
- [ ] Documentation updated and reviewed
- [ ] CHANGELOG updated (if applicable)
- [ ] Version bumped in relevant files
- [ ] Release branch stabilized and tested
- [ ] Breaking changes documented
- [ ] Migration guide provided (if needed)

### 📊 Release Statistics
- Files changed: [number]
- Lines added/removed: [stats]
- New tests: [number]
- Documentation updates: [list]

### 🏷️ Post-Merge Actions
- [ ] Tag release as $VERSION
- [ ] Update release notes
- [ ] Clean up merged feature branches
- [ ] Notify stakeholders

### 🔒 Security & Compliance
- [ ] Security review completed
- [ ] No secrets or credentials committed
- [ ] Dangerous command validation passes
- [ ] Branch protection rules respected
EOF
)"

   elif [[ $CURRENT_BRANCH == hotfix/* ]]; then
     # Hotfix → Main PR
     gh pr create \
       --base "main" \
       --head "$CURRENT_BRANCH" \
       --title "🚨 HOTFIX: $ARGUMENTS" \
       --label "hotfix,priority-high" \
       --body "$(cat <<'EOF'
## 🚨 Emergency Hotfix

### Issue Description
[Describe the critical issue being fixed]

### Root Cause
[Brief explanation of what caused the issue]

### Solution
[Explain the fix implemented]

### Impact Assessment
- **Severity**: [Critical/High/Medium]
- **Affected Systems**: [List what this impacts]
- **User Impact**: [How this affects users]

### Testing
- [ ] Fix verified in production-like environment
- [ ] Regression testing completed
- [ ] No additional issues introduced

### Emergency Checklist
- [ ] Minimal change scope (only what's needed)
- [ ] Thoroughly tested
- [ ] Stakeholders notified
- [ ] Documentation updated
- [ ] Post-deployment monitoring plan ready

### Follow-up Actions
- [ ] Schedule post-mortem
- [ ] Update processes to prevent recurrence
- [ ] Backport to release branches if needed
EOF
)"
   fi
   ```

### 8. **Post-Creation Tasks**

   ```bash
   # Add appropriate labels based on branch type
   if [[ $CURRENT_BRANCH == feature/* ]]; then
     gh pr edit --add-label "feature,needs-review"
   elif [[ $CURRENT_BRANCH == release/* ]]; then
     gh pr edit --add-label "release,needs-review,major"
   elif [[ $CURRENT_BRANCH == hotfix/* ]]; then
     gh pr edit --add-label "hotfix,priority-high,needs-review"
   fi

   # Request reviewers if configured
   # gh pr edit --add-reviewer "username"

   # Link to related issues/PRPs
   echo "PR created successfully!"
   echo "Don't forget to:"
   echo "- Link related issues in PR description"
   echo "- Request appropriate reviewers"
   echo "- Monitor CI/CD pipeline status"
   ```

## Release Flow Best Practices

### Feature → Release PRs

- Focus on specific feature/PRP implementation
- Include comprehensive testing
- Reference relevant PRP/ADR documents
- Ensure all PRP success criteria met

### Release → Main PRs

- Comprehensive release overview
- List all included features/fixes
- Complete release checklist
- Plan post-merge tagging and cleanup

### Emergency Hotfixes

- Minimal scope changes only
- Thorough impact assessment
- Immediate stakeholder notification
- Plan follow-up process improvements

## Branch Protection Compliance

- **main**: Requires PR review + comprehensive tests
- **release/***: Requires comprehensive tests (allows direct commits)
- **feature/***: Requires security critical tests

Refer to [Branch Protection Guide](../../docs/guides/branch-protection.md) and [ADR-001 Branching Strategy](../../docs/adr/adr-001-branching-strategy.md) for complete details.
