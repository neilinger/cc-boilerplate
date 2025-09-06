#!/usr/bin/env python3
"""
Golden dataset for PRP testing.
Contains minimal examples of good PRPs for self-referential testing.
"""

from pathlib import Path

# Test case 1: The json-structured output style feature (your target test)
JSON_OUTPUT_STYLE_PRP = """## Goal

**Feature Goal**: Add json-structured output style option to cc-boilerplate for machine-parseable responses

**Deliverable**: New output style that formats AI responses as valid JSON objects

**Success Definition**: `uv run python -m cc_boilerplate.main --style json-structured "Hello world"` returns valid JSON

## Why

- Enable programmatic consumption of AI responses
- Support integration with other tools and pipelines
- Follow existing output style patterns in codebase

## What

Add json-structured output style that wraps AI responses in consistent JSON format with metadata.

### Success Criteria

- [ ] JSON output is always valid (parseable by json.loads)
- [ ] Includes response content and metadata (timestamp, model, etc.)
- [ ] Follows existing output style architecture

## All Needed Context

### Documentation & References

```yaml
- file: src/output_styles/minimal.py
  why: Base pattern for output styles - class structure, format method
  pattern: OutputStyle base class with format() method
  gotcha: Must handle newlines and special characters in content

- file: src/main.py  
  why: How output styles are registered and used
  pattern: Output style import and registration pattern
  gotcha: Style name must match filename
```

## Implementation Blueprint

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: CREATE src/output_styles/json_structured.py
  - IMPLEMENT: JsonStructuredStyle class extending OutputStyle
  - FOLLOW pattern: src/output_styles/minimal.py (class structure)
  - NAMING: JsonStructuredStyle class, format() method
  - PLACEMENT: Output styles directory

Task 2: MODIFY src/main.py
  - INTEGRATE: Import and register JsonStructuredStyle
  - FIND pattern: existing output style imports
  - ADD: Import JsonStructuredStyle following existing pattern
  - PRESERVE: Existing output style registrations
```

## Validation Loop

### Level 1: Syntax & Style

```bash
ruff check src/output_styles/json_structured.py --fix
mypy src/output_styles/json_structured.py
```

### Level 2: Unit Tests

```bash
python -c "import json; from src.output_styles.json_structured import JsonStructuredStyle; s=JsonStructuredStyle(); result=s.format('test'); json.loads(result)"
```

### Level 3: Integration Testing  

```bash
uv run python -m cc_boilerplate.main --style json-structured "Hello world" | python -c "import json, sys; json.loads(sys.stdin.read())"
```
"""

# Test case 2: Simple feature with minimal context
SIMPLE_FEATURE_PRP = """## Goal

**Feature Goal**: Add --verbose flag to show debug information  

**Deliverable**: Command line flag that enables debug logging

**Success Definition**: `--verbose` flag shows additional logging output

## Why

- Help developers debug issues
- Standard CLI pattern users expect

## What

Add verbose logging flag that shows additional debug information during execution.

### Success Criteria

- [ ] --verbose flag accepted by CLI
- [ ] Shows debug-level log messages when enabled
- [ ] Default behavior unchanged when flag not used

## All Needed Context

### Documentation & References

```yaml
- file: src/main.py
  why: CLI argument parsing with click
  pattern: @click.option decorator usage
  gotcha: Must handle boolean flags correctly
```

## Implementation Blueprint

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: MODIFY src/main.py
  - ADD: @click.option('--verbose', is_flag=True) decorator
  - MODIFY: Configure logging level based on verbose flag
  - PATTERN: Follow existing CLI option patterns
```

## Validation Loop

### Level 1: Syntax & Style

```bash
ruff check src/main.py --fix
```

### Level 2: Integration Testing

```bash
uv run python -m cc_boilerplate.main --verbose "test" 2>&1 | grep -q "DEBUG"
```
"""

# Test case 3: Invalid PRP (for negative testing)
INVALID_PRP = """# This is not a proper PRP

Missing required sections and structure.

Some random content that doesn't follow the template.
"""

def get_golden_examples():
    """Return dictionary of golden PRP examples for testing."""
    return {
        "json_output_style": JSON_OUTPUT_STYLE_PRP,
        "verbose_flag": SIMPLE_FEATURE_PRP,
        "invalid": INVALID_PRP
    }

def create_test_prp_file(name: str, content: str, output_dir: Path):
    """Create a test PRP file in the specified directory."""
    output_dir.mkdir(parents=True, exist_ok=True)
    prp_file = output_dir / f"{name}.md"
    prp_file.write_text(content)
    return prp_file

if __name__ == "__main__":
    # Create test files for manual testing
    test_dir = Path("tests/test_prps")
    examples = get_golden_examples()
    
    for name, content in examples.items():
        prp_file = create_test_prp_file(name, content, test_dir)
        print(f"Created test PRP: {prp_file}")