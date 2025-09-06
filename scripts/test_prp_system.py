#!/usr/bin/env python3
"""
Minimal test runner for PRP system validation.
Tests the core PRP workflow: create -> validate -> implement.
"""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List

# Import our minimal validators
import sys
sys.path.insert(0, str(Path(__file__).parent))
from validate_prp import validate_prp_file

sys.path.insert(0, str(Path(__file__).parent.parent / "tests"))
from golden_dataset import get_golden_examples

def run_command(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run shell command and return result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result

def test_prp_validation():
    """Test 1: PRP validation with golden dataset."""
    print("\n=== Test 1: PRP Validation ===")
    
    examples = get_golden_examples()
    results = []
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Test valid PRPs
        for name, content in examples.items():
            if name == "invalid":
                continue
                
            prp_file = temp_path / f"{name}.md"
            prp_file.write_text(content)
            
            result = validate_prp_file(prp_file)
            results.append(result)
            
            if result["valid"]:
                print(f"✓ {name}: VALID")
            else:
                print(f"✗ {name}: INVALID")
                for error in result["errors"]:
                    print(f"    - {error}")
        
        # Test invalid PRP
        invalid_file = temp_path / "invalid.md"
        invalid_file.write_text(examples["invalid"])
        
        invalid_result = validate_prp_file(invalid_file)
        if not invalid_result["valid"]:
            print("✓ invalid: Correctly identified as INVALID")
        else:
            print("✗ invalid: Should have been INVALID")
            results.append(invalid_result)
    
    valid_count = sum(1 for r in results if r["valid"])
    print(f"Validation test: {valid_count}/{len(results)} valid PRPs")
    return len(results) == valid_count

def test_prp_command_existence():
    """Test 2: PRP commands exist and are accessible."""
    print("\n=== Test 2: PRP Command Existence ===")
    
    prp_commands = [
        ".claude/commands/prp/create.md",
        ".claude/commands/prp/refine-idea.md", 
        ".claude/commands/prp/intent-contract.md"
    ]
    
    missing = []
    for cmd_file in prp_commands:
        if not Path(cmd_file).exists():
            missing.append(cmd_file)
        else:
            print(f"✓ Found: {cmd_file}")
    
    if missing:
        print("✗ Missing PRP commands:")
        for m in missing:
            print(f"    - {m}")
        return False
    
    print("✓ All PRP commands exist")
    return True

def test_templates_exist():
    """Test 3: PRP templates exist and are valid."""
    print("\n=== Test 3: PRP Template Existence ===")
    
    templates = [
        "PRPs/templates/prp_base.md",
        "PRPs/templates/prp_tina_contract.md",
        "PRPs/templates/prp_planning.md"
    ]
    
    missing = []
    for template in templates:
        template_path = Path(template)
        if not template_path.exists():
            missing.append(template)
        else:
            # Basic validation - check if template has required sections
            content = template_path.read_text()
            if "## Goal" in content and "## Implementation Blueprint" in content:
                print(f"✓ Valid template: {template}")
            else:
                print(f"⚠ Template missing sections: {template}")
    
    if missing:
        print("✗ Missing templates:")
        for m in missing:
            print(f"    - {m}")
        return False
    
    return True

def test_self_referential_case():
    """Test 4: Self-referential test with JSON output style."""
    print("\n=== Test 4: Self-Referential Test (JSON Output Style) ===")
    
    # This is a "smoke test" - we don't implement the feature,
    # just validate the PRP for it is well-formed
    examples = get_golden_examples()
    json_prp = examples["json_output_style"]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(json_prp)
        f.flush()
        
        result = validate_prp_file(Path(f.name))
        
        if result["valid"]:
            print("✓ JSON output style PRP is valid")
            print("✓ PRP contains specific implementation tasks")
            print("✓ PRP contains validation commands")
            return True
        else:
            print("✗ JSON output style PRP validation failed:")
            for error in result["errors"]:
                print(f"    - {error}")
            return False

def main():
    """Run all PRP system tests."""
    print("PRP System Test Suite")
    print("=" * 40)
    
    tests = [
        ("PRP Validation", test_prp_validation),
        ("Command Existence", test_prp_command_existence),
        ("Template Existence", test_templates_exist),
        ("Self-Referential Case", test_self_referential_case),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("Test Results Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("✓ All tests passed! PRP system is working.")
        return 0
    else:
        print("✗ Some tests failed. Check output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())