# Task Specification Template

This template provides structure for creating clear, actionable specifications that specialist agents can execute reliably.

## Task: [Task Name]

### Context
**Problem/Opportunity:** [Brief description of what needs to be addressed]
**Business Impact:** [Why this matters]
**Dependencies:** [What this task depends on]

### Objectives
**Primary Goal:** [Main outcome expected]
**Success Criteria:**
- [ ] [Specific, measurable criterion 1]
- [ ] [Specific, measurable criterion 2]
- [ ] [Specific, measurable criterion 3]

### Scope
**In Scope:**
- [What will be included]
- [What will be delivered]

**Out of Scope:**
- [What will NOT be included]
- [Future work to be addressed separately]

### Specialist Assignment
**Recommended Agent:** [specialist-agent-name]
**Reasoning:** [Why this agent is best suited]

**Alternative Agents:**
- [backup-agent]: [When to use instead]

### Technical Requirements
**Input Requirements:**
- [What inputs the agent needs]
- [Format/structure of inputs]

**Output Requirements:**
- [Expected deliverables]
- [Format/structure of outputs]

**Constraints:**
- [Technical limitations]
- [Resource constraints]
- [Security requirements]

### Quality Gates
**Definition of Done:**
- [ ] [Functional requirement met]
- [ ] [Quality standard met]
- [ ] [Documentation complete]
- [ ] [Tests passing]

**Validation Method:**
- [How will success be verified]
- [Who will review]

### Risk Assessment
**Potential Issues:**
- [Risk 1]: [Mitigation strategy]
- [Risk 2]: [Mitigation strategy]

**Escalation Path:**
- [When to escalate]
- [Who to escalate to]

### Example Usage

```yaml
Task: "Implement user authentication API"
Specialist: api-architect
Input:
  - User requirements document
  - Security requirements
  - Existing system architecture
Output:
  - API specification
  - Security implementation plan
  - Integration guide
```

---

## Template Instructions

1. **Be Specific**: Avoid vague requirements
2. **Include Context**: Help the agent understand the bigger picture
3. **Define Success**: Clear criteria for completion
4. **Plan for Failure**: Identify risks and mitigation strategies
5. **Enable Handoffs**: Structure outputs for next agent in chain

## Specification-Driven Delegation Pattern

```
CEO creates spec using template
↓
Task(specialist-agent, spec)
↓
Agent executes based on clear requirements
↓
Output meets predefined success criteria
↓
Ready for next agent or completion
```

This approach reduces ambiguity, improves delegation success rates, and enables better task coordination across specialist agents.