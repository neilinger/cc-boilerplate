# CC-Boilerplate Synchronization Guide

This guide explains how to use the cc-boilerplate synchronization system to maintain your Claude Code projects while keeping them up-to-date with boilerplate improvements.

## Overview

The cc-boilerplate synchronization system enables:

- **Graceful Updates**: Pull boilerplate improvements without losing customizations
- **Project Customization**: Add domain-specific instructions and settings
- **Version Tracking**: Know exactly which boilerplate version you're using
- **Conflict Resolution**: Automatic backup and rollback capabilities

## Architecture

### Three-Layer Configuration

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Base Layer     │    │  Project Layer   │    │  Merged Layer   │
│                 │    │                  │    │                 │
│ Boilerplate     │ +  │ Customizations   │ =  │ Final Config    │
│ Templates       │    │ (.claude/project)│    │ (Generated)     │
│ (.claude/       │    │                  │    │                 │
│  boilerplate)   │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Directory Structure

```
your-project/
├── .claude/
│   ├── boilerplate/              # Git subtree from cc-boilerplate
│   │   ├── .claude/              # Core boilerplate files
│   │   ├── templates/            # Template files with merge markers
│   │   └── scripts/              # Synchronization scripts
│   ├── project/                  # Your project customizations
│   │   ├── CLAUDE.project.md     # Domain-specific instructions
│   │   └── settings.project.json # Custom settings
│   ├── settings.json             # Generated: merged settings
│   └── build/                    # Build artifacts and backups
├── .boilerplate-version          # Version tracking
├── CLAUDE.md                     # Generated: merged instructions
└── scripts/ -> .claude/boilerplate/scripts/  # Symlink to scripts
```

## Quick Start

### 1. Initialize Boilerplate in New Project

```bash
# Clone or create your project
git init my-project
cd my-project

# Initialize cc-boilerplate
curl -sSL https://raw.githubusercontent.com/neilinger/cc-boilerplate/main/scripts/init-boilerplate.sh | bash
```

### 2. Initialize Boilerplate in Existing Project

```bash
cd your-existing-project

# Download and run initialization script
curl -sSL https://raw.githubusercontent.com/neilinger/cc-boilerplate/main/scripts/init-boilerplate.sh | bash
```

### 3. Customize for Your Domain

```bash
# Edit project-specific instructions
vim .claude/project/CLAUDE.project.md

# Edit custom settings
vim .claude/project/settings.project.json

# Build merged configurations
scripts/build-config.sh
```

### 4. Stay Updated

```bash
# Check for updates
scripts/update-boilerplate.sh --dry-run

# Apply updates
scripts/update-boilerplate.sh
```

## Detailed Usage

### Installation

#### Prerequisites

- Git 2.20+ with subtree support
- jq (for JSON manipulation)
- Bash 4.0+
- Optional: shellcheck, yq

#### macOS Installation

```bash
# Install requirements
brew install git jq

# Verify git subtree
git subtree --help
```

#### Linux Installation

```bash
# Ubuntu/Debian
sudo apt-get install git jq

# CentOS/RHEL
sudo yum install git jq
```

### Project Initialization

The `init-boilerplate.sh` script sets up the synchronization system:

```bash
# Interactive initialization
scripts/init-boilerplate.sh

# With custom repository
CC_BOILERPLATE_REPO="https://github.com/your-fork/cc-boilerplate.git" scripts/init-boilerplate.sh
```

#### What Gets Created

- `.claude/boilerplate/` - Git subtree with boilerplate files
- `.claude/project/` - Directory for your customizations
- `.boilerplate-version` - Version tracking file
- Generated configurations (CLAUDE.md, settings.json)

### Customization

#### Adding Project Instructions

Edit `.claude/project/CLAUDE.project.md`:

```markdown
<!-- Project-specific CLAUDE.md customizations -->
## Project-Specific Guidelines

- Use TypeScript for all new code
- Follow React Hooks patterns
- Database queries use Prisma ORM

## Domain-Specific Rules

### Authentication
- JWT tokens expire after 1 hour
- Refresh tokens valid for 30 days
- Use bcrypt for password hashing

### API Design
- Version all APIs (e.g., /api/v1/)
- Rate limiting: 1000 requests/hour per user
```

#### Adding Custom Settings

Edit `.claude/project/settings.project.json`:

```json
{
  "__PROJECT_CUSTOM_PERMISSIONS__": [
    "Bash(docker:*)",
    "Bash(npm run:*)",
    "WebFetch(domain:api.yourservice.com)"
  ],
  "__PROJECT_CUSTOM_SETTINGS__": {
    "projectName": "my-awesome-project",
    "outputStyle": "JSON Structured"
  },
  "__PROJECT_CUSTOM_HOOKS__": {
    "PreCommit": [{
      "type": "command",
      "command": "npm run lint:fix"
    }]
  }
}
```

### Building Configurations

The `build-config.sh` script merges templates with customizations:

```bash
# Build all configurations
scripts/build-config.sh

# Dry run to see what would be generated
scripts/build-config.sh --dry-run

# Verbose output
scripts/build-config.sh --verbose
```

#### Generated Files

- **CLAUDE.md** - Merged instructions with your domain rules
- **.claude/settings.json** - Merged Claude settings
- **.pre-commit-config.yaml** - Pre-commit configuration (if template exists)

### Updating Boilerplate

The `update-boilerplate.sh` script pulls improvements:

```bash
# Check what would be updated
scripts/update-boilerplate.sh --dry-run

# Update from current branch
scripts/update-boilerplate.sh

# Update from specific branch
scripts/update-boilerplate.sh --branch develop

# Force update (ignore uncommitted changes)
scripts/update-boilerplate.sh --force
```

#### Update Process

1. **Backup** current configuration
2. **Fetch** latest changes from cc-boilerplate
3. **Merge** using git subtree pull
4. **Rebuild** configurations
5. **Update** version tracking

#### Version Tracking

The `.boilerplate-version` file tracks:

```json
{
  "version": "1.2.3",
  "commit": "abc1234",
  "date": "2025-01-16",
  "branch": "main",
  "repository": "https://github.com/neilinger/cc-boilerplate.git",
  "previous_commit": "def5678",
  "updated_from": "1.2.2"
}
```

## Merge Strategies

### JSON Deep Merge

Settings files use deep merge with placeholder replacement:

```json
{
  "permissions": {
    "allow": [...],
    "__PROJECT_CUSTOM_PERMISSIONS__": []  // Replaced with your additions
  },
  "__PROJECT_CUSTOM_SETTINGS__": {}     // Merged with top-level
}
```

### Markdown Section Merge

CLAUDE.md uses HTML comment markers:

```markdown
<!-- BEGIN BOILERPLATE -->
Standard boilerplate instructions
<!-- END BOILERPLATE -->

<!-- BEGIN PROJECT -->
Your domain-specific instructions
<!-- END PROJECT -->
```

### YAML Append/Replace

Pre-commit configurations use simple replacement or append strategy.

## Troubleshooting

### Common Issues

#### Git Subtree Errors

**Problem**: "fatal: ambiguous argument 'cc-boilerplate/main'"

**Solution**:

```bash
git remote remove cc-boilerplate
git remote add -f cc-boilerplate https://github.com/neilinger/cc-boilerplate.git
```

#### Merge Conflicts

**Problem**: Update fails with merge conflicts

**Solution**:

```bash
# Automatic rollback should occur, but manually restore if needed
cp -r .claude/backups/backup_YYYYMMDD_HHMMSS/* .
```

#### Invalid JSON

**Problem**: Generated settings.json is invalid

**Solution**:

```bash
# Check your project customizations
jq empty .claude/project/settings.project.json

# Fix syntax errors and rebuild
scripts/build-config.sh
```

#### Missing Tools

**Problem**: "command not found: jq"

**Solution**:

```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# CentOS/RHEL
sudo yum install jq
```

### Recovery Procedures

#### Restore from Backup

```bash
# List available backups
ls -la .claude/backups/

# Restore specific backup
cp -r .claude/backups/backup_20250116_143022/* .
```

#### Reset to Clean State

```bash
# Remove all generated files
rm -f CLAUDE.md .claude/settings.json .pre-commit-config.yaml

# Rebuild from templates
scripts/build-config.sh
```

#### Reinitialize Boilerplate

```bash
# Remove existing boilerplate
rm -rf .claude/boilerplate
git remote remove cc-boilerplate

# Reinitialize
scripts/init-boilerplate.sh
```

### Debug Mode

Enable verbose logging:

```bash
# Set debug flag
export CC_BOILERPLATE_DEBUG=1

# Run with detailed output
scripts/update-boilerplate.sh --verbose
```

## Advanced Usage

### Custom Repository

Use your own fork of cc-boilerplate:

```bash
# Set custom repository
export CC_BOILERPLATE_REPO="https://github.com/yourorg/cc-boilerplate.git"

# Initialize with custom repo
scripts/init-boilerplate.sh
```

### Multi-Environment Setup

Different configurations for different environments:

```bash
# Development configuration
scripts/build-config.sh --env development

# Production configuration
scripts/build-config.sh --env production
```

### CI/CD Integration

Add to your GitHub Actions:

```yaml
name: Update Boilerplate
on:
  schedule:
    - cron: '0 9 * * MON'  # Weekly on Monday

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: scripts/update-boilerplate.sh --dry-run
      - name: Create PR if updates available
        # ... create PR logic
```

### Validation Hooks

Add validation to your update process:

```bash
#!/bin/bash
# .claude/hooks/post-update.sh

# Validate merged configuration
scripts/build-config.sh --validate

# Run tests
npm test

# Security scan
npm audit
```

## Migration Guide

### From Manual Configuration

If you currently maintain CLAUDE.md and settings.json manually:

1. **Backup** current files:

   ```bash
   cp CLAUDE.md CLAUDE.md.backup
   cp .claude/settings.json .claude/settings.json.backup
   ```

2. **Initialize** boilerplate:

   ```bash
   scripts/init-boilerplate.sh
   ```

3. **Extract** customizations:
   - Compare CLAUDE.md.backup with generated CLAUDE.md
   - Move project-specific content to `.claude/project/CLAUDE.project.md`
   - Extract custom settings to `.claude/project/settings.project.json`

4. **Rebuild** and test:

   ```bash
   scripts/build-config.sh
   ```

### From Git Submodules

If you currently use git submodules:

1. **Remove** existing submodule:

   ```bash
   git submodule deinit .claude/boilerplate
   git rm .claude/boilerplate
   ```

2. **Initialize** with subtree:

   ```bash
   scripts/init-boilerplate.sh
   ```

3. **Migrate** customizations as above

## Best Practices

### Version Pinning

Pin to specific boilerplate versions in production:

```bash
# Update to specific version
scripts/update-boilerplate.sh --branch v1.2.3
```

### Testing Updates

Always test updates in development first:

```bash
# Create test branch
git checkout -b test-boilerplate-update

# Update and test
scripts/update-boilerplate.sh
# ... run your tests

# Merge when satisfied
git checkout main
git merge test-boilerplate-update
```

### Customization Guidelines

- **Keep customizations minimal** - easier to maintain
- **Document custom settings** - add comments explaining why
- **Regular reviews** - periodically review if customizations are still needed
- **Share improvements** - contribute useful patterns back to boilerplate

### Security Considerations

- **Review permissions** - audit custom permissions regularly
- **Validate sources** - ensure boilerplate repository is trusted
- **Backup regularly** - automated backups are your friend

## Contributing

### Improving the Synchronization System

1. Fork cc-boilerplate repository
2. Make improvements to synchronization scripts
3. Test with multiple project types
4. Submit pull request with detailed description

### Sharing Customization Patterns

Share useful customization patterns:

- Domain-specific instruction templates
- Common permission sets
- Workflow automation hooks

## Support

### Getting Help

- **Documentation**: This guide and inline script help
- **Examples**: See `examples/sample-project/`
- **Issues**: [GitHub Issues](https://github.com/neilinger/cc-boilerplate/issues)

### Reporting Bugs

Include in bug reports:

- Operating system and version
- Git version (`git --version`)
- jq version (`jq --version`)
- Full error output
- Contents of `.boilerplate-version`

---

## Appendix

### File Reference

| File | Purpose | Generated |
|------|---------|-----------|
| `.claude/boilerplate/` | Core boilerplate files | No |
| `.claude/project/` | Project customizations | No |
| `.claude/settings.json` | Merged Claude settings | Yes |
| `CLAUDE.md` | Merged instructions | Yes |
| `.boilerplate-version` | Version tracking | No |
| `.claude/build/manifest.json` | Build metadata | Yes |

### Script Reference

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `init-boilerplate.sh` | Initialize synchronization | Once per project |
| `update-boilerplate.sh` | Pull boilerplate updates | Weekly/monthly |
| `build-config.sh` | Build merged configurations | After customization changes |

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `CC_BOILERPLATE_REPO` | Repository URL | `https://github.com/neilinger/cc-boilerplate.git` |
| `CC_BOILERPLATE_DEBUG` | Enable debug output | `false` |

This completes the comprehensive synchronization guide for cc-boilerplate.
