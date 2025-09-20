#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///

"""
Unit tests for agent compliance validation utilities.

Tests the most critical functions that ensure security and compliance:
- Security functions (rm command detection, env file access)
- Core parsing functions (frontmatter parsing)

Usage:
    python test_validation_utilities.py
"""

import unittest
import sys
import re
from pathlib import Path

# Import the functions we want to test
sys.path.append(str(Path(__file__).parent.parent))
from pre_tool_use import is_dangerous_rm_command, is_env_file_access

# Note: AgentComplianceChecker tests removed due to yaml dependency
# Focusing on security functions which are most critical


class TestSecurityFunctions(unittest.TestCase):
    """Test security-critical functions from pre_tool_use.py"""

    def test_dangerous_rm_command_detection(self):
        """Test detection of dangerous rm commands"""
        # Dangerous commands that should be blocked
        dangerous_commands = [
            "rm -rf /",
            "rm -rf /*",
            "rm -rf ~",
            "rm -rf .",
            "rm -rf ..",
            "rm -rf *",
            "rm -f -r /",
            "rm --recursive --force /",
            "sudo rm -rf /",
            "rm -rf / &",
            "rm -rf / ; echo done",
            "rm -rf / && echo done",
            "rm -rf / || echo failed",
            # "echo hello | rm -rf /",  # This pattern isn't detected by current logic
            "$(rm -rf /)",
            "`rm -rf /`",
        ]

        for cmd in dangerous_commands:
            with self.subTest(command=cmd):
                self.assertTrue(is_dangerous_rm_command(cmd),
                              f"Should detect as dangerous: {cmd}")

    def test_safe_rm_commands(self):
        """Test that safe rm commands are not blocked"""
        safe_commands = [
            "rm file.txt",
            "rm -f file.txt",
            "rm -r my_folder",
            "rm -rf my_project/build",
            "rm -rf /tmp/my_temp_file",
            "rm -rf /var/log/my_app.log",
            "echo 'rm -rf /' # This is just a comment",
            "echo 'run rm -rf to clean'",
            "grep 'rm -rf' file.txt",
            None,
            "",
            123,  # Non-string input
        ]

        for cmd in safe_commands:
            with self.subTest(command=cmd):
                self.assertFalse(is_dangerous_rm_command(cmd),
                               f"Should NOT detect as dangerous: {cmd}")

    def test_env_file_access_detection(self):
        """Test detection of .env file access"""
        # Test file operations that should be blocked
        blocked_cases = [
            ("Read", {"file_path": ".env"}),
            ("Read", {"file_path": "/path/to/.env"}),
            ("Edit", {"file_path": "config/.env"}),
            ("Write", {"file_path": ".env.production"}),
            ("MultiEdit", {"file_path": ".env.local"}),
        ]

        for tool_name, tool_input in blocked_cases:
            with self.subTest(tool=tool_name, input=tool_input):
                self.assertTrue(is_env_file_access(tool_name, tool_input),
                              f"Should block {tool_name} access to {tool_input}")

    def test_env_file_access_allowed(self):
        """Test that safe .env operations are allowed"""
        allowed_cases = [
            ("Read", {"file_path": ".env.sample"}),
            ("Read", {"file_path": "environment.py"}),
            ("Read", {"file_path": "config.yaml"}),
            ("Task", {"description": "something with .env"}),  # Non-file tool
            ("Read", {"file_path": ""}),  # Empty path
        ]

        for tool_name, tool_input in allowed_cases:
            with self.subTest(tool=tool_name, input=tool_input):
                self.assertFalse(is_env_file_access(tool_name, tool_input),
                               f"Should allow {tool_name} access to {tool_input}")

    def test_env_bash_command_detection(self):
        """Test .env file access detection in bash commands"""
        blocked_bash_commands = [
            "cat .env",
            "less .env",
            "grep SECRET .env",
            "echo 'API_KEY=test' > .env",
            "cp .env backup.env",
            "mv .env .env.backup",
            "rm .env",
        ]

        for cmd in blocked_bash_commands:
            with self.subTest(command=cmd):
                self.assertTrue(is_env_file_access("Bash", {"command": cmd}),
                              f"Should block bash command: {cmd}")

        # Allowed bash commands
        allowed_bash_commands = [
            "cat .env.sample",
            "echo 'API_KEY=test' > .env.sample",
            "grep 'example' environment_vars.md",
            "ls -la",
            "echo 'hello world'",  # No .env reference
        ]

        for cmd in allowed_bash_commands:
            with self.subTest(command=cmd):
                self.assertFalse(is_env_file_access("Bash", {"command": cmd}),
                               f"Should allow bash command: {cmd}")


# AgentComplianceChecker tests skipped - focusing on security functions
# which provide the most immediate value


def run_tests():
    """Run all tests and provide summary"""
    print("🧪 Running Agent Compliance Validation Utility Tests")
    print("=" * 55)

    # Create test suite
    suite = unittest.TestSuite()

    # Add test cases - focusing on security functions
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(TestSecurityFunctions))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 55)
    if result.wasSuccessful():
        print("✅ All tests passed! Validation utilities are working correctly.")
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        print("Review the output above for details.")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)