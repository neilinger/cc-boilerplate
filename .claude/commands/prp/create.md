# Create Implementation PRP

## Feature: $ARGUMENTS

## PRP Creation Mission

Create a comprehensive implementation PRP that enables **one-pass implementation success** through systematic research and context curation.

**Position in Workflow**: This command creates technical implementation PRPs with codebase context. For feature discovery and business requirements, use:
- `/prp/init` → Creates PRD with research and architecture
- `/specify` → Creates formal business requirements from PRD
- `/prp/create` → Creates implementation PRP (this command)

**Critical Understanding**: The executing AI agent only receives:

- Start by reading and understanding the prp concepts PRPs/README.md
- The PRP content you create
- Its training data knowledge
- Access to codebase files (but needs guidance on which ones)

**Therefore**: Your research and context curation directly determines implementation success. Incomplete context = implementation failure.

## Research Process

> During the research process, create clear tasks and spawn as many agents and subagents as needed using the batch tools. The deeper research we do here the better the PRP will be. we optminize for chance of success and not for speed.

1. **Codebase Analysis in depth**
   - Create clear todos and spawn subagents to search the codebase for similar features/patterns Think hard and plan your approach
   - Identify all the necessary files to reference in the PRP
   - Note all existing conventions to follow
   - Check existing test patterns for validation approach
   - Use the batch tools to spawn subagents to search the codebase for similar features/patterns

2. **External Research at scale**
   - Create clear todos and spawn with instructions subagents to do deep research for similar features/patterns online and include urls to documentation and examples
   - Library documentation (include specific URLs)
   - For critical pieces of documentation add a .md file to PRPs/ai_docs and reference it in the PRP with clear reasoning and instructions
   - Implementation examples (GitHub/StackOverflow/blogs)
   - Best practices and common pitfalls found during research
   - Use the batch tools to spawn subagents to search for similar features/patterns online and include urls to documentation and examples

3. **User Clarification**
   - Ask for clarification if you need it

## PRP Generation Process

### Step 1: Choose Template

Use `PRPs/templates/prp_base.md` as your template structure - it contains all necessary sections and formatting.

### Step 2: Context Completeness Validation

Before writing, apply the **"No Prior Knowledge" test** from the template:
_"If someone knew nothing about this codebase, would they have everything needed to implement this successfully?"_

### Step 3: Research Integration

Transform your research findings into the template sections:

**Goal Section**: Use research to define specific, measurable Feature Goal and concrete Deliverable
**Context Section**: Populate YAML structure with your research findings - specific URLs, file patterns, gotchas
**Implementation Tasks**: Create dependency-ordered tasks using information-dense keywords from codebase analysis
**Validation Gates**: Use project-specific validation commands that you've verified work in this codebase

### Step 4: Information Density Standards

Ensure every reference is **specific and actionable**:

- URLs include section anchors, not just domain names
- File references include specific patterns to follow, not generic mentions
- Task specifications include exact naming conventions and placement
- Validation commands are project-specific and executable

### Step 5: ULTRATHINK Before Writing

After research completion, create comprehensive PRP writing plan using TodoWrite tool:

- Plan how to structure each template section with your research findings
- Identify gaps that need additional research
- Create systematic approach to filling template with actionable context

## Output

### Phase 1: PRP Creation

Save as: `PRPs/prp-{next-sequence-number}-{feature-name}.md`

**Naming Pattern**: prp-XXX-feature-name.md where:

- XXX is a 3-digit sequence number (001, 002, 003...)
- feature-name is a kebab-case description of the feature goal
- Example: `prp-001-documentation-migration.md`, `prp-002-github-maintenance-check.md`

**IMPORTANT**: When creating the PRP from the template, automatically:

1. Set `Status: PROPOSED`
2. Set `Status_Date:` to today's date (YYYY-MM-DD format)
3. Leave `Status_Note:` empty unless there's specific context to add

### Phase 2: Architectural Analysis & Spec Generation

After PRP creation, automatically spawn the `architect-review` agent to analyze the feature for spec splitting:

**Agent Task**: "Analyze this PRP for architectural boundaries and decide spec structure. Consider:
- Bounded contexts and domain separation
- Frontend/backend/infrastructure split needs
- Team ownership boundaries
- Implementation complexity and phasing
- Service decomposition opportunities

Decide between:
1. Single spec: One cohesive feature (specs/{number}-{feature}/spec.md)
2. Multiple specs: Split by components (specs/{number}-{feature}-{component}/spec.md)

For splits, use clear component names: frontend, backend, database, infrastructure, api, webhooks, auth, notifications."

### Phase 3: Spec File Generation

Based on architect decision, create spec files following **exact naming convention**:

**Single Spec Pattern**:
```
specs/{3-digit-sequence-number}-{feature-name}/spec.md
```

**Multiple Specs Pattern**:
```
specs/{3-digit-sequence-number}-{feature-name}-{component}/spec.md
```

**Examples**:
- Single: `specs/007-user-profile/spec.md`
- Multiple: `specs/008-auth-system-frontend/spec.md`, `specs/008-auth-system-backend/spec.md`

**Spec Content**: Transform PRP sections into spec-kit format:
- PRP Goal → Spec Overview & Functional Requirements
- PRP Why → Spec Business Value
- PRP What → Spec User-Visible Behavior
- PRP Context → Spec Context and Constraints

### Phase 4: Branch & Status Management

1. Create feature branch: `feature/prp-{3-digit-sequence-number}-{feature-name}`
2. Update PRP status to `IN_PROGRESS`
3. Add spec file references to PRP status note

## PRP Quality Gates

### Context Completeness Check

- [ ] Passes "No Prior Knowledge" test from template
- [ ] All YAML references are specific and accessible
- [ ] Implementation tasks include exact naming and placement guidance
- [ ] Validation commands are project-specific and verified working

### Template Structure Compliance

- [ ] All required template sections completed
- [ ] Goal section has specific Feature Goal, Deliverable, Success Definition
- [ ] Implementation Tasks follow dependency ordering
- [ ] Final Validation Checklist is comprehensive

### Information Density Standards

- [ ] No generic references - all are specific and actionable
- [ ] File patterns point at specific examples to follow
- [ ] URLs include section anchors for exact guidance
- [ ] Task specifications use information-dense keywords from codebase

## Success Metrics

**Confidence Score**: Rate 1-10 for one-pass implementation success likelihood

**Validation**: The completed PRP should enable an AI agent unfamiliar with the codebase to implement the feature successfully using only the PRP content and codebase access.
