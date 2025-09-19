# Product Requirement Prompt (PRP) Concept

"Over-specifying what to build while under-specifying the context, and how to build it, is why so many AI-driven coding attempts stall at 80%. A Product Requirement Prompt (PRP) fixes that by fusing the disciplined scope of a classic Product Requirements Document (PRD) with the "context-is-king" mindset of modern prompt engineering."

## Planning & Roadmap Location

- **Current Roadmap**: Always in main README.md (source of truth)
- **Feature Planning**: Create new PRP files here
- **NO separate planning docs** - they just create confusion

## What is a PRP?

Product Requirement Prompt (PRP)
A PRP is a structured prompt that supplies an AI coding agent with everything it needs to deliver a vertical slice of working software—no more, no less.

### How it differs from a PRD

A traditional PRD clarifies what the product must do and why customers need it, but deliberately avoids how it will be built.

A PRP keeps the goal and justification sections of a PRD yet adds three AI-critical layers:

### Context

- Precise file paths and content, library versions and library context, code snippets examples. LLMs generate higher-quality code when given direct, in-prompt references instead of broad descriptions. Usage of a ai_docs/ directory to pipe in library and other docs.

### Implementation Details and Strategy

- In contrast of a traditional PRD, a PRP explicitly states how the product will be built. This includes the use of API endpoints, test runners, or agent patterns (ReAct, Plan-and-Execute) to use. Usage of typehints, dependencies, architectural patterns and other tools to ensure the code is built correctly.

### Validation Gates

- Deterministic checks such as pytest, ruff, or static type passes “Shift-left” quality controls catch defects early and are cheaper than late re-work.
  Example: Each new funtion should be individaully tested, Validation gate = all tests pass.

### PRP Layer Why It Exists

- The PRP folder is used to prepare and pipe PRPs to the agentic coder.

## Why context is non-negotiable

Large-language-model outputs are bounded by their context window; irrelevant or missing context literally squeezes out useful tokens

The industry mantra “Garbage In → Garbage Out” applies doubly to prompt engineering and especially in agentic engineering: sloppy input yields brittle code

## In short

A PRP is PRD + curated codebase intelligence + agent/runbook—the minimum viable packet an AI needs to plausibly ship production-ready code on the first pass.

The PRP can be small and focusing on a single task or large and covering multiple tasks.
The true power of PRP is in the ability to chain tasks together to build, self-validate and ship complex features.

## NEW: Spec-Kit Integration Workflow

**Enhanced PRP System (v4+)**: PRPs now integrate with GitHub's spec-kit to provide structured phase separation while preserving automatic context discovery.

### The Enhanced Workflow

```
1. PRP Creation (Automatic Context Discovery)
   └─ /prp:create → PRPs/prp-XXX-feature.md
   └─ WHAT & WHY with curated context

2. Specification Transformation
   └─ /prp:to-spec → specs/XXX-feature/spec.md
   └─ PRP context → spec-kit format

3. Technical Planning
   └─ /plan → specs/XXX-feature/plan.md
   └─ Architecture decisions (HOW at system level)

4. Task Breakdown
   └─ /tasks → specs/XXX-feature/tasks.md
   └─ Implementation steps (HOW at code level)

5. Implementation
   └─ /implement → Working code
   └─ TDD execution with validation gates
```

### Why This Hybrid Approach

**Problem Solved**: The original PRP system mixed "WHAT" with "HOW" causing implementation drift and scope creep.

**Solution**:
- **Keep PRP's strength**: Automatic context discovery (superior to manual specification)
- **Add spec-kit's strength**: Clear phase separation prevents drift
- **Skip redundancy**: Don't use spec-kit's `/specify` - PRP already does it better

### Available Commands

```bash
# Install spec-kit integration
/prp:install-speckit

# Transform PRP to spec-kit format
/prp:to-spec PRPs/prp-005-my-feature.md

# Transform and proceed to planning
/prp:to-plan PRPs/prp-005-my-feature.md

# Validate KISS/YAGNI compliance
/prp:validate specs/005-my-feature/

# Check workflow status
/prp:workflow-status
```

### Context Engineering vs Specification Engineering

**PRP = Context Engineering**:
- Automatic discovery through codebase analysis
- Environmental awareness and pattern detection
- Minimal user input required
- AI actively curates context

**Spec-Kit = Specification Engineering**:
- Manual, exhaustive specification
- Clear phase boundaries
- Structured handoffs
- TDD-driven implementation

**Hybrid = Best of Both Worlds**: Automatic discovery + structured execution
