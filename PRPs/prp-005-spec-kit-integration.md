name: "PRP System Enhancement with GitHub Spec-Kit Integration"
description: |

---

## Status

Status: PROPOSED
Status_Date: 2025-01-19
Status_Note: Implements hybrid approach combining PRP's automatic context discovery with spec-kit's phase separation

## Goal

**Feature Goal**: Integrate GitHub's spec-kit as upstream dependency to solve implementation drift problem while preserving PRP's automatic context discovery innovation.

**Deliverable**:
- Enhanced PRP system with clear phase separation (PRP → Plan → Tasks → Implement)
- Transformation layer that feeds PRP output to spec-kit commands
- Wrapper scripts and commands for seamless workflow
- Migration approach for existing IN-PROGRESS PRPs

**Success Definition**:
- No more "freestyle implementation" after PRP creation
- Automatic context discovery preserved and enhanced
- Clear phase boundaries prevent scope drift
- One-pass implementation success through structured handoffs

## User Persona

**Target User**: Developers using PRP system who experience implementation drift and scope creep

**Use Case**: Developer creates PRP with automatic context discovery, then follows structured spec-kit phases for implementation without losing AI context

**User Journey**:
1. Run `/prp:create [feature]` - automatic context discovery creates comprehensive PRP
2. Run `/plan` - PRP context automatically feeds into architectural planning
3. Run `/tasks` - plan feeds into implementation breakdown
4. Run `/implement` - TDD execution with validation gates

**Pain Points Addressed**:
- Implementation gets derailed after PRP (freestyle coding)
- Mixing WHAT/WHY with HOW in PRP feels wrong
- Missing structured phases between requirements and implementation
- Manual context input required by traditional spec-driven approaches

## Why

- **Business Value**: Prevents implementation drift and scope creep, leading to successful one-pass implementations
- **Integration**: Leverages GitHub's maintained spec-kit instead of reinventing the wheel
- **Problems Solved**:
  - Eliminates the gap between PRP and implementation
  - Preserves PRP's automatic context discovery advantage
  - Adds missing phase separation for clear boundaries
  - Reduces manual specification burden through intelligent transformation

## What

### User-Visible Behavior

- PRP creation remains unchanged (automatic context discovery)
- New workflow commands available: `/prp:to-spec`, `/prp:to-plan`
- Clear progression through phases with validation gates
- Automatic transformation of PRP data to spec-kit format
- Structured handoffs prevent context loss

### Technical Requirements

- GitHub spec-kit installed as upstream dependency
- Transformation layer between PRP and spec-kit
- Modified PRP template without implementation tasks
- Integration scripts and wrapper commands
- Migration path for existing IN-PROGRESS PRPs

### Success Criteria

- [ ] Spec-kit successfully installed and integrated
- [ ] PRP output automatically transforms to spec-kit input
- [ ] Implementation tasks removed from PRP template
- [ ] Clear phase boundaries prevent scope drift
- [ ] Automatic context discovery preserved
- [ ] Existing prp-004 successfully migrated to new structure
- [ ] Validation gates maintain KISS/YAGNI principles
- [ ] One-pass implementation success rate improved

## All Needed Context

### Context Completeness Check

_This PRP provides complete implementation context including: spec-kit integration patterns, transformation approaches, existing system analysis, clear phase separation design, and specific implementation tasks ordered by dependencies._

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: https://github.com/github/spec-kit
  why: Upstream dependency for phase separation and structured development
  critical: Must not modify spec-kit itself - use as-is with transformation layer

- url: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
  why: Official spec-kit methodology and workflow explanation
  critical: Understanding three-phase approach (specify→plan→implement)

- file: PRPs/README.md
  why: Current PRP concept and methodology
  pattern: Context engineering approach vs specification engineering
  gotcha: Must preserve automatic context discovery advantage

- file: PRPs/templates/prp_base.md
  why: Current template structure with implementation tasks
  pattern: Template modification approach - remove tasks, add spec-kit integration
  gotcha: Maintain all context discovery sections

- file: PRPs/prp-004-agent-system-redesign.md
  why: Current IN-PROGRESS PRP for migration demonstration
  pattern: How to split WHAT/WHY from HOW (implementation)
  gotcha: Only IN-PROGRESS/PROPOSED PRPs need migration

- file: docs/adr/adr-005-adr-prp-separation.md
  why: Clear separation of concerns between different document types
  pattern: ADR (architectural) vs PRP (tactical) vs Spec (requirements)
  gotcha: Maintain clear boundaries between document purposes

- docfile: PRPs/ai_docs/context-engineering-principles.md
  why: Research findings on context engineering vs specification engineering
  section: Automatic discovery vs manual specification patterns
```

### Current Codebase Tree

```bash
cc-boilerplate/
├── PRPs/
│   ├── README.md                    # Current PRP concept
│   ├── templates/
│   │   ├── prp_base.md             # Current template (has implementation tasks)
│   │   ├── prp_tina_contract.md    # Alternative template
│   │   └── prp_planning.md         # Planning template
│   ├── prp-004-agent-system-redesign.md  # IN-PROGRESS PRP to migrate
│   └── ai_docs/                    # Documentation for complex patterns
├── docs/adr/
│   ├── adr-005-adr-prp-separation.md    # Separation of concerns
│   └── adr-007-agent-system-architecture.md  # Hierarchical agents
├── scripts/                        # Build and utility scripts
└── .claude/
    ├── commands/                   # Custom commands
    └── hooks/                      # Validation hooks
```

### Desired Codebase Tree with Files to be Added

```bash
cc-boilerplate/
├── PRPs/
│   ├── prp-005-spec-kit-integration.md     # This PRP
│   ├── templates/
│   │   └── prp_base.md             # MODIFIED: Remove implementation tasks
│   └── README.md                   # UPDATED: New workflow documentation
├── scripts/
│   └── prp-to-speckit.sh          # NEW: Transformation script
├── .claude/commands/
│   └── spec-workflow.sh           # NEW: Wrapper commands
├── specs/                          # NEW: Spec-kit output directory
│   └── 004-agent-system/          # NEW: Migrated prp-004
│       ├── spec.md                 # Transformed from PRP
│       ├── plan.md                 # Architecture decisions
│       └── tasks.md                # Implementation breakdown
└── memory/                         # NEW: Spec-kit constitution (if needed)
    └── constitution.md
```

### Known Gotchas of our codebase & Library Quirks

```bash
# CRITICAL: Spec-kit uses uvx for installation - no permanent install
# Must use: uvx --from git+https://github.com/github/spec-kit.git specify init
# Do not modify spec-kit itself - use transformation layer

# GOTCHA: Spec-kit creates /specify, /plan, /tasks, /implement commands
# Our PRP already does /specify better - skip that command
# Map PRP output directly to /plan phase

# CRITICAL: Only migrate IN-PROGRESS or PROPOSED PRPs
# Completed PRPs (prp-001, prp-002, prp-003) remain unchanged
# Current status check: grep -l "Status: PROPOSED\|Status: IN_PROGRESS" PRPs/*.md

# GOTCHA: Spec-kit expects manual user input for specification
# Our PRP provides automatic context discovery - must transform this data
# Don't lose the context advantage that makes PRP superior
```

## Implementation Blueprint

### Data Models and Structure

Create the transformation data models to ensure clean handoffs between systems.

```yaml
# PRP to Spec-Kit Data Mapping
prp_data:
  goal: Maps to spec.functional_requirements
  why: Maps to spec.business_value
  what: Maps to spec.user_scenarios
  context: Maps to plan.technical_context
  validation: Maps to implement.test_strategy

constitution_data:
  claude_md: Maps to constitution.principles
  adrs: Maps to constitution.decisions
  kiss_yagni: Maps to constitution.constraints
```

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: INSTALL spec-kit dependency
  - EXECUTE: uvx --from git+https://github.com/github/spec-kit.git specify init . --ai claude
  - VALIDATE: Commands /constitution, /plan, /tasks, /implement available
  - GOTCHA: Do not run /specify - we'll skip that with PRP
  - PLACEMENT: Root directory

Task 2: CREATE scripts/prp-to-speckit.sh transformation script
  - IMPLEMENT: Data transformation functions (prp_to_spec_format, claude_md_to_constitution)
  - FOLLOW pattern: scripts/build-config.sh (bash scripting approach)
  - FUNCTION: extract_prp_sections, transform_context, validate_transformation
  - DEPENDENCIES: None
  - PLACEMENT: scripts/ directory

Task 3: MODIFY PRPs/templates/prp_base.md template
  - REMOVE: "Implementation Tasks" section (lines 103-145)
  - ADD: "Spec-Kit Integration" section with next_command guidance
  - PRESERVE: All context discovery sections, validation gates, success criteria
  - FOLLOW pattern: Existing template structure and YAML frontmatter
  - DEPENDENCIES: Task 1 (understand spec-kit structure)
  - PLACEMENT: PRPs/templates/

Task 4: CREATE .claude/commands/spec-workflow.sh wrapper commands
  - IMPLEMENT: /prp:to-spec, /prp:to-plan, /prp:validate commands
  - FOLLOW pattern: .claude/hooks/ structure (executable scripts)
  - NAMING: spec-workflow.sh with multiple command functions
  - DEPENDENCIES: Task 2 (transformation script)
  - PLACEMENT: .claude/commands/

Task 5: UPDATE PRPs/README.md workflow documentation
  - MODIFY: Add new workflow section (PRP → Plan → Tasks → Implement)
  - PRESERVE: Existing PRP concept explanation
  - ADD: Command reference for new workflow
  - FOLLOW pattern: Existing README structure and tone
  - DEPENDENCIES: Tasks 1-4 (understand complete workflow)
  - PLACEMENT: PRPs/

Task 6: MIGRATE PRPs/prp-004-agent-system-redesign.md
  - EXTRACT: Implementation tasks to specs/004-agent-system/tasks.md
  - TRANSFORM: PRP context to specs/004-agent-system/plan.md
  - PRESERVE: WHAT/WHY in original PRP
  - FOLLOW pattern: Spec-kit plan and tasks templates
  - DEPENDENCIES: Tasks 1-2 (transformation capabilities)
  - PLACEMENT: specs/004-agent-system/

Task 7: CREATE comprehensive integration tests
  - IMPLEMENT: End-to-end workflow validation
  - TEST: PRP creation → transformation → spec-kit phases
  - VALIDATE: Context preservation, phase boundaries, KISS/YAGNI gates
  - FOLLOW pattern: Existing validation approaches
  - DEPENDENCIES: All previous tasks
  - PLACEMENT: Test validation commands
```

### Implementation Patterns & Key Details

```bash
# Transformation Script Pattern
transform_prp_to_spec() {
    local prp_file="$1"
    local spec_dir="$2"

    # Extract sections using yq/jq for YAML frontmatter
    # PATTERN: Preserve context while transforming format
    # GOTCHA: Don't lose automatic discovery data

    yq eval '.goal' "$prp_file" > "${spec_dir}/requirements.yaml"
    # CRITICAL: Maintain all context from PRP Context section
}

# Command Wrapper Pattern
prp_to_plan() {
    # PATTERN: Transform PRP → feed to spec-kit /plan
    ./scripts/prp-to-speckit.sh "$1"
    # GOTCHA: Ensure spec-kit has all needed context
    /plan  # Delegate to spec-kit
}

# Template Modification Pattern
# REMOVE implementation tasks section (current scope-bleed problem)
# ADD clear handoff to spec-kit phases
# PRESERVE context discovery sections (our innovation)
```

### Integration Points

```yaml
SPEC_KIT:
  - install: "uvx spec-kit with Claude templates"
  - commands: "/plan, /tasks, /implement (skip /specify and /constitution)"
  - output: "specs/ directory with phase-separated files"

PRP_SYSTEM:
  - modify: PRPs/templates/prp_base.md
  - preserve: "Automatic context discovery, validation gates"
  - enhance: "Integration with spec-kit phases"

TRANSFORMATION:
  - script: scripts/prp-to-speckit.sh
  - mapping: "PRP sections → spec-kit format"
  - validation: "KISS/YAGNI gates between phases"
```

## Validation Loop

### Level 1: Installation & Integration (Immediate Feedback)

```bash
# Verify spec-kit installation
uvx --from git+https://github.com/github/spec-kit.git specify init . --ai claude
echo "Checking for spec-kit commands..."
if command -v /plan >/dev/null 2>&1; then
    echo "✅ Spec-kit commands available"
else
    echo "❌ Spec-kit installation failed"
    exit 1
fi

# Verify transformation script
./scripts/prp-to-speckit.sh --test
echo "Testing PRP to spec transformation..."

# Expected: Spec-kit commands available, transformation script functional
```

### Level 2: Template & Command Validation (Component Testing)

```bash
# Test modified PRP template
echo "Validating PRP template changes..."
grep -q "Implementation Tasks" PRPs/templates/prp_base.md && echo "❌ Implementation tasks still present" || echo "✅ Implementation tasks removed"

# Test wrapper commands
source .claude/commands/spec-workflow.sh
prp_to_plan --test || echo "❌ Command wrapper failed"

# Test transformation accuracy
./scripts/prp-to-speckit.sh PRPs/prp-004-agent-system-redesign.md specs/004-agent-system/
ls specs/004-agent-system/ | grep -E "(plan|tasks)\.md" || echo "❌ Transformation failed"

# Expected: Template clean, commands working, transformation producing expected files
```

### Level 3: End-to-End Workflow (System Validation)

```bash
# Test complete workflow
echo "Testing end-to-end PRP → spec-kit workflow..."

# 1. Create test PRP (simulated)
echo "Creating test PRP..."
cp PRPs/templates/prp_base.md /tmp/test-prp.md

# 2. Transform to spec-kit format
./scripts/prp-to-speckit.sh /tmp/test-prp.md /tmp/test-spec/

# 3. Run spec-kit phases
cd /tmp/test-spec/
/plan < plan-input.md
/tasks < plan.md
/implement --dry-run

# 4. Validate outputs
test -f plan.md && test -f tasks.md && echo "✅ Complete workflow successful" || echo "❌ Workflow incomplete"

# Expected: All phases complete successfully, files generated, no context loss
```

### Level 4: Migration & Compatibility (Production Validation)

```bash
# Test prp-004 migration
echo "Testing prp-004 migration..."
./scripts/prp-to-speckit.sh PRPs/prp-004-agent-system-redesign.md specs/004-agent-system/

# Validate migration preserves content
original_tasks=$(grep -c "Task [0-9]" PRPs/prp-004-agent-system-redesign.md)
migrated_tasks=$(grep -c "T[0-9]" specs/004-agent-system/tasks.md)
[ "$original_tasks" -eq "$migrated_tasks" ] && echo "✅ Migration preserved all tasks" || echo "❌ Task count mismatch"

# Validate WHAT/WHY preserved in PRP
grep -q "Feature Goal" PRPs/prp-004-agent-system-redesign.md && echo "✅ WHAT/WHY preserved"

# Test KISS/YAGNI validation gates
./scripts/prp-to-speckit.sh --validate-kiss-yagni specs/004-agent-system/

# Expected: Migration successful, content preserved, validation gates functional
```

## Final Validation Checklist

### Technical Validation

- [ ] Spec-kit successfully installed: `uvx spec-kit commands available`
- [ ] Transformation script functional: `./scripts/prp-to-speckit.sh --test`
- [ ] PRP template updated: `grep -v "Implementation Tasks" PRPs/templates/prp_base.md`
- [ ] Wrapper commands working: `source .claude/commands/spec-workflow.sh && prp_to_plan --test`
- [ ] Migration successful: `test -d specs/004-agent-system/ && test -f specs/004-agent-system/plan.md`

### Feature Validation

- [ ] PRP automatic context discovery preserved
- [ ] Clear phase boundaries established (PRP → Plan → Tasks → Implement)
- [ ] Implementation drift prevented through structured handoffs
- [ ] KISS/YAGNI validation gates functional at each phase
- [ ] One-pass implementation success improved

### Code Quality Validation

- [ ] No modification to upstream spec-kit (used as-is)
- [ ] Transformation preserves all PRP context
- [ ] Integration follows existing codebase patterns
- [ ] Migration only affects IN-PROGRESS PRPs (prp-004)
- [ ] Backward compatibility maintained for completed PRPs

### Documentation & Workflow

- [ ] README updated with new workflow documentation
- [ ] Command reference available for new workflow
- [ ] Clear guidance on when to use each phase
- [ ] Migration instructions documented for future PRPs

---

## Anti-Patterns to Avoid

- ❌ Don't modify spec-kit itself - use transformation layer
- ❌ Don't lose PRP's automatic context discovery advantage
- ❌ Don't migrate completed PRPs - only IN-PROGRESS/PROPOSED
- ❌ Don't mix implementation details back into PRP template
- ❌ Don't skip validation gates between phases
- ❌ Don't use /specify command - PRP already does it better