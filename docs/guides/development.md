# Development Workflow

This document describes the development workflow for cc-boilerplate following Release Flow branching strategy and priority-based testing.

## Quick Reference

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Work on feature with security validation
git push origin feature/your-feature-name  # Runs security tests (~30s)

# Create release branch
git checkout -b release/v1.1.0

# Merge feature into release
git checkout release/v1.1.0
git merge feature/your-feature-name
git push origin release/v1.1.0  # Runs comprehensive tests (~5-7min)

# Create PR to main (enhanced validation)
gh pr create --base main --title "Release v1.1.0"  # Runs enhanced tests (~7-10min)

# Merge to main triggers deployment and tagging
```

## Branch Strategy Overview

Our workflow uses **Release Flow** with three branch types:

- **`feature/**`** - Development work, fast security feedback
- **`release/**`** - Stabilization and comprehensive testing
- **`main`** - Production-ready code with deployment automation

## Detailed Workflow

### 1. Feature Development

**Purpose**: Implement new features with fast security feedback

```bash
# Start from latest main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/descriptive-name
# Examples: feature/tts-fallback, feature/prp-validation

# Develop your feature
# ... make changes ...

# Commit with security validation
git add .
git commit -m "feat: implement TTS provider fallback"
git push origin feature/descriptive-name
```

**CI/CD**: Runs **security-critical tests only** (~30 seconds)

- Safety hooks (dangerous command detection)
- Hook integration pipeline tests
- PRP edge case security validation

✅ **Success**: Fast feedback, ready for release branch integration
❌ **Failure**: Security issue must be fixed before proceeding

### 2. Release Preparation

**Purpose**: Stabilize features and run comprehensive validation

```bash
# Create release branch from main
git checkout main
git pull origin main
git checkout -b release/v1.2.0

# Merge completed features
git merge feature/feature-1
git merge feature/feature-2

# Push for comprehensive testing
git push origin release/v1.2.0
```

**CI/CD**: Runs **comprehensive test suite** (~5-7 minutes)

- All security-critical tests
- Feature reliability tests (TTS providers)
- Coverage reporting
- Performance validation

✅ **Success**: Ready for main branch and production
❌ **Failure**: Fix issues in release branch or remove problematic features

### 3. Production Release

**Purpose**: Deploy stable code and create official release

```bash
# Create pull request to main
gh pr create --base main --title "Release v1.2.0" --body "
## Release v1.2.0

### Features
- New TTS provider fallback system
- Enhanced PRP validation
- Improved safety hooks

### Testing
- ✅ Security tests passed
- ✅ Integration tests passed
- ✅ Feature tests passed

### Breaking Changes
- None
"

# After PR approval and merge, automatic deployment runs:
# - Final test validation
# - Semantic version tagging
# - Release artifact creation
# - Badge updates
```

**CI/CD**: Runs **enhanced validation** (~7-10 minutes)

- Complete test suite
- Security scanning
- Dependency vulnerability checks
- Release notes validation

**Deployment**: Automatic on main branch push

- Creates semantic version tag (e.g., v1.2.0-20250109120000)
- Updates repository badges
- Generates release notes

## Testing Strategy

### Test Categories by Branch

| Branch Type | Tests Run | Duration | Purpose |
|-------------|-----------|----------|---------|
| `feature/**` | Security Critical | ~30s | Fast feedback |
| `release/**` | Comprehensive | ~5-7min | Quality assurance |
| PR to `main` | Enhanced | ~7-10min | Final validation |
| `main` push | Full + Deploy | ~3-5min | Production ready |

### Test Priorities

For detailed test categories and execution strategy, see [Testing Guide](testing.md#test-categories-and-priorities).

## Development Best Practices

### Before You Start

1. **Read ADRs**: Review [docs/adr/](../adr/) for architectural decisions
2. **Check CLAUDE.md**: Follow KISS/YAGNI principles
3. **Review test coverage**: Understand what needs testing

### During Development

1. **Small commits**: One logical change per commit
2. **Test locally**: Run `python tests/test_safety_hooks.py` before pushing
3. **Security first**: Never bypass safety validations
4. **Document decisions**: Create ADRs for significant choices

### Before Release

1. **Full test run**: Execute `python tests/run_all_tests.py`
2. **Manual validation**: Test key user scenarios
3. **Update documentation**: Keep README.md current
4. **Version planning**: Follow semantic versioning

### Documentation Standards

For markdown files (`.md`), the project uses automated linting to ensure quality and consistency.

#### Setup (First Time)

```bash
# Install pre-commit (using UV)
uv pip install pre-commit

# Install git hooks
pre-commit install

# Install VS Code extension (recommended)
# Search for "markdownlint" by David Anson in VS Code Extensions
```

#### Usage

```bash
# Automatic: Runs on every commit (fixes issues automatically)
git commit -m "docs: update API documentation"

# Manual: Check all markdown files
pre-commit run markdownlint --all-files

# Manual: Check specific file
markdownlint docs/reference/api.md --fix
```

#### Standards Enforced

- **File naming**: Use kebab-case (`api-guide.md` not `API_GUIDE.md`)
- **Exceptions**: `README.md`, `LICENSE`, `CHANGELOG.md` keep their standard names
- **Link formatting**: `[Setup Guide](setup-guide.md)` not `[here](setup-guide.md)`
- **Code blocks**: Specify language for syntax highlighting (```python,```bash)
- **Consistent lists**: Use either `*` or `-` throughout document

#### Configuration

Project uses `.markdownlint.json` with pragmatic rules:

- No line length limits (let editors wrap)
- Allow HTML when needed
- Focus on real quality issues, not pedantic formatting

## Repository Structure

```
cc-boilerplate/
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # Branch-specific CI/CD pipeline
├── docs/
│   ├── adr/                    # Architecture Decision Records
│   │   ├── adr-001-branching-strategy.md
│   │   ├── adr-002-cicd-pipeline.md
│   │   └── adr-003-testing-strategy.md
│   └── development.md          # This file
├── tests/
│   ├── test_safety_hooks.py    # 🔴 Security critical
│   ├── test_hook_integration.py # 🔴 Security critical
│   ├── test_prp_edge_cases.py  # 🔴 Security critical
│   ├── test_tts_providers.py   # 🟡 Feature reliability
│   └── run_all_tests.py        # Test orchestrator
└── [project files...]
```

## Common Scenarios

### Hot Fix

```bash
# Critical bug found in production
git checkout main
git checkout -b hotfix/v1.2.1

# Fix the bug
# ... make minimal changes ...

git commit -m "fix: resolve critical safety hook bypass"
git push origin hotfix/v1.2.1

# Create PR directly to main (skip release branch for urgency)
gh pr create --base main --title "Hotfix v1.2.1 - Critical security fix"
```

### Multiple Features in Parallel

```bash
# Developer A
git checkout -b feature/tts-enhancement

# Developer B
git checkout -b feature/new-hook

# Both work independently, merge to same release branch
git checkout release/v1.3.0
git merge feature/tts-enhancement
git merge feature/new-hook
```

### Failed Release Branch

```bash
# If release/v1.2.0 tests fail badly
git checkout main
git checkout -b release/v1.2.1  # New release branch

# Cherry-pick only working features
git cherry-pick feature/working-feature
# Skip the broken feature for now
```

## Badge System

The README badges reflect current status:

- **CI/CD Status**: Overall workflow health
- **Security Tests**: Safety hook validation status
- **Test Coverage**: Current coverage percentage
- **Hooks/Agents/Styles**: Static count badges
- **Release**: Latest version tag
- **License**: Project license

Update badges by editing the README.md links after repository setup.

## Troubleshooting

### Tests Failing on Feature Branch

- Only security tests run on feature branches
- Focus on safety hooks and dangerous command detection
- Check `.env` access patterns and JSON validation

### Comprehensive Tests Failing on Release

- Review all test categories (security + features)
- TTS provider tests may fail without API keys (acceptable)
- Check test timeout limits and performance

### Enhanced Validation Failing on PR

- Most comprehensive test suite runs
- Security scanning may flag new vulnerabilities
- Dependency checks may find outdated packages
- Manual review may be required

### Deployment Issues

- Check semantic versioning format
- Verify git credentials and permissions
- Review badge update automation
- Validate release notes generation

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

## Getting Help

1. **Review ADRs**: [docs/adr/](../adr/) explains architectural decisions
2. **Check test docs**: [Testing Guide](testing.md) for detailed test info
3. **KISS/YAGNI guidance**: [CLAUDE.md](../CLAUDE.md) for development principles
4. **Create issue**: Use GitHub issues for bugs or enhancement requests

Remember: **Security first, simplicity always, ship only what's needed now.**
