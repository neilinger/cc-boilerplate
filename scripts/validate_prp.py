#!/usr/bin/env python3
"""
Minimal PRP validator following KISS/YAGNI principles.
Validates structure, completeness, and basic quality of PRP files.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

def validate_prp_structure(content: str) -> Tuple[bool, List[str]]:
    """Check if PRP has required sections from template."""
    errors = []
    required_sections = [
        "## Goal",
        "## Why", 
        "## What",
        "## All Needed Context",
        "## Implementation Blueprint",
        "## Validation Loop"
    ]
    
    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section: {section}")
    
    return len(errors) == 0, errors

def validate_prp_completeness(content: str) -> Tuple[bool, List[str]]:
    """Check if key fields are filled out."""
    errors = []
    
    # Check for placeholder text that wasn't replaced
    placeholders = [
        "[Specific, measurable end state",
        "[Concrete artifact",
        "[How you'll know this is complete",
        "[exact/path/to/pattern",
        "TODO:",
        "FIXME:"
    ]
    
    for placeholder in placeholders:
        if placeholder in content:
            errors.append(f"Contains unfilled placeholder: {placeholder}")
    
    # Check YAML context section has actual content
    yaml_match = re.search(r'```yaml\n(.*?)```', content, re.DOTALL)
    if yaml_match:
        yaml_content = yaml_match.group(1).strip()
        # Check if YAML has actual content beyond comments
        yaml_lines = [line.strip() for line in yaml_content.split('\n') if line.strip()]
        non_comment_lines = [line for line in yaml_lines if not line.startswith('#')]
        if not yaml_content or len(non_comment_lines) == 0:
            errors.append("YAML context section is empty or only has comments")
    else:
        errors.append("Missing YAML context section")
    
    return len(errors) == 0, errors

def validate_prp_clarity(content: str) -> Tuple[bool, List[str]]:
    """Basic readability and clarity checks."""
    errors = []
    
    # Check for overly long lines (basic readability)
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if len(line) > 200:  # Arbitrary but reasonable limit
            errors.append(f"Line {i} is too long ({len(line)} chars)")
    
    # Check for implementation tasks
    if "Task 1:" not in content:
        errors.append("Missing numbered implementation tasks")
    
    # Check for validation commands
    if "```bash" not in content:
        errors.append("Missing bash validation commands")
    
    return len(errors) == 0, errors

def validate_prp_file(filepath: Path) -> Dict:
    """Validate a single PRP file and return results."""
    try:
        content = filepath.read_text()
    except Exception as e:
        return {
            "file": str(filepath),
            "valid": False,
            "errors": [f"Failed to read file: {e}"]
        }
    
    all_errors = []
    
    # Run all validation checks
    structure_valid, structure_errors = validate_prp_structure(content)
    completeness_valid, completeness_errors = validate_prp_completeness(content)
    clarity_valid, clarity_errors = validate_prp_clarity(content)
    
    all_errors.extend(structure_errors)
    all_errors.extend(completeness_errors)
    all_errors.extend(clarity_errors)
    
    return {
        "file": str(filepath),
        "valid": len(all_errors) == 0,
        "errors": all_errors,
        "checks": {
            "structure": structure_valid,
            "completeness": completeness_valid,
            "clarity": clarity_valid
        }
    }

def main():
    """Run PRP validation on specified files or directory."""
    if len(sys.argv) < 2:
        print("Usage: python validate_prp.py <prp_file_or_directory>")
        sys.exit(1)
    
    target = Path(sys.argv[1])
    
    if not target.exists():
        print(f"Error: {target} does not exist")
        sys.exit(1)
    
    # Collect PRP files
    if target.is_file():
        prp_files = [target]
    else:
        prp_files = list(target.glob("*.md"))
        # Exclude templates and README
        prp_files = [f for f in prp_files if not f.name.startswith("README") and "template" not in f.name.lower()]
    
    if not prp_files:
        print(f"No PRP files found in {target}")
        sys.exit(0)
    
    # Validate each file
    results = []
    for prp_file in prp_files:
        result = validate_prp_file(prp_file)
        results.append(result)
    
    # Report results
    total_files = len(results)
    valid_files = sum(1 for r in results if r["valid"])
    
    print(f"PRP Validation Results: {valid_files}/{total_files} files valid")
    print("=" * 50)
    
    for result in results:
        status = "✓ VALID" if result["valid"] else "✗ INVALID"
        print(f"\n{status}: {result['file']}")
        
        if result["errors"]:
            for error in result["errors"]:
                print(f"  - {error}")
    
    # Exit with error code if any files invalid
    if valid_files != total_files:
        sys.exit(1)
    else:
        print(f"\n✓ All {total_files} PRP files are valid!")

if __name__ == "__main__":
    main()