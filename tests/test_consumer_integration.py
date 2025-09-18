#!/usr/bin/env python3
"""
Integration tests for consumer project workflow.

Tests the full end-to-end experience of installing and using cc-boilerplate
in a consumer project, including:
- Initial setup and git subtree installation
- Configuration building
- Version management
- Real-world usage scenarios

These tests catch issues that unit tests miss by simulating the actual
user experience in a temporary project directory.
"""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path
import json
import pytest


class TestConsumerIntegration:
    """Test the full consumer project integration workflow."""

    def setup_method(self):
        """Create a temporary project directory for each test."""
        self.test_dir = tempfile.mkdtemp(prefix="cc_boilerplate_test_")
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Initialize a git repository
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], check=True)

        # Create initial commit
        Path("README.md").write_text("# Test Project\n")
        subprocess.run(["git", "add", "README.md"], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)

    def teardown_method(self):
        """Clean up temporary directory."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_init_script_creates_proper_structure(self):
        """Test that init script creates the expected directory structure."""
        # Get the path to our init script
        script_path = Path(self.original_cwd) / "scripts" / "init-boilerplate.sh"

        # Run the init script in non-interactive mode
        env = os.environ.copy()
        env["INTERACTIVE"] = "false"

        result = subprocess.run(
            ["bash", str(script_path)],
            env=env,
            capture_output=True,
            text=True,
            input="\n\n"  # Accept defaults
        )

        # Check that the script succeeded
        if result.returncode != 0:
            pytest.fail(f"Init script failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")

        # Verify expected directory structure
        assert Path(".claude/boilerplate").is_dir(), "Boilerplate directory not created"
        assert Path(".claude/project").is_dir(), "Project directory not created"
        assert Path(".boilerplate-version").is_file(), "Version file not created"

        # Verify key boilerplate files exist
        assert Path(".claude/boilerplate/.claude/settings.template.json").is_file(), \
            "Settings template not found in expected location"
        assert Path(".claude/boilerplate/templates/CLAUDE.template.md").is_file(), \
            "CLAUDE template not found in expected location"

    def test_config_builder_works_after_init(self):
        """Test that config builder works after boilerplate installation."""
        # First run init
        script_path = Path(self.original_cwd) / "scripts" / "init-boilerplate.sh"
        env = os.environ.copy()
        env["INTERACTIVE"] = "false"

        init_result = subprocess.run(
            ["bash", str(script_path)],
            env=env,
            capture_output=True,
            text=True
        )

        if init_result.returncode != 0:
            pytest.skip(f"Init failed, skipping config test: {init_result.stderr}")

        # Now test config builder
        config_script = Path(".claude/boilerplate/scripts/build-config.sh")
        if not config_script.exists():
            pytest.skip("Config script not found in boilerplate")

        config_result = subprocess.run(
            ["bash", str(config_script)],
            capture_output=True,
            text=True
        )

        # Check that config build succeeded
        if config_result.returncode != 0:
            pytest.fail(f"Config build failed:\nSTDOUT:\n{config_result.stdout}\nSTDERR:\n{config_result.stderr}")

        # Verify output files were created
        assert Path(".claude/settings.json").is_file(), "Settings file not created"
        assert Path("CLAUDE.md").is_file(), "CLAUDE.md not created"

    def test_latest_tag_detection(self):
        """Test that the init script uses latest tag instead of main."""
        script_path = Path(self.original_cwd) / "scripts" / "init-boilerplate.sh"

        # Run init script and capture output
        env = os.environ.copy()
        env["INTERACTIVE"] = "false"

        result = subprocess.run(
            ["bash", str(script_path)],
            env=env,
            capture_output=True,
            text=True
        )

        # Check that output mentions a version tag, not "main"
        output = result.stdout + result.stderr
        assert "v1.3" in output or "latest stable" in output, \
            f"Expected version tag in output, got: {output}"
        assert "Branch: main" not in output, \
            f"Should not use main branch, got: {output}"

    def test_uncommitted_changes_handling(self):
        """Test that init script handles uncommitted changes gracefully."""
        # Create uncommitted changes
        Path("uncommitted.txt").write_text("test content")
        Path("README.md").write_text("# Modified README\nUncommitted change")

        # Run init script
        script_path = Path(self.original_cwd) / "scripts" / "init-boilerplate.sh"
        env = os.environ.copy()
        env["INTERACTIVE"] = "false"

        result = subprocess.run(
            ["bash", str(script_path)],
            env=env,
            capture_output=True,
            text=True
        )

        # Check that script succeeded despite uncommitted changes
        if result.returncode != 0:
            pytest.fail(f"Init failed with uncommitted changes:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")

        # Verify our uncommitted changes are still there
        assert Path("uncommitted.txt").exists(), "Uncommitted file was lost"
        readme_content = Path("README.md").read_text()
        assert "Modified README" in readme_content, "Uncommitted changes were lost"

    def test_version_file_format(self):
        """Test that version file is created with correct format."""
        script_path = Path(self.original_cwd) / "scripts" / "init-boilerplate.sh"
        env = os.environ.copy()
        env["INTERACTIVE"] = "false"

        result = subprocess.run(
            ["bash", str(script_path)],
            env=env,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            pytest.skip(f"Init failed: {result.stderr}")

        # Check version file format
        version_file = Path(".boilerplate-version")
        assert version_file.exists(), "Version file not created"

        version_data = json.loads(version_file.read_text())

        # Verify required fields
        required_fields = ["version", "commit", "date", "branch", "repository", "initialized_at"]
        for field in required_fields:
            assert field in version_data, f"Missing required field: {field}"

        # Verify version format (should be tag, not commit hash)
        version = version_data["version"]
        assert version.startswith("v") and "." in version, \
            f"Version should be tag format (v1.2.3), got: {version}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])