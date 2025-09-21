# Data Model: CC-Boilerplate Strategic Accelerator Framework

**Specification**: 002-prps-prd-cc
**Version**: 1.0.0
**Last Updated**: 2025-01-21
**Authority**: CEO - Executive Decision for Strategic Framework

## Overview

This document defines the comprehensive data model for the CC-Boilerplate Strategic Accelerator Framework, establishing entity definitions, relationships, validation rules, and state transitions for the agent orchestration system.

## Core Entities

### Agent

Specialized AI assistant with defined capabilities and tool permissions.

**Fields:**
- `agent_id`: string (UUID, required, unique)
- `name`: string (required, 3-50 chars, alphanumeric+dash+underscore)
- `role`: string (required, enum: specialist|orchestrator|analyzer)
- `category`: string (required, domain-specific classification)
- `capabilities`: list[string] (required, non-empty, predefined capability IDs)
- `tool_permissions`: dict[string, Permission] (required, tool_name -> permission_level)
- `cognitive_load_tier`: string (required, enum: haiku|sonnet|opus)
- `competency_scores`: dict[string, CompetencyScore] (task_type -> score)
- `status`: string (required, enum: active|inactive|maintenance|deprecated)
- `created_at`: datetime (required, ISO 8601)
- `updated_at`: datetime (required, ISO 8601)
- `certification_level`: string (enum: basic|advanced|expert|custom)
- `security_clearance`: string (required, enum: public|restricted|confidential|secret)

**Relationships:**
- One-to-many with `AgentExecution`
- Many-to-many with `Workflow` through `WorkflowStep`
- One-to-many with `CompetencyScore`

**Validation Rules:**
- Agent name must be unique within category
- At least one capability required
- Tool permissions must reference valid tools
- Cognitive load tier must match capability complexity
- Security clearance must be sufficient for assigned tools

**State Transitions:**
```
active -> inactive (manual deactivation)
active -> maintenance (system maintenance)
inactive -> active (manual reactivation)
maintenance -> active (maintenance complete)
* -> deprecated (permanent removal)
```

### PRD (Product Requirements Document)

Comprehensive requirements document generated from ideas or existing code.

**Fields:**
- `prd_id`: string (UUID, required, unique)
- `title`: string (required, 5-100 chars)
- `description`: text (required, 50-5000 chars)
- `source_type`: string (required, enum: idea|brownfield|greenfield|recovery)
- `source_data`: json (optional, context-dependent structure)
- `functional_requirements`: list[FunctionalRequirement] (required, non-empty)
- `key_entities`: list[EntityDefinition] (optional)
- `user_scenarios`: list[UserScenario] (required, non-empty)
- `acceptance_criteria`: list[AcceptanceCriterion] (required, non-empty)
- `priority`: string (required, enum: critical|high|medium|low)
- `complexity_score`: float (required, 1.0-10.0)
- `estimated_hours`: integer (required, 1-1000)
- `status`: string (required, enum: draft|review|approved|implementation|completed|cancelled)
- `created_by`: string (required, agent_id or user_id)
- `created_at`: datetime (required, ISO 8601)
- `updated_at`: datetime (required, ISO 8601)
- `completion_deadline`: datetime (optional, ISO 8601)

**Relationships:**
- One-to-many with `Spec`
- One-to-many with `Workflow`
- Many-to-many with `LinearIssue`
- One-to-many with `QualityGate`

**Validation Rules:**
- Title must be unique within project scope
- Functional requirements must be testable
- User scenarios must include given-when-then format
- Complexity score must align with estimated hours
- Status transitions must follow approval workflow

**State Transitions:**
```
draft -> review (completeness validation)
review -> draft (revision required)
review -> approved (stakeholder approval)
approved -> implementation (development start)
implementation -> completed (delivery acceptance)
* -> cancelled (project termination)
```

### Workflow

Coordinated sequence of agent actions with security validation and quality gates.

**Fields:**
- `workflow_id`: string (UUID, required, unique)
- `name`: string (required, 3-100 chars)
- `description`: text (required, 20-1000 chars)
- `workflow_type`: string (required, enum: discovery|implementation|validation|recovery|security)
- `trigger_conditions`: list[TriggerCondition] (required, non-empty)
- `steps`: list[WorkflowStep] (required, non-empty, ordered)
- `security_chain_required`: boolean (required, default: false)
- `parallel_execution_allowed`: boolean (required, default: false)
- `timeout_minutes`: integer (required, 5-480)
- `retry_strategy`: RetryStrategy (required)
- `quality_gates`: list[QualityGate] (optional)
- `status`: string (required, enum: pending|running|completed|failed|timeout|halted)
- `execution_context`: json (optional, runtime data)
- `created_at`: datetime (required, ISO 8601)
- `started_at`: datetime (optional, ISO 8601)
- `completed_at`: datetime (optional, ISO 8601)
- `created_by`: string (required, agent_id)

**Relationships:**
- One-to-many with `WorkflowStep`
- Many-to-one with `PRD`
- One-to-many with `AgentExecution`
- Many-to-many with `SecurityChain`

**Validation Rules:**
- Steps must form valid execution graph
- Security chain required for sensitive operations
- Timeout must be realistic for step complexity
- Trigger conditions must be mutually exclusive
- Quality gates must be non-blocking

**State Transitions:**
```
pending -> running (trigger condition met)
running -> completed (all steps successful)
running -> failed (required step failed)
running -> timeout (execution time exceeded)
running -> halted (manual intervention)
failed -> pending (retry with fixes)
halted -> running (manual resume)
```

### CompetencyScore

AI-generated confidence metric for task execution capability.

**Fields:**
- `score_id`: string (UUID, required, unique)
- `agent_id`: string (required, foreign key to Agent)
- `task_type`: string (required, standardized task classification)
- `confidence_score`: float (required, 0.0-1.0)
- `evidence_data`: json (required, supporting metrics)
- `calculation_method`: string (required, enum: heuristic|ml_model|benchmark|manual)
- `sample_size`: integer (required, minimum 1)
- `last_updated`: datetime (required, ISO 8601)
- `validity_period_days`: integer (required, 1-365)
- `performance_history`: list[PerformanceRecord] (optional)
- `feedback_integration`: boolean (required, default: true)

**Relationships:**
- Many-to-one with `Agent`
- One-to-many with `PerformanceRecord`
- Many-to-many with `LinearIssue` (task assignment scoring)

**Validation Rules:**
- Confidence score must be between 0.0 and 1.0
- Evidence data must contain required metrics
- Sample size must be statistically significant
- Validity period must not exceed data freshness
- Performance history must be chronologically ordered

**State Transitions:**
```
fresh -> stale (validity period expired)
stale -> fresh (recalculation completed)
fresh -> deprecated (task type obsoleted)
```

### SecurityChain

Mandatory validation sequence preventing dangerous operations.

**Fields:**
- `chain_id`: string (UUID, required, unique)
- `name`: string (required, 5-50 chars)
- `description`: text (required, 20-500 chars)
- `chain_type`: string (required, enum: code_execution|data_access|system_modification|external_integration)
- `validation_steps`: list[ValidationStep] (required, non-empty, ordered)
- `security_level`: string (required, enum: basic|elevated|critical|maximum)
- `bypass_allowed`: boolean (required, default: false)
- `bypass_authorization`: list[string] (optional, authorized agent_ids)
- `audit_required`: boolean (required, default: true)
- `failure_action`: string (required, enum: block|warn|escalate|abort)
- `created_at`: datetime (required, ISO 8601)
- `last_validated`: datetime (required, ISO 8601)
- `validation_frequency_hours`: integer (required, 1-168)

**Relationships:**
- Many-to-many with `Workflow`
- One-to-many with `ValidationStep`
- One-to-many with `SecurityAuditLog`

**Validation Rules:**
- Validation steps must cover all security aspects
- Security level must match operational risk
- Bypass authorization only for maximum clearance agents
- Failure action must align with security level
- Validation frequency must match risk profile

**State Transitions:**
```
valid -> expired (validation period exceeded)
expired -> valid (revalidation successful)
valid -> compromised (security incident detected)
compromised -> valid (remediation completed)
* -> disabled (emergency shutdown)
```

### LinearIssue

Task management entity with AI/human assignment and competency tracking.

**Fields:**
- `issue_id`: string (required, Linear issue ID format)
- `title`: string (required, 5-200 chars)
- `description`: text (optional, markdown format)
- `status`: string (required, Linear status enum)
- `priority`: string (required, enum: urgent|high|medium|low|no_priority)
- `assignee_type`: string (required, enum: ai|human|hybrid)
- `assignee_id`: string (optional, agent_id or user_id)
- `competency_requirement`: float (required, 0.0-1.0)
- `estimated_complexity`: integer (required, 1-13, Fibonacci)
- `actual_effort_hours`: float (optional, 0.1-1000.0)
- `ai_confidence`: float (optional, 0.0-1.0)
- `labels`: list[string] (optional, Linear labels)
- `project_id`: string (required, Linear project ID)
- `cycle_id`: string (optional, Linear cycle ID)
- `created_at`: datetime (required, ISO 8601)
- `updated_at`: datetime (required, ISO 8601)
- `completed_at`: datetime (optional, ISO 8601)
- `linear_sync_status`: string (required, enum: synced|pending|failed|manual)

**Relationships:**
- Many-to-many with `PRD`
- Many-to-one with `Agent` (AI assignee)
- One-to-many with `CompetencyScore` (assignment evaluation)

**Validation Rules:**
- Issue ID must follow Linear format
- Assignee must exist in respective system
- Competency requirement must match assignee capability
- Complexity estimation must use Fibonacci sequence
- AI confidence required for AI assignments

**State Transitions:**
```
backlog -> in_progress (assignment and start)
in_progress -> in_review (work completion)
in_review -> done (acceptance)
in_review -> in_progress (revision required)
* -> cancelled (scope change)
```

### Spec

Technical specification derived from PRD for implementation planning.

**Fields:**
- `spec_id`: string (UUID, required, unique)
- `prd_id`: string (required, foreign key to PRD)
- `title`: string (required, 5-100 chars)
- `spec_type`: string (required, enum: technical|api|database|integration|deployment)
- `content`: text (required, markdown format, 100-50000 chars)
- `version`: string (required, semantic versioning)
- `status`: string (required, enum: draft|review|approved|implemented|obsolete)
- `technical_complexity`: float (required, 1.0-10.0)
- `implementation_priority`: integer (required, 1-100)
- `dependencies`: list[string] (optional, spec_ids)
- `validation_criteria`: list[ValidationCriterion] (required, non-empty)
- `author_agent_id`: string (required, foreign key to Agent)
- `reviewer_ids`: list[string] (optional, agent_ids or user_ids)
- `created_at`: datetime (required, ISO 8601)
- `updated_at`: datetime (required, ISO 8601)
- `implementation_deadline`: datetime (optional, ISO 8601)

**Relationships:**
- Many-to-one with `PRD`
- One-to-many with `ValidationCriterion`
- Many-to-many with `Spec` (dependencies)
- One-to-many with `QualityGate`

**Validation Rules:**
- Content must be valid markdown
- Technical complexity must align with implementation effort
- Dependencies must not create circular references
- Validation criteria must be testable
- Version must follow semantic versioning

**State Transitions:**
```
draft -> review (completion and submission)
review -> draft (revision required)
review -> approved (technical approval)
approved -> implemented (development completion)
implemented -> obsolete (superseded by newer version)
```

### QualityGate

Non-blocking validation checkpoint ensuring standards compliance.

**Fields:**
- `gate_id`: string (UUID, required, unique)
- `name`: string (required, 5-50 chars)
- `description`: text (required, 20-500 chars)
- `gate_type`: string (required, enum: code_quality|security|performance|compliance|documentation)
- `trigger_conditions`: list[TriggerCondition] (required, non-empty)
- `validation_rules`: list[ValidationRule] (required, non-empty)
- `blocking_level`: string (required, enum: non_blocking|warning|error|critical)
- `auto_fix_available`: boolean (required, default: false)
- `fix_agent_id`: string (optional, foreign key to Agent)
- `success_threshold`: float (required, 0.0-1.0)
- `execution_timeout_seconds`: integer (required, 1-3600)
- `retry_count`: integer (required, 0-5)
- `metrics_collection`: boolean (required, default: true)
- `created_at`: datetime (required, ISO 8601)
- `last_executed`: datetime (optional, ISO 8601)

**Relationships:**
- Many-to-many with `Workflow`
- Many-to-many with `PRD`
- Many-to-many with `Spec`
- One-to-many with `QualityGateExecution`

**Validation Rules:**
- Validation rules must be executable
- Success threshold must be achievable
- Timeout must be reasonable for validation complexity
- Auto-fix agent must have appropriate capabilities
- Blocking level must match validation criticality

**State Transitions:**
```
active -> disabled (manual deactivation)
disabled -> active (manual reactivation)
active -> maintenance (system update)
maintenance -> active (update completion)
```

### BehavioralTest

Python-based validation scenario using subprocess to test Claude CLI behavioral patterns.

**Fields:**
- `test_id`: string (UUID, required, unique)
- `name`: string (required, 5-100 chars)
- `description`: text (required, 50-1000 chars)
- `test_category`: string (required, enum: ceo_role|delegation|contrarian_discipline|agent_usage|decision_making)
- `scenario_prompt`: text (required, 100-5000 chars)
- `python_test_file`: string (required, relative path to test file)
- `expected_behaviors`: list[ExpectedBehavior] (required, non-empty)
- `cli_invocation_pattern`: string (required, subprocess command template)
- `response_parser_config`: dict (required, output parsing configuration)
- `baseline_score`: float (optional, 0.0-1.0)
- `detection_accuracy_target`: float (required, 0.95-1.0)
- `test_frequency`: string (required, enum: continuous|daily|weekly|on_change)
- `auto_regression_threshold`: float (required, 0.0-0.2)
- `created_at`: datetime (required, ISO 8601)
- `last_executed`: datetime (optional, ISO 8601)
- `active`: boolean (required, default: true)

**Relationships:**
- One-to-many with `BehavioralTestExecution`
- Many-to-one with `BehavioralBaseline`
- One-to-many with `RegressionReport`

**Validation Rules:**
- Scenario prompt must be realistic and testable via CLI
- Python test file must exist and be executable
- CLI invocation pattern must be valid subprocess format
- Expected behaviors must be measurable from CLI output
- Detection accuracy target must be achievable
- Regression threshold must be sensitive enough

**State Transitions:**
```
active -> disabled (manual deactivation)
disabled -> active (manual reactivation)
active -> failed (execution failure)
failed -> active (issue resolution)
```

### RegressionReport

Analysis of behavioral changes between CLAUDE.md versions.

**Fields:**
- `report_id`: string (UUID, required, unique)
- `claude_md_version_from`: string (required, git commit hash)
- `claude_md_version_to`: string (required, git commit hash)
- `analysis_timestamp`: datetime (required, ISO 8601)
- `overall_regression_score`: float (required, 0.0-1.0)
- `behavioral_changes`: list[BehavioralChange] (optional)
- `degraded_capabilities`: list[DegradedCapability] (optional)
- `improved_capabilities`: list[ImprovedCapability] (optional)
- `test_results_summary`: TestResultsSummary (required)
- `recommendation`: string (required, enum: accept|review|reject|investigate)
- `risk_level`: string (required, enum: low|medium|high|critical)
- `generated_by_agent_id`: string (required, foreign key to Agent)
- `reviewed_by`: string (optional, user_id)
- `action_required`: boolean (required, default: false)

**Relationships:**
- Many-to-one with `BehavioralBaseline`
- One-to-many with `BehavioralChange`
- Many-to-many with `BehavioralTest`

**Validation Rules:**
- Version identifiers must be valid git commit hashes
- Regression score must reflect actual test results
- Recommendation must align with risk level
- Action required flag must match regression severity
- Test results summary must be comprehensive

**State Transitions:**
```
generated -> under_review (human review initiated)
under_review -> accepted (approval)
under_review -> rejected (revision required)
accepted -> archived (action completion)
```

### BehavioralBaseline

Reference metrics for expected AI behavior patterns.

**Fields:**
- `baseline_id`: string (UUID, required, unique)
- `name`: string (required, 5-50 chars)
- `description`: text (required, 20-500 chars)
- `claude_md_version`: string (required, git commit hash)
- `baseline_metrics`: dict[string, float] (required, test_id -> baseline_score)
- `sample_size`: integer (required, minimum 10)
- `confidence_interval`: float (required, 0.90-0.99)
- `measurement_period_days`: integer (required, 1-30)
- `statistical_significance`: boolean (required, default: false)
- `outlier_threshold`: float (required, 0.05-0.20)
- `created_at`: datetime (required, ISO 8601)
- `expires_at`: datetime (required, ISO 8601)
- `recalculation_frequency_days`: integer (required, 1-90)
- `active`: boolean (required, default: true)

**Relationships:**
- One-to-many with `BehavioralTest`
- One-to-many with `RegressionReport`
- Many-to-one with `Agent` (measurement subject)

**Validation Rules:**
- Baseline metrics must cover all active behavioral tests
- Sample size must be statistically significant
- Confidence interval must be appropriate for use case
- Measurement period must capture behavioral variance
- Outlier threshold must balance sensitivity and stability

**State Transitions:**
```
active -> expired (expiration date reached)
expired -> active (recalculation and renewal)
active -> deprecated (CLAUDE.md major version change)
deprecated -> archived (historical preservation)
```

## Supporting Data Structures

### TriggerCondition
```json
{
  "condition_type": "enum: event|schedule|threshold|manual",
  "condition_value": "string",
  "parameters": "dict[string, any]"
}
```

### WorkflowStep
```json
{
  "step_id": "string",
  "agent_id": "string",
  "order": "integer",
  "required": "boolean",
  "timeout_minutes": "integer",
  "condition": "string",
  "inputs": "dict[string, any]",
  "outputs": "dict[string, any]"
}
```

### ValidationStep
```json
{
  "step_name": "string",
  "validation_type": "enum: static_analysis|dynamic_check|manual_review|automated_scan",
  "criteria": "string",
  "required": "boolean",
  "timeout_seconds": "integer"
}
```

### ExpectedBehavior
```json
{
  "behavior_name": "string",
  "description": "string",
  "measurement_method": "string",
  "success_criteria": "string",
  "weight": "float"
}
```

### BehavioralChange
```json
{
  "change_type": "enum: improvement|degradation|new_capability|removed_capability",
  "description": "string",
  "impact_score": "float",
  "affected_tests": "list[string]",
  "confidence": "float"
}
```

## Validation Framework

### Cross-Entity Consistency Rules

1. **Agent-Workflow Consistency**: Agents assigned to workflow steps must have required capabilities and security clearance
2. **PRD-Spec Traceability**: All functional requirements in PRD must map to technical specifications
3. **Security Chain Coverage**: High-risk workflows must have mandatory security chain validation
4. **Competency-Assignment Alignment**: Linear issue assignments must respect agent competency scores
5. **Behavioral Test Coverage**: All CEO behavioral requirements must have corresponding test scenarios

### Data Integrity Constraints

1. **Referential Integrity**: All foreign key relationships must reference existing entities
2. **Temporal Consistency**: Created_at <= updated_at for all entities with both fields
3. **Status Transitions**: Status changes must follow defined state transition rules
4. **Score Boundaries**: All score fields must remain within defined ranges (0.0-1.0)
5. **Unique Constraints**: Entities with uniqueness requirements must be enforced at system level

### Performance Considerations

1. **Indexing Strategy**: Primary keys, foreign keys, and frequently queried fields must be indexed
2. **Archival Policy**: Completed workflows and historical data should be archived after retention period
3. **Caching Strategy**: Frequently accessed read-only data (baselines, capabilities) should be cached
4. **Batch Operations**: Bulk data operations should use batch processing to avoid performance degradation

---

**Document Status**: Approved by CEO
**Implementation Authority**: Workflow Orchestrator delegation to specialist agents
**Next Review**: Upon major system architecture changes