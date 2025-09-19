name: "Claude Code Sub-Agent System Redesign - Hierarchical Orchestration with Autonomous Selection"
description: |

---

## Status

Status: IN_PROGRESS
Status_Date: 2025-01-19
Status_Note: MIGRATED to spec-kit workflow - specification extracted to specs/004-agent-system/spec.md. Implementation details remain here as reference. Next phase: use /plan in specs/004-agent-system/ directory.

## Goal

**Feature Goal**: Transform the Claude Code sub-agent system from flat agent delegation to hierarchical orchestration with autonomous agent selection, security-first tool allocation, and proactive quality assurance through soft hooks.

**Deliverable**:

- Hierarchical orchestration system with primary orchestrator agents
- Security-based tool allocation matrix with role-based permissions
- Missing critical agents (debugger, security-scanner, dependency-manager, pr-optimizer, context-engineer)
- Soft hook system for drift prevention
- Cognitive load-based model allocation strategy
- Agent orchestration chains for common workflows

**Success Definition**:

- Agents autonomously coordinate in chains (code-reviewer → security-scanner → test-automator)
- Tool permissions enforced by role (read-only agents cannot edit)
- Proactive quality hooks prevent issues before they occur
- Model allocation optimizes cost vs complexity
- One-pass implementation success through comprehensive context

## User Persona

**Target User**: Claude Code users working on complex software projects requiring multi-step workflows, security validation, and code quality assurance

**Use Case**: Developer writes code, system automatically triggers code-reviewer → security-scanner → test-automator chain, prevents insecure code from reaching production, and optimizes agent model usage based on task complexity

**User Journey**:

1. User makes code change
2. Soft hook triggers proactive quality chain
3. Hierarchical agents coordinate automatically
4. Security boundaries enforced throughout
5. User receives comprehensive feedback
6. System prevents drift and maintains quality

**Pain Points Addressed**:

- Current flat agent selection misses coordinated workflows
- No security boundaries on tool access
- Reactive rather than proactive quality assurance
- Inefficient model allocation increases costs
- Missing critical agents cause workflow gaps

## Why

- **Business Value**: Prevents security vulnerabilities and code quality issues before they reach production
- **Integration**: Extends existing Claude Code agent system with minimal breaking changes
- **Problems Solved**:
  - Eliminates manual agent coordination
  - Prevents tool access security vulnerabilities
  - Reduces technical debt through proactive quality hooks
  - Optimizes AI model costs through cognitive load matching
  - Fills critical workflow gaps with missing agents

## What

### User-Visible Behavior

- Agents automatically coordinate in predefined chains for common workflows
- Security-sensitive operations require explicit confirmation
- Proactive quality suggestions appear before problems occur
- Model selection happens transparently based on task complexity
- Comprehensive validation occurs before code reaches production

### Technical Requirements

- Hierarchical orchestration layer above current agent system
- Role-based tool permission enforcement
- Soft hook system that integrates with existing Claude Code hooks
- Dynamic model allocation based on cognitive complexity
- Agent chain configuration and execution engine

### Success Criteria

- [ ] Primary orchestrator agents coordinate multi-agent workflows automatically
- [ ] Tool permissions enforced - read-only agents cannot use Write/Edit/Bash tools
- [ ] Soft hooks trigger proactive quality chains on code changes
- [ ] Model allocation matches cognitive complexity (haiku→sonnet→opus)
- [ ] Missing agents (debugger, security-scanner, etc.) fill workflow gaps
- [ ] Agent chains execute reliably with fallback mechanisms
- [ ] Security boundaries prevent unauthorized tool access across agents
- [ ] Performance maintains sub-2-second agent selection times
- [ ] Cost optimization through appropriate model allocation
- [ ] Integration preserves existing agent functionality

## All Needed Context

### Context Completeness Check

_This PRP provides complete implementation context including: existing agent patterns analysis, external multi-agent research, security principles, architectural decisions, file structures, dependency mapping, validation approaches, and specific implementation tasks ordered by dependencies._

### Documentation & References

```yaml
# MUST READ - Critical for understanding existing patterns
- file: boilerplate/.claude/agents/meta-agent.md
  why: Demonstrates current agent YAML frontmatter + markdown structure
  pattern: Tool restriction syntax, model allocation, description formatting
  gotcha: Tool permissions must be comma-separated, no brackets or wildcards

- file: boilerplate/.claude/agents/engineer-code-reviewer.md
  why: Example of read-only agent with restricted tools (Read, Grep, Glob, Bash)
  pattern: Security-focused agent design, structured feedback approach
  gotcha: Some agents have Bash but only for specific diagnostic commands

- file: boilerplate/.claude/settings.template.json
  why: Current hook system implementation and tool permission structure
  pattern: Hook matcher syntax, command execution, tool allowlist format
  gotcha: Hooks run as subprocess calls with JSON input/output

- url: https://docs.anthropic.com/en/docs/claude-code/sub-agents
  why: Official Claude Code sub-agent configuration reference
  critical: Tool inheritance rules, frontmatter schema, file location priorities

- url: https://github.com/awslabs/agent-squad/blob/main/docs/src/content/docs/agents/built-in/supervisor-agent.mdx
  why: SupervisorAgent pattern for hierarchical coordination and team management
  critical: Lead agent + team delegation, classifier-based routing patterns

- file: PRPs/README.md
  why: PRP methodology and validation standards
  pattern: Information density requirements, context completeness validation
  gotcha: PRPs must enable one-pass implementation success
```

### Current Codebase Tree

```bash
cc-boilerplate/
├── boilerplate/
│   └── .claude/
│       ├── agents/                    # Current agent definitions
│       │   ├── meta-agent.md         # Agent creation automation
│       │   ├── engineer-code-reviewer.md  # Read-only security pattern
│       │   ├── test-automator.md     # Test creation specialist
│       │   └── technical.researcher.md    # Research coordination
│       ├── hooks/                    # Current hook system
│       │   ├── subagent_stop.py     # Agent lifecycle management
│       │   ├── pre_tool_use.py      # Tool execution validation
│       │   └── post_tool_use.py     # Post-execution logging
│       └── settings.template.json   # Hook configuration and permissions
└── PRPs/
    ├── templates/prp_base.md        # PRP structure template
    └── ai_docs/                     # Implementation guidance docs
```

### Desired Codebase Tree with Files to be Added

```bash
cc-boilerplate/
├── boilerplate/
│   └── .claude/
│       ├── agents/                           # EXTENDED agent system
│       │   ├── orchestrators/               # NEW: Primary orchestrator agents
│       │   │   ├── workflow-orchestrator.md      # Coordinates multi-step workflows
│       │   │   ├── code-lifecycle-manager.md     # Code→review→test→deploy chains
│       │   │   └── security-orchestrator.md      # Security scanning + remediation
│       │   ├── core/                        # NEW: Missing critical agents
│       │   │   ├── debugger.md                   # Root cause analysis specialist
│       │   │   ├── security-scanner.md           # OWASP/vulnerability detection
│       │   │   ├── dependency-manager.md         # Package management + security
│       │   │   ├── pr-optimizer.md               # GitHub PR optimization
│       │   │   └── context-engineer.md           # Context window management
│       │   └── [existing agents...]         # Preserved existing agents
│       ├── config/                          # NEW: System configuration
│       │   ├── agent-orchestration.yaml         # Chain definitions and routing
│       │   ├── tool-permissions.yaml            # Role-based tool allocation
│       │   ├── model-allocation.yaml            # Cognitive complexity mapping
│       │   └── soft-hooks.yaml                  # Proactive quality trigger rules
│       ├── hooks/                           # EXTENDED hook system
│       │   ├── soft-hooks/                      # NEW: Proactive quality hooks
│       │   │   ├── pre_code_change.py              # Architecture drift prevention
│       │   │   ├── pre_pr_creation.py              # Quality chain trigger
│       │   │   ├── complexity_threshold.py         # Refactoring automation
│       │   │   └── dependency_change.py            # Security validation
│       │   └── [existing hooks...]          # Preserved existing hooks
│       └── orchestration/                   # NEW: Agent coordination engine
│           ├── chain_executor.py                # Executes agent chains
│           ├── agent_selector.py                # Autonomous agent selection
│           ├── tool_enforcer.py                 # Security boundary enforcement
│           └── model_allocator.py               # Dynamic model assignment
└── PRPs/
    └── ai_docs/
        ├── agent-orchestration-patterns.md     # NEW: Multi-agent coordination
        ├── tool-security-principles.md         # NEW: Permission enforcement
        └── cognitive-load-modeling.md          # NEW: Model allocation strategy
```

### Known Gotchas of our Codebase & Library Quirks

```python
# CRITICAL: Claude Code agent tool restrictions
# Agent tools field must be comma-separated strings, no brackets
# WRONG: tools: [Read, Write, Edit]
# WRONG: tools: ["Read", "Write", "Edit"]
# RIGHT: tools: Read, Write, Edit

# CRITICAL: Hook system subprocess communication
# Hooks receive JSON via stdin, must output JSON to stdout
# All hook scripts must handle timeout gracefully (10 second limit)
# UV run required for dependency isolation

# CRITICAL: Agent frontmatter schema
# name: kebab-case (no spaces, no underscores)
# description: Natural language for Claude's automatic delegation
# model: haiku, sonnet, or opus (exactly these strings)
# tools: Optional field - omit entirely for full access

# CRITICAL: MCP tool inheritance
# Agents inherit MCP tools from main thread unless tools field specified
# Tool restrictions apply to both built-in and MCP tools
# Security implications for unrestricted MCP access
```

## Implementation Blueprint

### Data Models and Structure

Create the core configuration models for orchestration system:

```yaml
# .claude/config/agent-orchestration.yaml - Chain definitions
orchestration:
  chains:
    code_quality:
      trigger: "code_change"
      sequence: ["code-reviewer", "security-scanner", "test-automator"]
      fallback: ["manual-review"]

    feature_development:
      trigger: "feature_request"
      sequence: ["technical-researcher", "workflow-orchestrator", "implementer"]
      parallel: ["test-automator", "smart-doc-generator"]

    bug_fix:
      trigger: "error_detected"
      sequence: ["debugger", "root-cause-analyzer", "fix-implementer"]
      validation: ["regression-tester"]

# .claude/config/tool-permissions.yaml - Security boundaries
permissions:
  read_only:
    tools: [Read, Grep, Glob, WebFetch, mcp__Ref]
    agents: [code-reviewer, security-scanner, technical-researcher]

  write_limited:
    tools: [Read, Write, Edit]
    patterns: ["*.md", "test/**/*", "docs/**/*"]
    agents: [smart-doc-generator, test-automator]

  execution_restricted:
    tools: [Read, Bash, Grep]
    commands: ["git status", "npm test", "pytest", "security-scan"]
    agents: [debugger, dependency-manager]

  full_access:
    tools: ["*"]
    confirmation_required: true
    agents: [meta-agent, workflow-orchestrator]

# .claude/config/model-allocation.yaml - Cognitive complexity mapping
models:
  haiku:
    complexity: "simple"
    tasks: ["formatting", "validation", "status_checks"]
    cost_factor: 1

  sonnet:
    complexity: "moderate"
    tasks: ["analysis", "debugging", "code_review", "testing"]
    cost_factor: 3

  opus:
    complexity: "high"
    tasks: ["orchestration", "architecture", "security", "meta_reasoning"]
    cost_factor: 15
```

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: CREATE .claude/config/tool-permissions.yaml
  - IMPLEMENT: Role-based tool permission matrix
  - FOLLOW pattern: boilerplate/.claude/settings.template.json (tool allowlist structure)
  - NAMING: Snake_case for permission groups, kebab-case for agent names
  - PLACEMENT: New config directory in .claude/config/

Task 2: CREATE .claude/orchestration/tool_enforcer.py
  - IMPLEMENT: Tool permission validation engine
  - FOLLOW pattern: boilerplate/.claude/hooks/pre_tool_use.py (subprocess structure)
  - NAMING: Snake_case Python module, validate_tool_access main function
  - DEPENDENCIES: tool-permissions.yaml from Task 1
  - PLACEMENT: New orchestration directory

Task 3: CREATE .claude/agents/core/debugger.md
  - IMPLEMENT: Root cause analysis agent with restricted tools
  - FOLLOW pattern: boilerplate/.claude/agents/engineer-code-reviewer.md (YAML frontmatter)
  - NAMING: kebab-case filename, tools: Read, Edit, Bash (diagnostic only)
  - MODEL: sonnet (complex reasoning within domain)
  - PLACEMENT: New core agents subdirectory

Task 4: CREATE .claude/agents/core/security-scanner.md
  - IMPLEMENT: OWASP top 10 vulnerability detection agent
  - FOLLOW pattern: boilerplate/.claude/agents/engineer-code-reviewer.md (read-only tools)
  - NAMING: tools: Read, Grep, Bash (security tools), WebFetch
  - MODEL: opus (security requires deep analysis)
  - DEPENDENCIES: Tool enforcer from Task 2
  - PLACEMENT: Core agents directory

Task 5: CREATE .claude/agents/core/dependency-manager.md
  - IMPLEMENT: Package management and vulnerability scanning agent
  - FOLLOW pattern: Technical researcher agent structure
  - NAMING: tools: Read, Bash (package commands), WebFetch, mcp__Ref
  - MODEL: sonnet
  - PLACEMENT: Core agents directory

Task 6: CREATE .claude/agents/core/pr-optimizer.md
  - IMPLEMENT: GitHub PR analysis and optimization agent
  - FOLLOW pattern: Existing agent frontmatter structure
  - NAMING: tools: Read, Bash (gh commands), Grep, Write (limited)
  - MODEL: sonnet
  - PLACEMENT: Core agents directory

Task 7: CREATE .claude/agents/core/context-engineer.md
  - IMPLEMENT: Context window and information density management
  - FOLLOW pattern: Meta-agent structure (meta-reasoning focus)
  - NAMING: tools: Read, mcp__serena tools, sequential-thinking
  - MODEL: opus (meta-reasoning required)
  - PLACEMENT: Core agents directory

Task 8: CREATE .claude/config/agent-orchestration.yaml
  - IMPLEMENT: Agent chain definitions and routing rules
  - FOLLOW pattern: Hook system configuration in settings.template.json
  - NAMING: YAML structure with chains, triggers, sequences
  - DEPENDENCIES: All core agents from Tasks 3-7
  - PLACEMENT: Config directory

Task 9: CREATE .claude/orchestration/chain_executor.py
  - IMPLEMENT: Agent chain execution engine
  - FOLLOW pattern: Hook execution in boilerplate/.claude/hooks/ (subprocess calls)
  - NAMING: execute_chain main function, handle_fallback error handling
  - DEPENDENCIES: agent-orchestration.yaml from Task 8
  - PLACEMENT: Orchestration directory

Task 10: CREATE .claude/agents/orchestrators/workflow-orchestrator.md
  - IMPLEMENT: Primary orchestrator agent for complex workflows
  - FOLLOW pattern: Meta-agent structure (high-level coordination)
  - NAMING: tools: All tools (full access), confirmation required
  - MODEL: opus (system-level reasoning)
  - DEPENDENCIES: Chain executor from Task 9
  - PLACEMENT: New orchestrators subdirectory

Task 11: CREATE .claude/hooks/soft-hooks/pre_code_change.py
  - IMPLEMENT: Proactive quality hook triggered before code modifications
  - FOLLOW pattern: boilerplate/.claude/hooks/pre_tool_use.py (hook structure)
  - NAMING: validate_code_change main function, trigger_quality_chain
  - DEPENDENCIES: Workflow orchestrator from Task 10
  - PLACEMENT: New soft-hooks subdirectory

Task 12: MODIFY .claude/settings.template.json
  - INTEGRATE: Soft hook registration and orchestration configuration
  - FIND pattern: Existing hook registrations in settings.template.json
  - ADD: Soft hook triggers, tool permission enforcement
  - PRESERVE: All existing hook configurations and permissions
```

### Implementation Patterns & Key Details

```python
# Agent frontmatter pattern - Tool security enforcement
---
name: security-scanner
description: Proactively scans code for OWASP top 10 vulnerabilities and security issues. Use immediately after code changes or before PR creation.
tools: Read, Grep, Bash, WebFetch  # NO Write/Edit - read-only security agent
model: opus  # Security analysis requires deep reasoning
---

# Orchestration chain execution pattern
async def execute_agent_chain(chain_name: str, context: dict) -> dict:
    # PATTERN: Load chain configuration from YAML
    chain_config = load_chain_config(chain_name)

    # CRITICAL: Validate agent tool permissions before execution
    for agent in chain_config.sequence:
        validate_agent_tools(agent, context.get('operation_type'))

    # PATTERN: Sequential execution with context passing
    results = []
    for agent in chain_config.sequence:
        result = await execute_agent(agent, context)
        context.update(result)  # Context accumulation
        results.append(result)

    return aggregate_results(results)

# Tool permission enforcement pattern
def validate_tool_access(agent_name: str, tool_name: str) -> bool:
    # PATTERN: Load permission matrix from YAML config
    permissions = load_tool_permissions()

    # CRITICAL: Explicit permission required, no implicit access
    agent_role = get_agent_role(agent_name)
    allowed_tools = permissions.get(agent_role, {}).get('tools', [])

    # GOTCHA: Handle wildcard permissions carefully for security
    if '*' in allowed_tools:
        return requires_confirmation(agent_name, tool_name)

    return tool_name in allowed_tools

# Soft hook integration pattern
def register_soft_hook(hook_name: str, trigger_condition: callable):
    # PATTERN: Extend existing hook system without breaking changes
    # CRITICAL: Hooks can be overridden but must log warnings
    # INTEGRATION: Use existing hook subprocess communication protocol
    pass
```

### Integration Points

```yaml
HOOKS:
  - extend: .claude/settings.template.json with soft hook registrations
  - pattern: "PreToolUse hooks with agent chain triggers"
  - preserve: "All existing hook configurations and functionality"

AGENT_SYSTEM:
  - extend: .claude/agents/ with orchestrator and core agent subdirectories
  - pattern: "Existing YAML frontmatter + markdown body structure"
  - preserve: "All existing agent definitions and functionality"

CONFIGURATION:
  - add: .claude/config/ directory for system configuration files
  - pattern: "YAML configuration files with clear schema validation"
  - integration: "Hook system reads config for orchestration rules"

ORCHESTRATION:
  - add: .claude/orchestration/ directory for coordination engine
  - pattern: "Python modules following existing hook subprocess pattern"
  - integration: "Hooks trigger orchestration engine for agent chains"
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Validate YAML configuration syntax
uv run python -c "import yaml; yaml.safe_load(open('.claude/config/agent-orchestration.yaml'))"
uv run python -c "import yaml; yaml.safe_load(open('.claude/config/tool-permissions.yaml'))"

# Validate agent frontmatter syntax
for agent in .claude/agents/core/*.md .claude/agents/orchestrators/*.md; do
  uv run python -c "
import yaml, sys
with open('$agent') as f:
  content = f.read()
  if '---' in content:
    frontmatter = content.split('---')[1]
    yaml.safe_load(frontmatter)
  else:
    print('No frontmatter found'); sys.exit(1)
"
done

# Validate Python orchestration modules
uv run ruff check .claude/orchestration/ --fix
uv run mypy .claude/orchestration/
uv run ruff format .claude/orchestration/

# Expected: Zero errors, all configurations parse correctly
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test tool permission enforcement
uv run pytest .claude/orchestration/tests/test_tool_enforcer.py -v
# Verify: read-only agents cannot access Write tools
# Verify: security boundaries enforced across all agent types

# Test agent chain execution
uv run pytest .claude/orchestration/tests/test_chain_executor.py -v
# Verify: chains execute in correct sequence
# Verify: context accumulation between agents
# Verify: fallback mechanisms work on agent failure

# Test model allocation logic
uv run pytest .claude/orchestration/tests/test_model_allocator.py -v
# Verify: cognitive complexity mapped to appropriate models
# Verify: cost optimization through efficient model selection

# Expected: All tests pass, security boundaries validated
```

### Level 3: Integration Testing (System Validation)

```bash
# Test soft hook integration
echo '{"tool": "Write", "agent": "code-reviewer"}' | \
  uv run .claude/hooks/soft-hooks/pre_code_change.py
# Verify: Security violation blocked (code-reviewer is read-only)
# Verify: Hook logs security violation appropriately

# Test agent orchestration end-to-end
echo '{"trigger": "code_change", "files": ["src/test.py"]}' | \
  uv run .claude/orchestration/chain_executor.py code_quality
# Verify: code-reviewer → security-scanner → test-automator chain executes
# Verify: Each agent respects tool permissions
# Verify: Context flows correctly between agents

# Test agent autonomous selection
uv run .claude/orchestration/agent_selector.py "I need help debugging a memory leak"
# Verify: debugger agent selected based on description matching
# Verify: sonnet model allocated for moderate complexity task

# Expected: Full orchestration chains work, security enforced throughout
```

### Level 4: Creative & Domain-Specific Validation

```bash
# Test hierarchical orchestration with real workflow
# Create test code change and verify full quality chain
echo "def insecure_function(): os.system('rm -rf /')" > test_security.py
git add test_security.py

# Should trigger: pre_code_change hook → security-orchestrator → security-scanner
# Should result: Code change blocked due to security violation
# Should log: Complete audit trail of agent interactions

# Test agent coordination complexity
uv run .claude/orchestration/chain_executor.py feature_development \
  --context '{"feature": "user authentication", "complexity": "high"}'
# Verify: workflow-orchestrator coordinates multiple agents
# Verify: technical-researcher runs in parallel with implementer
# Verify: opus model used for high-complexity orchestration

# Test tool security boundaries in practice
# Attempt to use debugger agent to modify production code
echo '{"agent": "debugger", "tool": "Write", "target": "production.py"}' | \
  uv run .claude/orchestration/tool_enforcer.py
# Verify: Access denied (debugger has execution-restricted permissions)
# Verify: Security audit log created

# Performance validation
time uv run .claude/orchestration/agent_selector.py "Review my code"
# Verify: Agent selection completes under 2 seconds
# Verify: Model allocation happens efficiently

# Expected: Real workflows execute correctly, security boundaries hold
```

## Final Validation Checklist

### Technical Validation

- [ ] All 4 validation levels completed successfully
- [ ] Agent chain execution: `uv run pytest .claude/orchestration/tests/ -v`
- [ ] Security boundaries: Tool permission violations blocked and logged
- [ ] Configuration syntax: All YAML files parse without errors
- [ ] Integration tests: Soft hooks trigger orchestration chains correctly

### Feature Validation

- [ ] Hierarchical orchestration: workflow-orchestrator coordinates sub-agents
- [ ] Autonomous selection: Agents selected based on task complexity and description
- [ ] Tool security: Read-only agents cannot access Write/Edit tools
- [ ] Proactive quality: Soft hooks prevent issues before code changes
- [ ] Model optimization: Cognitive complexity matched to appropriate models
- [ ] Agent chains: code-reviewer → security-scanner → test-automator executes
- [ ] Missing agents: debugger, security-scanner, dependency-manager functional

### Code Quality Validation

- [ ] Follows existing codebase patterns (YAML frontmatter, hook subprocess)
- [ ] File placement matches desired codebase tree structure
- [ ] Security principles implemented (role-based permissions, audit trails)
- [ ] Performance requirements met (sub-2-second agent selection)
- [ ] Integration preserves existing functionality (no breaking changes)

### Documentation & Deployment

- [ ] Agent descriptions enable autonomous delegation
- [ ] Configuration files documented with clear schemas
- [ ] Orchestration chains documented with trigger conditions
- [ ] Tool permission matrix provides security guidance

---

## Anti-Patterns to Avoid

- ❌ Don't create agents without clear tool restrictions - security risk
- ❌ Don't bypass tool permission validation - undermines security model
- ❌ Don't use opus model for simple tasks - cost optimization failure
- ❌ Don't create linear agent chains without fallback - reliability risk
- ❌ Don't modify existing agent configurations - breaking change risk
- ❌ Don't implement orchestration without proper error handling
- ❌ Don't skip context accumulation between chained agents
- ❌ Don't allow unlimited tool access without confirmation requirements
