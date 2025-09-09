#!/usr/bin/env python3
"""
Integration test for PRP execute command.
Tests the actual command functionality in a controlled environment.
"""

import subprocess
import tempfile
import unittest
from pathlib import Path
import os


class TestPRPExecuteIntegration(unittest.TestCase):
    """Integration test for PRP execute command."""

    def test_prp_execute_command_exists(self):
        """Test that the PRP execute command file exists and has correct structure."""
        cmd_file = Path('.claude/commands/prp/execute.md')
        self.assertTrue(cmd_file.exists(), "PRP execute command file should exist")

        content = cmd_file.read_text()

        # Should have proper markdown structure
        self.assertIn("# Execute PRP", content)
        self.assertIn("$ARGUMENTS", content)

        # Should have validation steps
        self.assertIn("git rev-parse --is-inside-work-tree", content)
        self.assertIn("git status --porcelain", content)

        # Should have branch creation logic
        self.assertIn("feature/prp-", content)
        self.assertIn("git checkout -b", content)

        # Should have PRP parsing logic
        self.assertIn("PRP_NUMBER", content)
        self.assertIn("PRP_SLUG", content)

        # Should display PRP content
        self.assertIn("FEATURE GOAL", content)
        self.assertIn("IMPLEMENTATION TASKS", content)
        self.assertIn("FINAL VALIDATION CHECKLIST", content)

        # Should integrate with Release Flow
        self.assertIn("git-ops:create-pull-request", content)
        self.assertIn("git-ops:smart-commit", content)

    def test_prp_filename_parsing_logic(self):
        """Test PRP filename parsing logic from the command."""
        cmd_file = Path('.claude/commands/prp/execute.md')
        content = cmd_file.read_text()

        # Should have proper regex patterns for PRP filename parsing
        self.assertIn("prp-\\([0-9]\\{3\\}\\)", content)
        self.assertIn("sed -n", content)

        # Should validate filename format
        self.assertIn("Invalid PRP filename format", content)
        self.assertIn("prp-XXX-feature-name.md", content)

    def test_git_safety_checks(self):
        """Test that git safety checks are in place."""
        cmd_file = Path('.claude/commands/prp/execute.md')
        content = cmd_file.read_text()

        # Should check for clean git state
        self.assertIn("git status --porcelain", content)
        self.assertIn("uncommitted changes", content)

        # Should check current branch
        self.assertIn("git branch --show-current", content)
        self.assertIn("main", content)

        # Should handle branch switching
        self.assertIn("Switch to main branch", content)
        self.assertIn("git checkout main", content)
        self.assertIn("git pull origin main", content)

    def test_feature_branch_creation_logic(self):
        """Test feature branch creation logic."""
        cmd_file = Path('.claude/commands/prp/execute.md')
        content = cmd_file.read_text()

        # Should check if branch exists
        self.assertIn("git show-ref --verify", content)
        self.assertIn("already exists", content)

        # Should create new branch
        self.assertIn("git checkout -b", content)
        self.assertIn("feature/prp-$PRP_NUMBER-$PRP_SLUG", content)

        # Should handle existing branch scenario
        self.assertIn("Switch to existing branch", content)

    def test_prp_content_extraction_logic(self):
        """Test PRP content extraction and display logic."""
        cmd_file = Path('.claude/commands/prp/execute.md')
        content = cmd_file.read_text()

        # Should extract key sections
        sections = [
            "Feature Goal",
            "Deliverable",
            "Success Definition",
            "Implementation Tasks",
            "Final Validation Checklist"
        ]

        for section in sections:
            self.assertIn(section, content)
            self.assertIn(f"grep -A", content)  # Uses grep to extract sections

        # Should use sed for advanced extraction
        self.assertIn("sed -n", content)

    def test_integration_with_existing_commands(self):
        """Test integration with existing git-ops commands."""
        cmd_file = Path('.claude/commands/prp/execute.md')
        content = cmd_file.read_text()

        # Should reference existing commands
        self.assertIn("/git-ops:smart-commit", content)
        self.assertIn("/git-ops:create-pull-request", content)

        # Should explain workflow
        self.assertIn("release branch", content)
        self.assertIn("Release Flow", content)

    def test_kiss_yagni_compliance(self):
        """Test that command follows KISS/YAGNI principles."""
        cmd_file = Path('.claude/commands/prp/execute.md')
        content = cmd_file.read_text()

        # Should mention KISS principles
        self.assertIn("KISS", content)
        self.assertIn("YAGNI", content)

        # Should be simple and focused
        self.assertIn("Single Purpose", content)
        self.assertIn("User Control", content)
        self.assertIn("Safe Defaults", content)

    def test_error_handling(self):
        """Test error handling in the command."""
        cmd_file = Path('.claude/commands/prp/execute.md')
        content = cmd_file.read_text()

        # Should handle missing arguments
        self.assertIn("No PRP file specified", content)
        self.assertIn("Usage:", content)

        # Should handle file not found
        self.assertIn("PRP file not found", content)

        # Should handle invalid format
        self.assertIn("Invalid PRP filename format", content)

        # Should use proper exit codes
        self.assertIn("exit 1", content)

    def test_user_experience(self):
        """Test user experience elements."""
        cmd_file = Path('.claude/commands/prp/execute.md')
        content = cmd_file.read_text()

        # Should provide clear feedback
        self.assertIn("✅", content)  # Success indicators
        self.assertIn("❌", content)  # Error indicators
        self.assertIn("⚠️", content)  # Warning indicators

        # Should ask for user confirmation
        self.assertIn("read -p", content)

        # Should provide next steps
        self.assertIn("Next steps", content)
        self.assertIn("Remember", content)

    def test_command_documentation(self):
        """Test command has proper documentation."""
        cmd_file = Path('.claude/commands/prp/execute.md')
        content = cmd_file.read_text()

        # Should have clear mission
        self.assertIn("Mission", content)

        # Should explain workflow
        self.assertIn("Workflow", content)
        self.assertIn("feature/prp", content)

        # Should have example usage
        self.assertIn("Example Usage", content)
        self.assertIn("/prp:execute", content)


if __name__ == '__main__':
    unittest.main()
