
# Implementation Plan: CC-Boilerplate Strategic Accelerator Framework

**Branch**: `002-prps-prd-cc` | **Date**: 2025-01-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-prps-prd-cc/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code or `AGENTS.md` for opencode).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Implement comprehensive development framework enabling rapid project recovery and MVP creation within 6 hours. Primary focus on LLM behavioral testing framework (FR-021-025) to validate CEO role adherence, delegation patterns, and contrarian discipline compliance through automated conversation analysis and regression testing.

## Technical Context
**Language/Version**: Python 3.11+ (behavioral testing framework, agent validation)
**Primary Dependencies**: pytest (testing), langchain/anthropic (LLM integration), Linear API (task management), GitHub API (repo management)
**Storage**: File-based specs structure, conversation logs (JSON), git-tracked artifacts
**Testing**: pytest (behavioral validation), LLM-as-Judge methodology, regression testing suite
**Target Platform**: macOS/Linux development environments, Claude Code CLI
**Project Type**: single - CLI framework with agent coordination
**Performance Goals**: <6 hours idea-to-MVP, >95% behavioral compliance detection, <30 minutes onboarding
**Constraints**: Zero security incidents tolerance, maintain <150 lines CLAUDE.md, non-blocking quality gates
**Scale/Scope**: 100+ agents, enterprise-grade security, 10x productivity multiplier target

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**CEO Framework Compliance**:
- ✓ Delegation through workflow-orchestrator (not direct implementation)
- ✓ Contrarian discipline application to architectural decisions
- ✓ Security-orchestrator mandatory for sensitive operations
- ✓ KISS/YAGNI principles: behavioral testing essential, not over-engineering
- ✓ 10x productivity goal aligns with strategic framework purpose

**No Constitution Violations Detected** - Framework enhances rather than violates CEO principles

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure]
```

**Structure Decision**: Option 1 (Single project) - CLI framework with agent coordination, no frontend/backend separation needed

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/bash/update-agent-context.sh claude` for your AI assistant
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from behavioral testing requirements (FR-021-025)
- Each behavioral test category → test implementation task [P]
- Each API endpoint → contract test task [P]
- Each data entity → model creation task [P]
- Conversation log analysis → background processing task
- LLM-as-Judge integration → evaluation service task
- Regression analysis → reporting task
- pytest integration → test suite enhancement task

**Specific Task Categories**:
1. **Behavioral Testing Infrastructure**: Core testing framework setup
2. **LLM Judge Integration**: External LLM evaluation service setup
3. **Conversation Log Processing**: Real-time analysis pipeline
4. **Baseline Management**: Behavioral baseline creation and maintenance
5. **Regression Detection**: Automated regression analysis
6. **API Implementation**: REST API for behavioral testing
7. **Integration Tests**: End-to-end behavioral validation
8. **Documentation**: Behavioral testing guide and examples

**Ordering Strategy**:
- Infrastructure first: Testing framework foundation
- TDD order: Behavioral tests before implementation
- Dependency order: Models → Services → API → Integration
- Mark [P] for parallel execution (independent components)
- Critical path: Conversation logging → Analysis → Regression detection

**Estimated Output**: 25-30 numbered, ordered tasks focusing on behavioral testing framework

**Priority Focus**: FR-021-025 implementation (LLM behavioral regression testing) as highest priority

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*
