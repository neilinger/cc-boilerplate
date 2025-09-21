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

### 5. Python-Based Behavioral Testing
**Scenario**: Validate AI assistant behavioral consistency using external CLI testing

```bash
# Run Python behavioral test suite (implementation in Phase 3)
python tests/behavioral/run_behavioral_tests.py

# Test CEO delegation patterns via CLI
python tests/behavioral/test_ceo_delegation.py

# Validate contrarian discipline application
python tests/behavioral/test_contrarian_discipline.py

# Generate behavioral regression report
python tests/behavioral/generate_regression_report.py
```

**Note**: Behavioral testing framework implementation is planned for Phase 3. This section will be updated with actual usage examples once the Python testing infrastructure is built.

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