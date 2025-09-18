#!/usr/bin/env python3
"""
Simple integration test for consumer project workflow.
No external dependencies - just standard library.
"""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path
import json
import sys


def run_test(test_name, test_func):
    """Run a single test and report results."""
    try:
        print(f"🧪 {test_name}...")
        test_func()
        print(f"✅ {test_name} PASSED")
        return True
    except Exception as e:
        print(f"❌ {test_name} FAILED: {e}")
        return False


def setup_test_project():
    """Create a temporary project directory."""
    test_dir = tempfile.mkdtemp(prefix="cc_boilerplate_test_")
    original_cwd = os.getcwd()
    os.chdir(test_dir)

    # Initialize a git repository
    subprocess.run(["git", "init"], check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], check=True)

    # Create initial commit
    Path("README.md").write_text("# Test Project\n")
    subprocess.run(["git", "add", "README.md"], check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)

    return test_dir, original_cwd


def cleanup_test_project(test_dir, original_cwd):
    """Clean up temporary directory."""
    os.chdir(original_cwd)
    shutil.rmtree(test_dir, ignore_errors=True)


def test_init_script_basic():
    """Test basic init script functionality."""
    test_dir, original_cwd = setup_test_project()

    try:
        # Get the path to our init script (go up one level from tests dir)
        script_path = Path(original_cwd).parent / "scripts" / "init-boilerplate.sh"

        # Run the init script in non-interactive mode
        env = os.environ.copy()
        env["INTERACTIVE"] = "false"

        result = subprocess.run(
            ["bash", str(script_path)],
            env=env,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )

        if result.returncode != 0:
            raise Exception(f"Init script failed (exit {result.returncode}):\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")

        # Verify expected structure exists
        if not Path(".claude/boilerplate").is_dir():
            raise Exception("Boilerplate directory not created")

        if not Path(".boilerplate-version").is_file():
            raise Exception("Version file not created")

        print(f"   📁 Created boilerplate structure in {test_dir}")

    finally:
        cleanup_test_project(test_dir, original_cwd)


def test_latest_tag_in_output():
    """Test that init script mentions using latest tag."""
    test_dir, original_cwd = setup_test_project()

    try:
        script_path = Path(original_cwd).parent / "scripts" / "init-boilerplate.sh"
        env = os.environ.copy()
        env["INTERACTIVE"] = "false"

        result = subprocess.run(
            ["bash", str(script_path)],
            env=env,
            capture_output=True,
            text=True,
            timeout=120
        )

        output = result.stdout + result.stderr

        # Should mention version tag, not main
        if "v1.3" not in output and "latest stable" not in output:
            raise Exception(f"Expected version tag in output, got: {output[:500]}...")

        if "Branch: main" in output:
            raise Exception(f"Should not use main branch, output contained: {output[:500]}...")

        print(f"   🔖 Correctly using latest tag instead of main branch")

    finally:
        cleanup_test_project(test_dir, original_cwd)


def test_config_builder_diagnostic():
    """Test that config builder provides helpful diagnostics."""
    test_dir, original_cwd = setup_test_project()

    try:
        # Don't run init - just test config builder on empty project
        config_script = Path(original_cwd).parent / "scripts" / "build-config.sh"

        result = subprocess.run(
            ["bash", str(config_script)],
            capture_output=True,
            text=True
        )

        # Should fail but with helpful message
        if result.returncode == 0:
            raise Exception("Config builder should fail on uninitialized project")

        output = result.stdout + result.stderr
        if "Boilerplate not found" not in output:
            raise Exception(f"Expected helpful error message, got: {output}")

        print(f"   💬 Config builder provides helpful error messages")

    finally:
        cleanup_test_project(test_dir, original_cwd)


def main():
    """Run all integration tests."""
    print("🚀 Running CC-Boilerplate Integration Tests")
    print("=" * 50)

    tests = [
        ("Basic Init Script Functionality", test_init_script_basic),
        ("Latest Tag Usage", test_latest_tag_in_output),
        ("Config Builder Diagnostics", test_config_builder_diagnostic),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        if run_test(test_name, test_func):
            passed += 1
        else:
            failed += 1
        print()

    print("=" * 50)
    print(f"📊 Results: {passed} passed, {failed} failed")

    if failed > 0:
        print("❌ Some tests failed - there may be integration issues")
        sys.exit(1)
    else:
        print("✅ All integration tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()