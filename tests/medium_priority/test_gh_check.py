"""Tests for gh-check command functionality

This test file verifies the GitHub maintenance check command implementation
as specified in prp-002-github-maintenance-check.md
"""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


class TestGhCheckCommand(unittest.TestCase):
    """Test cases for the gh-check command"""

    @classmethod
    def setUpClass(cls):
        """Set up test class"""
        cls.command_file = Path('.claude/commands/git-ops/gh-check.md')
        cls.repo_root = Path('.')

    def test_command_file_exists(self):
        """Verify gh-check command file exists in correct location"""
        self.assertTrue(self.command_file.exists(),
                       f"Command file not found at {self.command_file}")

    def test_command_file_not_empty(self):
        """Verify command file has content"""
        self.assertGreater(self.command_file.stat().st_size, 0,
                          "Command file is empty")

    def test_command_contains_error_handling(self):
        """Verify command includes proper error handling"""
        content = self.command_file.read_text()

        # Check for gh CLI dependency check
        self.assertIn('command -v gh', content,
                     "Missing gh CLI dependency check")

        # Check for authentication check
        self.assertIn('gh auth status', content,
                     "Missing GitHub authentication check")

        # Check for git repository check
        self.assertIn('git rev-parse --is-inside-work-tree', content,
                     "Missing git repository check")

    def test_command_uses_correct_json_syntax(self):
        """Verify command uses correct JSON syntax (not --arg)"""
        content = self.command_file.read_text()

        # Should NOT contain the broken --arg syntax
        self.assertNotIn('--jq --arg', content,
                        "Command still contains broken --arg syntax")

        # Should contain proper JSON parsing
        self.assertIn('--jq "', content,
                     "Command should use proper --jq syntax")

    def test_command_is_read_only(self):
        """Verify command performs no write operations"""
        content = self.command_file.read_text()

        # Extract only the bash script part (between ```bash markers)
        lines = content.split('\n')
        bash_start = None
        bash_end = None

        for i, line in enumerate(lines):
            if line.strip() == '```bash':
                bash_start = i + 1
            elif bash_start and line.strip() == '```':
                bash_end = i
                break

        # Only check the actual script, not the documentation
        if bash_start and bash_end:
            bash_script = '\n'.join(lines[bash_start:bash_end])
        else:
            bash_script = content

        # Should not contain any write operations in the actual script
        write_commands = ['gh issue close', 'gh pr merge', 'gh issue edit',
                         'gh pr edit', 'git commit', 'git push']

        for cmd in write_commands:
            self.assertNotIn(cmd, bash_script,
                           f"Command should be read-only, found: {cmd}")

    def test_command_checks_all_categories(self):
        """Verify command checks all required maintenance categories"""
        content = self.command_file.read_text()

        # Check for all required categories from prp-002
        categories = [
            'unlabeled',  # Issues needing labels
            'stale',      # Stale issues
            'review',     # PRs awaiting review
            'draft',      # Draft PRs
            'approved'    # Approved PRs
        ]

        for category in categories:
            self.assertIn(category.lower(), content.lower(),
                         f"Missing check for {category} items")

    def test_bash_syntax_validity(self):
        """Verify bash script has valid syntax (basic check)"""
        content = self.command_file.read_text()

        # Extract the bash script part (between ```bash markers)
        lines = content.split('\n')
        bash_start = None
        bash_end = None

        for i, line in enumerate(lines):
            if line.strip() == '```bash':
                bash_start = i + 1
            elif bash_start and line.strip() == '```':
                bash_end = i
                break

        self.assertIsNotNone(bash_start, "Could not find bash script start")
        self.assertIsNotNone(bash_end, "Could not find bash script end")

        # Extract bash script
        bash_script = '\n'.join(lines[bash_start:bash_end])

        # Write to temp file and check syntax
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write(bash_script)
            temp_file = f.name

        try:
            # Check bash syntax
            result = subprocess.run(['bash', '-n', temp_file],
                                  capture_output=True, text=True)
            self.assertEqual(result.returncode, 0,
                           f"Bash syntax error: {result.stderr}")
        finally:
            os.unlink(temp_file)

    def test_cross_platform_date_handling(self):
        """Verify command handles cross-platform date differences"""
        content = self.command_file.read_text()

        # Should contain fallback for macOS/Linux date command differences
        self.assertIn('date -d', content, "Missing Linux date format")
        self.assertIn('date -v', content, "Missing macOS date format")
        self.assertIn('2>/dev/null', content, "Missing error redirection")


if __name__ == '__main__':
    unittest.main()
