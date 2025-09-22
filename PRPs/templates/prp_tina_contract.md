name: "TINA Contract Template - There Is No Alternative Analysis"
description: |

## Purpose

TINA (There Is No Alternative) Contract Template for rigorous requirement validation through systematic alternative analysis. Prevents scope creep by forcing explicit justification of every feature component.

## Philosophy

1. **Challenge Everything**: Every requirement must justify its existence
2. **Alternative Exploration**: Force consideration of simpler alternatives
3. **Cost-Benefit Analysis**: Explicit value proposition for each component
4. **Scope Minimization**: Eliminate everything that isn't essential
5. **Evidence-Based Decisions**: No assumptions without validation

---

## Goal

**Feature Goal**: Validate requirement necessity through systematic alternative analysis before implementation

**Deliverable**: Evidence-based contract with approved scope and rejected alternatives

**Success Definition**: Stakeholders unanimously agree chosen solution is the only viable option

## Initial Request

$ARGUMENTS

## TINA Analysis Framework

### Phase 1: Requirement Decomposition

#### Core Requirement Breakdown
```yaml
primary_need:
  user_problem: "[What specific problem are we solving?]"
  current_pain: "[What happens today that's broken?]"
  desired_outcome: "[What does success look like?]"

request_components:
  must_have:
    - component: "[Essential component 1]"
      justification: "[Why this is absolutely required]"
      user_impact: "[What breaks without this]"

  nice_to_have:
    - component: "[Optional component 1]"
      justification: "[Why user wants this]"
      user_impact: "[What's better with this]"

  assumptions:
    - assumption: "[Unstated assumption 1]"
      validation_needed: "[How to verify this]"
      risk_if_wrong: "[What happens if assumption fails]"
```

#### Complexity Assessment
```yaml
implementation_burden:
  development_time: "[Estimated effort]"
  testing_overhead: "[QA complexity added]"
  maintenance_cost: "[Long-term support burden]"
  integration_risk: "[What could break]"

value_proposition:
  user_benefit: "[Quantified user value]"
  business_benefit: "[Quantified business value]"
  roi_timeline: "[When do benefits outweigh costs]"
```

### Phase 2: Alternative Analysis

#### Alternative 1: Do Nothing
```markdown
## Status Quo Analysis
**Current State**: [How users solve this today]
**Workarounds**: [Existing solutions people use]
**Cost of Inaction**: [What happens if we don't build this]
**Evidence**: [Data supporting need for change]

**TINA Question**: Is the current pain severe enough to justify any solution?
- [ ] Yes - proceed to alternative solutions
- [ ] No - recommend rejecting the request
```

#### Alternative 2: Minimal Viable Solution
```markdown
## Simplest Possible Implementation
**Approach**: [Absolute minimum that addresses core need]
**User Experience**: [How users would interact with minimal version]
**Limitations**: [What this approach can't do]
**Benefits**: [Reduced complexity, faster delivery, lower risk]

**TINA Question**: Would the minimal solution solve 80% of the problem?
- [ ] Yes - recommend minimal approach
- [ ] No - justify additional complexity
```

#### Alternative 3: Adjacent Solutions
```markdown
## Existing Tool Integration
**External Options**: [Could we integrate existing tools instead?]
**Configuration Changes**: [Could we solve this with settings/config?]
**Process Changes**: [Could we solve this with workflow changes?]
**Third-Party Services**: [Could we use external APIs/services?]

**TINA Question**: Can we solve this without building anything new?
- [ ] Yes - recommend external solution
- [ ] No - justify custom development
```

#### Alternative 4: Future-Proof Solution
```markdown
## Comprehensive Implementation
**Full Feature Set**: [Everything the user could want]
**Advanced Capabilities**: [Additional functionality beyond core need]
**Extensibility**: [How this could grow over time]
**Complexity Cost**: [Development, testing, maintenance burden]

**TINA Question**: Do the additional features justify the complexity?
- [ ] Yes - recommend comprehensive approach
- [ ] No - recommend simpler alternative
```

### Phase 3: TINA Validation

#### Evidence Requirements
```yaml
user_research:
  problem_validation:
    - source: "[User interview/survey/analytics]"
      finding: "[Specific evidence of pain point]"
      sample_size: "[How many users affected]"

  solution_validation:
    - source: "[Prototype testing/market research]"
      finding: "[Evidence solution would work]"
      confidence: "[How sure are we this solves it]"

business_case:
  quantified_benefits:
    - metric: "[Specific business metric]"
      current_value: "[Baseline measurement]"
      target_value: "[Expected improvement]"
      measurement_plan: "[How we'll track success]"

  cost_justification:
    - investment: "[Development cost]"
      roi_timeline: "[When we break even]"
      risk_factors: "[What could derail ROI]"
```

#### Decision Matrix
```markdown
## Alternative Comparison

| Criteria | Do Nothing | Minimal | Adjacent | Comprehensive |
|----------|------------|---------|----------|---------------|
| **User Value** | [1-5 score] | [1-5 score] | [1-5 score] | [1-5 score] |
| **Development Cost** | [1-5 score] | [1-5 score] | [1-5 score] | [1-5 score] |
| **Risk Level** | [1-5 score] | [1-5 score] | [1-5 score] | [1-5 score] |
| **Time to Value** | [1-5 score] | [1-5 score] | [1-5 score] | [1-5 score] |
| **Maintenance Burden** | [1-5 score] | [1-5 score] | [1-5 score] | [1-5 score] |

**Weighted Score**: [Show calculation with criteria weights]
**Recommended Alternative**: [Highest scoring option]
```

### Phase 4: Contract Definition

#### Approved Scope
```markdown
## TINA Contract: [Feature Name]

### Validated Requirements
Based on alternative analysis, we commit to:

**Core Problem**: [Single sentence problem statement]
**Chosen Solution**: [Selected alternative with brief justification]
**Success Criteria**: [Measurable outcomes that justify the effort]

### Scope Boundaries
**In Scope**:
- [ ] [Specific capability 1 - justified by TINA analysis]
- [ ] [Specific capability 2 - justified by TINA analysis]

**Explicitly Out of Scope** (for this phase):
- [ ] [Nice-to-have feature - deferred by TINA analysis]
- [ ] [Advanced feature - not justified by current need]

### Evidence-Based Justification
**Problem Evidence**: [Specific data showing problem exists]
**Solution Evidence**: [Specific data showing solution will work]
**Alternative Rejection**: [Why other options were insufficient]

### Success Metrics
- **Primary Metric**: [How we measure core value delivery]
- **Secondary Metrics**: [Additional success indicators]
- **Failure Criteria**: [What would indicate solution isn't working]

### TINA Validation Gates
Before implementation begins:
- [ ] All alternatives have been explored and documented
- [ ] Evidence supports chosen solution over alternatives
- [ ] Scope is minimized to essential components only
- [ ] Success criteria are measurable and time-bound
- [ ] Stakeholders agree this is the only viable path forward
```

## TINA Quality Gates

### Completeness Check
- [ ] Every requirement component has been challenged
- [ ] At least 3 alternatives have been seriously considered
- [ ] Evidence exists for problem and solution claims
- [ ] Scope has been minimized to essential elements
- [ ] All assumptions have been identified and validated

### Rigor Check
- [ ] "Do nothing" alternative was honestly evaluated
- [ ] Minimal solution was seriously considered
- [ ] External/adjacent solutions were explored
- [ ] Cost-benefit analysis includes hidden costs
- [ ] Decision matrix uses weighted criteria

### Output Check
- [ ] Recommended solution is clearly superior to alternatives
- [ ] Scope is constrained to highest-value components
- [ ] Success metrics are specific and measurable
- [ ] Contract prevents future scope creep
- [ ] Stakeholders understand why alternatives were rejected

## Anti-Patterns to Avoid

- ❌ Going through motions without serious alternative consideration
- ❌ Assuming complex solution is better than simple one
- ❌ Ignoring existing tools/processes that could solve problem
- ❌ Missing hidden costs (maintenance, support, training)
- ❌ Using unvalidated assumptions as evidence
- ❌ Allowing "nice-to-have" features to slip into scope

## Success Indicators

- ✅ Stakeholders clearly understand why this is the only viable option
- ✅ Scope is minimal but sufficient for core need
- ✅ Evidence strongly supports solution choice
- ✅ Future scope discussions reference TINA analysis
- ✅ Implementation team has clear constraints and priorities
- ✅ Success can be measured objectively

## Template Usage Example

Input: "We need a dashboard for user analytics"

TINA Analysis would explore:
1. **Do Nothing**: Current reporting tools sufficient?
2. **Minimal**: Simple data export + existing visualization
3. **Adjacent**: Third-party analytics integration
4. **Comprehensive**: Custom dashboard with advanced features

Output: Evidence-based recommendation with scope constraints and justification for why other alternatives were insufficient.

## Implementation Blueprint

### TINA Analysis Execution
Execute systematic alternative analysis to validate requirements:

```yaml
analysis_phases:
  requirement_decomposition:
    - Break down user request into components
    - Identify must-have vs nice-to-have
    - Surface hidden assumptions

  alternative_exploration:
    - Do nothing alternative
    - Minimal viable solution
    - Adjacent/external solutions
    - Comprehensive solution

  evidence_validation:
    - User research requirements
    - Business case validation
    - Cost-benefit analysis
    - Decision matrix scoring

  contract_generation:
    - Approved scope definition
    - Evidence-based justification
    - Success metrics establishment
    - TINA validation gates
```

### Implementation Process
1. **Requirements Decomposition**: Break down request systematically
2. **Alternative Analysis**: Explore all viable options with equal rigor
3. **Evidence Collection**: Gather data supporting each alternative
4. **Decision Matrix**: Score alternatives on weighted criteria
5. **Contract Creation**: Document approved scope with justifications
6. **Validation Gates**: Ensure TINA analysis is complete and rigorous

## Next Steps

**Implementation Handoff**: Use approved TINA contract as input to:
- `/prp/create` - Create implementation PRP with constrained scope
- Technical architecture decisions within validated boundaries
- Project estimation based on approved scope only
- Quality gates that verify TINA assumptions remain valid