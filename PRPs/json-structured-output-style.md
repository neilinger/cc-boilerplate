name: "JSON Structured Output Style PRP"
description: |

---

## Goal

**Feature Goal**: Create a JSON-structured output style for Claude Code that formats all AI responses as valid, human-readable JSON with consistent schema structure

**Deliverable**: `.claude/output-styles/json-structured.md` output style file that enables structured JSON responses

**Success Definition**: Claude Code can format responses as valid JSON with consistent schema, parseable by both humans and machines

## User Persona

**Target User**: Developers integrating Claude Code responses with automation tools, CI/CD pipelines, or applications requiring structured data

**Use Case**: Developer needs Claude responses in machine-parseable format for processing by external tools, logging systems, or API integrations

**User Journey**: 
1. Developer selects "json-structured" output style
2. Makes request to Claude Code
3. Receives response formatted as valid JSON with consistent structure
4. Processes JSON programmatically while maintaining human readability

**Pain Points Addressed**: 
- Inconsistent response formatting makes automation difficult
- Manual parsing of free-form text responses is error-prone
- Need for both human-readable and machine-parseable output

## Why

- Enable seamless integration with automation tools and external systems
- Provide consistent, predictable response structure for programmatic processing
- Complement existing output styles with structured data format
- Support developers building workflows around Claude Code responses

## What

A Claude Code output style that structures all responses as valid JSON with:
- Consistent schema with type/content/metadata pattern
- Human-readable formatting with proper indentation
- Error handling following RFC 7807 standards
- Support for different response types (analysis, commands, processes)

### Success Criteria

- [ ] All responses are valid JSON (100% schema compliance)
- [ ] JSON structure is human-readable with proper formatting
- [ ] Schema includes metadata (timestamp, tokens, processing time)
- [ ] Error responses follow RFC 7807 Problem Details format
- [ ] Compatible with existing Claude Code workflow

## All Needed Context

### Context Completeness Check

_If someone knew nothing about this codebase, would they have everything needed to implement this successfully?_ YES - All patterns, file locations, and implementation details provided below.

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: https://platform.openai.com/docs/guides/structured-outputs
  why: JSON schema compliance patterns and validation techniques
  critical: Achieving 100% schema compliance vs 35% with prompting alone

- file: .claude/output-styles/yaml-structured.md
  why: Structured output pattern to follow for consistent formatting
  pattern: Frontmatter with name/description, structured response guidelines
  gotcha: Must follow exact frontmatter format for Claude Code recognition

- file: .claude/output-styles/genui.md
  why: Complex output style example with detailed formatting rules
  pattern: Comprehensive workflow steps, file conventions, response patterns
  gotcha: Output styles control AI behavior through specific instructions

- file: .claude/output-styles/ultra-concise.md
  why: Minimal output style example showing simplest implementation
  pattern: Frontmatter + direct behavioral instructions
  gotcha: Keep instructions clear and actionable

- docfile: PRPs/ai_docs/json_schema_standards.md
  why: JSON Schema implementation patterns for AI response formatting
  section: Base Structure and Error Handling patterns
```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase

```bash
cc-boilerplate/
├── .claude/
│   ├── output-styles/         # 8 existing output styles
│   │   ├── genui.md          # Complex HTML generation style
│   │   ├── yaml-structured.md # Structured YAML responses
│   │   ├── ultra-concise.md  # Minimal word output
│   │   └── ...               # 5 other styles
```

### Desired Codebase tree with files to be added and responsibility of file

```bash
cc-boilerplate/
├── .claude/
│   ├── output-styles/
│   │   └── json-structured.md # NEW: JSON response formatting style
├── PRPs/
│   └── ai_docs/
│       └── json_schema_standards.md # NEW: JSON schema reference docs
```

### Known Gotchas of our codebase & Library Quirks

```python
# CRITICAL: Claude Code output styles use frontmatter format
# Example: All output styles MUST start with YAML frontmatter
---
name: "Style Name"
description: "Brief description"
---
# Content follows...

# GOTCHA: Output styles control AI response behavior through instructions
# They are NOT code - they are behavioral prompts for the AI
# Focus on clear, actionable instructions for response formatting

# CRITICAL: File placement in .claude/output-styles/ is required
# Claude Code automatically discovers files in this directory
```

## Implementation Blueprint

### Data models and structure

JSON response schema following type/content/metadata pattern:

```python
# Core JSON Schema Structure
{
  "type": "response|analysis|command|process|error",
  "timestamp": "ISO-8601 format",
  "content": {
    "message": "Primary response content",
    "details": {},
    "actions": [],
    "summary": {}
  },
  "metadata": {
    "model": "claude-sonnet-4",
    "tokens": {"input": int, "output": int},
    "duration_ms": int
  },
  "context": {
    "session_id": "uuid",
    "request_id": "uuid"
  }
}
```

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: CREATE PRPs/ai_docs/json_schema_standards.md
  - IMPLEMENT: JSON schema reference documentation with examples
  - FOLLOW pattern: Research findings from technical-researcher on JSON standards
  - NAMING: json_schema_standards.md (clear descriptive name)
  - PLACEMENT: PRPs/ai_docs/ directory for AI documentation

Task 2: CREATE .claude/output-styles/json-structured.md
  - IMPLEMENT: Output style with frontmatter and JSON formatting instructions
  - FOLLOW pattern: .claude/output-styles/yaml-structured.md (structured output approach)
  - NAMING: json-structured.md (matches existing naming convention)
  - DEPENDENCIES: Reference json_schema_standards.md from Task 1
  - PLACEMENT: .claude/output-styles/ directory

Task 3: VALIDATE json-structured.md format
  - TEST: Ensure frontmatter format matches existing output styles
  - VALIDATE: JSON schema examples are valid and parseable
  - CHECK: Instructions are clear and actionable for AI behavior
  - VERIFY: File is discoverable by Claude Code system

Task 4: TEST json-structured output style functionality
  - EXECUTE: Select json-structured output style in Claude Code
  - GENERATE: Sample responses using the new output style
  - VALIDATE: All responses are valid JSON with expected schema
  - MEASURE: Human readability and machine parseability
```

### Implementation Patterns & Key Details

```python
# Output Style Pattern (follows existing conventions)
---
name: "JSON Structured"
description: "Structure all responses as valid JSON with consistent schema"
---

# Response formatting instructions that control AI behavior
Structure all responses in valid JSON format with the following guidelines:

# Base schema pattern
{
  "type": "response",
  "timestamp": "2025-01-09T10:30:00Z",
  "content": {
    "message": "Primary response content here",
    "actions": ["list", "of", "actions"],
    "summary": {"key": "value"}
  },
  "metadata": {
    "duration_ms": 1500,
    "confidence": 0.95
  }
}

# PATTERN: Use 2-space indentation for readability
# GOTCHA: All JSON must be valid - test with JSON.parse()
# CRITICAL: Include error handling for malformed responses
```

### Integration Points

```yaml
CLAUDE_CODE:
  - integration: "Automatic discovery from .claude/output-styles/"
  - pattern: "Frontmatter YAML + instruction content"

VALIDATION:
  - add_to: "scripts/validate_prp.py (existing validation framework)"
  - pattern: "JSON schema validation for output style testing"

DOCUMENTATION:
  - reference: "PRPs/ai_docs/json_schema_standards.md"
  - purpose: "Provide AI with detailed JSON formatting context"
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Validate JSON syntax in output style file
python3 -c "import json; print('Valid JSON examples')" # Basic syntax check

# Validate frontmatter format matches existing styles
grep -E "^---" .claude/output-styles/json-structured.md # Check frontmatter

# Validate file placement and naming
ls -la .claude/output-styles/json-structured.md # Confirm file exists

# Expected: File exists, frontmatter present, examples valid
```

### Level 2: Output Style Testing (Component Validation)

```bash
# Test output style functionality with sample request
# (Manual test - select json-structured style and make request)

# Validate generated JSON with external parser
echo '{"test": "json"}' | python3 -m json.tool # Test JSON validity

# Check schema compliance
python3 scripts/validate_prp.py PRPs/json-structured-output-style.md

# Expected: Valid JSON output, schema compliance, human readable
```

### Level 3: Integration Testing (System Validation)

```bash
# Test with various request types
# - Simple questions
# - File operations
# - Code generation
# - Error scenarios

# Validate JSON parsing in different environments
node -e "JSON.parse('${JSON_OUTPUT}')" # Node.js validation
python3 -c "import json; json.loads('${JSON_OUTPUT}')" # Python validation

# Test with automation tools (if available)
curl -X POST -d '{"json_response": true}' localhost:test # API integration

# Expected: All response types produce valid JSON, parseable across environments
```

### Level 4: Creative & Domain-Specific Validation

```bash
# Schema validation with external tools
pip install jsonschema
python3 -c "
import jsonschema
# Validate response against defined schema
"

# Performance testing for large JSON responses
# Measure parsing time and memory usage

# Human readability assessment
# Review JSON formatting for developer experience

# Error scenario testing
# Ensure malformed requests produce valid error JSON

# Expected: Schema compliant, performant, readable, robust error handling
```

## Final Validation Checklist

### Technical Validation

- [ ] JSON output style file created with proper frontmatter
- [ ] All JSON examples in file are syntactically valid
- [ ] File placed in correct location (.claude/output-styles/)
- [ ] Schema documentation created (PRPs/ai_docs/json_schema_standards.md)

### Feature Validation

- [ ] Responses formatted as valid JSON with consistent schema
- [ ] Human-readable formatting with proper indentation
- [ ] Error responses follow RFC 7807 Problem Details format
- [ ] Compatible with existing Claude Code workflow
- [ ] Machine-parseable by common JSON parsers

### Code Quality Validation

- [ ] Follows existing output style naming and structure conventions
- [ ] Instructions are clear and actionable for AI behavior
- [ ] JSON schema examples are comprehensive and accurate
- [ ] Documentation references are specific and helpful

### Documentation & Deployment

- [ ] JSON schema standards documented in ai_docs
- [ ] Output style instructions are self-contained and complete
- [ ] Examples cover common response types and error scenarios

---

## Anti-Patterns to Avoid

- ❌ Don't create overly complex JSON schemas - keep it simple and consistent
- ❌ Don't forget frontmatter format - Claude Code won't recognize the style
- ❌ Don't use malformed JSON examples - they'll break the AI's understanding
- ❌ Don't create parsing dependencies on external libraries
- ❌ Don't ignore error handling - invalid JSON breaks automation
- ❌ Don't sacrifice readability for brevity - developers need to debug