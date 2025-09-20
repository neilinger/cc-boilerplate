# Claude Code Agent Soft Hook System

This directory contains the **soft hook system for drift prevention**, designed to maintain compliance with the hierarchical multi-agent architecture defined in ADR-007 and ADR-008.

## 🎯 Purpose

The soft hook system prevents agents from drifting away from architectural principles by:

- **Validating agent structure** and metadata compliance
- **Checking tool allocation** boundaries (3-7 tools per agent)
- **Monitoring description format** adherence (ALWAYS/NEVER/RUNS AFTER/HANDS OFF TO)
- **Ensuring model allocation** follows cognitive load rules
- **Validating orchestration chains** and security boundaries

## 📁 Components

### Core Validation

- **`scripts/agent-validation/agent-compliance-checker.py`** - Main compliance validation script
- **`scripts/agent-validation/check-agents.sh`** - Developer-friendly wrapper script

### Integration Options

- **`scripts/agent-validation/pre-commit-agent-check.sh`** - Optional git pre-commit hook
- **`ci-agent-validation.yml`** - GitHub Actions workflow template

### Documentation

- **`README.md`** - This documentation
- **Configuration files** in `.claude/agents/config/`

## 🚀 Quick Start

### Basic Usage

```bash
# Quick compliance check
./scripts/agent-validation/check-agents.sh

# Detailed analysis with suggestions
./scripts/agent-validation/check-agents.sh --verbose

# Direct Python script usage
python3 scripts/agent-validation/agent-compliance-checker.py --verbose
```

### Expected Output

```text
🤖 Claude Code Agent Compliance Checker
=============================================

📁 Project root: /path/to/project
🔍 Checking agents in: .claude/agents/
📊 Found 19 agent files to validate

🔍 Running compliance analysis...

✅ All agents are compliant with hierarchical architecture!

🎉 SUCCESS: All agents are compliant!
   Your agent architecture follows ADR-007 and ADR-008
```

## 🔧 Setup Options

### Option 1: Manual Validation (Recommended)

Run compliance checks manually during development:

```bash
# Make script executable
chmod +x scripts/agent-validation/check-agents.sh

# Run before committing changes
./scripts/agent-validation/check-agents.sh --verbose
```

### Option 2: Git Hook Integration (Optional)

Enable automatic checking during commits:

```bash
# Link the pre-commit hook
ln -sf ../../scripts/agent-validation/pre-commit-agent-check.sh .git/hooks/pre-commit

# Make executable
chmod +x .git/hooks/pre-commit
```

**Note**: The git hook uses **soft validation** - it warns but doesn't block commits by default.

### Option 3: CI/CD Integration (Optional)

Add continuous validation to your GitHub repository:

```bash
# Copy the workflow template
mkdir -p .github/workflows
cp .claude/hooks/ci-agent-validation.yml .github/workflows/

# Commit and push to enable
git add .github/workflows/ci-agent-validation.yml
git commit -m "feat: add agent compliance CI validation"
git push
```

## 📊 What Gets Validated

### Hierarchical Structure

```text
.claude/agents/
├── orchestrators/     # Coordination agents (workflow, security)
├── specialists/       # Domain experts (security, testing, docs)
├── analyzers/         # Analysis-only agents (code review, coverage)
├── config/           # Configuration files
└── meta-agent.md     # System-level agent
```

### Tool Allocation Rules

- **Haiku**: ≤3 tools (simple tasks, low cognitive load)
- **Sonnet**: 4-7 tools (standard complexity)
- **Opus**: Orchestration/high complexity only

### Security Boundaries

- **Read-only**: Analysis agents cannot modify files
- **Write-limited**: Creation agents have restricted tool access
- **Execution-restricted**: Specialized agents have limited bash commands
- **Full-access**: Orchestrators and meta-agents only

### Description Format

All agents must use standardized description format:

```yaml
description: |
  ALWAYS use when: [specific trigger conditions]
  NEVER use when: [exclusion conditions]
  Runs AFTER: [predecessor agents]
  Hands off to: [successor agents]
```

### Orchestration Chains

- **Security chain**: code-reviewer → security-orchestrator (mandatory)
- **Test chain**: test-automator → test-coverage-analyzer
- **Documentation**: smart-doc-generator → workflow-orchestrator

## 🛠️ Troubleshooting

### Common Issues

#### "Missing required field in frontmatter"

**Problem**: Agent missing `name`, `description`, or `model` fields.

**Solution**:

```yaml
---
name: my-agent
description: |
  ALWAYS use when: ...
  NEVER use when: ...
model: sonnet
---
```

#### "Should be in X directory"

**Problem**: Agent in wrong hierarchical directory.

**Solution**: Move agent to correct location:

- `orchestrators/` - coordination agents
- `specialists/` - domain-specific agents
- `analyzers/` - analysis-only agents

#### "Tool 'X' not in allowed list"

**Problem**: Agent using tools not permitted by security level.

**Solution**: Check `.claude/agents/config/tool-permissions.yaml` for allowed tools.

#### "Should use new description format"

**Problem**: Using old description format.

**Solution**: Update to new format with ALWAYS/NEVER/RUNS AFTER/HANDS OFF TO structure.

### Validation Levels

1. **Errors** (🚨): Must fix - architectural violations
2. **Warnings** (⚠️): Should fix - format or boundary issues
3. **Suggestions** (💡): Consider - optimization opportunities

## 📚 Architecture References

### Core Documentation

- **[ADR-007](../../docs/adr/adr-007-agent-system-architecture.md)**: Hierarchical Multi-Agent Architecture
- **[ADR-008](../../docs/adr/adr-008-cognitive-load-model-allocation.md)**: Cognitive Load Model Allocation
- **[PRP-004](../../PRPs/prp-004-agent-system-redesign.md)**: Agent System Redesign Process

### Configuration Files

- **[Tool Permissions](../agents/config/tool-permissions.yaml)**: Security boundaries and tool allocation
- **[Orchestration Config](../agents/config/agent-orchestration.yaml)**: Agent chains and coordination rules

## 🔄 Soft Hook Philosophy

This system follows a **"soft hook" approach**:

### ✅ What It Does

- **Validates** agent compliance with architecture
- **Provides** clear, actionable guidance
- **Educates** developers about architectural principles
- **Suggests** improvements and optimizations
- **Reports** issues with helpful context

### ❌ What It Doesn't Do

- **Block** commits or deployments (by default)
- **Auto-fix** issues without developer review
- **Enforce** strict rules that prevent innovation
- **Replace** human judgment and architectural decisions

### 🎯 Design Goals

1. **Developer-friendly**: Clear messages, helpful guidance
2. **Educational**: Explain the "why" behind rules
3. **Flexible**: Soft validation with override options
4. **Comprehensive**: Cover all architectural aspects
5. **Actionable**: Provide specific steps to fix issues

## 🤝 Contributing

When adding new validation rules:

1. **Add to `agent-compliance-checker.py`**
2. **Update this README** with new validations
3. **Test with existing agents** to ensure no false positives
4. **Follow soft hook philosophy** - educate, don't block

## 🔍 Advanced Usage

### Custom Validation

```python
# Add custom validation to agent-compliance-checker.py
def _check_custom_rule(self, agent_file: Path, frontmatter: Dict) -> None:
    """Add your custom validation logic"""
    agent_name = frontmatter.get('name', agent_file.stem)

    # Your validation logic here
    if not meets_custom_requirement:
        self.warnings.append(f"{agent_name}: Custom rule violation")
```

### Integration with Other Tools

```bash
# Use in scripts
if ./scripts/agent-validation/check-agents.sh; then
    echo "Agents compliant, proceeding..."
else
    echo "Compliance issues found, see above"
fi

# JSON output (future feature)
python3 scripts/agent-validation/agent-compliance-checker.py --json > compliance.json
```

## 📈 Metrics and Monitoring

The compliance checker tracks:

- **Agent count** by category (orchestrators/specialists/analyzers)
- **Tool allocation** distribution
- **Model usage** patterns
- **Compliance trends** over time
- **Common violation** patterns

This data helps maintain architectural health and identify areas for improvement.

---

**Remember**: The goal is not perfect compliance, but rather maintaining architectural integrity while enabling productive development. The soft hook system guides and educates rather than constrains creativity.
