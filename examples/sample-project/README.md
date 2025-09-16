# Sample E-commerce Project

This is an example project demonstrating the cc-boilerplate synchronization system for a fictional e-commerce application.

## Project Structure

```
.
├── .claude/
│   ├── boilerplate/          # Git subtree from cc-boilerplate
│   │   ├── .claude/          # Core boilerplate configuration
│   │   ├── templates/        # Base templates
│   │   └── scripts/          # Synchronization scripts
│   └── project/              # Project-specific customizations
│       ├── CLAUDE.project.md        # Domain-specific instructions
│       └── settings.project.json   # Custom settings and permissions
├── .boilerplate-version      # Version tracking
└── README.md                 # This file
```

## Boilerplate Integration

This project demonstrates how to:

1. **Initialize boilerplate** in an existing project
2. **Customize configurations** for specific domain needs
3. **Maintain synchronization** with upstream boilerplate updates
4. **Preserve customizations** during updates

## Domain-Specific Customizations

### Payment Processing Rules

- PCI compliance requirements
- Stripe API integration
- Audit logging for financial transactions

### Data Protection

- GDPR compliance measures
- Encryption requirements
- User session management

### Development Workflow

- TypeScript enforcement
- Testing coverage requirements
- Deployment safety checks

## Synchronization Workflow

### Initial Setup

```bash
# From the cc-boilerplate repository
cd /path/to/sample-project
../../scripts/init-boilerplate.sh
```

### Daily Development

```bash
# Build current configuration
../../scripts/build-config.sh

# Generated files:
# - CLAUDE.md (merged instructions)
# - .claude/settings.json (merged settings)
```

### Receiving Updates

```bash
# Check for updates
../../scripts/update-boilerplate.sh --dry-run

# Apply updates
../../scripts/update-boilerplate.sh
```

## Generated Configuration Example

After running `build-config.sh`, this project generates:

### `CLAUDE.md`

Merges base boilerplate instructions with e-commerce specific rules like:

- Payment processing guidelines
- User data protection requirements
- API design standards
- Testing and deployment rules

### `.claude/settings.json`

Combines base permissions with project-specific additions:

- Docker and package manager permissions
- Stripe API access
- Custom status line for e-commerce metrics
- Deployment hooks for production safety

## Version Tracking

The `.boilerplate-version` file tracks:

- Current boilerplate version
- Source commit hash
- Last update timestamp
- Repository information

## Benefits Demonstrated

1. **Consistency**: Core development practices maintained across projects
2. **Flexibility**: Domain-specific rules added without conflicts
3. **Maintainability**: Updates flow smoothly from boilerplate
4. **Transparency**: Clear separation between base and custom configurations

## Testing Integration

This example shows integration with:

- Unit testing with Jest
- Integration testing for payment flows
- E2E testing with Cypress
- Security scanning in deployment pipeline

## Real-world Usage

In practice, you would:

1. Fork this example for your e-commerce project
2. Replace sample customizations with your actual requirements
3. Add real API endpoints and business logic
4. Maintain synchronization with cc-boilerplate updates

## File Customization Guide

### Adding New Instructions

Edit `.claude/project/CLAUDE.project.md`:

```markdown
## New Domain Rule
- Your specific requirement here
- Implementation guidelines
```

### Adding Permissions

Edit `.claude/project/settings.project.json`:

```json
{
  "__PROJECT_CUSTOM_PERMISSIONS__": [
    "Bash(your-tool:*)",
    "WebFetch(domain:your-api.com)"
  ]
}
```

### Adding Custom Hooks

```json
{
  "__PROJECT_CUSTOM_HOOKS__": {
    "PreCommit": [{
      "type": "command",
      "command": "npm run lint:fix"
    }]
  }
}
```

This structure ensures your project-specific needs are preserved while benefiting from boilerplate improvements.
