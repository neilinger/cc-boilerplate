# Quickstart Guide: CC-Boilerplate Strategic Accelerator Framework

**Time to Productivity**: <30 minutes
**Time to MVP**: <6 hours

## Prerequisites

- Unix-like system (macOS or Linux)
- Claude Code installed and configured
- GitHub CLI (`gh`) authenticated
- Git configured with proper credentials

## 30-Minute Onboarding Path

### Step 1: Clone and Initialize (5 minutes)

```bash
# Clone the CC-Boilerplate repository
git clone https://github.com/your-org/cc-boilerplate.git my-project
cd my-project

# Initialize boilerplate for your project
./scripts/init-boilerplate.sh

# Verify agent system
./.claude/hooks/check-agents.sh --verbose
```

**Expected Output**:
- ✅ 100+ agents available
- ✅ Security chains configured
- ✅ Validation hooks installed

### Step 2: Test Agent Discovery (5 minutes)

```bash
# Test workflow orchestrator discovery
claude "I need to write comprehensive tests for my authentication system"

# Observe: workflow-orchestrator automatically selects test-automator
# Observe: Security chain validates operations
# Observe: Non-blocking quality gates in action
```

### Step 3: Try PRP Discovery Workflow (10 minutes)

```bash
# Create a PRP from a rough idea
claude "I want to build a real-time dashboard for monitoring API performance"

# System will:
# 1. Launch PRP discovery workflow
# 2. Research existing solutions
# 3. Generate comprehensive requirements
# 4. Create PRP document in PRPs/ directory
```

### Step 4: Transform PRP to Implementation (5 minutes)

```bash
# Transform PRP to specification
claude "/specify @PRPs/your-prp-name.md"

# Then create implementation plan
claude "/plan"

# Generate task list
claude "/tasks"
```

### Step 5: Verify Security and Recovery (5 minutes)

```bash
# Test dangerous pattern prevention
claude "delete all files in root directory"
# Observe: Command blocked by security chain

# Create recovery checkpoint
claude "Create a recovery checkpoint before I start major refactoring"

# Test smart commit splitting
claude "I've made changes to multiple features, help me create logical commits"
```

## Common Workflows

### Turnaround Specialist: Rescue Brown-Field Project

```bash
# 1. Analyze existing codebase
claude "Analyze this project and identify technical debt and missing documentation"

# 2. Generate missing specifications
claude "Backfill PRPs for the existing authentication and payment systems"

# 3. Establish security boundaries
claude "Set up mandatory security chains for all code modifications"

# 4. Create recovery checkpoint
claude "Create checkpoint before beginning turnaround"

# 5. Deliver MVP within 6 hours
claude "Focus on core user journey and deliver working MVP"
```

### AI-First Consultant: Day 1 Productivity

```bash
# 1. Initialize for client project
./scripts/init-boilerplate.sh --client "ClientName"

# 2. Capture requirements via PRP
claude "Interview me about the client's needs for their inventory management system"

# 3. Generate implementation plan
claude "/specify @PRPs/client-inventory.md"
claude "/plan"
claude "/tasks"

# 4. Start implementation with agents
claude "Implement task #1 from the task list"
```

### Portfolio Builder: Linear Integration

```bash
# 1. Configure Linear integration
export LINEAR_API_KEY="your-key"
claude "Set up Linear integration for my team"

# 2. Sync existing issues
claude "Sync all issues from Linear and calculate AI competency scores"

# 3. Enable AI task assignment
claude "Assign Linear issues to AI agents based on competency scores"

# 4. Monitor progress
claude "Show me the status of AI-assigned tasks"
```

### Developer: Mid-Journey Course Correction

```bash
# 1. Detect messy state
git status  # Mixed changes across features

# 2. Use smart commit splitting
claude "Help me split these changes into logical commits"

# 3. Repair branch workflow
claude "I'm on the wrong branch, help me fix my git workflow without losing work"

# 4. Restore from checkpoint if needed
claude "List available recovery checkpoints"
claude "Restore from checkpoint <id>"
```

## Validation Checklist

After 30 minutes, you should be able to:

- [ ] **Agent Discovery**: Workflow-orchestrator selects appropriate specialists
- [ ] **Security Validation**: Dangerous commands are blocked
- [ ] **PRP Generation**: Transform ideas into comprehensive requirements
- [ ] **Specification Flow**: PRP → Spec → Plan → Tasks workflow works
- [ ] **Recovery Operations**: Create checkpoints and restore state
- [ ] **Quality Gates**: Non-blocking validation maintains velocity

## Performance Benchmarks

Measure your setup success:

| Metric | Target | Your Result |
|--------|--------|-------------|
| Agent selection time | <2 seconds | ___ |
| PRP generation | <30 minutes | ___ |
| Security validation | 0 bypasses | ___ |
| Checkpoint creation | <5 seconds | ___ |
| Task assignment accuracy | >80% | ___ |

## Advanced Features

### Custom Agent Development

```bash
# Create new specialist agent
claude "Create a new agent specialized in GraphQL API optimization"

# Agent will be created in .claude/agents/specialists/
# Automatic validation against ADR-007/008
# Tool permissions assigned based on role
```

### Competency Learning

```bash
# View AI competency scores
claude "Show competency scores for all agents"

# Update scores based on outcome
claude "Update competency score for test-automator based on successful task"

# Override automatic assignment
claude "Manually assign this task despite low competency score"
```

### Integration Ecosystem

```bash
# MCP Servers
claude "List all available MCP servers and their capabilities"

# Spec-kit transformation
claude "Show me the complete PRP → MVP pipeline"

# GitHub integration
claude "Create PR with comprehensive review request"
```

## Troubleshooting

### Agent Not Found
```bash
# Use workflow-orchestrator for discovery
claude "workflow-orchestrator: find best agent for database optimization"
```

### Security Chain Blocking Valid Operation
```bash
# Request temporary bypass with audit
claude "Request security bypass for specific operation with justification"
```

### Sync Conflicts with Linear
```bash
# Resolve conflicts with latest-wins strategy
claude "Resolve Linear sync conflicts using timestamp comparison"
```

### Recovery Checkpoint Full
```bash
# Clean old checkpoints
claude "Remove recovery checkpoints older than 7 days"
```

## Next Steps

1. **Run pilot project**: Test <6 hour MVP delivery
2. **Customize agents**: Add domain-specific specialists
3. **Integrate Linear**: Enable AI-human task allocation
4. **Measure metrics**: Track productivity improvements
5. **Contribute**: Share custom agents with community

## Support

- **Documentation**: `docs/` directory
- **Agent Help**: `claude "Show help for [agent-name]"`
- **Architecture**: Review ADR-007 and ADR-008
- **Validation**: Run `./.claude/hooks/check-agents.sh`

---
*You're now ready to deliver 10x impact with CC-Boilerplate!*