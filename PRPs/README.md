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

### Command Purposes & Value-Add

#### 1. `/prp/init` - Discovery & PRD Creation
**Input**: Raw feature idea or concept
**Output**: Comprehensive PRD with research and architecture
**Value-Add**:
- Market and technical research (web searches)
- User story development with acceptance criteria
- Technical architecture diagrams (Mermaid)
- API design and data models
- Implementation strategy and phases
- Risk analysis with mitigations
- Success metrics definition

**Template**: `PRPs/templates/prp_planning.md`

#### 2. `/specify` - Business Requirements Formalization
**Input**: PRD from step 1 (or raw description)
**Output**: Formal business specification
**Value-Add**:
- Extracts functional requirements (FR-XXX format)
- Creates user scenarios in Given/When/Then format
- Identifies edge cases and error scenarios
- Simplifies technical concepts to business language
- Marks ambiguities for clarification
- Focuses on WHAT not HOW

**Template**: `.specify/templates/spec-template.md`

#### 3. `/prp/create` - Implementation Planning
**Input**: Business spec from step 2
**Output**: Technical implementation PRP
**Value-Add**:
- Codebase analysis and pattern identification
- Technical context and file references
- Implementation-specific gotchas and constraints
- Validation commands and testing strategy
- Code-level details and integration points

**Template**: `PRPs/templates/prp_base.md`

### Key Separation Principles

| Phase | Focus | Audience | Technical Detail |
|-------|-------|----------|------------------|
| **PRD (init)** | Discovery & Architecture | Product/Tech stakeholders | Medium (architectural) |
| **Spec (specify)** | Business Requirements | Business stakeholders | Low (user-focused) |
| **PRP (create)** | Implementation | Developer | High (code-level) |

### Usage Examples

#### Starting from Scratch
```bash
# 1. Create PRD
claude /prp/init "Build notification system for user alerts"

# 2. Generate business spec
claude /specify "$(cat PRPs/notification-system-prd.md)"

# 3. Create implementation PRP
claude /prp/create "Implement notification system per spec-001-notification"
```

#### Skip PRD (Simple Features)
```bash
# Direct to spec for simple features
claude /specify "Add dark mode toggle to settings page"

# Then implementation PRP
claude /prp/create "Implement dark mode per spec-002-dark-mode"
```

**Problem Solved**: The original PRP system mixed "WHAT" with "HOW" causing implementation drift and scope creep.

**Solution**:
- **Keep PRP's strength**: Automatic context discovery (superior to manual specification)
- **Add spec-kit's strength**: Clear phase separation prevents drift
- **Skip redundancy**: Don't use spec-kit's `/specify` - PRP already does it better

### Available Commands

```bash
# Create PRP with automatic spec generation
/prp:create "feature description"

# Legacy: Direct PRP implementation (use spec-kit workflow instead)
/prp:execute PRPs/prp-XXX-feature.md
```

### Naming Conventions

**Strict naming patterns ensure consistency and traceability:**

#### PRP Files
```
PRPs/prp-{3-digit-sequence-number}-{feature-name}.md
```
Examples:
- `PRPs/prp-007-user-profile.md`
- `PRPs/prp-008-auth-system.md`

#### Spec Files

**Single Spec (cohesive feature)**:
```
specs/{3-digit-sequence-number}-{feature-name}/spec.md
```
Example: `specs/007-user-profile/spec.md`

**Multiple Specs (architect splits)**:
```
specs/{3-digit-sequence-number}-{feature-name}-{component}/spec.md
```
Examples:
- `specs/008-auth-system-frontend/spec.md`
- `specs/008-auth-system-backend/spec.md`
- `specs/008-auth-system-infrastructure/spec.md`

#### Branch Names
```
feature/prp-{3-digit-sequence-number}-{feature-name}
```
Example: `feature/prp-008-auth-system`

**Key Rules**:
- Sequence numbers are always 3 digits (007, not 7)
- Same sequence number links PRP to all its spec files
- Component names are architect-decided: frontend, backend, database, infrastructure, api, webhooks, auth, notifications

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
