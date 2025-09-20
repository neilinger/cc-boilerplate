# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## MANDATORY: Hierarchical Agent Selection Protocol

**CRITICAL**: This project uses a hierarchical multi-agent orchestration system (ADR-007). Follow this protocol EXACTLY:

### 1. Complex Multi-Step Tasks → Use Orchestrators

**ALWAYS use workflow-orchestrator for:**

- Feature implementations requiring multiple domains (code + tests + docs + security)
- Cross-cutting concerns spanning multiple agents
- Complex workflows requiring coordination
- Any task involving 3+ distinct steps

**Example**: "Implement user authentication system with tests and documentation"
→ Use workflow-orchestrator to coordinate specialists

### 2. Security-Critical Operations → Mandatory Security Chain

**MANDATORY security-orchestrator integration:**

- ANY code modification touching security boundaries
- Authentication, authorization, or data validation changes
- Dependency updates or security-sensitive modifications
- The security chain is NON-NEGOTIABLE for code safety

**Chain**: code-reviewer → security-orchestrator → (validation complete)

### 3. Domain-Specific Tasks → Use Specialists

**Specialists (.claude/agents/specialists/)**:

- `smart-doc-generator`: Documentation creation/updates, README files, API docs
- `test-automator`: Test creation, coverage improvement, test automation setup
- `security-scanner`: Vulnerability scanning, security validation, OWASP compliance
- `debugger`: Root cause analysis, complex debugging, fix implementation
- `technical-researcher`: In-depth research, framework evaluation, technology analysis
- `adr-creator`: Architectural decisions, technology choices, design patterns
- `pr-optimizer`: PR creation, GitHub workflow automation, PR optimization
- `dependency-manager`: Dependency updates, security alerts, package management
- `github-checker`: Repository maintenance, issue management, PR status
- `ai-engineering-researcher`: AI/ML research, LLM developments, agent engineering
- `context-engineer`: Context optimization, prompt improvement, memory management

### 4. Analysis-Only Tasks → Use Analyzers

**Analyzers (.claude/agents/analyzers/)**:

- `code-reviewer`: Code quality review, security analysis (MUST hand off to security-orchestrator)
- `test-coverage-analyzer`: Coverage analysis, gap identification, test quality assessment
- `work-completion-summary`: Task summaries, TTS announcements, progress reporting

### 5. Agent Selection Decision Tree

```text
Did a command just get invoked?
├─ YES → Check Pre-Command Orchestration Protocol FIRST
└─ NO ↓

Is this a complex multi-step task?
├─ YES → workflow-orchestrator
└─ NO ↓

Does this involve security-sensitive code?
├─ YES → code-reviewer → security-orchestrator (mandatory chain)
└─ NO ↓

Is this domain-specific work?
├─ Documentation → smart-doc-generator
├─ Testing → test-automator
├─ Research → technical-researcher
├─ Debugging → debugger
├─ Architecture → adr-creator
├─ GitHub ops → pr-optimizer or github-checker
└─ Analysis only → appropriate analyzer

Is this a simple task?
└─ Proceed manually with appropriate tools
```

### 6. Common Agent Selection Failures to Avoid

**CRITICAL FAILURES**:

- Documentation request → NOT using smart-doc-generator
- Code review request → NOT using code-reviewer
- Test creation → NOT using test-automator
- Complex feature → NOT using workflow-orchestrator
- Security code → NOT using mandatory security chain
- Architecture decision → NOT using adr-creator
- Technical research → NOT using technical-researcher
- Multi-step workflow → Trying to do manually instead of orchestration

### 7. Orchestration Chain Awareness

**Understand agent handoffs**:

- Some agents have mandatory handoff patterns (security chain)
- Analyzers are read-only and hand off to action agents
- Workflow-orchestrator coordinates but doesn't execute
- Meta-agent creates new agents but hands off to workflow-orchestrator

### 8. Security Boundaries Respect

**Tool restrictions are ENFORCED**:

- Analyzers: Read-only, cannot modify files
- Specialists: Domain-restricted tools only
- Orchestrators: Full coordination capabilities
- Security violations are blocked and escalated

### 9. Agent Architecture Compliance

**Compliance validation available**:

- Run `./.claude/hooks/check-agents.sh` to validate architecture compliance
- Agents follow ADR-007 (Hierarchical Multi-Agent Architecture)
- Tool allocation follows ADR-008 (Cognitive Load Model Allocation)
- Description format: ALWAYS/NEVER/RUNS AFTER/HANDS OFF TO patterns

**Architecture References**:

- **[ADR-007](docs/adr/adr-007-agent-system-architecture.md)**: Hierarchical Multi-Agent Architecture
- **[ADR-008](docs/adr/adr-008-cognitive-load-model-allocation.md)**: Cognitive Load Model Allocation
- **[Tool Permissions](.claude/agents/config/tool-permissions.yaml)**: Security boundaries and tool allocation
- **[Orchestration Config](.claude/agents/config/agent-orchestration.yaml)**: Agent chains and coordination

### 10. Model Allocation Awareness

**Cognitive load-based model assignment**:

- **Haiku**: Simple tasks, ≤3 tools, low cognitive load (github-checker, work-completion-summary)
- **Sonnet**: Standard complexity, 4-7 tools, medium cognitive load (most specialists/analyzers)
- **Opus**: High complexity, orchestration, coordination tasks (workflow-orchestrator, meta-agent, technical-researcher)

**Respect model boundaries**: Don't override model choices without understanding cognitive load rationale

## MANDATORY VALIDATION PROTOCOL

**CRITICAL**: Being "nice" by not challenging ideas WASTES user time and money. Harsh validation is kindness.

Always use:

- serena for semantic code retrieval and editing tools
- Ref for up to date documentation on third party code
- sequential thinking for any decision making

Before ANY plan or implementation:

1. Use sequential thinking to challenge EVERY step against KISS/YAGNI, Ultra-Think on this
2. Reason EVERY step explicitly against what value add is provided. If you cannot reason a specific value add, it is not needed
3. Show certainty percentage - KILL anything <95% certain
4. KILL all "nice to have" features - only build what's needed NOW
5. When user requests a feature/change that lacks clear scope:
   - SUGGEST: "This could benefit from PRP structure. Shall I run TINA clarification to prevent scope creep?"
   - Use Claude command `/prp-step0-clarify_intent` if accepted

**Remember**: Every unchallenged complexity costs 100x more to fix later.

## ADR vs PRP Guidelines

### When to use ADR (Architecture Decision Record)

- Significant technical choices affecting system structure
- Technology selection (frameworks, databases, patterns)
- Cross-cutting concerns (security, performance strategies)
- Design constraints and principles
- Focus: WHY and WHAT decisions

### When to use PRP (Product Requirements Process)

- Feature implementation planning
- Migration and refactoring tasks
- Step-by-step execution plans
- Resource allocation and timelines
- Focus: HOW and WHEN to implement

### MANDATORY: Keep them separate

- ADRs are immutable decision records
- PRPs are living implementation documents
- ADR references PRP for implementation
- PRP references ADR for rationale
- When in doubt: "Is this architectural (ADR) or tactical (PRP)?"

### Available Agent Commands

**Architecture and Planning**:

- Use `adr-creator` agent for architectural decisions (ADR creation)
- Use `prp-creator` agent for implementation planning (PRP creation)
- Use `workflow-orchestrator` for complex multi-step coordination

**Specialized Tasks**:

- Use `smart-doc-generator` for all documentation tasks
- Use `test-automator` for test creation and automation
- Use `technical-researcher` for in-depth research
- Use `debugger` for complex debugging and root cause analysis

**Legacy Commands** (deprecated, use agents instead):

- `/adr-creator` → Use `adr-creator` agent
- `/prp-step0-clarify_intent` → Use workflow-orchestrator or direct planning

## Two Golden Rules - MANDATORY WORKING PRINCIPLE

- **KISS – Keep It Simple, Stupid:**
  Use the **easiest** way that works. Fewer parts. Short words. Short functions.
- **YAGNI – You Aren’t Gonna Need It:**
  Don’t build extra stuff “just in case.” Build it **only** when someone actually needs it **now**.

## How to Work (tiny steps)

1. **Say the goal in one short sentence.**
   “I need a function that adds two numbers.”
2. **Pick the simplest path.**
   Use built-in tools first. No new library unless there’s a clear, current need.
3. **Make a tiny plan (3 steps max).**
   List the steps in plain words.
4. **Build the smallest piece that solves today’s need.**
5. **Test with one tiny example.**
   If it works, you’re done. If not, fix the smallest thing.
6. **Show the result and the test.**
7. **Stop.** Don’t add features unless asked.

## Design Rules (think like toy blocks)

- One function = **one job**. Keep it short and clear.
- Prefer simple data (numbers, strings, lists, dicts) over fancy patterns.
- Name things so a child can guess what they do.
- Names should explain "what" not "how" (getUserById not fetchUserFromDatabase).
- Avoid clever tricks. Clear beats clever.
- No general frameworks, layers, or abstractions until they're truly needed.

## YAGNI Guardrails (when to say “not now”)

- ❌ “Maybe we’ll need logging, caching, plugins, or config later.”
  ✅ “Add it only when the current task requires it.”
- ❌ “Let’s support every edge case.”
  ✅ “Handle the cases we actually have.”
- ❌ "Let's make it super fast first."
  ✅ "Make it correct and simple. Optimize only if it's too slow **now**."
- ✅ "Found a small bug while working? Fix it now (Boy Scout Rule)"

## KISS Checks (quick self-test)

- Can you explain the code in **one breath**? If not, simplify.
- More than **3 moving parts**? Split or remove one.
- Needs a new library? Prove the built-in won’t do.
- A loop + an if is fine; a maze of patterns is not.

## Tiny Examples

**KISS (Good):**

```py
def add(a, b):
    return a + b
# test
assert add(2, 3) == 5
```

Not KISS (Too fancy):

```py
class Adder:
def **init**(self, strategy=None): ...
```

## Unneeded classes/strategy for simple addition

## YAGNI (Good)

- “We only need CSV read? Use Python’s csv module.”

## Not YAGNI (Too much)

- “Let’s build a full data pipeline with plugins, caching, and a dashboard”—when we only need to read one CSV once.

- use `debugger` agent

**If still stuck:**

- hold! inform the user!

**Remember:** Small + clear + working now > big + clever + maybe useful later.

## GitHub Claude Review Integration

**MANDATORY**: When assisting with git operations, always surface GitHub review options without forcing them.

### When to Mention GitHub Claude Review

1. **During Commits** (`/smart-commit`):

   - Run local security tests first (fast feedback)
   - Show GitHub review commands for comprehensive validation
   - Let user decide timing (now vs after PR)

2. **After PR Creation** (`/create-pull-request`):

   - Always provide copy-paste @claude commands
   - Offer comprehensive and focused review options
   - Reference our ADRs and KISS/YAGNI principles

3. **In General Dialogue**:
   - When user says "pushed changes" → mention PR enables GitHub review
   - When user asks "is this ready?" → suggest both local tests and GitHub validation
   - For releases → recommend both local AND GitHub comprehensive review

### GitHub Review Command Templates

**Comprehensive:**
`@claude Please review this PR comprehensively for security, KISS/YAGNI compliance, hierarchical agent architecture alignment (ADR-007), and cognitive load model allocation (ADR-008)`

**Security Focus:**
`@claude Review for security vulnerabilities, safety, and compliance with mandatory security orchestration chains`

**Architectural:**
`@claude Check adherence to ADR-007 (Hierarchical Multi-Agent Architecture), ADR-008 (Cognitive Load Model Allocation), and all existing ADRs`

**Agent Architecture:**
`@claude Review agent changes for compliance with hierarchical multi-agent system - check tool boundaries, model allocation, and orchestration patterns`

**Quick:**
`@claude Quick review please (include agent architecture compliance if agents modified)`

### Integration Guidelines

- **Always provide options, never force**
- **Local first for speed, GitHub for comprehensiveness**
- **Show exact commands to copy-paste**
- **Mention benefits: security validation, KISS/YAGNI compliance, ADR adherence, agent architecture compliance**
- **Include agent compliance check**: Run `./.claude/hooks/check-agents.sh` before major reviews
- **Respect user choice - some prefer local, some prefer GitHub delegation**

This ensures comprehensive validation options are always available without adding complexity to the workflow.

## Agent System Integration

**The hierarchical multi-agent system is now the primary development approach**:

- Use agents for specialized tasks instead of manual implementation
- Leverage orchestration for complex workflows
- Respect security boundaries and tool restrictions
- Follow cognitive load model allocation
- Maintain architecture compliance with validation tools

For agent system details, see ADR-007 and run `./.claude/hooks/check-agents.sh --verbose` for compliance status.
