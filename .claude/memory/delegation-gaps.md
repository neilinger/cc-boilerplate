# Delegation Gaps - Role Requirements

This document tracks tasks that cannot be effectively delegated to existing specialist agents, documenting what new roles/capabilities we need.

## Current Gaps

### Gap: Orchestration Validator
**Needed for:** Validating actual agent coordination vs claims
**Current workaround:** Manual inspection of Task tool usage
**Ideal specialist would:**
- Parse conversation logs for Task tool invocations
- Verify agent handoffs and timing patterns
- Detect coordination theater vs real delegation
- Generate orchestration performance metrics

**Priority:** High - Addresses Issue #37

### Gap: Configuration Migration Specialist
**Needed for:** Complex config file migrations and transformations
**Current workaround:** Using python-pro + manual validation
**Ideal specialist would:**
- YAML/JSON schema validation and migration
- Multi-format config transformations
- Backward compatibility checking
- Automated config testing

**Priority:** Medium

### Gap: Integration Test Coordinator
**Needed for:** Cross-service integration testing
**Current workaround:** test-automator + manual coordination
**Ideal specialist would:**
- Multi-service test orchestration
- Environment provisioning for integration tests
- Service dependency management
- End-to-end test scenario creation

**Priority:** Medium

## Gap Tracking Template

```markdown
### Gap: [Role Name]
**Needed for:** [Specific use case]
**Current workaround:** [How we handle it now]
**Ideal specialist would:**
- [Capability 1]
- [Capability 2]
- [Capability 3]

**Priority:** [High/Medium/Low]
**Impact:** [Description of current pain points]
```

## Guidelines for Adding Gaps

1. **Be Specific**: Describe exactly what capabilities are missing
2. **Document Workarounds**: How are we currently handling this?
3. **Justify Need**: Why can't existing specialists handle this?
4. **Set Priority**: Based on frequency and impact
5. **Update Status**: Mark when gaps are filled by new specialists

## Gap Resolution Process

1. **Identify Gap**: Task cannot be effectively delegated
2. **Document Here**: Use template above
3. **Evaluate Options**:
   - Can existing specialist be enhanced?
   - Should task be decomposed differently?
   - Is new specialist truly needed?
4. **Create Specialist**: If justified, create new agent
5. **Update Gaps**: Mark as resolved

## Metrics

- **Total Gaps:** 3
- **High Priority:** 1
- **Recent Additions:** orchestration-validator (2025-01-24)
- **Resolution Rate:** 0% (new tracking system)

---

*Last Updated: 2025-01-24*
*Next Review: Weekly during agent architecture reviews*