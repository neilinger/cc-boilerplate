#!/usr/bin/env python3
"""
Clean, simple test infrastructure with proper isolation and cleanup.

This module provides base classes and utilities for creating isolated,
reproducible tests that work both in CI and local environments.

Following KISS/YAGNI: Simple base classes, essential functionality only.
"""

import os
import sys
import tempfile
import shutil
import unittest
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
from unittest.mock import Mock, patch


class IsolatedTestCase(unittest.TestCase):
    """
    Base test case with proper environment isolation and cleanup.
    
    Provides:
    - Isolated temporary directory
    - Environment variable backup/restore  
    - sys.path backup/restore
    - Working directory backup/restore
    - Automatic cleanup
    """
    
    def setUp(self):
        """Set up isolated test environment."""
        # Create isolated temporary directory
        self.test_dir = Path(tempfile.mkdtemp(prefix='cc_test_'))
        
        # Backup original state
        self.original_cwd = Path.cwd()
        self.original_env = os.environ.copy()
        self.original_syspath = sys.path.copy()
        
        # Change to test directory
        os.chdir(self.test_dir)
        
        # Create basic project structure in test directory
        self._setup_test_project_structure()
        
    def tearDown(self):
        """Clean up isolated test environment."""
        # Restore original state
        os.chdir(self.original_cwd)
        os.environ.clear()
        os.environ.update(self.original_env)
        sys.path[:] = self.original_syspath
        
        # Clean up test directory
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def _setup_test_project_structure(self):
        """Create basic project structure for testing."""
        # Create essential directories
        (self.test_dir / 'logs').mkdir(exist_ok=True)
        (self.test_dir / '.claude' / 'hooks').mkdir(parents=True, exist_ok=True)
        (self.test_dir / 'scripts').mkdir(exist_ok=True)
        (self.test_dir / 'tests').mkdir(exist_ok=True)
        
        # Create basic .env.sample (safe to read)
        (self.test_dir / '.env.sample').write_text(
            "# Sample environment variables\n"
            "EXAMPLE_VAR=sample_value\n"
            "API_KEY_TEMPLATE=your_api_key_here\n"
        )
        
        # Create test .env file (should be protected)
        (self.test_dir / '.env').write_text(
            "SECRET_KEY=test_secret_123\n"
            "API_KEY=real_api_key_456\n"
        )
    
    def create_test_file(self, path: str, content: str = "") -> Path:
        """Create a test file with given content."""
        file_path = self.test_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return file_path
    
    def set_env_var(self, key: str, value: str):
        """Set environment variable for this test only."""
        os.environ[key] = value
    
    def unset_env_var(self, key: str):
        """Remove environment variable for this test only."""
        if key in os.environ:
            del os.environ[key]


class MockHookTestCase(IsolatedTestCase):
    """
    Test case with hook mocking infrastructure.
    
    Provides utilities for testing hook behavior without actual hook installation.
    """
    
    def setUp(self):
        """Set up with hook mocking capabilities."""
        super().setUp()
        self.hook_calls = []
        self.hook_responses = {}
    
    def create_mock_hook(self, hook_name: str, return_code: int = 0, 
                        stdout: str = "", stderr: str = "") -> Path:
        """
        Create a mock hook script that records calls and returns controlled output.
        
        Args:
            hook_name: Name of the hook (e.g., 'pre_tool_use')
            return_code: Exit code to return
            stdout: Standard output to return
            stderr: Standard error to return
            
        Returns:
            Path to the created mock hook
        """
        hook_path = self.test_dir / '.claude' / 'hooks' / f'{hook_name}.py'
        
        # Create mock hook script
        hook_content = f'''#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path

# Record this call
call_log = Path("{self.test_dir}") / "hook_calls.json"
if call_log.exists():
    with open(call_log) as f:
        calls = json.load(f)
else:
    calls = []

# Read input
try:
    input_data = json.load(sys.stdin)
except:
    input_data = {{"error": "failed_to_read_input"}}

calls.append({{
    "hook": "{hook_name}",
    "input": input_data,
    "env": dict(os.environ)
}})

with open(call_log, "w") as f:
    json.dump(calls, f, indent=2)

# Return controlled output
if "{stdout}":
    print("{stdout}")
if "{stderr}":
    print("{stderr}", file=sys.stderr)

sys.exit({return_code})
'''
        
        hook_path.write_text(hook_content)
        hook_path.chmod(0o755)
        return hook_path
    
    def get_hook_calls(self) -> List[Dict[str, Any]]:
        """Get all recorded hook calls."""
        call_log = self.test_dir / "hook_calls.json"
        if call_log.exists():
            return json.loads(call_log.read_text())
        return []
    
    def run_hook_with_input(self, hook_name: str, input_data: Dict[str, Any],
                           timeout: int = 10) -> subprocess.CompletedProcess:
        """
        Run a hook with given input data.
        
        Args:
            hook_name: Name of the hook to run
            input_data: Input data to send to hook
            timeout: Timeout in seconds
            
        Returns:
            CompletedProcess result
        """
        hook_path = self.test_dir / '.claude' / 'hooks' / f'{hook_name}.py'
        
        if not hook_path.exists():
            raise FileNotFoundError(f"Hook not found: {hook_path}")
        
        return subprocess.run(
            [sys.executable, str(hook_path)],
            input=json.dumps(input_data),
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=self.test_dir
        )


class SafetyLogicTestCase(unittest.TestCase):
    """
    Pure unit test case for safety logic without environmental dependencies.
    
    Tests the extracted safety_logic module functions directly without
    subprocess calls or hook installation.
    """
    
    @classmethod
    def setUpClass(cls):
        """Import safety logic module once for all tests."""
        # Add scripts directory to path to import safety_logic
        scripts_path = Path(__file__).parent.parent / "scripts"
        if str(scripts_path) not in sys.path:
            sys.path.insert(0, str(scripts_path))
        
        try:
            import safety_logic
            cls.safety = safety_logic
        except ImportError as e:
            raise unittest.SkipTest(f"Could not import safety_logic: {e}")
    
    def assert_dangerous_command(self, command: str, msg: str = ""):
        """Assert that a command is detected as dangerous."""
        result = self.safety.is_dangerous_rm_command(command)
        self.assertTrue(result, f"Command should be dangerous: {command}. {msg}")
    
    def assert_safe_command(self, command: str, msg: str = ""):
        """Assert that a command is detected as safe."""
        result = self.safety.is_dangerous_rm_command(command)
        self.assertFalse(result, f"Command should be safe: {command}. {msg}")
    
    def assert_blocks_env_access(self, tool_name: str, tool_input: Dict[str, Any], msg: str = ""):
        """Assert that tool call is blocked due to .env access."""
        result = self.safety.is_env_file_access(tool_name, tool_input)
        self.assertTrue(result, f"Should block .env access: {tool_name} {tool_input}. {msg}")
    
    def assert_allows_env_access(self, tool_name: str, tool_input: Dict[str, Any], msg: str = ""):
        """Assert that tool call is allowed (no .env access)."""
        result = self.safety.is_env_file_access(tool_name, tool_input)
        self.assertFalse(result, f"Should allow access: {tool_name} {tool_input}. {msg}")


class CICompatibleTestCase(unittest.TestCase):
    """
    Test case designed to work reliably in CI environments.
    
    - No subprocess calls to actual hooks
    - No file system dependencies outside test directory
    - No network calls
    - Environment detection and adaptation
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up CI environment detection."""
        cls.is_ci = os.environ.get('CI', 'false').lower() == 'true'
        cls.is_github_actions = os.environ.get('GITHUB_ACTIONS', 'false').lower() == 'true'
    
    def setUp(self):
        """Set up CI-compatible test environment."""
        if self.is_ci:
            # In CI: use faster, more reliable test setup
            self.test_timeout = 5
            self.use_mocks = True
        else:
            # Locally: can use more comprehensive testing
            self.test_timeout = 30
            self.use_mocks = False
    
    def skip_if_ci(self, reason: str = "Test requires local environment"):
        """Skip test if running in CI."""
        if self.is_ci:
            self.skipTest(reason)
    
    def skip_if_not_ci(self, reason: str = "Test only runs in CI"):
        """Skip test if not running in CI."""
        if not self.is_ci:
            self.skipTest(reason)


class TestEnvironmentValidator:
    """
    Validates test environment before running tests.
    
    Provides early failure for environmental issues rather than
    letting tests fail with cryptic errors.
    """
    
    @staticmethod
    def validate_basic_requirements() -> List[str]:
        """Validate basic Python environment requirements."""
        issues = []
        
        # Check Python version
        if sys.version_info < (3, 8):
            issues.append(f"Python 3.8+ required, got {sys.version_info}")
        
        # Check required modules
        required_modules = ['json', 're', 'subprocess', 'unittest', 'pathlib']
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                issues.append(f"Required module missing: {module}")
        
        return issues
    
    @staticmethod
    def validate_project_structure() -> List[str]:
        """Validate project structure for testing."""
        issues = []
        
        project_root = Path(__file__).parent.parent
        
        # Check for essential directories
        essential_dirs = ['tests', 'scripts', '.claude']
        for dir_name in essential_dirs:
            if not (project_root / dir_name).exists():
                issues.append(f"Missing directory: {dir_name}")
        
        return issues
    
    @staticmethod
    def validate_ci_environment() -> List[str]:
        """Validate CI-specific requirements."""
        issues = []
        
        if not os.environ.get('CI'):
            return issues  # Not in CI, nothing to validate
        
        # Check CI-specific requirements
        if not shutil.which('python'):
            issues.append("Python executable not found in PATH")
        
        return issues
    
    @classmethod
    def validate_all(cls) -> List[str]:
        """Run all validations and return combined issues."""
        issues = []
        issues.extend(cls.validate_basic_requirements())
        issues.extend(cls.validate_project_structure())
        issues.extend(cls.validate_ci_environment())
        return issues


def run_validation():
    """Run environment validation and report results."""
    print("Validating test environment...")
    issues = TestEnvironmentValidator.validate_all()
    
    if issues:
        print("❌ Environment validation failed:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ Environment validation passed")
        return True


class ComprehensiveMockTestCase(IsolatedTestCase):
    """
    Comprehensive mock test case that provides unified access to all mock systems.
    
    This class brings together all the mock infrastructure (hooks, subprocess,
    filesystem, environment) with convenient methods for easy testing.
    
    Following KISS/YAGNI: Simple unified interface for comprehensive mocking.
    """
    
    def setUp(self):
        """Set up all mock systems."""
        super().setUp()
        
        # Import mock systems
        try:
            from .mocks import (
                MockHookRunner, MockSafetyHook, MockSubprocessRunner,
                MockFileSystem, MockEnvironment, MockHookAction
            )
        except ImportError:
            # Handle when running directly
            from mocks import (
                MockHookRunner, MockSafetyHook, MockSubprocessRunner,
                MockFileSystem, MockEnvironment, MockHookAction
            )
        
        # Initialize all mock systems
        self.mock_hooks = MockHookRunner()
        self.mock_safety_hook = MockSafetyHook()
        self.mock_subprocess = MockSubprocessRunner()
        self.mock_filesystem = MockFileSystem()
        self.mock_environment = MockEnvironment(isolated=True)
        
        # Store reference to MockHookAction for tests
        self.MockHookAction = MockHookAction
        
        # Track safety logic import for optional real evaluation
        self.safety_logic = None
        try:
            # Try to import safety logic for real evaluations
            scripts_path = Path(__file__).parent.parent / "scripts"
            if str(scripts_path) not in sys.path:
                sys.path.insert(0, str(scripts_path))
            import safety_logic
            self.safety_logic = safety_logic
        except ImportError:
            # Safety logic not available, use mocks only
            pass
    
    def tearDown(self):
        """Clean up all mock systems."""
        self.mock_hooks.reset()
        self.mock_subprocess.reset()
        self.mock_filesystem.reset()
        self.mock_environment.restore()
        super().tearDown()
    
    # Hook management convenience methods
    def set_hook_to_block(self, hook_name: str, reason: str = "Blocked by test"):
        """Configure hook to block operations."""
        try:
            from .mocks import MockHookResponse, MockHookAction
        except ImportError:
            from mocks import MockHookResponse, MockHookAction
        # Configure both the regular mock hook and the safety hook
        self.mock_hooks.set_hook_response(hook_name, MockHookResponse(
            action=MockHookAction.BLOCK,
            reason=reason,
            exit_code=1
        ))
        # Also configure the safety hook specifically
        if hook_name == 'pre_tool_use':
            self.mock_safety_hook.set_block_response(reason)
    
    def set_hook_to_allow(self, hook_name: str, reason: str = "Allowed by test"):
        """Configure hook to allow operations."""
        try:
            from .mocks import MockHookResponse, MockHookAction
        except ImportError:
            from mocks import MockHookResponse, MockHookAction
        self.mock_hooks.set_hook_response(hook_name, MockHookResponse(
            action=MockHookAction.ALLOW,
            reason=reason,
            exit_code=0
        ))
        # Also configure the safety hook specifically
        if hook_name == 'pre_tool_use':
            self.mock_safety_hook.set_allow_response(reason)
    
    def set_hook_to_error(self, hook_name: str, reason: str = "Error from test"):
        """Configure hook to return error."""
        try:
            from .mocks import MockHookResponse, MockHookAction
        except ImportError:
            from mocks import MockHookResponse, MockHookAction
        self.mock_hooks.set_hook_response(hook_name, MockHookResponse(
            action=MockHookAction.ERROR,
            reason=reason,
            exit_code=2,
            stderr=reason
        ))
        # Also configure the safety hook specifically
        if hook_name == 'pre_tool_use':
            self.mock_safety_hook.set_error_response(reason)
    
    def assert_hook_was_called(self, hook_name: str, expected_calls: int = 1):
        """Assert that hook was called expected number of times."""
        calls = self.mock_hooks.get_hook_calls(hook_name)
        self.assertEqual(len(calls), expected_calls, 
                        f"Expected {expected_calls} calls to {hook_name}, got {len(calls)}")
    
    # Subprocess management convenience methods
    def add_safe_command(self, command: str, stdout: str, return_code: int = 0, stderr: str = ""):
        """Add safe command response."""
        try:
            from .mocks import MockSubprocessResult
        except ImportError:
            from mocks import MockSubprocessResult
        self.mock_subprocess.add_command_response(command, MockSubprocessResult(
            args=command,
            returncode=return_code,
            stdout=stdout,
            stderr=stderr
        ))
    
    def block_dangerous_commands(self):
        """Ensure dangerous command blocking is enabled."""
        self.mock_subprocess.enable_dangerous_blocking()
    
    def assert_command_was_executed(self, pattern: str, expected_count: int = 1):
        """Assert that command matching pattern was executed."""
        commands = self.mock_subprocess.get_executed_commands(pattern)
        self.assertEqual(len(commands), expected_count,
                        f"Expected {expected_count} executions matching '{pattern}', got {len(commands)}")
    
    # Filesystem management convenience methods
    def create_test_file(self, path: str, content: str = "", permissions: int = 0o644):
        """Create test file in mock filesystem."""
        self.mock_filesystem.write_file(path, content, permissions)
    
    def create_test_directory(self, path: str):
        """Create test directory in mock filesystem."""
        self.mock_filesystem.create_directory(path)
    
    def protect_file(self, path: str):
        """Make file read-only."""
        self.mock_filesystem.make_read_only(path)
    
    def block_file_access(self, path: str):
        """Block access to file/directory path."""
        self.mock_filesystem.block_path(path)
    
    def assert_file_was_accessed(self, path: str, operation: str, expected_count: int = 1):
        """Assert that file was accessed with specific operation."""
        operations = self.mock_filesystem.get_operations(operation)
        matching_ops = [op for op in operations if op['path'] == path]
        self.assertEqual(len(matching_ops), expected_count,
                        f"Expected {expected_count} {operation} operations on {path}, got {len(matching_ops)}")
    
    # Environment management convenience methods
    def set_test_env_var(self, key: str, value: str):
        """Set test environment variable."""
        self.mock_environment.set(key, value)
    
    def protect_env_var(self, key: str):
        """Protect environment variable from modification."""
        self.mock_environment.protect(key)
    
    def block_env_var(self, key: str):
        """Block environment variable access."""
        self.mock_environment.block(key)
    
    def assert_env_var_was_set(self, key: str, expected_value: str):
        """Assert that environment variable was set to expected value."""
        actual_value = self.mock_environment.get(key)
        self.assertEqual(actual_value, expected_value,
                        f"Expected {key}={expected_value}, got {key}={actual_value}")
    
    # Safety evaluation integration methods
    def enable_safety_evaluation(self):
        """Enable real safety logic evaluation if available."""
        if self.safety_logic:
            self.mock_safety_hook.enable_auto_evaluation(self.safety_logic)
            return True
        return False
    
    def evaluate_tool_call_safety(self, tool_name: str, tool_input: dict):
        """Test tool call safety using mock safety hook."""
        return self.mock_safety_hook.evaluate_tool_call(tool_name, tool_input)


if __name__ == '__main__':
    """When run directly, perform environment validation."""
    success = run_validation()
    sys.exit(0 if success else 1)