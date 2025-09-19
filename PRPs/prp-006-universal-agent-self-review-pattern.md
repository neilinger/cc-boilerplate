---
name: "Universal Agent Self-Review Pattern with Progressive Enforcement (PRP-011)"
description: |
  Implement universal agent self-review pattern with root cause analysis that enforces agent protocol
  compliance through mandatory validation checks and progressive enforcement, preventing validation
  skip incidents across all specialized agents.
---

## Status

Status: PROPOSED
Status_Date: 2025-01-19
Status_Note: Addresses GitHub Issue #29 - systematic reliability issues across all agents

## Goal

**Feature Goal**: Implement universal enforcement system that detects when agents complete tasks without following their documented validation requirements and applies progressive enforcement with intelligent root cause analysis.

**Deliverable**: Enhanced hook system with three-strikes progressive enforcement, validation detection engine, and root cause analysis integration that reduces validation skip incidents by 80%.

**Success Definition**:
- post_tool_use hook automatically detects agent Task completions and validates protocol compliance
- Progressive three-strikes system implemented with session-aware failure tracking
- workflow-orchestrator enforces mandatory review gates with escalation paths
- Sequential thinking integration provides actionable root cause analysis
- System maintains graceful degradation and never blocks Claude Code operation

## User Persona

**Target User**: Claude Code developers using specialized agents for complex workflows

**Use Case**: Developer relies on agents like n8n-mcp-specialist for workflow creation, expecting validation phases (Pre-Validation, Workflow Validation, Post-Validation) to be followed consistently

**User Journey**:
1. User requests complex task requiring specialized agent
2. Agent receives task with documented validation requirements
3. System automatically detects if agent skips validation steps
4. Progressive enforcement provides warnings, corrections, or escalation
5. User receives reliable agent outputs with clear feedback on any compliance issues

**Pain Points Addressed**:
- Agents ignoring validation protocols without consequence
- Unreliable outputs from specialized agents due to skipped validation
- No automatic detection of protocol violations
- Lack of intelligent escalation when agents repeatedly fail compliance

## Why

- **System Reliability**: Any agent can currently ignore validation protocols without consequence, leading to unreliable outputs and user frustration
- **Quality Assurance**: Documented validation phases exist but lack enforcement mechanism - they are suggestions, not contracts
- **User Trust**: Validation skip incidents undermine confidence in the agent system
- **Scalability**: Manual monitoring of agent compliance doesn't scale with growing agent ecosystem

## What

**Core Enforcement System**:
- Universal validation detection engine using NLP pattern matching and Constitutional AI principles
- Progressive three-strikes enforcement with session-aware failure tracking
- Intelligent escalation with root cause analysis using sequential thinking integration
- Audit trail with tamper-proof logging and compliance metrics

**Integration Points**:
- Enhanced post_tool_use hook with validation detection
- Workflow orchestrator updates with mandatory review gates
- Agent compliance framework integration
- Session management with violation tracking

### Success Criteria

- [ ] post_tool_use hook detects agent Task completions and validates protocol compliance with >90% accuracy
- [ ] Progressive three-strikes system implemented with session isolation and 90-day rolling windows
- [ ] workflow-orchestrator enforces mandatory review gates with clear escalation paths
- [ ] Sequential thinking integration provides root cause analysis after 3 strikes with actionable insights
- [ ] 80% reduction in validation skip incidents measured through comprehensive audit logs
- [ ] System maintains <100ms hook execution time and graceful degradation on all errors

## All Needed Context

### Context Completeness Check

_This PRP provides comprehensive context for someone with no prior knowledge of this codebase to implement universal agent self-review patterns successfully. All patterns, file structures, validation logic, and integration points are documented with specific implementation guidance._

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- docfile: PRPs/ai_docs/progressive_enforcement_patterns.md
  why: Constitutional AI implementation patterns, three-strikes algorithms, validation detection
  section: Complete document contains working code examples and proven effectiveness metrics
  critical: Progressive enforcement decision trees, Constitutional AI self-critique patterns

- file: .claude/hooks/post_tool_use.py
  why: Existing hook structure with graceful error handling and JSON logging patterns
  pattern: Hook input/output structure, error handling, sys.exit(0) on failures
  gotcha: Must preserve existing functionality and JSON structure exactly

- file: .claude/hooks/utils/agent-compliance-checker.py
  why: Proven validation logic patterns and error classification system
  pattern: AgentComplianceChecker class structure, error/warning/suggestion classification
  gotcha: Reuse existing validation detection methods and frontmatter parsing

- file: .claude/agents/config/tool-permissions.yaml
  why: Security boundary enforcement and agent permission validation
  pattern: Agent permission matrix, security levels, tool restriction patterns
  gotcha: Runtime permission validation required, security boundary respect

- file: .claude/agents/config/agent-orchestration.yaml
  why: Agent coordination patterns and mandatory security chain integration
  pattern: Chain definitions, agent categorization, model allocation rules
  gotcha: Preserve existing security_chain and orchestration patterns

- file: .claude/agents/orchestrators/workflow-orchestrator.md
  why: Orchestration patterns and agent handoff protocols
  pattern: ALWAYS/NEVER/RUNS AFTER/HANDS OFF TO description format
  gotcha: Mandatory security chain integration must be preserved

- url: https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback
  why: Constitutional AI self-critique and revision loop implementation
  critical: Two-phase supervised learning and RLAIF patterns for agent self-correction

- url: https://arxiv.org/abs/2502.08224
  why: Flow-of-Action framework for multi-agent root cause analysis
  critical: SOP-guided RCA workflow with specialist agent coordination

- url: https://support.google.com/adspolicy/answer/10922738?hl=en-GB
  why: Proven three-strikes implementation with 90-day rolling windows
  critical: Grace period patterns, graduated escalation, appeal mechanisms
```

### Current Codebase Tree

```bash
.
├── .claude/
│   ├── hooks/
│   │   ├── post_tool_use.py              # Hook to enhance with validation detection
│   │   ├── utils/
│   │   │   ├── agent-compliance-checker.py  # Validation logic patterns to reuse
│   │   │   └── (agent-review-enforcer.py)   # NEW: Progressive enforcement utility
│   ├── agents/
│   │   ├── config/
│   │   │   ├── tool-permissions.yaml         # Security boundary enforcement
│   │   │   └── agent-orchestration.yaml     # Agent coordination patterns
│   │   └── orchestrators/
│   │       └── workflow-orchestrator.md     # Update with mandatory review gates
├── logs/
│   ├── post_tool_use.json                   # Existing audit structure
│   └── (agent-review-audit.json)            # NEW: Validation failure tracking
├── tests/
│   └── (test_agent_review_enforcement.py)   # NEW: Comprehensive test suite
└── PRPs/
    └── ai_docs/
        └── progressive_enforcement_patterns.md  # Implementation reference guide
```

### Desired Codebase Tree with Files to be Added

```bash
.
├── .claude/
│   ├── hooks/
│   │   ├── post_tool_use.py                    # ENHANCED: Add validation detection
│   │   └── utils/
│   │       └── agent-review-enforcer.py       # NEW: Progressive enforcement engine
├── logs/
│   └── agent-review-audit.json                # NEW: Strike tracking and audit trail
├── tests/
│   └── test_agent_review_enforcement.py       # NEW: Validation enforcement tests
└── .claude/agents/
    ├── config/
    │   └── agent-orchestration.yaml           # ENHANCED: Add enforcement configuration
    └── orchestrators/
        └── workflow-orchestrator.md           # ENHANCED: Add self-review patterns
```

### Known Gotchas of our Codebase & Library Quirks

```python
# CRITICAL: Claude Code hook requirements
# Hooks MUST exit gracefully with sys.exit(0) on ANY error to prevent blocking
# JSON parsing requires strict validation - malformed input will crash the system
# Hook execution time must be <100ms to maintain responsiveness

# CRITICAL: Session management patterns
# Session IDs are UUID format: 'a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6'
# Session data stored in .claude/data/sessions/ with isolation requirements
# Strike tracking must be session-aware, not global per agent

# CRITICAL: Agent validation detection patterns
# Agents like n8n-mcp-specialist document validation requirements in descriptions
# Validation language patterns: "validate", "validation", "checked", "verified"
# Constitutional AI patterns require self-critique and revision detection

# CRITICAL: Tool permission enforcement
# tool-permissions.yaml defines security boundaries but lacks runtime enforcement
# Pattern matching for tools: "Bash(git:*)" matches "Bash(git log:*)"
# Security levels: read_only, write_limited, execution_restricted, full_access

# CRITICAL: Progressive enforcement requirements
# Three-strikes algorithm: Warning → Remediation → Root Cause Analysis
# Strike expiration: 90-day rolling window for agent rehabilitation
# Session isolation: Strikes tracked per session, not globally per agent
```

## Implementation Blueprint

### Data Models and Structure

Create comprehensive data models for validation enforcement with type safety and session isolation.

```python
# Core enforcement data models
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Union
from enum import Enum

class ViolationType(Enum):
    VALIDATION_SKIPPED = "validation_skipped"
    PROTOCOL_VIOLATION = "protocol_violation"
    TOOL_PERMISSION_VIOLATION = "tool_permission_violation"
    SECURITY_BOUNDARY_VIOLATION = "security_boundary_violation"

class EnforcementAction(Enum):
    WARNING = "warning"
    REMEDIATION = "remediation"
    ROOT_CAUSE_ANALYSIS = "root_cause_analysis"
    ESCALATION = "escalation"

@dataclass
class ViolationRecord:
    session_id: str
    agent_name: str
    violation_type: ViolationType
    timestamp: datetime
    context: Dict[str, Any]
    strike_number: int
    enforcement_action: EnforcementAction

@dataclass
class ValidationDetectionResult:
    validation_detected: bool
    compliance_score: float
    missing_patterns: List[str]
    confidence_level: str
```

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: CREATE .claude/hooks/utils/agent-review-enforcer.py
  - IMPLEMENT: ProgressiveEnforcementEngine, ValidationDetectionEngine, StrikeTracker classes
  - FOLLOW pattern: .claude/hooks/utils/agent-compliance-checker.py (class structure, error handling)
  - NAMING: PascalCase for classes, snake_case for methods, descriptive function names
  - DEPENDENCIES: None (standalone utility with Pydantic models)
  - PLACEMENT: Hook utilities directory alongside existing agent-compliance-checker.py
  - SECURITY: Implement secure session tracking, cryptographic strike integrity
  - VALIDATION: Constitutional AI pattern matching, NLP validation detection

Task 2: MODIFY .claude/hooks/post_tool_use.py
  - ENHANCE: Add validation detection and enforcement after Task tool completions
  - FOLLOW pattern: Existing graceful error handling, JSON structure preservation
  - NAMING: Preserve existing function names, add detect_validation_compliance()
  - DEPENDENCIES: Import ProgressiveEnforcementEngine from Task 1
  - PLACEMENT: Integrate into existing hook workflow after JSON logging
  - CRITICAL: Must preserve existing functionality, graceful degradation on errors
  - PERFORMANCE: Ensure <100ms execution time, efficient validation detection

Task 3: CREATE logs/agent-review-audit.json
  - IMPLEMENT: Audit trail structure for validation failure tracking
  - FOLLOW pattern: logs/post_tool_use.json (JSON array structure, file handling)
  - NAMING: agent-review-audit.json in logs directory
  - DEPENDENCIES: Called by enhanced post_tool_use.py from Task 2
  - PLACEMENT: logs/ directory alongside existing audit files
  - STRUCTURE: Session-aware violation tracking with integrity verification
  - SECURITY: Tamper-proof logging with cryptographic signatures

Task 4: MODIFY .claude/agents/orchestrators/workflow-orchestrator.md
  - ADD: Mandatory Self-Review Pattern section with progressive enforcement integration
  - FOLLOW pattern: Existing ALWAYS/NEVER/RUNS AFTER/HANDS OFF TO description format
  - NAMING: Add "Self-Review Enforcement" section, preserve existing structure
  - DEPENDENCIES: Reference enforcement system from Tasks 1-3
  - PLACEMENT: Add section after existing orchestration patterns
  - INTEGRATION: Three-strikes protocol and root cause analysis requirements
  - HANDOFF: Define escalation paths to security-orchestrator when needed

Task 5: CREATE tests/test_agent_review_enforcement.py
  - IMPLEMENT: Comprehensive test suite for all enforcement components
  - FOLLOW pattern: tests/ directory structure, pytest conventions
  - NAMING: test_agent_review_enforcement.py with descriptive test function names
  - DEPENDENCIES: Test components from Tasks 1-4
  - PLACEMENT: tests/ directory alongside existing test files
  - COVERAGE: Validation detection, progressive enforcement, session isolation
  - MOCKS: Sequential thinking MCP calls, agent Task completions, session data

Task 6: ENHANCE .claude/agents/config/agent-orchestration.yaml
  - ADD: Validation enforcement configuration to existing orchestration structure
  - FOLLOW pattern: Existing chain definitions and agent categorization
  - NAMING: Add validation_enforcement section, preserve existing keys
  - DEPENDENCIES: Integration with enforcement system from Tasks 1-5
  - PLACEMENT: Extend existing configuration file
  - INTEGRATION: Extend security_chain with validation enforcement requirements
  - CONFIGURATION: Progressive enforcement thresholds and escalation rules
```

### Implementation Patterns & Key Details

```python
# Progressive Enforcement Algorithm (Core Pattern)
class ProgressiveEnforcementEngine:
    def __init__(self):
        self.strike_thresholds = {
            1: {"action": "warning", "message": "Please follow validation protocols"},
            2: {"action": "remediation", "message": "Re-run task with mandatory validation"},
            3: {"action": "root_cause_analysis", "message": "Analyzing why validation was skipped"}
        }

    def evaluate_agent_compliance(self, session_id: str, agent_name: str,
                                 task_result: str) -> EnforcementAction:
        # PATTERN: Constitutional AI validation detection
        validation_result = self.detect_validation_compliance(task_result)

        if not validation_result.validation_detected:
            strike_count = self.increment_strike_count(session_id, agent_name)
            return self.determine_enforcement_action(strike_count)

        return EnforcementAction.NO_ACTION

# Validation Detection Engine (NLP Pattern Matching)
class ValidationDetectionEngine:
    def __init__(self):
        self.validation_patterns = {
            "sequential_thinking": [r"let me think step by step", r"analyzing each component"],
            "validation_language": [r"validated.*against", r"compliance.*check"],
            "self_critique": [r"reviewing.*approach", r"checking.*assumptions"]
        }

    def detect_validation_compliance(self, agent_response: str) -> ValidationDetectionResult:
        # PATTERN: Multi-pattern NLP validation with confidence scoring
        compliance_scores = {}
        for category, patterns in self.validation_patterns.items():
            matches = [p for p in patterns if re.search(p, agent_response, re.IGNORECASE)]
            compliance_scores[category] = len(matches) / len(patterns)

        overall_compliance = sum(compliance_scores.values()) / len(compliance_scores)
        return ValidationDetectionResult(
            validation_detected=overall_compliance >= 0.67,  # 2/3 threshold
            compliance_score=overall_compliance,
            confidence_level="high" if overall_compliance > 0.8 else "medium"
        )

# Hook Integration Pattern (Preserve Existing Structure)
def enhanced_post_tool_use_main():
    try:
        # PRESERVE: Existing JSON input processing
        input_data = json.load(sys.stdin)

        # PRESERVE: Existing logging functionality
        log_existing_tool_usage(input_data)

        # NEW: Add validation enforcement for Task completions
        if input_data.get("tool_name") == "Task":
            enforce_agent_compliance(input_data)

        # CRITICAL: Always exit gracefully
        sys.exit(0)

    except Exception:
        # CRITICAL: Never block Claude Code operation
        sys.exit(0)
```

### Integration Points

```yaml
HOOK_INTEGRATION:
  - enhance: .claude/hooks/post_tool_use.py
  - preserve: "Existing JSON logging structure and graceful error handling"
  - add: "Validation detection after Task tool completions"

AGENT_ORCHESTRATION:
  - update: .claude/agents/orchestrators/workflow-orchestrator.md
  - pattern: "ALWAYS/NEVER/RUNS AFTER/HANDS OFF TO description format"
  - add: "Mandatory Self-Review Pattern section with enforcement escalation"

SECURITY_BOUNDARIES:
  - reference: .claude/agents/config/tool-permissions.yaml
  - enforce: "Runtime tool permission validation with audit logging"
  - maintain: "Security levels and agent permission matrix integrity"

AUDIT_TRAIL:
  - extend: logs/ directory with agent-review-audit.json
  - pattern: "Session-aware violation tracking with cryptographic integrity"
  - integration: "Called by enhanced post_tool_use.py for compliance auditing"

MCP_INTEGRATION:
  - use: mcp__sequential-thinking__sequentialthinking
  - purpose: "Root cause analysis after 3 strikes with actionable insights"
  - trigger: "Automatic escalation when progressive enforcement reaches threshold"
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Run after each Python file creation - fix before proceeding
ruff check .claude/hooks/utils/agent-review-enforcer.py --fix
mypy .claude/hooks/utils/agent-review-enforcer.py
ruff format .claude/hooks/utils/agent-review-enforcer.py

# Validate enhanced hook functionality
python -m py_compile .claude/hooks/post_tool_use.py
ruff check .claude/hooks/post_tool_use.py --fix

# Project-wide validation
ruff check .claude/ --fix
mypy .claude/hooks/utils/
ruff format .claude/

# Agent compliance validation
.claude/hooks/utils/agent-compliance-checker.py --verbose

# Expected: Zero errors. If errors exist, READ output and fix before proceeding.
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test progressive enforcement engine
uv run pytest tests/test_agent_review_enforcement.py::TestProgressiveEnforcement -v

# Test validation detection accuracy
uv run pytest tests/test_agent_review_enforcement.py::TestValidationDetection -v

# Test session isolation and strike tracking
uv run pytest tests/test_agent_review_enforcement.py::TestSessionIsolation -v

# Test hook integration without breaking existing functionality
uv run pytest tests/test_agent_review_enforcement.py::TestHookIntegration -v

# Full enforcement system test suite
uv run pytest tests/test_agent_review_enforcement.py -v

# Coverage validation for new components
uv run pytest tests/ --cov=.claude/hooks/utils --cov-report=term-missing

# Expected: All tests pass with >90% coverage. If failing, debug and fix implementation.
```

### Level 3: Integration Testing (System Validation)

```bash
# Test enforcement system with simulated agent Task completions
echo '{"session_id": "test-session", "tool_name": "Task", "subagent_type": "n8n-mcp-specialist", "tool_response": {"result": "workflow created without validation"}}' | python .claude/hooks/post_tool_use.py

# Test three-strikes progression with multiple violations
for i in {1..3}; do
  echo '{"session_id": "test-strikes", "tool_name": "Task", "subagent_type": "test-agent", "tool_response": {"result": "task completed without validation"}}' | python .claude/hooks/post_tool_use.py
  sleep 1
done

# Test validation detection with compliant agent responses
echo '{"session_id": "test-compliant", "tool_name": "Task", "subagent_type": "test-agent", "tool_response": {"result": "Let me think step by step and validate against requirements. Checking compliance before proceeding."}}' | python .claude/hooks/post_tool_use.py

# Test session isolation - different sessions should have separate strike counts
echo '{"session_id": "session-1", "tool_name": "Task", "subagent_type": "test-agent", "tool_response": {"result": "violation"}}' | python .claude/hooks/post_tool_use.py
echo '{"session_id": "session-2", "tool_name": "Task", "subagent_type": "test-agent", "tool_response": {"result": "violation"}}' | python .claude/hooks/post_tool_use.py

# Verify audit trail integrity
if [ -f logs/agent-review-audit.json ]; then
  echo "✅ Audit trail created"
  jq . logs/agent-review-audit.json | head -20
else
  echo "❌ Audit trail missing"
fi

# Performance validation - hook execution time
time (echo '{"session_id": "perf-test", "tool_name": "Task", "tool_response": {"result": "test"}}' | python .claude/hooks/post_tool_use.py)

# Expected: All integrations working, audit trail populated, execution time <100ms
```

### Level 4: Real-World Validation

```bash
# Test with actual agent violation scenario (n8n workflow case)
claude_session_id=$(uuidgen | tr '[:upper:]' '[:lower:]')
echo "{\"session_id\": \"$claude_session_id\", \"tool_name\": \"Task\", \"subagent_type\": \"n8n-mcp-specialist\", \"tool_response\": {\"result\": \"Created n8n workflow with API integration. The workflow includes: 1. HTTP Request node for data fetching 2. JavaScript node for data transformation 3. Database node for storage\"}}" | python .claude/hooks/post_tool_use.py

# Test Constitutional AI pattern detection
echo "{\"session_id\": \"$claude_session_id\", \"tool_name\": \"Task\", \"subagent_type\": \"test-agent\", \"tool_response\": {\"result\": \"Let me review this approach step by step. First, I'll validate the requirements against the specification. Second, I'll check the implementation for compliance. Third, I'll verify the test coverage meets standards.\"}}" | python .claude/hooks/post_tool_use.py

# Security boundary validation
echo "{\"session_id\": \"$claude_session_id\", \"tool_name\": \"Bash\", \"tool_input\": {\"command\": \"rm -rf /\"}, \"tool_response\": {\"result\": \"blocked\"}}" | python .claude/hooks/post_tool_use.py

# Memory usage validation during enforcement
ps aux | grep python | grep post_tool_use | awk '{print $6}' | head -1 # Should be <50MB

# Root cause analysis integration test (requires 3 strikes)
for i in {1..3}; do
  echo "{\"session_id\": \"rca-test\", \"tool_name\": \"Task\", \"subagent_type\": \"persistent-violator\", \"tool_response\": {\"result\": \"Task completed without any validation or compliance checking\"}}" | python .claude/hooks/post_tool_use.py
done

# Agent compliance framework integration
.claude/hooks/utils/agent-compliance-checker.py --verbose | grep -E "(ERRORS|WARNINGS|enforcement)"

# Expected: Real-world scenarios handled correctly, memory usage <50MB, RCA triggered at 3 strikes
```

## Final Validation Checklist

### Technical Validation

- [ ] All 4 validation levels completed successfully with zero critical errors
- [ ] Progressive enforcement engine passes all unit tests: `uv run pytest tests/test_agent_review_enforcement.py -v`
- [ ] Hook integration preserves existing functionality: No regression in existing tool usage logging
- [ ] Validation detection accuracy >90%: Constitutional AI patterns and NLP matching working correctly
- [ ] Session isolation working: Different sessions maintain separate strike counts
- [ ] Performance requirements met: Hook execution <100ms, memory usage <50MB
- [ ] Security boundaries enforced: Tool permissions validated, audit trail tamper-proof

### Feature Validation

- [ ] Three-strikes progression working: Warning → Remediation → Root Cause Analysis
- [ ] Validation detection identifies common patterns: "step by step", "validated against", "compliance check"
- [ ] Root cause analysis integration triggered after 3 strikes with sequential thinking MCP
- [ ] Audit trail populated with session-aware violation tracking in logs/agent-review-audit.json
- [ ] workflow-orchestrator updated with mandatory self-review patterns and escalation paths
- [ ] Real-world validation scenarios pass: n8n workflow case, security boundary enforcement

### Code Quality Validation

- [ ] Follows existing codebase patterns: Hook structure, error handling, JSON logging preserved
- [ ] File placement matches desired codebase tree structure: All files in correct directories
- [ ] Security anti-patterns avoided: Graceful degradation, no Claude Code blocking, session isolation
- [ ] Constitutional AI integration working: Self-critique detection, progressive enforcement decisions
- [ ] Agent orchestration integration: Mandatory review gates, security chain preservation

### Documentation & Deployment

- [ ] Implementation follows PRP guidance exactly: All tasks completed in dependency order
- [ ] Audit logs are informative and secure: Cryptographic integrity, session correlation
- [ ] Error handling maintains system stability: All exceptions caught, graceful sys.exit(0)
- [ ] Integration preserves existing security: Tool permissions, agent boundaries, compliance checking

---

## Anti-Patterns to Avoid

- ❌ Don't create complex config files when existing agent instructions suffice
- ❌ Don't block Claude Code operation on hook failures - always exit gracefully with sys.exit(0)
- ❌ Don't over-validate agents that genuinely don't require validation protocols
- ❌ Don't skip the three-strikes progression - progressive enforcement is critical for learning
- ❌ Don't ignore session isolation - strikes must be per-session, not global
- ❌ Don't modify tool permissions without security review - maintain existing boundaries
- ❌ Don't bypass Constitutional AI patterns - self-critique detection is core to the system
- ❌ Don't ignore performance requirements - hook execution must remain <100ms
- ❌ Don't compromise audit trail integrity - cryptographic signatures prevent tampering
- ❌ Don't assume agent validation requirements - use NLP pattern matching for detection