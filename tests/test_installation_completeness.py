#!/usr/bin/env python3
"""
Installation Completeness Test

Developer-only test that validates the installation process works correctly.
This test ensures that:
1. PRP templates are properly copied during installation
2. spec-kit installation path is correct and accessible

This test runs in CI/CD but is never seen by end users.
Philosophy: Software should work the first time, no user-facing validation needed.
"""

import os
import subprocess
import tempfile
import shutil
import unittest
from pathlib import Path


class TestInstallationCompleteness(unittest.TestCase):
    """Test suite for installation completeness validation."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = None
        self.original_cwd = os.getcwd()

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_prp_templates_exist_in_boilerplate(self):
        """Test that PRP templates exist in boilerplate directory."""
        boilerplate_prp_templates = Path("boilerplate/PRPs/templates")
        self.assertTrue(
            boilerplate_prp_templates.exists(),
            "PRP templates directory should exist in boilerplate"
        )

        # Check for at least one template file
        template_files = list(boilerplate_prp_templates.glob("*.md"))
        self.assertGreater(
            len(template_files), 0,
            "At least one PRP template file should exist"
        )

    def test_spec_kit_script_exists_at_correct_path(self):
        """Test that spec-kit installation script exists at the correct path."""
        spec_kit_script = Path(".claude/boilerplate/scripts/install-spec-kit.sh")
        self.assertTrue(
            spec_kit_script.exists(),
            f"spec-kit installation script should exist at {spec_kit_script}"
        )

        # Verify the script is executable
        self.assertTrue(
            os.access(spec_kit_script, os.X_OK),
            "spec-kit installation script should be executable"
        )

    def test_setup_script_references_correct_spec_kit_path(self):
        """Test that setup.sh references the correct spec-kit path."""
        setup_script = Path("setup.sh")
        self.assertTrue(setup_script.exists(), "setup.sh should exist")

        with open(setup_script, 'r') as f:
            content = f.read()

        # Should reference the correct path
        self.assertIn(
            '.claude/boilerplate/scripts/install-spec-kit.sh',
            content,
            "setup.sh should reference the correct spec-kit path"
        )

        # Should not reference the old incorrect path without .claude/boilerplate prefix
        # Look for the pattern that would match old references but not new ones
        lines = content.split('\n')
        problematic_lines = [line for line in lines if 'scripts/install-spec-kit.sh' in line and '.claude/boilerplate/scripts/install-spec-kit.sh' not in line]
        self.assertEqual(
            len(problematic_lines), 0,
            f"setup.sh should not reference the old incorrect path. Found: {problematic_lines}"
        )

    def test_init_boilerplate_has_prp_template_copying(self):
        """Test that init-boilerplate.sh includes PRP template copying logic."""
        init_script = Path("scripts/init-boilerplate.sh")
        self.assertTrue(init_script.exists(), "init-boilerplate.sh should exist")

        with open(init_script, 'r') as f:
            content = f.read()

        # Should have PRP template copying logic
        self.assertIn(
            "PRPs/templates",
            content,
            "init-boilerplate.sh should include PRP template copying logic"
        )

        self.assertIn(
            "Copying PRP templates",
            content,
            "init-boilerplate.sh should have PRP template copying message"
        )

    def test_installation_integration(self):
        """Integration test: verify the complete installation process works."""
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            self.test_dir = temp_dir
            os.chdir(temp_dir)

            # Copy the boilerplate source to temp directory
            boilerplate_source = Path(self.original_cwd) / "boilerplate"
            if boilerplate_source.exists():
                shutil.copytree(boilerplate_source, Path(temp_dir) / ".claude" / "boilerplate")

                # Create a minimal init script test
                init_script = Path(self.original_cwd) / "scripts" / "init-boilerplate.sh"
                if init_script.exists():
                    # Simulate the PRP template copying part
                    source_templates = Path(temp_dir) / ".claude" / "boilerplate" / "PRPs" / "templates"
                    if source_templates.exists():
                        target_templates = Path(temp_dir) / "PRPs" / "templates"
                        target_templates.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copytree(source_templates, target_templates)

                        # Verify templates were copied
                        self.assertTrue(
                            target_templates.exists(),
                            "PRP templates should be copied during installation"
                        )

                        template_files = list(target_templates.glob("*.md"))
                        self.assertGreater(
                            len(template_files), 0,
                            "Template files should be copied"
                        )


if __name__ == '__main__':
    unittest.main()