
# Implementation Plan: CC-Boilerplate Strategic Accelerator Framework

**Branch**: `002-prps-prd-cc` | **Date**: 2025-01-21 | **Spec**: [/specs/002-prps-prd-cc/spec.md](./spec.md)
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
Primary requirement: Comprehensive development framework enabling rapid project recovery and MVP creation within 6 hours, transforming chaotic brown-field projects or green-field opportunities into production-ready systems with enterprise-grade quality and security through hierarchical agent orchestration, automated PRP discovery workflow, and mandatory security validation chains.

## Technical Context
**Language/Version**: Python 3.11+ (required minimum), Bash scripting, Markdown, YAML
**Primary Dependencies**: UV package manager, Python standard library only, Pre-commit hooks, GitHub Actions, Git/GitHub CLI
**Storage**: File-based storage, JSON configuration files, Markdown documentation, Git repository as primary data store, structured log files
**Testing**: Python unittest framework, subprocess-based testing, mock infrastructure, tiered testing (Unit → Integration → Full), behavioral regression testing
**Target Platform**: Cross-platform (macOS, Linux, Windows), Claude Code environment required, CI/CD on Ubuntu Latest
**Project Type**: CLI/Framework hybrid - Agent orchestration system with 100+ specialized AI agents
**Performance Goals**: Hook execution <3s, test suite <2min, real-time agent delegation, interactive CLI, memory <100MB
**Constraints**: Zero external dependencies (KISS/YAGNI), security-first design, standard library only, no database dependencies, subprocess isolation
**Scale/Scope**: 100+ specialist agents, 8 pre-configured hooks, ~60% test coverage, multi-tier CI/CD, enterprise-ready audit trails

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**KISS/YAGNI Supremacy Check**:
- ✅ Uses simplest approach (file-based storage, standard library only)
- ✅ No unnecessary abstractions or frameworks
- ✅ Clear naming and single-responsibility functions
- ✅ 95%+ certainty requirement met for all technical choices

**Security-First Architecture Check**:
- ✅ Mandatory security chains implemented (code-reviewer → security-orchestrator → security-scanner)
- ✅ Tool least privilege enforced for all 100+ agents
- ✅ Command protection (rm -rf prevention, environment variable blocking)
- ✅ Real-time validation before tool execution

**Hierarchical Agent Orchestration Check**:
- ✅ 100+ specialized agents with dynamic discovery via workflow-orchestrator
- ✅ Cognitive load optimization (Haiku/Sonnet/Opus allocation)
- ✅ Agent boundary enforcement (analyzers read-only, specialists domain-restricted)
- ✅ Mandatory orchestration for complex multi-step tasks

**Validation-Driven Development Check**:
- ✅ Contrarian discipline protocol implemented for all decisions
- ✅ Problem resolution hierarchy (tactical/operational/strategic)
- ✅ PRP structure prevents scope creep
- ✅ Harsh validation with certainty percentages

**Test-Driven Development Check**:
- ✅ Tests before implementation enforced
- ✅ Red-Green-Refactor cycle followed
- ✅ Contract tests generated before endpoints
- ✅ Coverage requirements with test-coverage-analyzer

**CEO Behavioral Framework Check**:
- ✅ Identity transformation: "I am a CEO who delegates everything"
- ✅ Submarine leadership protocol with intent statements
- ✅ Named organizational roles (CoS: workflow-orchestrator, CISO: security-orchestrator)
- ✅ Intelligence vs implementation distinction maintained
- ✅ Bad CEO smell detection prevents direct implementation

**Constitution Compliance**: ✅ PASS - All principles aligned with feature requirements

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

**Structure Decision**: [DEFAULT to Option 1 unless Technical Context indicates web/mobile app]

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
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each contract → contract test task [P]
- Each entity → model creation task [P] 
- Each user story → integration test task
- Implementation tasks to make tests pass

**Ordering Strategy**:
- TDD order: Tests before implementation 
- Dependency order: Models before services before UI
- Mark [P] for parallel execution (independent files)

**Estimated Output**: 25-30 numbered, ordered tasks in tasks.md

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
- [ ] Phase 0: Research complete (/plan command)
- [ ] Phase 1: Design complete (/plan command)
- [ ] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [ ] Initial Constitution Check: PASS
- [ ] Post-Design Constitution Check: PASS
- [ ] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*
