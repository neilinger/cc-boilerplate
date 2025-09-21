# Quickstart: CC-Boilerplate Strategic Accelerator Framework

## Overview
Get productive with CC-Boilerplate in under 30 minutes. This guide covers the core workflows that enable 6-hour idea-to-MVP delivery.

## Quick Setup

### Prerequisites
- Python 3.11+
- Git configured
- Claude Code CLI installed
- Linear workspace (optional)

### Installation
```bash
git clone <cc-boilerplate-repo>
cd cc-boilerplate
./setup.sh
```

## Core Workflows

### 1. Brown-field Project Recovery
**Scenario**: Inherited messy codebase, need to establish order and productivity

```bash
# Initialize framework
./scripts/recover-project.sh

# Generate missing specifications
claude /prd-discovery --brownfield

# Establish security boundaries
claude security-audit --fix

# Validate recovery
./scripts/validate-recovery.sh
```

### 2. Day 1 Consultant Productivity
**Scenario**: New consulting engagement, need immediate productive development

```bash
# Setup consultant environment
./scripts/consultant-setup.sh

# Discover project context
claude /discover-context

# Generate initial PRP
claude /prd --consulting-mode

# Begin feature development
claude /plan && claude /tasks
```

### 3. Portfolio Tool Rapid Prototyping
**Scenario**: Internal tool idea needs rapid validation and deployment

```bash
# Transform idea to specification
claude /prd-discovery --idea="your tool concept"

# Generate implementation plan
claude /plan

# Execute MVP development
claude /tasks --execute --target=mvp

# Deploy to AWS
./scripts/deploy-mvp.sh
```

### 4. Git Workflow Course Correction
**Scenario**: Mixed commits, broken workflow, need clean state without losing work

```bash
# Analyze current state
./scripts/analyze-git-state.sh

# Smart commit splitting
claude git-recovery --split-commits

# Repair branch workflow
claude git-workflow --repair

# Validate clean state
git log --oneline -10
```

### 5. Behavioral Testing Validation
**Scenario**: Validate AI assistant behavioral consistency and CEO role adherence

```bash
# Run behavioral test suite
./scripts/behavioral-tests.sh

# Validate CEO role adherence
claude behavioral-audit --role=ceo

# Check delegation patterns
claude delegation-analysis

# Generate regression report
claude behavioral-report
```

## Success Validation

### Checkpoints
- [ ] Agent orchestration responding correctly
- [ ] Security validation chains active
- [ ] PRP discovery workflow functional
- [ ] Linear integration (if configured)
- [ ] Behavioral tests passing >95%

### Troubleshooting
- **Agent not responding**: Check tool permissions in `.claude/agents/config/`
- **Security blocks**: Review security-orchestrator logs
- **Slow performance**: Verify cognitive load model allocation
- **Integration failures**: Validate API endpoints and credentials

## Next Steps
- Explore advanced agent customization
- Configure Linear workspace integration
- Set up continuous behavioral testing
- Review architectural decision records (ADRs)