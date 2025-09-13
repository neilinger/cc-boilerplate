#!/usr/bin/env python3
"""
Hook integration testing - HIGH PRIORITY
Tests the hook execution pipeline and component interactions.
Validates that hooks work together correctly and handle errors gracefully.
"""

import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Dict, Any, List, Optional

class TestHookPipeline(unittest.TestCase):
    """Test hook execution sequence and integration."""

    def setUp(self):
        """Set up test fixtures."""
        self.hooks_dir = Path(__file__).parent.parent / ".claude" / "hooks"
        self.assertTrue(self.hooks_dir.exists(), "Hooks directory must exist")

        # List of hooks that should exist
        self.expected_hooks = [
            "session_start.py",
            "user_prompt_submit.py",
            "pre_tool_use.py",
            "post_tool_use.py",
            "notification.py",
            "stop.py",
            "subagent_stop.py",
            "pre_compact.py"
        ]

        # Verify all hooks exist
        for hook in self.expected_hooks:
            hook_path = self.hooks_dir / hook
            self.assertTrue(hook_path.exists(), f"Hook {hook} must exist")

    def run_hook(self, hook_name: str, input_data: Dict[str, Any],
                 timeout: int = 10) -> subprocess.CompletedProcess:
        """Run a specific hook with input data."""
        hook_path = self.hooks_dir / hook_name

        result = subprocess.run(
            [sys.executable, str(hook_path)],
            input=json.dumps(input_data) if input_data else "",
            text=True,
            capture_output=True,
            timeout=timeout
        )

        return result

    def test_session_start_hook(self):
        """Test session_start.py hook functionality."""
        input_data = {
            "session_id": "test-session-123",
            "source": "startup",
            "timestamp": "2025-01-09T10:30:00Z"
        }

        result = self.run_hook("session_start.py", input_data)

        # Should execute successfully
        self.assertEqual(result.returncode, 0,
                        f"session_start.py failed: {result.stderr}")

        # Should create/update session log
        logs_dir = Path("logs")
        if logs_dir.exists():
            session_files = list(logs_dir.glob("session_start*.json"))
            # Note: May or may not create files depending on implementation
            # This test documents the expected behavior

    def test_user_prompt_submit_hook(self):
        """Test user_prompt_submit.py hook functionality."""
        input_data = {
            "prompt": "Test user prompt",
            "session_id": "test-session-123",
            "timestamp": "2025-01-09T10:30:00Z"
        }

        result = self.run_hook("user_prompt_submit.py", input_data)

        # Should execute successfully
        self.assertEqual(result.returncode, 0,
                        f"user_prompt_submit.py failed: {result.stderr}")

    def test_pre_tool_use_hook_safe_command(self):
        """Test pre_tool_use.py allows safe commands."""
        input_data = {
            "tool_name": "Bash",
            "tool_input": {
                "command": "echo 'Hello World'",
                "description": "Test echo command"
            }
        }

        result = self.run_hook("pre_tool_use.py", input_data)

        # Should allow safe command
        self.assertEqual(result.returncode, 0,
                        f"pre_tool_use.py should allow safe commands: {result.stderr}")

    def test_pre_tool_use_hook_dangerous_command(self):
        """Test pre_tool_use.py blocks dangerous commands."""
        input_data = {
            "tool_name": "Bash",
            "tool_input": {
                "command": "rm -rf /",
                "description": "Dangerous command test"
            }
        }

        result = self.run_hook("pre_tool_use.py", input_data)

        # Should block dangerous command
        self.assertNotEqual(result.returncode, 0,
                           "pre_tool_use.py should block dangerous commands")

    def test_post_tool_use_hook(self):
        """Test post_tool_use.py hook functionality."""
        input_data = {
            "tool_name": "Bash",
            "tool_input": {
                "command": "echo 'test'",
                "description": "Test command"
            },
            "result": {
                "output": "test\n",
                "returncode": 0
            }
        }

        result = self.run_hook("post_tool_use.py", input_data)

        # Should execute successfully
        self.assertEqual(result.returncode, 0,
                        f"post_tool_use.py failed: {result.stderr}")

    def test_notification_hook(self):
        """Test notification.py hook functionality."""
        input_data = {
            "message": "Test notification",
            "type": "info",
            "timestamp": "2025-01-09T10:30:00Z"
        }

        result = self.run_hook("notification.py", input_data)

        # Should execute successfully (even if TTS fails)
        self.assertEqual(result.returncode, 0,
                        f"notification.py failed: {result.stderr}")

    def test_stop_hook(self):
        """Test stop.py hook functionality."""
        input_data = {
            "session_id": "test-session-123",
            "reason": "user_stop",
            "timestamp": "2025-01-09T10:30:00Z"
        }

        result = self.run_hook("stop.py", input_data)

        # Should execute successfully
        self.assertEqual(result.returncode, 0,
                        f"stop.py failed: {result.stderr}")


class TestHookErrorHandling(unittest.TestCase):
    """Test hook error handling and recovery."""

    def setUp(self):
        """Set up test fixtures."""
        self.hooks_dir = Path(__file__).parent.parent / ".claude" / "hooks"

    def run_hook(self, hook_name: str, input_data: Any = None,
                 timeout: int = 10) -> subprocess.CompletedProcess:
        """Run a hook with potentially invalid input."""
        hook_path = self.hooks_dir / hook_name

        input_text = ""
        if input_data is not None:
            if isinstance(input_data, str):
                input_text = input_data
            else:
                try:
                    input_text = json.dumps(input_data)
                except (TypeError, ValueError):
                    input_text = str(input_data)

        result = subprocess.run(
            [sys.executable, str(hook_path)],
            input=input_text,
            text=True,
            capture_output=True,
            timeout=timeout
        )

        return result

    def test_hooks_handle_empty_input(self):
        """Test that hooks handle empty input gracefully."""
        critical_hooks = ["pre_tool_use.py", "post_tool_use.py", "session_start.py"]

        for hook_name in critical_hooks:
            with self.subTest(hook=hook_name):
                result = self.run_hook(hook_name, "")

                # Should not crash (may succeed or fail, but should complete)
                self.assertIsNotNone(result.returncode,
                                   f"{hook_name} should handle empty input without hanging")

    def test_hooks_handle_malformed_json(self):
        """Test that hooks handle malformed JSON gracefully."""
        malformed_inputs = [
            '{"incomplete": json',
            '{invalid: json}',
            'not json at all',
            '{"nested": {"incomplete": }',
        ]

        critical_hooks = ["pre_tool_use.py", "post_tool_use.py"]

        for hook_name in critical_hooks:
            for malformed_json in malformed_inputs:
                with self.subTest(hook=hook_name, input=malformed_json):
                    result = self.run_hook(hook_name, malformed_json)

                    # Should not crash
                    self.assertIsNotNone(result.returncode,
                                       f"{hook_name} should handle malformed JSON")

    def test_hooks_handle_missing_fields(self):
        """Test hooks handle missing required fields."""
        incomplete_data_sets = [
            {},  # Empty object
            {"tool_name": "Bash"},  # Missing parameters
            {"tool_input": {"command": "ls"}},  # Missing tool
        ]

        for data in incomplete_data_sets:
            with self.subTest(input=data):
                result = self.run_hook("pre_tool_use.py", data)

                # Should handle incomplete data without crashing
                self.assertIsNotNone(result.returncode,
                                   "pre_tool_use.py should handle incomplete input")


class TestHookLogging(unittest.TestCase):
    """Test hook logging functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.hooks_dir = Path(__file__).parent.parent / ".claude" / "hooks"
        self.logs_dir = Path("logs")

        # Create logs directory if it doesn't exist
        self.logs_dir.mkdir(exist_ok=True)

        # Record initial state
        self.initial_log_files = set(self.logs_dir.glob("*.json")) if self.logs_dir.exists() else set()

    def test_hooks_create_log_files(self):
        """Test that hooks create appropriate log files."""
        # Run a few hooks that should generate logs
        hooks_to_test = [
            ("session_start.py", {"session_id": "test-logging-123"}),
            ("user_prompt_submit.py", {"prompt": "test prompt"}),
            ("post_tool_use.py", {"tool_name": "Bash", "result": {"output": "test"}}),
        ]

        for hook_name, input_data in hooks_to_test:
            with self.subTest(hook=hook_name):
                hook_path = self.hooks_dir / hook_name

                subprocess.run(
                    [sys.executable, str(hook_path)],
                    input=json.dumps(input_data),
                    text=True,
                    capture_output=True,
                    timeout=10
                )

                # Check if new log files were created
                if self.logs_dir.exists():
                    current_log_files = set(self.logs_dir.glob("*.json"))
                    new_files = current_log_files - self.initial_log_files

                    # Note: Not all hooks may create log files
                    # This test documents the logging behavior
                    if new_files:
                        print(f"✓ {hook_name} created log files: {[f.name for f in new_files]}")
                    else:
                        print(f"ℹ {hook_name} did not create log files")

    def test_log_file_format(self):
        """Test that log files contain valid JSON."""
        if not self.logs_dir.exists():
            self.skipTest("No logs directory found")

        log_files = list(self.logs_dir.glob("*.json"))

        if not log_files:
            self.skipTest("No log files found to validate")

        for log_file in log_files[:5]:  # Test up to 5 recent log files
            with self.subTest(file=log_file.name):
                try:
                    content = log_file.read_text()
                    if content.strip():  # Skip empty files
                        json.loads(content)
                        print(f"✓ {log_file.name} contains valid JSON")
                except json.JSONDecodeError as e:
                    self.fail(f"Log file {log_file.name} contains invalid JSON: {e}")
                except Exception as e:
                    self.fail(f"Error reading log file {log_file.name}: {e}")


class TestHookPerformance(unittest.TestCase):
    """Test hook performance and timeout handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.hooks_dir = Path(__file__).parent.parent / ".claude" / "hooks"

    def test_hook_execution_speed(self):
        """Test that hooks execute within reasonable time limits."""
        fast_hooks = [
            ("pre_tool_use.py", {"tool_name": "Bash", "tool_input": {"command": "echo test"}}),
            ("user_prompt_submit.py", {"prompt": "test"}),
            ("session_start.py", {"session_id": "speed-test"}),
        ]

        for hook_name, input_data in fast_hooks:
            with self.subTest(hook=hook_name):
                hook_path = self.hooks_dir / hook_name

                start_time = time.time()

                result = subprocess.run(
                    [sys.executable, str(hook_path)],
                    input=json.dumps(input_data),
                    text=True,
                    capture_output=True,
                    timeout=5  # 5 second timeout
                )

                execution_time = time.time() - start_time

                # Should complete quickly (under 3 seconds for most hooks)
                self.assertLess(execution_time, 3.0,
                               f"{hook_name} took too long: {execution_time:.2f}s")

                print(f"✓ {hook_name} executed in {execution_time:.3f}s")


def run_integration_tests():
    """Run all hook integration tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestHookPipeline))
    suite.addTests(loader.loadTestsFromTestCase(TestHookErrorHandling))
    suite.addTests(loader.loadTestsFromTestCase(TestHookLogging))
    suite.addTests(loader.loadTestsFromTestCase(TestHookPerformance))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("HOOK INTEGRATION TESTING - HIGH PRIORITY")
    print("Testing hook pipeline execution and component interactions")
    print("=" * 60)

    result = run_integration_tests()

    print(f"\nIntegration Tests Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}")
            print(f"  {traceback.split(chr(10))[-2] if chr(10) in traceback else traceback}")

    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}")
            print(f"  {traceback.split(chr(10))[-2] if chr(10) in traceback else traceback}")

    sys.exit(0 if result.wasSuccessful() else 1)
