name: "Base PRP Template v4 - Spec-Kit Integration with Context Engineering"
description: |

---

## Status

Status: PROPOSED
Status_Date: YYYY-MM-DD
Status_Note: # Optional explanation

## Goal

**Feature Goal**: [Specific, measurable end state of what needs to be built]

**Deliverable**: [Concrete artifact - API endpoint, service class, integration, etc.]

**Success Definition**: [How you'll know this is complete and working]

## User Persona (if applicable)

**Target User**: [Specific user type - developer, end user, admin, etc.]

**Use Case**: [Primary scenario when this feature will be used]

**User Journey**: [Step-by-step flow of how user interacts with this feature]

**Pain Points Addressed**: [Specific user frustrations this feature solves]

## Why

- [Business value and user impact]
- [Integration with existing features]
- [Problems this solves and for whom]

## What

[User-visible behavior and technical requirements]

### Success Criteria

- [ ] [Specific measurable outcomes]

## All Needed Context

### Context Completeness Check

_Before writing this PRP, validate: "If someone knew nothing about this codebase, would they have everything needed to implement this successfully?"_

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: [Complete URL with section anchor]
  why: [Specific methods/concepts needed for implementation]
  critical: [Key insights that prevent common implementation errors]

- file: [exact/path/to/pattern/file.py]
  why: [Specific pattern to follow - class structure, error handling, etc.]
  pattern: [Brief description of what pattern to extract]
  gotcha: [Known constraints or limitations to avoid]

- docfile: [PRPs/ai_docs/domain_specific.md]
  why: [Custom documentation for complex library/integration patterns]
  section: [Specific section if document is large]
```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase

```bash

```

### Desired Codebase tree with files to be added and responsibility of file

```bash

```

### Known Gotchas of our codebase & Library Quirks

```python
# CRITICAL: [Library name] requires [specific setup]
# Example: FastAPI requires async functions for endpoints
# Example: This ORM doesn't support batch inserts over 1000 records
```

## Implementation Blueprint

### Data models and structure

Create the core data models, we ensure type safety and consistency.

```python
Examples:
 - orm models
 - pydantic models
 - pydantic schemas
 - pydantic validators

```

### Spec-Kit Integration

**Next Phase**: After completing this PRP, proceed to structured implementation phases:

```yaml
# Phase 1: Technical Planning
next_command: /plan
input: This PRP's context and requirements
output: specs/{feature-number}-{feature-name}/plan.md
purpose: Architectural decisions and technical strategy

# Phase 2: Task Breakdown
next_command: /tasks
input: Plan from Phase 1
output: specs/{feature-number}-{feature-name}/tasks.md
purpose: Implementation breakdown with dependencies

# Phase 3: Implementation
next_command: /implement
input: Tasks from Phase 2
output: Working code with validation
purpose: TDD execution with KISS/YAGNI gates
```

**Handoff Context**: The following sections provide all context needed for `/plan`:
- Documentation & References (URLs, file patterns, gotchas)
- Current/Desired Codebase Tree (structure understanding)
- Implementation Patterns & Key Details (coding patterns)
- Integration Points (system connections)
- Validation Loop (quality gates)

### Implementation Patterns & Key Details

```python
# Show critical patterns and gotchas - keep concise, focus on non-obvious details

# Example: Service method pattern
async def {domain}_operation(self, request: {Domain}Request) -> {Domain}Response:
    # PATTERN: Input validation first (follow src/services/existing_service.py)
    validated = self.validate_request(request)

    # GOTCHA: [Library-specific constraint or requirement]
    # PATTERN: Error handling approach (reference existing service pattern)
    # CRITICAL: [Non-obvious requirement or configuration detail]

    return {Domain}Response(status="success", data=result)

# Example: MCP tool pattern
@app.tool()
async def {tool_name}({parameters}) -> str:
    # PATTERN: Tool validation and service delegation (see src/tools/existing_tool.py)
    # RETURN: JSON string with standardized response format
```

### Integration Points

```yaml
DATABASE:
  - migration: "Add column 'feature_enabled' to users table"
  - index: "CREATE INDEX idx_feature_lookup ON users(feature_id)"

CONFIG:
  - add to: config/settings.py
  - pattern: "FEATURE_TIMEOUT = int(os.getenv('FEATURE_TIMEOUT', '30'))"

ROUTES:
  - add to: src/api/routes.py
  - pattern: "router.include_router(feature_router, prefix='/feature')"
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Run after each file creation - fix before proceeding
ruff check src/{new_files} --fix     # Auto-format and fix linting issues
mypy src/{new_files}                 # Type checking with specific files
ruff format src/{new_files}          # Ensure consistent formatting

# Project-wide validation
ruff check src/ --fix
mypy src/
ruff format src/

# Expected: Zero errors. If errors exist, READ output and fix before proceeding.
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test each component as it's created
uv run pytest src/services/tests/test_{domain}_service.py -v
uv run pytest src/tools/tests/test_{action}_{resource}.py -v

# Full test suite for affected areas
uv run pytest src/services/tests/ -v
uv run pytest src/tools/tests/ -v

# Coverage validation (if coverage tools available)
uv run pytest src/ --cov=src --cov-report=term-missing

# Expected: All tests pass. If failing, debug root cause and fix implementation.
```

### Level 3: Integration Testing (System Validation)

```bash
# Service startup validation
uv run python main.py &
sleep 3  # Allow startup time

# Health check validation
curl -f http://localhost:8000/health || echo "Service health check failed"

# Feature-specific endpoint testing
curl -X POST http://localhost:8000/{your_endpoint} \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}' \
  | jq .  # Pretty print JSON response

# MCP server validation (if MCP-based)
# Test MCP tool functionality
echo '{"method": "tools/call", "params": {"name": "{tool_name}", "arguments": {}}}' | \
  uv run python -m src.main

# Database validation (if database integration)
# Verify database schema, connections, migrations
psql $DATABASE_URL -c "SELECT 1;" || echo "Database connection failed"

# Expected: All integrations working, proper responses, no connection errors
```

### Level 4: Creative & Domain-Specific Validation

```bash
# MCP Server Validation Examples:

# Playwright MCP (for web interfaces)
playwright-mcp --url http://localhost:8000 --test-user-journey

# Docker MCP (for containerized services)
docker-mcp --build --test --cleanup

# Database MCP (for data operations)
database-mcp --validate-schema --test-queries --check-performance

# Custom Business Logic Validation
# [Add domain-specific validation commands here]

# Performance Testing (if performance requirements)
ab -n 100 -c 10 http://localhost:8000/{endpoint}

# Security Scanning (if security requirements)
bandit -r src/

# Load Testing (if scalability requirements)
# wrk -t12 -c400 -d30s http://localhost:8000/{endpoint}

# API Documentation Validation (if API endpoints)
# swagger-codegen validate -i openapi.json

# Expected: All creative validations pass, performance meets requirements
```

## Final Validation Checklist

### Technical Validation

- [ ] All 4 validation levels completed successfully
- [ ] All tests pass: `uv run pytest src/ -v`
- [ ] No linting errors: `uv run ruff check src/`
- [ ] No type errors: `uv run mypy src/`
- [ ] No formatting issues: `uv run ruff format src/ --check`

### Feature Validation

- [ ] All success criteria from "What" section met
- [ ] Manual testing successful: [specific commands from Level 3]
- [ ] Error cases handled gracefully with proper error messages
- [ ] Integration points work as specified
- [ ] User persona requirements satisfied (if applicable)

### Code Quality Validation

- [ ] Follows existing codebase patterns and naming conventions
- [ ] File placement matches desired codebase tree structure
- [ ] Anti-patterns avoided (check against Anti-Patterns section)
- [ ] Dependencies properly managed and imported
- [ ] Configuration changes properly integrated

### Documentation & Deployment

- [ ] Code is self-documenting with clear variable/function names
- [ ] Logs are informative but not verbose
- [ ] Environment variables documented if new ones added

---

## Anti-Patterns to Avoid

- ❌ Don't create new patterns when existing ones work
- ❌ Don't skip validation because "it should work"
- ❌ Don't ignore failing tests - fix them
- ❌ Don't use sync functions in async context
- ❌ Don't hardcode values that should be config
- ❌ Don't catch all exceptions - be specific
