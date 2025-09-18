#!/usr/bin/env python3
"""
Security Boundaries Tests - Priority 2 High Risk Coverage

Tests the security boundary enforcement introduced in PRP-004:
- Tool permission validation
- Security chain enforcement
- Unauthorized access detection

Following KISS/YAGNI: Test ONE security boundary per test,
focus on critical security failures that could compromise safety.
"""

import os
import sys
import unittest
import tempfile
import yaml
import importlib.util
from pathlib import Path
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Add .claude directories to path for importing the modules
claude_agents_config = Path(__file__).parent.parent / ".claude" / "agents" / "config"
claude_hooks_utils = Path(__file__).parent.parent / ".claude" / "hooks" / "utils"
if str(claude_agents_config) not in sys.path:
    sys.path.insert(0, str(claude_agents_config))
if str(claude_hooks_utils) not in sys.path:
    sys.path.insert(0, str(claude_hooks_utils))

from test_base import IsolatedTestCase


class TestToolPermissionEnforcement(IsolatedTestCase):
    """Test tool permission boundary enforcement."""

    def setUp(self):
        """Set up test environment with tool permissions config."""
        super().setUp()

        # Create mock config directory
        self.config_dir = self.test_dir / ".claude" / "agents" / "config"
        self.config_dir.mkdir(parents=True)

        # Mock tool permissions with different security levels
        self.tool_permissions = {
            "security_levels": {
                "read_only": {
                    "description": "Analysis agents that cannot modify any files",
                    "tools_allowed": ["Read", "Grep", "Glob", "Task"],
                    "tools_forbidden": ["Write", "Edit", "MultiEdit", "Bash"]
                },
                "write_limited": {
                    "description": "Agents that can create/modify files with restrictions",
                    "tools_allowed": ["Read", "Write", "Edit", "Task"],
                    "tools_forbidden": ["Bash"]
                },
                "full_access": {
                    "description": "Orchestrators with full capabilities",
                    "tools_allowed": ["*"],
                    "tools_forbidden": []
                }
            },
            "agent_permissions": {
                "code-reviewer": {
                    "security_level": "read_only",
                    "specific_tools": ["Read", "Grep", "Task"]
                },
                "test-automator": {
                    "security_level": "write_limited",
                    "specific_tools": ["Read", "Write", "Edit", "Task"]
                },
                "workflow-orchestrator": {
                    "security_level": "full_access",
                    "specific_tools": ["*"]
                },
                "security-scanner": {
                    "security_level": "read_only",
                    "specific_tools": ["Read", "Grep", "Bash(security:*)"]
                }
            }
        }

        # Write tool permissions config
        with open(self.config_dir / "tool-permissions.yaml", 'w') as f:
            yaml.dump(self.tool_permissions, f)

    def test_tool_permission_validation_read_only_agent(self):
        """Test read-only agent cannot access forbidden tools."""
        # Test that code-reviewer (read-only) cannot use Write tool
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.config_dir.parent.parent)

        # Simulate checking an agent with unauthorized tools
        agent_name = "code-reviewer"
        tools = ["Read", "Write"]  # Write is forbidden for read-only
        frontmatter = {
            "name": agent_name,
            "tools": tools,
            "model": "sonnet"
        }

        # Create a mock agent file to test tool allocation
        mock_file = Path("test-agent.md")
        checker._check_tool_allocation(mock_file, agent_name, frontmatter)

        # Should have error for unauthorized tool
        self.assertGreater(len(checker.errors), 0)
        error_text = " ".join(checker.errors)
        self.assertIn("not in allowed list", error_text)

    def test_tool_permission_validation_write_limited_agent(self):
        """Test write-limited agent can access allowed tools but not forbidden ones."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.config_dir.parent.parent)

        # Test allowed tools for test-automator
        agent_name = "test-automator"
        allowed_tools = ["Read", "Write", "Edit", "Task"]
        frontmatter = {
            "name": agent_name,
            "tools": allowed_tools,
            "model": "sonnet"
        }

        mock_file = Path("test-agent.md")
        checker._check_tool_allocation(mock_file, agent_name, frontmatter)

        # Should have no errors for allowed tools
        tool_errors = [e for e in checker.errors if "not in allowed list" in e]
        self.assertEqual(len(tool_errors), 0)

    def test_tool_permission_validation_forbidden_tool(self):
        """Test agent using forbidden tool is detected."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.config_dir.parent.parent)

        # Test forbidden tool for test-automator (Bash not allowed)
        agent_name = "test-automator"
        forbidden_tools = ["Read", "Bash"]  # Bash is forbidden for write_limited
        frontmatter = {
            "name": agent_name,
            "tools": forbidden_tools,
            "model": "sonnet"
        }

        mock_file = Path("test-agent.md")
        checker._check_tool_allocation(mock_file, agent_name, frontmatter)

        # Should have error for forbidden tool
        self.assertGreater(len(checker.errors), 0)
        error_text = " ".join(checker.errors)
        self.assertIn("not in allowed list", error_text)

    def test_tool_permission_validation_full_access_agent(self):
        """Test full access agent can use any tools."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.config_dir.parent.parent)

        # Test full access for workflow-orchestrator
        agent_name = "workflow-orchestrator"
        any_tools = ["Read", "Write", "Edit", "Bash", "Task"]
        frontmatter = {
            "name": agent_name,
            "tools": any_tools,
            "model": "opus"
        }

        mock_file = Path("test-agent.md")
        checker._check_tool_allocation(mock_file, agent_name, frontmatter)

        # Should have no errors for full access agent
        tool_errors = [e for e in checker.errors if "not in allowed list" in e]
        self.assertEqual(len(tool_errors), 0)

    def test_tool_permission_pattern_matching(self):
        """Test tool permission pattern matching (e.g., Bash(security:*))."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.config_dir.parent.parent)

        # Test pattern matching for security-scanner
        self.assertTrue(checker._tool_matches_pattern("Bash(security:scan)", "Bash(security:*)"))
        self.assertTrue(checker._tool_matches_pattern("Read", "Read"))
        self.assertFalse(checker._tool_matches_pattern("Bash(rm:*)", "Bash(security:*)"))
        self.assertFalse(checker._tool_matches_pattern("Write", "Read"))

    def test_tool_count_validation_haiku_model(self):
        """Test tool count validation for Haiku model (≤3 tools)."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.config_dir.parent.parent)

        # Test Haiku model with too many tools
        agent_name = "test-haiku-agent"
        too_many_tools = ["Read", "Grep", "Glob", "Task"]  # 4 tools > 3 limit
        frontmatter = {
            "name": agent_name,
            "tools": too_many_tools,
            "model": "haiku"
        }

        mock_file = Path("test-agent.md")
        checker._check_tool_allocation(mock_file, agent_name, frontmatter)

        # Should have warning about too many tools
        warning_text = " ".join(checker.warnings)
        self.assertIn("Haiku model should have ≤3 tools", warning_text)

    def test_tool_count_validation_sonnet_model(self):
        """Test tool count validation for Sonnet model (≤7 tools)."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.config_dir.parent.parent)

        # Test Sonnet model with too many tools
        agent_name = "test-sonnet-agent"
        too_many_tools = ["Read", "Write", "Edit", "Grep", "Glob", "Task", "Bash", "MultiEdit"]  # 8 tools > 7 limit
        frontmatter = {
            "name": agent_name,
            "tools": too_many_tools,
            "model": "sonnet"
        }

        mock_file = Path("test-agent.md")
        checker._check_tool_allocation(mock_file, agent_name, frontmatter)

        # Should have warning about too many tools
        warning_text = " ".join(checker.warnings)
        self.assertIn("Sonnet model should have ≤7 tools", warning_text)


class TestSecurityChainEnforcement(IsolatedTestCase):
    """Test mandatory security chain enforcement."""

    def setUp(self):
        """Set up test environment with security chain configurations."""
        super().setUp()

        # Create mock config directory
        self.config_dir = self.test_dir / ".claude" / "agents" / "config"
        self.config_dir.mkdir(parents=True)

        # Mock chain definitions with security validation
        self.chain_definitions = {
            "chains": {
                "security_validation": {
                    "name": "Mandatory Security Validation Chain",
                    "type": "mandatory",
                    "sequence": [
                        {
                            "agent": "code-reviewer",
                            "role": "initial_analysis",
                            "required": True
                        },
                        {
                            "agent": "security-orchestrator",
                            "role": "security_checkpoint",
                            "required": True
                        }
                    ],
                    "triggers": ["code modification"],
                    "validation_rules": ["security_clearance must be approved"]
                },
                "testing_chain": {
                    "name": "Testing Chain",
                    "type": "optional",
                    "sequence": [
                        {
                            "agent": "test-automator",
                            "role": "create_tests"
                        }
                    ]
                }
            }
        }

        # Mock orchestration config
        self.orchestration_config = {
            "categories": {
                "analyzers": {
                    "agents": ["code-reviewer"]
                },
                "orchestrators": {
                    "agents": ["security-orchestrator"]
                },
                "specialists": {
                    "agents": ["test-automator"]
                }
            }
        }

        # Write configs
        with open(self.config_dir / "chain-definitions.yaml", 'w') as f:
            yaml.dump(self.chain_definitions, f)
        with open(self.config_dir / "agent-orchestration.yaml", 'w') as f:
            yaml.dump(self.orchestration_config, f)
        with open(self.config_dir / "tool-permissions.yaml", 'w') as f:
            yaml.dump({}, f)

    def test_security_validation_chain_exists(self):
        """Test that mandatory security validation chain exists."""
        try:
            from validate_chains import ChainValidator
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("validate_chains", claude_hooks_utils / "validate-chains.py")
            validate_chains_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(validate_chains_module)
            ChainValidator = validate_chains_module.ChainValidator

        validator = ChainValidator(self.config_dir.parent.parent)
        validator._validate_security_requirements()

        # Should pass - security_validation chain exists
        security_errors = [e for e in validator.errors if "security_validation" in e]
        self.assertEqual(len(security_errors), 0)

    def test_security_validation_chain_missing(self):
        """Test detection when mandatory security chain is missing."""
        # Remove security_validation chain
        bad_config = {
            "chains": {
                "testing_chain": {
                    "name": "Testing Chain",
                    "type": "optional",
                    "sequence": []
                }
            }
        }

        with open(self.config_dir / "chain-definitions.yaml", 'w') as f:
            yaml.dump(bad_config, f)

        try:
            from validate_chains import ChainValidator
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("validate_chains", claude_hooks_utils / "validate-chains.py")
            validate_chains_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(validate_chains_module)
            ChainValidator = validate_chains_module.ChainValidator
        validator = ChainValidator(self.config_dir.parent.parent)
        validator._validate_security_requirements()

        # Should fail - missing security_validation chain
        self.assertGreater(len(validator.errors), 0)
        self.assertIn("Missing 'security_validation' chain", " ".join(validator.errors))

    def test_security_chain_missing_required_agents(self):
        """Test detection when security chain is missing required agents."""
        # Create security chain without required agents
        bad_security_config = {
            "chains": {
                "security_validation": {
                    "name": "Incomplete Security Chain",
                    "type": "mandatory",
                    "sequence": [
                        {
                            "agent": "code-reviewer",
                            "role": "initial_analysis"
                        }
                        # Missing: security-orchestrator
                    ]
                }
            }
        }

        with open(self.config_dir / "chain-definitions.yaml", 'w') as f:
            yaml.dump(bad_security_config, f)

        try:
            from validate_chains import ChainValidator
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("validate_chains", claude_hooks_utils / "validate-chains.py")
            validate_chains_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(validate_chains_module)
            ChainValidator = validate_chains_module.ChainValidator
        validator = ChainValidator(self.config_dir.parent.parent)
        validator._validate_security_requirements()

        # Should fail - missing security-orchestrator
        self.assertGreater(len(validator.errors), 0)
        self.assertIn("missing required agent: 'security-orchestrator'", " ".join(validator.errors))

    def test_security_orchestrator_must_be_required(self):
        """Test that security-orchestrator must be marked as required."""
        # Create security chain with security-orchestrator not required
        bad_config = {
            "chains": {
                "security_validation": {
                    "name": "Security Chain",
                    "type": "mandatory",
                    "sequence": [
                        {
                            "agent": "code-reviewer",
                            "role": "initial_analysis",
                            "required": True
                        },
                        {
                            "agent": "security-orchestrator",
                            "role": "security_checkpoint",
                            "required": False  # Should be True
                        }
                    ]
                }
            }
        }

        with open(self.config_dir / "chain-definitions.yaml", 'w') as f:
            yaml.dump(bad_config, f)

        try:
            from validate_chains import ChainValidator
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("validate_chains", claude_hooks_utils / "validate-chains.py")
            validate_chains_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(validate_chains_module)
            ChainValidator = validate_chains_module.ChainValidator
        validator = ChainValidator(self.config_dir.parent.parent)
        validator._validate_security_requirements()

        # Should fail - security-orchestrator must be required
        self.assertGreater(len(validator.errors), 0)
        self.assertIn("security-orchestrator must be marked as required", " ".join(validator.errors))

    def test_code_reviewer_handoff_to_security_orchestrator(self):
        """Test that code-reviewer must hand off to security-orchestrator."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        # Create mock agent directory structure
        agents_dir = self.config_dir.parent
        analyzers_dir = agents_dir / "analyzers"
        analyzers_dir.mkdir(parents=True)

        # Create code-reviewer agent without security handoff
        bad_agent_content = """---
name: code-reviewer
description: "ALWAYS use when: code review needed\nNEVER use when: no code changes\nRuns AFTER: None\nHands off to: test-coverage-analyzer"
model: sonnet
---

# Code Reviewer
"""

        agent_file = analyzers_dir / "code-reviewer.md"
        with open(agent_file, 'w') as f:
            f.write(bad_agent_content)

        checker = AgentComplianceChecker(self.config_dir.parent.parent)
        checker._check_agent_file(agent_file)

        # Should fail - code-reviewer must hand off to security-orchestrator
        self.assertGreater(len(checker.errors), 0)
        self.assertIn("Must hand off to security-orchestrator", " ".join(checker.errors))

    def test_code_reviewer_with_correct_security_handoff(self):
        """Test that code-reviewer with security handoff passes validation."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        # Create mock agent directory structure
        agents_dir = self.config_dir.parent
        analyzers_dir = agents_dir / "analyzers"
        analyzers_dir.mkdir(parents=True)

        # Create code-reviewer agent with correct security handoff
        good_agent_content = """---
name: code-reviewer
description: "ALWAYS use when: code review needed\nNEVER use when: no code changes\nRuns AFTER: None\nHands off to: security-orchestrator"
model: sonnet
---

# Code Reviewer
"""

        agent_file = analyzers_dir / "code-reviewer.md"
        with open(agent_file, 'w') as f:
            f.write(good_agent_content)

        checker = AgentComplianceChecker(self.config_dir.parent.parent)
        checker._check_agent_file(agent_file)

        # Should pass - code-reviewer correctly hands off to security-orchestrator
        security_errors = [e for e in checker.errors if "security-orchestrator" in e]
        self.assertEqual(len(security_errors), 0)


class TestUnauthorizedAccessDetection(IsolatedTestCase):
    """Test detection of unauthorized access attempts."""

    def setUp(self):
        """Set up test environment for unauthorized access detection."""
        super().setUp()

        # Create mock config directory
        self.config_dir = self.test_dir / ".claude" / "agents" / "config"
        self.config_dir.mkdir(parents=True)

        # Create simple tool permissions for testing
        self.tool_permissions = {
            "agent_permissions": {
                "read-only-agent": {
                    "security_level": "read_only",
                    "specific_tools": ["Read", "Grep"]
                }
            }
        }

        with open(self.config_dir / "tool-permissions.yaml", 'w') as f:
            yaml.dump(self.tool_permissions, f)

    def test_unauthorized_tool_access_detected(self):
        """Test detection of agent trying to use unauthorized tools."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.config_dir.parent.parent)

        # Test unauthorized tool usage
        agent_name = "read-only-agent"
        unauthorized_tools = ["Read", "Write", "Bash"]  # Write and Bash not allowed
        frontmatter = {
            "name": agent_name,
            "tools": unauthorized_tools,
            "model": "sonnet"
        }

        mock_file = Path("test-agent.md")
        checker._check_tool_allocation(mock_file, agent_name, frontmatter)

        # Should detect unauthorized tools
        self.assertGreater(len(checker.errors), 0)
        error_text = " ".join(checker.errors)
        self.assertIn("not in allowed list", error_text)

    def test_tool_pattern_bypass_attempt_detected(self):
        """Test detection of attempts to bypass tool restrictions with patterns."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.config_dir.parent.parent)

        # Test if agent tries to use pattern that doesn't match allowed patterns
        agent_name = "read-only-agent"
        bypass_tools = ["Read", "Bash(security:scan)"]  # Bash pattern not in allowed list
        frontmatter = {
            "name": agent_name,
            "tools": bypass_tools,
            "model": "sonnet"
        }

        mock_file = Path("test-agent.md")
        checker._check_tool_allocation(mock_file, agent_name, frontmatter)

        # Should detect unauthorized pattern usage
        self.assertGreater(len(checker.errors), 0)
        error_text = " ".join(checker.errors)
        self.assertIn("not in allowed list", error_text)

    def test_missing_agent_permissions_handled(self):
        """Test handling of agent not defined in permissions matrix."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.config_dir.parent.parent)

        # Test agent not in permissions matrix
        agent_name = "undefined-agent"
        tools = ["Read", "Task"]
        frontmatter = {
            "name": agent_name,
            "tools": tools,
            "model": "sonnet"
        }

        mock_file = Path("test-agent.md")

        # This should not crash - undefined agents should be handled gracefully
        try:
            checker._check_tool_allocation(mock_file, agent_name, frontmatter)
            # Test passes if no exception is thrown
        except Exception as e:
            self.fail(f"Should handle undefined agent gracefully, but got: {e}")

    def test_empty_tools_list_handled(self):
        """Test handling of agent with empty tools list."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.config_dir.parent.parent)

        # Test agent with no tools specified
        agent_name = "read-only-agent"
        frontmatter = {
            "name": agent_name,
            "tools": [],  # Empty tools list
            "model": "sonnet"
        }

        mock_file = Path("test-agent.md")

        # Should handle empty tools gracefully (some agents might not specify tools)
        try:
            checker._check_tool_allocation(mock_file, agent_name, frontmatter)
            # Test passes if no exception is thrown
        except Exception as e:
            self.fail(f"Should handle empty tools gracefully, but got: {e}")

    def test_string_tools_format_handled(self):
        """Test handling of tools specified as comma-separated string."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.config_dir.parent.parent)

        # Test tools as string format
        agent_name = "read-only-agent"
        frontmatter = {
            "name": agent_name,
            "tools": "Read, Grep",  # String format instead of list
            "model": "sonnet"
        }

        mock_file = Path("test-agent.md")

        # Should handle string format correctly
        try:
            checker._check_tool_allocation(mock_file, agent_name, frontmatter)
            # Should not have errors for allowed tools in string format
            tool_errors = [e for e in checker.errors if "not in allowed list" in e]
            self.assertEqual(len(tool_errors), 0)
        except Exception as e:
            self.fail(f"Should handle string tools format, but got: {e}")


if __name__ == '__main__':
    unittest.main()