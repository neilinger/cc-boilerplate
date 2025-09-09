#!/usr/bin/env python3
"""
Test PRP execution command with feature branch automation.
Validates proper branch creation and PRP integration workflow.
"""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
import os
import shutil


class TestPRPExecuteCommand(unittest.TestCase):
    """Test PRP execute command functionality."""

    def setUp(self):
        """Set up test environment with temporary git repo."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_dir = Path.cwd()

        # Change to test directory
        os.chdir(self.test_dir)

        # Initialize git repo
        subprocess.run(['git', 'init'], check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], check=True)

        # Create initial commit on main
        (self.test_dir / 'README.md').write_text('# Test Repo')
        subprocess.run(['git', 'add', 'README.md'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)

        # Create PRPs directory
        prp_dir = self.test_dir / 'PRPs'
        prp_dir.mkdir()

        # Create test PRP file
        self.test_prp = prp_dir / 'prp-001-test-feature.md'
        self.test_prp.write_text("""# PRP-001: Test Feature Implementation

## Feature Goal
Implement test feature functionality

## Deliverable
Working test feature with validation

## Success Definition
- Feature works as expected
- Tests pass
- Documentation updated

## Implementation Tasks

1. Create test feature module
2. Add comprehensive tests
3. Update documentation
4. Validate functionality

## Final Validation Checklist

- [ ] All tests pass
- [ ] Code follows KISS/YAGNI principles
- [ ] Documentation updated
- [ ] Feature meets requirements
""")

        # Copy command file to test location
        self.claude_dir = self.test_dir / '.claude' / 'commands' / 'prp'
        self.claude_dir.mkdir(parents=True)

        # Copy the execute command
        original_cmd = self.original_dir / '.claude' / 'commands' / 'prp' / 'execute.md'
        test_cmd = self.claude_dir / 'execute.md'
        if original_cmd.exists():
            shutil.copy(original_cmd, test_cmd)

        # Commit all test files to have clean git state
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Add test files'], check=True)

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def run_command_script(self, prp_path: str) -> tuple:
        """Extract and run bash script from execute.md command."""
        cmd_file = self.claude_dir / 'execute.md'
        if not cmd_file.exists():
            return 1, "", "Command file not found"

        # Extract bash code blocks from markdown
        content = cmd_file.read_text()
        bash_blocks = []
        in_bash_block = False
        current_block = []

        for line in content.split('\n'):
            if line.strip() == '```bash':
                in_bash_block = True
                current_block = []
            elif line.strip() == '```' and in_bash_block:
                bash_blocks.append('\n'.join(current_block))
                in_bash_block = False
                current_block = []
            elif in_bash_block:
                current_block.append(line)

        # Create test script
        script_content = f"""#!/bin/bash
set -e

# Set PRP file argument
ARGUMENTS="{prp_path}"

{chr(10).join(bash_blocks)}
"""

        script_path = self.test_dir / 'test_execute.sh'
        script_path.write_text(script_content)
        script_path.chmod(0o755)

        # Commit the script to avoid it showing as uncommitted
        subprocess.run(['git', 'add', 'test_execute.sh'], capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Add test script'], capture_output=True)

        try:
            # Run with input for prompts (answer 'y' to switch to main)
            result = subprocess.run(
                [str(script_path)],
                input="y\n",  # Answer yes to switch to main
                text=True,
                capture_output=True,
                timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return 1, "", "Command timed out"

    def test_prp_file_validation(self):
        """Test PRP file validation logic."""
        # Test with non-existent file
        returncode, stdout, stderr = self.run_command_script("nonexistent.md")

        # Should fail with file not found
        self.assertNotEqual(returncode, 0)
        self.assertIn("not found", stdout + stderr)

    def test_prp_filename_parsing(self):
        """Test PRP filename parsing for branch name generation."""
        # This should succeed in parsing
        returncode, stdout, stderr = self.run_command_script("PRPs/prp-001-test-feature.md")

        # Should extract correct branch name
        output = stdout + stderr
        self.assertIn("feature/prp-001-test-feature", output)

    def test_invalid_prp_filename_format(self):
        """Test handling of invalid PRP filename formats."""
        # Create invalid PRP file
        invalid_prp = self.test_dir / 'PRPs' / 'invalid-name.md'
        invalid_prp.write_text("Invalid PRP")

        # Commit it to avoid uncommitted changes error
        subprocess.run(['git', 'add', 'PRPs/invalid-name.md'], capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Add invalid PRP for testing'], capture_output=True)

        returncode, stdout, stderr = self.run_command_script("PRPs/invalid-name.md")

        # Should fail with format error
        self.assertNotEqual(returncode, 0)
        self.assertIn("Invalid PRP filename format", stdout + stderr)

    def test_feature_branch_creation(self):
        """Test feature branch creation workflow."""
        # Ensure we're on main
        subprocess.run(['git', 'checkout', 'main'], check=True)

        # Run command
        returncode, stdout, stderr = self.run_command_script("PRPs/prp-001-test-feature.md")

        # Should succeed
        if returncode != 0:
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")

        # Check if branch was created
        result = subprocess.run(
            ['git', 'branch'],
            capture_output=True,
            text=True
        )

        self.assertIn("feature/prp-001-test-feature", result.stdout)

    def test_git_environment_validation(self):
        """Test git environment validation."""
        # Create uncommitted changes after the initial commit
        (self.test_dir / 'dirty.txt').write_text('uncommitted')

        # Run command - should detect dirty working directory
        returncode, stdout, stderr = self.run_command_script("PRPs/prp-001-test-feature.md")

        # Should detect uncommitted changes
        output = stdout + stderr
        self.assertIn("uncommitted changes", output.lower())

    def test_prp_content_extraction(self):
        """Test PRP content extraction and display."""
        # Ensure clean git state
        subprocess.run(['git', 'checkout', 'main'], check=True)

        returncode, stdout, stderr = self.run_command_script("PRPs/prp-001-test-feature.md")

        output = stdout + stderr

        # Should display key sections
        self.assertIn("FEATURE GOAL", output)
        self.assertIn("DELIVERABLE", output)
        self.assertIn("SUCCESS DEFINITION", output)
        self.assertIn("IMPLEMENTATION TASKS", output)
        self.assertIn("FINAL VALIDATION CHECKLIST", output)

        # Should show actual content from PRP
        self.assertIn("test feature functionality", output.lower())

    def test_integration_with_release_flow(self):
        """Test integration with Release Flow branching strategy."""
        # Ensure clean state on main
        subprocess.run(['git', 'checkout', 'main'], check=True)

        returncode, stdout, stderr = self.run_command_script("PRPs/prp-001-test-feature.md")

        output = stdout + stderr

        # Should mention Release Flow integration
        self.assertIn("release branch", output.lower())
        self.assertIn("git-ops:create-pull-request", output)
        self.assertIn("git-ops:smart-commit", output)

    def test_existing_branch_handling(self):
        """Test handling when feature branch already exists."""
        # Create branch manually first
        subprocess.run(['git', 'checkout', '-b', 'feature/prp-001-test-feature'], check=True)
        subprocess.run(['git', 'checkout', 'main'], check=True)

        # Run command - should detect existing branch
        returncode, stdout, stderr = self.run_command_script("PRPs/prp-001-test-feature.md")

        output = stdout + stderr
        self.assertIn("already exists", output)


if __name__ == '__main__':
    unittest.main()
