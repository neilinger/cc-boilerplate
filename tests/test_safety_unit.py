#!/usr/bin/env python3
"""
Tier 1: Pure Unit Tests for Safety Logic (CI Always)

Environment-agnostic unit tests that work reliably in both CI and local environments.
These tests focus on the extracted safety logic without any environmental dependencies.

Test Categories:
- Command pattern detection
- Path validation logic  
- Environment file access detection
- Security assessment logic

Following KISS/YAGNI: Test the logic, not the environment.
"""

import unittest
import sys
from pathlib import Path

# Import our test infrastructure
from test_base import SafetyLogicTestCase, CICompatibleTestCase


class TestDangerousCommandDetection(SafetyLogicTestCase):
    """Test dangerous rm command detection logic."""
    
    def test_basic_dangerous_patterns(self):
        """Test detection of basic dangerous rm patterns."""
        dangerous_commands = [
            "rm -rf /",
            "rm -rf /*",
            "rm -fr /",
            "rm -Rf /",
            "rm --recursive --force /",
            "rm --force --recursive /",
            "rm -r -f /",
            "rm -f -r /",
        ]
        
        for cmd in dangerous_commands:
            with self.subTest(command=cmd):
                self.assert_dangerous_command(cmd)
    
    def test_dangerous_path_patterns(self):
        """Test detection of dangerous paths with rm."""
        dangerous_commands = [
            "rm -rf ~",
            "rm -rf ~/",
            "rm -rf $HOME", 
            "rm -rf ..",
            "rm -rf .",
            "rm -rf *",
        ]
        
        for cmd in dangerous_commands:
            with self.subTest(command=cmd):
                self.assert_dangerous_command(cmd)
    
    def test_safe_rm_commands(self):
        """Test that safe rm commands are not flagged."""
        safe_commands = [
            "rm file.txt",
            "rm -f file.txt",
            "rm -r project/build",
            "rm -rf /tmp/specific_temp_dir",
            "rm *.log",
            "rm -rf build/",
        ]
        
        for cmd in safe_commands:
            with self.subTest(command=cmd):
                self.assert_safe_command(cmd)
    
    def test_commented_commands_are_safe(self):
        """Test that commented or echoed rm commands are not flagged."""
        safe_commands = [
            "echo rm -rf /",
            "# rm -rf /",
            "echo 'This would be dangerous: rm -rf /'",
        ]
        
        for cmd in safe_commands:
            with self.subTest(command=cmd):
                self.assert_safe_command(cmd, "Comments/echoes should not be flagged")
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Empty/invalid inputs
        self.assert_safe_command("", "Empty command should be safe")
        self.assert_safe_command(None, "None command should be safe")  
        
        # Non-rm commands
        self.assert_safe_command("ls -la", "Non-rm commands should be safe")
        self.assert_safe_command("cp -r source dest", "Copy commands should be safe")
        
        # Complex but safe rm
        self.assert_safe_command("rm -rf /tmp/$(date +%Y%m%d)", "Specific temp cleanup should be safe")


class TestEnvFileAccessDetection(SafetyLogicTestCase):
    """Test .env file access detection logic."""
    
    def test_file_tool_env_access(self):
        """Test detection of .env access via file tools."""
        file_tools = ['Read', 'Edit', 'MultiEdit', 'Write']
        
        for tool in file_tools:
            with self.subTest(tool=tool):
                # Should block .env access
                self.assert_blocks_env_access(tool, {"file_path": ".env"})
                self.assert_blocks_env_access(tool, {"file_path": "/path/to/.env"})
                self.assert_blocks_env_access(tool, {"file_path": "project/.env"})
                
                # Should allow .env.sample access
                self.assert_allows_env_access(tool, {"file_path": ".env.sample"})
                self.assert_allows_env_access(tool, {"file_path": "/path/to/.env.sample"})
                
                # Should allow other files
                self.assert_allows_env_access(tool, {"file_path": "config.json"})
                self.assert_allows_env_access(tool, {"file_path": "environment.yml"})
    
    def test_bash_tool_env_access(self):
        """Test detection of .env access via bash commands."""
        dangerous_commands = [
            "cat .env",
            "less .env", 
            "head .env",
            "tail .env",
            "grep SECRET .env",
            "cp .env backup.env",
            "mv .env old.env",
            "rm .env",
            "echo 'new_var=value' >> .env",
        ]
        
        for cmd in dangerous_commands:
            with self.subTest(command=cmd):
                self.assert_blocks_env_access("Bash", {"command": cmd})
        
        # Safe commands should be allowed
        safe_commands = [
            "cat .env.sample",
            "cp .env.sample .env.local", 
            "ls -la",
            "echo 'This mentions .env but is safe'",
        ]
        
        for cmd in safe_commands:
            with self.subTest(command=cmd):
                self.assert_allows_env_access("Bash", {"command": cmd})
    
    def test_env_access_edge_cases(self):
        """Test edge cases for env access detection.""" 
        # Empty/invalid inputs
        self.assert_allows_env_access("Read", {})
        self.assert_allows_env_access("Bash", {"command": ""})
        self.assert_allows_env_access("UnknownTool", {"file_path": ".env"})


class TestCommandInjectionDetection(SafetyLogicTestCase):
    """Test command injection pattern detection."""
    
    def test_command_chaining_detection(self):
        """Test detection of command chaining patterns."""
        injection_patterns = [
            ("ls; rm -rf /", ["command_chaining_semicolon"]),
            ("ls && rm -rf /", ["command_chaining_and"]),
            ("ls || rm -rf /", ["command_chaining_or"]),
            ("ls | rm -rf /", ["pipe_injection"]),
            ("cmd1; cmd2 && cmd3", ["command_chaining_semicolon", "command_chaining_and"]),
        ]
        
        for command, expected_patterns in injection_patterns:
            with self.subTest(command=command):
                detected = self.safety.detect_command_injection_patterns(command)
                for pattern in expected_patterns:
                    self.assertIn(pattern, detected, 
                                f"Pattern {pattern} not detected in: {command}")
    
    def test_command_substitution_detection(self):
        """Test detection of command substitution patterns."""
        injection_patterns = [
            ("ls $(rm -rf /)", ["command_substitution_dollar"]),
            ("ls `rm -rf /`", ["command_substitution_backtick"]),
            ("echo ${DANGEROUS_VAR}", ["variable_expansion"]),
        ]
        
        for command, expected_patterns in injection_patterns:
            with self.subTest(command=command):
                detected = self.safety.detect_command_injection_patterns(command)
                for pattern in expected_patterns:
                    self.assertIn(pattern, detected,
                                f"Pattern {pattern} not detected in: {command}")
    
    def test_safe_commands_no_injection(self):
        """Test that safe commands don't trigger injection detection."""
        safe_commands = [
            "ls -la",
            "echo 'hello world'", 
            "python script.py",
            "git status",
            "npm install",
        ]
        
        for command in safe_commands:
            with self.subTest(command=command):
                patterns = self.safety.detect_command_injection_patterns(command)
                self.assertEqual(patterns, [], 
                               f"Safe command incorrectly flagged: {command}")


class TestFilePathValidation(SafetyLogicTestCase):
    """Test file path access validation."""
    
    def test_allowed_path_patterns(self):
        """Test that allowed paths are correctly validated."""
        allowed_paths = [
            "./project/file.txt",
            "relative/path.json", 
            "file.py",
            "/tmp/tempfile",
            "/var/tmp/temp.log",
        ]
        
        for path in allowed_paths:
            with self.subTest(path=path):
                result = self.safety.validate_file_path_access(path)
                self.assertTrue(result, f"Path should be allowed: {path}")
    
    def test_dangerous_path_patterns(self):
        """Test that dangerous paths are correctly blocked."""
        dangerous_paths = [
            "/etc/passwd",
            "/bin/sh",
            "/sbin/init", 
            "/usr/bin/sudo",
            "/root/.bashrc",
            "/home/user/.ssh/id_rsa",
            "../../../etc/passwd",
        ]
        
        for path in dangerous_paths:
            with self.subTest(path=path):
                result = self.safety.validate_file_path_access(path)
                self.assertFalse(result, f"Path should be blocked: {path}")
    
    def test_custom_allowed_patterns(self):
        """Test file path validation with custom allowed patterns."""
        custom_patterns = [r'^/custom/']
        
        # Should allow custom pattern
        result = self.safety.validate_file_path_access("/custom/file.txt", custom_patterns)
        self.assertTrue(result, "Custom allowed pattern should work")
        
        # Should still block dangerous patterns
        result = self.safety.validate_file_path_access("/etc/passwd", custom_patterns)
        self.assertFalse(result, "Dangerous paths should still be blocked")


class TestSafetyAssessment(SafetyLogicTestCase):
    """Test comprehensive safety assessment functionality."""
    
    def test_dangerous_rm_assessment(self):
        """Test safety assessment for dangerous rm commands."""
        assessment = self.safety.get_safety_assessment("Bash", {"command": "rm -rf /"})
        
        self.assertTrue(assessment['blocked'], "Dangerous rm should be blocked")
        self.assertEqual(assessment['reason'], "Dangerous rm command detected")
        self.assertIn('dangerous_rm', assessment['patterns_detected'])
        self.assertEqual(assessment['tool_name'], "Bash")
    
    def test_env_access_assessment(self):
        """Test safety assessment for .env file access."""
        assessment = self.safety.get_safety_assessment("Read", {"file_path": ".env"})
        
        self.assertTrue(assessment['blocked'], ".env access should be blocked")
        self.assertIn('sensitive data', assessment['reason'])
        self.assertIn('env_file_access', assessment['patterns_detected'])
    
    def test_command_injection_assessment(self):
        """Test safety assessment for command injection."""
        assessment = self.safety.get_safety_assessment("Bash", {"command": "ls; rm file"})
        
        # Currently warns but doesn't block (can be made stricter)
        self.assertFalse(assessment['blocked'], "Command chaining currently warns")
        self.assertTrue(len(assessment['warnings']) > 0, "Should have warnings")
        self.assertTrue(len(assessment['patterns_detected']) > 0, "Should detect patterns")
    
    def test_safe_tool_assessment(self):
        """Test safety assessment for safe tool calls."""
        assessment = self.safety.get_safety_assessment("Read", {"file_path": "config.json"})
        
        self.assertFalse(assessment['blocked'], "Safe tool call should not be blocked")
        self.assertIsNone(assessment['reason'], "Safe calls should have no block reason")
        self.assertEqual(len(assessment['warnings']), 0, "Safe calls should have no warnings")


class TestCICompatibility(CICompatibleTestCase):
    """Test that our safety logic works in CI environments."""
    
    def test_imports_work_in_ci(self):
        """Test that safety logic can be imported in CI."""
        # This test will only run if safety_logic is importable
        try:
            import safety_logic
            self.assertTrue(hasattr(safety_logic, 'is_dangerous_rm_command'))
            self.assertTrue(hasattr(safety_logic, 'is_env_file_access'))
            self.assertTrue(hasattr(safety_logic, 'get_safety_assessment'))
        except ImportError:
            self.skipTest("safety_logic module not available")
    
    def test_basic_functionality_in_ci(self):
        """Test basic safety functions work in CI."""
        if self.is_ci:
            # In CI: run quick smoke tests
            self.skip_if_not_ci()  # Only run this in CI
            
            # Quick tests that should work anywhere
            try:
                import safety_logic
                result = safety_logic.is_dangerous_rm_command("rm -rf /")
                self.assertTrue(result, "Basic dangerous command detection should work in CI")
            except ImportError:
                self.skipTest("safety_logic module not available in CI")


def main():
    """Run the unit tests."""
    # First validate the environment
    from test_base import run_validation
    if not run_validation():
        print("❌ Environment validation failed - cannot run tests safely")
        return 1
    
    # Run the tests
    print("\n" + "="*60)
    print("TIER 1: PURE UNIT TESTS (CI ALWAYS)")
    print("Testing safety logic without environmental dependencies")
    print("="*60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestDangerousCommandDetection,
        TestEnvFileAccessDetection, 
        TestCommandInjectionDetection,
        TestFilePathValidation,
        TestSafetyAssessment,
        TestCICompatibility,
    ]
    
    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TIER 1 TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print(f"\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print(f"\n❌ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    if result.skipped:
        print(f"\n⏭️  SKIPPED:")
        for test, reason in result.skipped:
            print(f"  - {test}: {reason}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    status = "✅ PASSED" if success else "❌ FAILED"
    print(f"\nOverall: {status}")
    
    return 0 if success else 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)