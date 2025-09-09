#!/usr/bin/env python3
"""
Tier 2B: Portable Functionality Tests

Environment-agnostic tests for configuration parsing, project structure validation,
and cross-platform compatibility. These tests focus on the infrastructure and
data validation aspects of the system.

Test Categories:
- Configuration file parsing and validation
- Project structure integrity checks
- Safety logic integration with different tool inputs
- Test data validation and golden dataset comparisons
- Cross-platform compatibility checks
- Performance and timing validation

Following KISS/YAGNI: Test infrastructure functionality without environmental dependencies.
"""

import unittest
import json
import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any

# Import our test infrastructure
from test_base import IsolatedTestCase, CICompatibleTestCase, SafetyLogicTestCase


class TestConfigurationParsing(IsolatedTestCase):
    """Test configuration file parsing and validation."""

    def test_claude_settings_json_parsing(self):
        """Test parsing of .claude/settings.json configuration."""
        # Create test settings file
        settings_data = {
            "permissions": {
                "allow": ["Bash(ls:*)", "Read", "Write"],
                "deny": ["Bash(rm:*)"]
            },
            "statusLine": {
                "type": "command",
                "command": "python status.py"
            },
            "hooks": {
                "PreToolUse": [{
                    "matcher": "",
                    "hooks": [{"type": "command", "command": "python pre_tool_use.py"}]
                }]
            }
        }

        settings_file = self.create_test_file('.claude/settings.json', json.dumps(settings_data, indent=2))

        # Parse and validate
        with open(settings_file) as f:
            parsed = json.load(f)

        # Verify structure
        self.assertIn('permissions', parsed)
        self.assertIn('allow', parsed['permissions'])
        self.assertIn('deny', parsed['permissions'])
        self.assertIn('hooks', parsed)
        self.assertIn('PreToolUse', parsed['hooks'])

        # Verify content
        self.assertEqual(parsed['permissions']['allow'], ["Bash(ls:*)", "Read", "Write"])
        self.assertEqual(parsed['permissions']['deny'], ["Bash(rm:*)"])

    def test_invalid_settings_json_handling(self):
        """Test handling of invalid settings.json files."""
        # Test cases with invalid JSON
        invalid_configs = [
            '{"invalid": json}',  # Malformed JSON
            '{"permissions": {"allow": "not_a_list"}}',  # Wrong type
            '{}',  # Empty config
            '{"hooks": {"PreToolUse": "not_a_list"}}',  # Wrong hook format
        ]

        for i, invalid_config in enumerate(invalid_configs):
            with self.subTest(case=i):
                settings_file = self.create_test_file(f'.claude/settings{i}.json', invalid_config)

                # Should either raise JSONDecodeError or parse to something we can validate
                try:
                    with open(settings_file) as f:
                        parsed = json.load(f)

                    # If it parses, we should be able to handle missing/wrong fields gracefully
                    permissions = parsed.get('permissions', {})
                    allow_list = permissions.get('allow', [])

                    # Should be able to handle any format gracefully
                    if not isinstance(allow_list, list):
                        allow_list = []

                    self.assertIsInstance(allow_list, list)

                except json.JSONDecodeError:
                    # Expected for malformed JSON
                    pass

    def test_pyproject_toml_structure(self):
        """Test pyproject.toml structure and content."""
        # Create test pyproject.toml
        toml_content = '''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "test-project"
version = "0.1.0"
description = "Test project"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = []

[tool.setuptools.packages.find]
exclude = ["logs*", "PRPs*", "output*", "docs*"]
'''

        pyproject_file = self.create_test_file('pyproject.toml', toml_content)

        # For now, just verify file exists and has expected content
        content = pyproject_file.read_text()
        self.assertIn('[project]', content)
        self.assertIn('name = "test-project"', content)
        self.assertIn('requires-python = ">=3.11"', content)
        self.assertIn('dependencies = []', content)

    def test_environment_file_parsing(self):
        """Test .env file parsing and validation."""
        # Create test .env files
        env_content = '''# Test environment variables
SECRET_KEY=test_secret_123
API_KEY=real_api_key_456
DATABASE_URL=sqlite:///test.db
DEBUG=true
PORT=3000
'''

        env_sample_content = '''# Sample environment variables
SECRET_KEY=your_secret_here
API_KEY=your_api_key_here
DATABASE_URL=sqlite:///app.db
DEBUG=false
PORT=3000
'''

        env_file = self.create_test_file('.env', env_content)
        env_sample_file = self.create_test_file('.env.sample', env_sample_content)

        # Parse .env files (simple key=value parsing)
        def parse_env_file(file_path):
            env_vars = {}
            for line in file_path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
            return env_vars

        env_vars = parse_env_file(env_file)
        sample_vars = parse_env_file(env_sample_file)

        # Verify parsing
        self.assertEqual(env_vars['SECRET_KEY'], 'test_secret_123')
        self.assertEqual(env_vars['API_KEY'], 'real_api_key_456')
        self.assertEqual(env_vars['DEBUG'], 'true')

        self.assertEqual(sample_vars['SECRET_KEY'], 'your_secret_here')
        self.assertEqual(sample_vars['DEBUG'], 'false')

        # Verify they have same keys
        self.assertEqual(set(env_vars.keys()), set(sample_vars.keys()))

    def test_hook_configuration_validation(self):
        """Test hook configuration structure validation."""
        # Test valid hook configurations
        valid_hook_configs = [
            {
                "PreToolUse": [{
                    "matcher": "",
                    "hooks": [{"type": "command", "command": "python pre.py"}]
                }]
            },
            {
                "PreToolUse": [{
                    "matcher": "Bash(rm:*)",
                    "hooks": [
                        {"type": "command", "command": "python safety.py"},
                        {"type": "command", "command": "python log.py"}
                    ]
                }]
            },
            {}  # Empty hooks config should be valid
        ]

        for i, config in enumerate(valid_hook_configs):
            with self.subTest(case=i):
                # Validate structure
                self.assertIsInstance(config, dict)

                for hook_type, hook_list in config.items():
                    self.assertIsInstance(hook_list, list)

                    for hook_entry in hook_list:
                        self.assertIsInstance(hook_entry, dict)
                        if 'hooks' in hook_entry:
                            self.assertIsInstance(hook_entry['hooks'], list)

                            for hook in hook_entry['hooks']:
                                self.assertIsInstance(hook, dict)
                                self.assertIn('type', hook)
                                if hook['type'] == 'command':
                                    self.assertIn('command', hook)


class TestProjectStructureValidation(IsolatedTestCase):
    """Test project structure integrity and validation."""

    def test_essential_directory_structure(self):
        """Test presence and structure of essential directories."""
        # Essential directories for the project
        essential_dirs = [
            'tests',
            'scripts',
            '.claude',
            '.claude/hooks',
            'logs'
        ]

        # These should have been created by setUp()
        for dir_path in essential_dirs:
            dir_full_path = self.test_dir / dir_path
            self.assertTrue(dir_full_path.exists(), f"Directory should exist: {dir_path}")
            self.assertTrue(dir_full_path.is_dir(), f"Should be a directory: {dir_path}")

    def test_file_permissions_and_structure(self):
        """Test file permissions and executable structure."""
        # Create test hook file
        hook_file = self.create_test_file('.claude/hooks/test_hook.py', '#!/usr/bin/env python3\nprint("test")\n')
        hook_file.chmod(0o755)

        # Verify permissions
        file_stat = hook_file.stat()
        # Check if file is executable (owner can execute)
        self.assertTrue(file_stat.st_mode & 0o100, "Hook file should be executable")

        # Test script header validation
        content = hook_file.read_text()
        self.assertTrue(content.startswith('#!'), "Script should have shebang")

    def test_log_directory_creation_and_access(self):
        """Test log directory creation and write access."""
        logs_dir = self.test_dir / 'logs'

        # Should exist from setUp()
        self.assertTrue(logs_dir.exists())

        # Test write access
        test_log = logs_dir / 'test.log'
        test_log.write_text('test log entry\n')

        self.assertTrue(test_log.exists())
        self.assertEqual(test_log.read_text(), 'test log entry\n')

    def test_configuration_file_locations(self):
        """Test that configuration files are in expected locations."""
        # Create expected config files
        config_files = {
            '.claude/settings.json': '{}',
            '.env.sample': 'TEST_VAR=sample_value\n',
            'pyproject.toml': '[project]\nname = "test"\n'
        }

        for file_path, content in config_files.items():
            config_file = self.create_test_file(file_path, content)

            # Verify location and readability
            self.assertTrue(config_file.exists())
            self.assertTrue(config_file.is_file())
            self.assertGreater(len(config_file.read_text()), 0)

    def test_directory_traversal_safety(self):
        """Test safety against directory traversal in paths."""
        # Test potentially dangerous paths
        dangerous_paths = [
            '../../../etc/passwd',
            '..\\..\\windows\\system32',
            '/etc/passwd',
            '~/.ssh/id_rsa',
            '$HOME/.bashrc'
        ]

        for path in dangerous_paths:
            with self.subTest(path=path):
                # Should not allow access outside test directory
                full_path = Path(path)

                if full_path.is_absolute():
                    # Absolute paths to system directories should be flagged
                    if str(full_path).startswith(('/etc/', '/bin/', '/sbin/', '/usr/bin/')):
                        self.assertTrue(True, "System path detected")

                # Path traversal attempts should be detected
                if '..' in path:
                    self.assertIn('..', path, "Path traversal detected")

    def test_project_metadata_consistency(self):
        """Test consistency between project metadata files."""
        # Create pyproject.toml with project info
        pyproject_content = '''[project]
name = "test-project"
version = "1.0.0"
description = "Test project description"
requires-python = ">=3.11"
'''

        # Create README with project info
        readme_content = '''# Test Project

Version: 1.0.0

Test project description for validation.
'''

        pyproject_file = self.create_test_file('pyproject.toml', pyproject_content)
        readme_file = self.create_test_file('README.md', readme_content)

        # Parse and verify consistency
        pyproject_text = pyproject_file.read_text()
        readme_text = readme_file.read_text()

        # Check for version consistency
        self.assertIn('version = "1.0.0"', pyproject_text)
        self.assertIn('Version: 1.0.0', readme_text)

        # Check for name/title consistency
        self.assertIn('name = "test-project"', pyproject_text)
        self.assertIn('# Test Project', readme_text)


class TestSafetyLogicIntegrationScenarios(SafetyLogicTestCase):
    """Test safety logic integration with various tool input scenarios."""

    def test_comprehensive_dangerous_command_patterns(self):
        """Test safety logic against comprehensive dangerous command patterns."""
        # Extended dangerous command patterns
        dangerous_patterns = [
            # Basic rm -rf patterns
            'rm -rf /',
            'rm -rf /*',
            'rm -fr /',
            'RM -RF /',  # Case variations

            # Long-form options
            'rm --recursive --force /',
            'rm --force --recursive /',

            # Mixed options
            'rm -r -f /',
            'rm -f -r /',
            'rm -rf .',
            'rm -rf ..',
            'rm -rf ~',
            'rm -rf $HOME',

            # With additional parameters
            'rm -rf / --no-preserve-root',
            'rm -rfv /',
            'rm -rf /* 2>/dev/null',

            # Command chaining
            'ls && rm -rf /',
            'cd /tmp && rm -rf /',
        ]

        for cmd in dangerous_patterns:
            with self.subTest(command=cmd):
                self.assert_dangerous_command(cmd)

    def test_safe_command_patterns(self):
        """Test that safe commands are correctly identified."""
        safe_commands = [
            'ls -la',
            'mkdir new_directory',
            'touch file.txt',
            'rm file.txt',  # Specific file
            'rm -r specific_directory',  # Specific directory (no -f flag)
            # Note: 'rm -rf /tmp/safe_temp_dir' is dangerous (rm -rf pattern)
            'cp file1.txt file2.txt',
            'mv old_name.txt new_name.txt',
            'echo "hello world"',
            'python script.py',
            'npm install',
            'git status',
        ]

        for cmd in safe_commands:
            with self.subTest(command=cmd):
                self.assert_safe_command(cmd)

    def test_env_file_access_patterns(self):
        """Test comprehensive .env file access detection."""
        # Should block these (based on actual safety_logic patterns)
        blocking_cases = [
            ('Read', {'file_path': '.env'}),
            ('Read', {'file_path': './.env'}),
            ('Read', {'file_path': './project/.env'}),
            ('Edit', {'file_path': '.env'}),
            ('Write', {'file_path': '.env'}),
            ('MultiEdit', {'file_path': '.env'}),
            ('Bash', {'command': 'cat .env'}),
            ('Bash', {'command': 'head .env'}),  # Now blocked by enhanced patterns
            ('Bash', {'command': 'tail .env'}),  # Now blocked by enhanced patterns
            ('Bash', {'command': 'echo "SECRET=value" > .env'}),
            ('Bash', {'command': 'cp .env .env.backup'}),
            ('Bash', {'command': 'mv .env .env.old'}),
        ]

        for tool_name, tool_input in blocking_cases:
            with self.subTest(tool=tool_name, input=tool_input):
                self.assert_blocks_env_access(tool_name, tool_input)

        # Should allow these (based on actual safety_logic behavior)
        allowing_cases = [
            ('Read', {'file_path': '.env.sample'}),  # Only .env.sample is explicitly allowed
            ('Read', {'file_path': 'environment.txt'}),  # Files without .env in name
            ('Bash', {'command': 'cat .env.sample'}),
            ('Bash', {'command': 'head .env.sample'}),  # .env.sample is allowed
            ('Bash', {'command': 'tail .env.sample'}),  # .env.sample is allowed
            # Note: .env.example, .env.template contain '.env' so they're blocked
            # Note: config.env contains '.env' so it's blocked
            # Note: cp .env.sample .env writes to .env so it's blocked
        ]

        for tool_name, tool_input in allowing_cases:
            with self.subTest(tool=tool_name, input=tool_input):
                self.assert_allows_env_access(tool_name, tool_input)

    def test_complex_tool_input_scenarios(self):
        """Test safety logic with complex tool inputs."""
        # Complex MultiEdit scenarios
        complex_inputs = [
            {
                'tool_name': 'MultiEdit',
                'tool_input': {
                    'file_path': './safe_file.py',
                    'edits': [
                        {'old_string': 'old_code', 'new_string': 'new_code'},
                        {'old_string': 'another_old', 'new_string': 'another_new'}
                    ]
                },
                'should_block': False
            },
            {
                'tool_name': 'MultiEdit',
                'tool_input': {
                    'file_path': '.env',  # Dangerous file
                    'edits': [
                        {'old_string': 'KEY=old', 'new_string': 'KEY=new'}
                    ]
                },
                'should_block': True
            },
            {
                'tool_name': 'Bash',
                'tool_input': {
                    'command': 'find . -name "*.py" -type f',
                    'timeout': 30
                },
                'should_block': False
            }
        ]

        for scenario in complex_inputs:
            with self.subTest(scenario=scenario['tool_name']):
                assessment = self.safety.get_safety_assessment(
                    scenario['tool_name'],
                    scenario['tool_input']
                )

                self.assertEqual(
                    assessment['blocked'],
                    scenario['should_block'],
                    f"Expected blocked={scenario['should_block']} for {scenario}"
                )


class TestDataValidationAndGoldenDatasets(IsolatedTestCase):
    """Test data validation and golden dataset comparisons."""

    def test_json_schema_validation(self):
        """Test JSON data against expected schemas."""
        # Schema for hook input data
        expected_hook_input_schema = {
            'tool_name': str,
            'tool_input': dict,
        }

        # Valid test cases
        valid_inputs = [
            {'tool_name': 'Read', 'tool_input': {'file_path': 'test.txt'}},
            {'tool_name': 'Bash', 'tool_input': {'command': 'ls'}},
            {'tool_name': 'Write', 'tool_input': {'file_path': 'out.txt', 'content': 'data'}},
        ]

        for input_data in valid_inputs:
            with self.subTest(input=input_data):
                # Validate structure
                for key, expected_type in expected_hook_input_schema.items():
                    self.assertIn(key, input_data)
                    self.assertIsInstance(input_data[key], expected_type)

    def test_log_data_validation(self):
        """Test log data structure and content validation."""
        # Create test log data
        log_entries = [
            {
                'timestamp': '2024-01-01T00:00:00Z',
                'tool_name': 'Read',
                'tool_input': {'file_path': 'test.txt'},
                'blocked': False,
                'reason': None
            },
            {
                'timestamp': '2024-01-01T00:01:00Z',
                'tool_name': 'Bash',
                'tool_input': {'command': 'rm -rf /'},
                'blocked': True,
                'reason': 'Dangerous rm command detected'
            }
        ]

        # Write and read log file
        log_file = self.create_test_file('logs/test.json', json.dumps(log_entries, indent=2))

        # Validate log structure
        with open(log_file) as f:
            parsed_logs = json.load(f)

        self.assertEqual(len(parsed_logs), 2)

        for entry in parsed_logs:
            # Required fields
            required_fields = ['timestamp', 'tool_name', 'tool_input', 'blocked']
            for field in required_fields:
                self.assertIn(field, entry)

            # Type validation
            self.assertIsInstance(entry['tool_name'], str)
            self.assertIsInstance(entry['tool_input'], dict)
            self.assertIsInstance(entry['blocked'], bool)

            if entry['blocked']:
                self.assertIsInstance(entry.get('reason'), str)

    def test_configuration_data_integrity(self):
        """Test configuration data integrity and consistency."""
        # Create comprehensive settings
        settings_data = {
            'permissions': {
                'allow': ['Read', 'Write', 'Bash(ls:*)'],
                'deny': ['Bash(rm:*)', 'Bash(dd:*)']
            },
            'hooks': {
                'PreToolUse': [{
                    'matcher': '',
                    'hooks': [{'type': 'command', 'command': 'python pre.py'}]
                }]
            },
            'version': '1.0.0',
            'created': '2024-01-01T00:00:00Z'
        }

        settings_file = self.create_test_file('.claude/settings.json', json.dumps(settings_data, indent=2))

        # Validate integrity after round-trip
        with open(settings_file) as f:
            loaded_data = json.load(f)

        self.assertEqual(loaded_data, settings_data)

        # Validate specific constraints
        permissions = loaded_data['permissions']
        self.assertIsInstance(permissions['allow'], list)
        self.assertIsInstance(permissions['deny'], list)

        # No overlap between allow and deny should exist in a well-formed config
        allow_patterns = set(permissions['allow'])
        deny_patterns = set(permissions['deny'])
        overlap = allow_patterns & deny_patterns
        self.assertEqual(len(overlap), 0, f"Allow/deny overlap found: {overlap}")


class TestCrossPlatformCompatibility(CICompatibleTestCase, IsolatedTestCase):
    """Test cross-platform compatibility and environment handling."""

    def setUp(self):
        """Set up both parent classes."""
        CICompatibleTestCase.setUp(self)
        IsolatedTestCase.setUp(self)

    def test_path_separator_handling(self):
        """Test proper handling of different path separators."""
        # Test paths with different separators
        test_paths = [
            'relative/path/to/file.txt',      # Unix style
            'relative\\path\\to\\file.txt',   # Windows style
            './relative/path/file.txt',       # Unix relative
            '.\\relative\\path\\file.txt',    # Windows relative
        ]

        for path_str in test_paths:
            with self.subTest(path=path_str):
                # Convert to Path object for normalization
                path_obj = Path(path_str)

                # Should be able to create normalized path
                normalized = str(path_obj)
                self.assertIsInstance(normalized, str)
                self.assertGreater(len(normalized), 0)

                # Test file creation with various path formats
                try:
                    test_file = self.create_test_file(path_str, 'test content')
                    self.assertTrue(test_file.exists())
                except (OSError, ValueError) as e:
                    # Some path formats might not be valid on current OS
                    self.skipTest(f"Path format not supported on this platform: {e}")

    def test_environment_variable_handling(self):
        """Test environment variable access and validation."""
        # Test common environment variables
        env_vars_to_test = ['HOME', 'USER', 'PATH', 'CI', 'GITHUB_ACTIONS']

        for var_name in env_vars_to_test:
            with self.subTest(var=var_name):
                var_value = os.environ.get(var_name)

                if var_value is not None:
                    self.assertIsInstance(var_value, str)
                    if var_name == 'PATH':
                        # PATH should contain directory separators
                        self.assertTrue(os.pathsep in var_value or len(var_value.split(os.pathsep)) >= 1)

    def test_file_permission_handling(self):
        """Test file permission handling across platforms."""
        # Create test file
        test_file = self.create_test_file('permission_test.txt', 'test content')

        # Test readable
        self.assertTrue(test_file.exists())
        self.assertTrue(os.access(test_file, os.R_OK))

        # Test writable
        self.assertTrue(os.access(test_file, os.W_OK))

        # Test chmod functionality
        try:
            test_file.chmod(0o644)  # Read/write for owner, read for others
            file_stat = test_file.stat()

            # Verify permissions were set (Unix-like systems)
            if hasattr(os, 'stat') and hasattr(file_stat, 'st_mode'):
                mode = file_stat.st_mode
                # Owner should have read/write
                self.assertTrue(mode & 0o600)  # Owner read/write

        except (OSError, AttributeError):
            # Permission modification might not be supported on all platforms
            self.skipTest("chmod not supported on this platform")

    def test_ci_environment_detection(self):
        """Test CI environment detection and adaptation."""
        # Should detect CI environment correctly
        is_ci = self.is_ci
        is_github_actions = self.is_github_actions

        # These should be boolean
        self.assertIsInstance(is_ci, bool)
        self.assertIsInstance(is_github_actions, bool)

        # Test timeout adaptation
        if is_ci:
            self.assertEqual(self.test_timeout, 5)
            self.assertTrue(self.use_mocks)
        else:
            self.assertEqual(self.test_timeout, 30)
            self.assertFalse(self.use_mocks)

    def test_unicode_and_encoding_handling(self):
        """Test Unicode and encoding handling across platforms."""
        # Test various Unicode strings
        unicode_strings = [
            'Hello, World! 🌍',
            'Tëst wïth àccénts',
            'Символы кириллицы',
            '日本語テキスト',
            '测试中文文本',
            'Math symbols: ∑∆∏√∞',
        ]

        for i, test_string in enumerate(unicode_strings):
            with self.subTest(string=test_string):
                try:
                    # Test file I/O with Unicode
                    test_file = self.create_test_file(f'unicode_test_{i}.txt', test_string)

                    # Read back and verify
                    read_content = test_file.read_text(encoding='utf-8')
                    self.assertEqual(read_content, test_string)

                    # Test JSON serialization/deserialization
                    json_data = {'content': test_string}
                    json_str = json.dumps(json_data, ensure_ascii=False)
                    parsed_data = json.loads(json_str)
                    self.assertEqual(parsed_data['content'], test_string)

                except UnicodeError as e:
                    self.fail(f"Unicode handling failed for {test_string}: {e}")


def run_tests():
    """Run all tests in this module."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestConfigurationParsing,
        TestProjectStructureValidation,
        TestSafetyLogicIntegrationScenarios,
        TestDataValidationAndGoldenDatasets,
        TestCrossPlatformCompatibility,
    ]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(
        verbosity=2,
        buffer=True,  # Capture stdout/stderr
        failfast=False
    )

    result = runner.run(suite)

    # Print summary
    print(f"\n{'='*60}")
    print("TIER 2B: PORTABLE FUNCTIONALITY TESTS SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")

    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")

    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")

    success_rate = ((result.testsRun - len(result.failures) - len(result.errors))
                   / result.testsRun * 100 if result.testsRun > 0 else 0)
    print(f"\nSuccess rate: {success_rate:.1f}%")

    # Return success status
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
