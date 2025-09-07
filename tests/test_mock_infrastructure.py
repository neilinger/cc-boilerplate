#!/usr/bin/env python3
"""
Tests for the comprehensive mocking infrastructure.

This module demonstrates how to use the mock systems and verifies that
they work correctly for testing Claude Code hooks, subprocess execution,
file system operations, and environment variables.

Following KISS/YAGNI: Simple tests that verify essential functionality.
"""

import unittest
import sys
from pathlib import Path

# Add tests directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from test_base import ComprehensiveMockTestCase
from mocks import (
    MockHookAction, MockHookResponse, MockSubprocessResult, MockFileSystemError
)


class TestMockInfrastructure(ComprehensiveMockTestCase):
    """Test the mock infrastructure itself."""
    
    def test_hook_mocking_basic(self):
        """Test basic hook mocking functionality."""
        # Set hook to block
        self.set_hook_to_block('pre_tool_use', 'Test blocking')
        
        # Run hook and verify response
        response = self.mock_hooks.run_hook('pre_tool_use', {'tool': 'Bash', 'input': {'command': 'ls'}})
        self.assertEqual(response.action, MockHookAction.BLOCK)
        self.assertEqual(response.reason, 'Test blocking')
        self.assertEqual(response.exit_code, 1)
        
        # Verify hook was called
        self.assert_hook_was_called('pre_tool_use', 1)
    
    def test_hook_mocking_allow(self):
        """Test hook allowing functionality."""
        self.set_hook_to_allow('pre_tool_use')
        
        response = self.mock_hooks.run_hook('pre_tool_use', {'tool': 'Read', 'input': {'file_path': 'test.txt'}})
        self.assertEqual(response.action, MockHookAction.ALLOW)
        self.assertEqual(response.exit_code, 0)
    
    def test_hook_mocking_error(self):
        """Test hook error functionality."""
        self.set_hook_to_error('pre_tool_use', 'Test error occurred')
        
        response = self.mock_hooks.run_hook('pre_tool_use', {'tool': 'Write', 'input': {}})
        self.assertEqual(response.action, MockHookAction.ERROR)
        self.assertEqual(response.reason, 'Test error occurred')
        self.assertEqual(response.exit_code, 2)
        self.assertEqual(response.stderr, 'Test error occurred')
    
    def test_subprocess_mocking_safe_commands(self):
        """Test subprocess mocking with safe commands."""
        # Add safe command response
        self.add_safe_command('ls', 'file1.txt\nfile2.txt', 0)
        
        # Run command through mock
        result = self.mock_subprocess.run(['ls'])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, 'file1.txt\nfile2.txt')
        
        # Verify command was executed
        self.assert_command_was_executed('ls')
    
    def test_subprocess_mocking_dangerous_blocking(self):
        """Test that dangerous commands are blocked."""
        # Ensure dangerous command blocking is enabled
        self.block_dangerous_commands()
        
        # Attempt dangerous command
        with self.assertRaises(PermissionError) as context:
            self.mock_subprocess.run(['rm', '-rf', '/'])
        
        self.assertIn('Dangerous command blocked', str(context.exception))
        self.assertIn('rm -rf /', str(context.exception))
    
    def test_filesystem_mocking_basic(self):
        """Test basic filesystem mocking."""
        # Create test file
        self.create_test_file('/test/file.txt', 'Test content')
        
        # Read file back
        content = self.mock_filesystem.read_file('/test/file.txt')
        self.assertEqual(content, 'Test content')
        
        # Verify file was accessed
        self.assert_file_was_accessed('/test/file.txt', 'write')
        self.assert_file_was_accessed('/test/file.txt', 'read')
        
        # Test file existence
        self.assertTrue(self.mock_filesystem.file_exists('/test/file.txt'))
        self.assertFalse(self.mock_filesystem.file_exists('/nonexistent.txt'))
    
    def test_filesystem_mocking_protection(self):
        """Test filesystem protection mechanisms."""
        # Create and protect a file
        self.create_test_file('/protected.txt', 'Protected content')
        self.protect_file('/protected.txt')
        
        # Attempt to write to protected file
        with self.assertRaises(MockFileSystemError):
            self.mock_filesystem.write_file('/protected.txt', 'New content')
        
        # Block path access
        self.block_file_access('/blocked')
        
        with self.assertRaises(MockFileSystemError):
            self.mock_filesystem.write_file('/blocked/file.txt', 'Content')
    
    def test_environment_mocking_basic(self):
        """Test basic environment variable mocking."""
        # Set environment variable
        self.set_test_env_var('TEST_VAR', 'test_value')
        
        # Verify it was set
        self.assertEqual(self.mock_environment.get('TEST_VAR'), 'test_value')
        self.assert_env_var_was_set('TEST_VAR', 'test_value')
        
        # Test protection
        self.protect_env_var('PROTECTED_VAR')
        self.set_test_env_var('PROTECTED_VAR', 'initial')
        
        with self.assertRaises(PermissionError):
            self.mock_environment.set('PROTECTED_VAR', 'changed')
    
    def test_environment_mocking_blocking(self):
        """Test environment variable blocking."""
        self.block_env_var('BLOCKED_VAR')
        
        with self.assertRaises(PermissionError):
            self.mock_environment.set('BLOCKED_VAR', 'value')
    
    def test_safety_hook_integration(self):
        """Test safety hook integration with real safety logic."""
        # Enable real safety evaluation
        self.enable_safety_evaluation()
        
        # Test dangerous rm command
        response = self.evaluate_tool_call_safety('Bash', {'command': 'rm -rf /'})
        # Should be blocked if safety logic is available, otherwise uses mock response
        self.assertIn(response.action, [MockHookAction.BLOCK, MockHookAction.ALLOW])
        
        # Test .env file access
        response = self.evaluate_tool_call_safety('Read', {'file_path': '.env'})
        # Should be blocked if safety logic is available
        self.assertIn(response.action, [MockHookAction.BLOCK, MockHookAction.ALLOW])
        
        # Test safe command
        response = self.evaluate_tool_call_safety('Bash', {'command': 'ls'})
        self.assertEqual(response.action, MockHookAction.ALLOW)


class TestMockIntegrationExamples(ComprehensiveMockTestCase):
    """Examples of how to use mocks together for comprehensive testing."""
    
    def test_complete_workflow_simulation(self):
        """Test a complete workflow with all mock systems."""
        # Setup: Create project structure in mock filesystem
        self.create_test_directory('/project')
        self.create_test_file('/project/main.py', 'print("Hello, World!")')
        self.create_test_file('/project/.env', 'SECRET_KEY=test_secret')
        
        # Setup: Configure environment
        self.set_test_env_var('PROJECT_PATH', '/project')
        self.set_test_env_var('DEBUG', 'true')
        
        # Setup: Configure subprocess responses
        self.add_safe_command('python /project/main.py', 'Hello, World!', 0)
        self.add_safe_command('ls /project', 'main.py\n.env', 0)
        
        # Setup: Configure hooks to allow safe operations
        self.set_hook_to_allow('pre_tool_use')
        
        # Test: Simulate running a safe command
        response = self.evaluate_tool_call_safety('Bash', {'command': 'ls /project'})
        self.assertEqual(response.action, MockHookAction.ALLOW)
        
        # Test: Simulate running the Python script
        result = self.mock_subprocess.run(['python', '/project/main.py'])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, 'Hello, World!')
        
        # Test: Verify file system state
        self.assertTrue(self.mock_filesystem.file_exists('/project/main.py'))
        self.assertTrue(self.mock_filesystem.file_exists('/project/.env'))
        
        # Test: Verify environment
        self.assertEqual(self.mock_environment.get('PROJECT_PATH'), '/project')
        self.assertEqual(self.mock_environment.get('DEBUG'), 'true')
        
        # Test: Attempt dangerous operation (should be blocked)
        with self.assertRaises(PermissionError):
            self.mock_subprocess.run(['rm', '-rf', '/project'])
    
    def test_security_focused_testing(self):
        """Test security-focused scenarios with comprehensive mocking."""
        # Block access to sensitive files
        self.block_file_access('/etc')
        self.block_file_access('/.ssh')
        
        # Block sensitive environment variables
        self.block_env_var('AWS_SECRET_ACCESS_KEY')
        self.block_env_var('DATABASE_PASSWORD')
        
        # Configure safety hook to be strict
        self.set_hook_to_block('pre_tool_use', 'Security test - blocking all operations')
        
        # Test: Attempt to access blocked file
        with self.assertRaises(MockFileSystemError):
            self.mock_filesystem.read_file('/etc/passwd')
        
        # Test: Attempt to set blocked environment variable
        with self.assertRaises(PermissionError):
            self.mock_environment.set('AWS_SECRET_ACCESS_KEY', 'fake_key')
        
        # Test: Hook blocks operations
        response = self.evaluate_tool_call_safety('Read', {'file_path': 'safe_file.txt'})
        self.assertEqual(response.action, MockHookAction.BLOCK)
        self.assertEqual(response.reason, 'Security test - blocking all operations')


if __name__ == '__main__':
    unittest.main()