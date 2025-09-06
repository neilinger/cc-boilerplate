# DELETE_FILE_CONTENT

## Overview

Based on [ADR-001 (Branching Strategy)](adr/ADR-001-branching-strategy.md), we implement different protection levels for each branch type:

- **`main`**: Maximum protection - production code
- **`release/**`**: Medium protection - allow stabilization 
- **`feature/**`**: Minimal protection - development freedom

## GitHub Repository Setup

### Step 1: Access Branch Protection Settings

1. Navigate to your GitHub repository
2. Go to **Settings** > **Branches**
3. Click **Add rule** for each branch type

### Step 2: Main Branch Protection

**Branch name pattern**: `main`

**Protection settings to enable**:
- ✅ **Require a pull request before merging**
  - ✅ **Require approvals**: 1 (or more for team)
  - ✅ **Dismiss stale PR approvals when new commits are pushed**
  - ✅ **Require review from code owners** (if CODEOWNERS file exists)
- ✅ **Require status checks to pass before merging**
  - ✅ **Require branches to be up to date before merging**
  - **Required status checks**:
    - `Comprehensive Test Suite` (from ci-cd.yml)
    - `Enhanced Validation` (for PRs)
- ✅ **Require conversation resolution before merging**
- ✅ **Require signed commits** (recommended)
- ✅ **Require linear history**
- ✅ **Include administrators**
- ✅ **Restrict pushes that create files** (optional)
- ✅ **Restrict force pushes**
- ✅ **Allow deletion** ❌ (disabled - protect production)

**Rationale**: Maximum protection for production-ready code. All changes must go through PR review and comprehensive testing.

### Step 3: Release Branch Protection  

**Branch name pattern**: `release/**`

**Protection settings to enable**:
- ✅ **Require status checks to pass before merging**
  - ✅ **Require branches to be up to date before merging**
  - **Required status checks**:
    - `Comprehensive Test Suite` (from ci-cd.yml)
- ✅ **Require conversation resolution before merging**
- ❌ **Require a pull request before merging** (disabled - allow direct commits for stabilization)
- ❌ **Restrict force pushes** (disabled - allow force push for release stabilization)
- ✅ **Allow deletion** ✅ (enabled - clean up old releases)

**Rationale**: Moderate protection allowing release stabilization while ensuring comprehensive test validation.

### Step 4: Feature Branch Protection (Optional)

**Branch name pattern**: `feature/**`

**Protection settings to enable**:
- ✅ **Require status checks to pass before merging**
  - **Required status checks**:
    - `Security Critical Tests` (from ci-cd.yml)
- ❌ **All other protections disabled**
- ✅ **Allow deletion** ✅ (enabled - clean up completed features)

**Rationale**: Minimal protection for development freedom, but security validation required.

## GitHub CLI Setup (Alternative)

Use `gh` CLI for scripted setup:

```bash
# Main branch protection
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["Comprehensive Test Suite","Enhanced Validation"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
  --field restrictions=null \
  --field allow_force_pushes=false \
  --field allow_deletions=false

# Release branch protection pattern
gh api repos/:owner/:repo/branches/release/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["Comprehensive Test Suite"]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews=null \
  --field restrictions=null \
  --field allow_force_pushes=true \
  --field allow_deletions=true

# Feature branch protection pattern  
gh api repos/:owner/:repo/branches/feature/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["Security Critical Tests"]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews=null \
  --field restrictions=null \
  --field allow_force_pushes=true \
  --field allow_deletions=true
```

## Repository Permissions

### Team Permissions (if applicable)

**Maintainers/Owners**:
- Can push to `release/**` branches
- Can force push for release stabilization
- Can delete old release branches
- Can bypass protection rules in emergencies

**Developers/Contributors**:
- Can create `feature/**` branches
- Can push to own feature branches
- Must create PRs to `main`
- Cannot force push to `main`

**External Contributors**:
- Can fork and create PRs
- All changes must go through review
- Cannot push directly to any protected branch

### Code Owners (Optional)

Create `.github/CODEOWNERS` file:

```
# Global code owners
* @username

# Critical security components
.claude/hooks/ @username @security-reviewer
tests/test_safety_hooks.py @username @security-reviewer

# CI/CD configuration
.github/workflows/ @username @devops-reviewer

# Architecture decisions
docs/adr/ @username @architecture-reviewer
```

## Status Check Requirements

### Required Checks by Branch

| Branch Pattern | Required Status Checks | Timeout |
|---------------|------------------------|---------|
| `main` | Comprehensive Test Suite, Enhanced Validation | 20min |
| `release/**` | Comprehensive Test Suite | 15min |
| `feature/**` | Security Critical Tests | 5min |

### Check Configuration in GitHub

1. Go to **Settings** > **Branches**
2. Edit branch protection rule
3. Under **Require status checks**, add:
   - Check name exactly as it appears in `.github/workflows/ci-cd.yml`
   - Job names: `Security Critical Tests`, `Comprehensive Test Suite`, `Enhanced Validation`

### Troubleshooting Status Checks

**Check not appearing in list**:
1. Ensure workflow has run at least once on the branch
2. Verify job names match exactly (case-sensitive)
3. Check workflow trigger conditions

**Check failing unexpectedly**:
1. Review workflow logs in Actions tab
2. Verify required environment variables/secrets
3. Check test dependencies and setup

**Check timeout**:
1. Increase `timeout-minutes` in workflow
2. Optimize test execution time
3. Consider splitting large test suites

## Emergency Procedures

### Bypassing Protection (Emergencies Only)

**Main branch emergency fix**:
```bash
# Create hotfix branch from main
git checkout main
git checkout -b hotfix/emergency-fix

# Make minimal fix
git commit -m "fix: emergency security patch"

# Create PR with EMERGENCY label
gh pr create --label "EMERGENCY" --title "Emergency: Critical security fix"
```

**Release branch emergency fix**:
```bash
# Direct push allowed on release branches
git checkout release/v1.2.0
git commit -m "fix: critical issue in release"
git push origin release/v1.2.0  # Will run comprehensive tests
```

### Recovery Procedures

**Accidentally deleted main branch**:
1. Find latest commit hash: `git log --oneline -n 10`
2. Recreate branch: `git checkout -b main <commit-hash>`
3. Force push: `git push --force-with-lease origin main`
4. Re-apply branch protection rules

**Failed merge to main**:
1. Revert the merge: `git revert -m 1 <merge-commit-hash>`
2. Fix issues in feature/release branch
3. Create new PR with fixes

## Monitoring and Maintenance

### Weekly Review Checklist

- [ ] Review failed status checks and address issues
- [ ] Clean up old feature branches
- [ ] Archive completed release branches
- [ ] Update required status checks if workflow changes
- [ ] Review and approve pending PRs

### Monthly Review Checklist

- [ ] Audit branch protection rules
- [ ] Review team permissions
- [ ] Update CODEOWNERS if team changes
- [ ] Analyze CI/CD performance and costs
- [ ] Update protection strategy documentation

### Quarterly Review Checklist

- [ ] Evaluate branching strategy effectiveness
- [ ] Review and update ADRs
- [ ] Consider protection rule optimizations
- [ ] Team training on workflow changes
- [ ] Performance metrics analysis

## Integration with Development Workflow

This branch protection strategy integrates with:

- **[Development Workflow](DEVELOPMENT.md)**: Day-to-day development process
- **[ADR-001](adr/ADR-001-branching-strategy.md)**: Branching strategy decisions
- **[ADR-002](adr/ADR-002-cicd-pipeline.md)**: CI/CD pipeline configuration  
- **[ADR-003](adr/ADR-003-testing-strategy.md)**: Testing strategy and priorities

## Best Practices

### Do's ✅
- Always require status checks on protected branches
- Use meaningful commit messages for emergency fixes
- Document any temporary protection rule changes
- Regular cleanup of old branches
- Monitor CI/CD performance and costs

### Don'ts ❌
- Don't bypass protection rules without documentation
- Don't disable required status checks without team approval
- Don't force push to main branch (ever)
- Don't leave broken status checks unfixed
- Don't create long-lived feature branches

### Security Considerations

- **API keys**: Never commit secrets to any branch
- **Dangerous commands**: All branches validate against dangerous patterns
- **Code review**: Main branch always requires human review
- **Audit trail**: All protection changes logged in repository settings
- **Emergency access**: Document and justify any emergency bypasses

This branch protection strategy ensures code quality, security, and development velocity while maintaining the flexibility needed for effective Release Flow development.