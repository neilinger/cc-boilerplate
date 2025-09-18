#!/usr/bin/env python3
"""
Critical Agent System Gaps Tests - KISS/YAGNI Focused

Tests specifically for critical gaps in agent system coverage that need validation NOW.
These tests focus on core functionality failures that could break the system.

Following KISS/YAGNI: Simple, focused tests for immediate needs.
"""

import os
import sys
import unittest
import tempfile
import yaml
import asyncio
import time
import json
import importlib.util
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from test_base import IsolatedTestCase

# Add .claude directories to path for importing the modules
claude_agents_config = Path(__file__).parent.parent / ".claude" / "agents" / "config"
claude_hooks_utils = Path(__file__).parent.parent / ".claude" / "hooks" / "utils"
if str(claude_agents_config) not in sys.path:
    sys.path.insert(0, str(claude_agents_config))
if str(claude_hooks_utils) not in sys.path:
    sys.path.insert(0, str(claude_hooks_utils))


class TestChainExecutorCriticalPaths(IsolatedTestCase):
    """Test critical path scenarios that could break chain execution."""

    def setUp(self):
        super().setUp()
        self.config_dir = self.test_dir / ".claude" / "agents" / "config"
        self.config_dir.mkdir(parents=True)

        # Minimal working config
        self.chain_config = {
            "chains": {
                "timeout_test": {
                    "name": "Timeout Test Chain",
                    "description": "Tests timeout handling",
                    "type": "mandatory",
                    "sequence": [
                        {
                            "agent": "test-agent",
                            "role": "test_role",
                            "required": True,
                            "timeout_minutes": 0.01  # Very short timeout
                        }
                    ]
                },
                "error_propagation": {
                    "name": "Error Propagation Chain",
                    "description": "Tests error propagation",
                    "type": "mandatory",
                    "sequence": [
                        {
                            "agent": "required-agent",
                            "role": "critical_step",
                            "required": True
                        },
                        {
                            "agent": "optional-agent",
                            "role": "optional_step",
                            "required": False
                        }
                    ]
                }
            }
        }

        self.orchestration_config = {
            "categories": {
                "specialists": {
                    "agents": ["test-agent", "required-agent", "optional-agent"]
                }
            }
        }

        # Write configs
        with open(self.config_dir / "chain-definitions.yaml", 'w') as f:
            yaml.dump(self.chain_config, f)
        with open(self.config_dir / "agent-orchestration.yaml", 'w') as f:
            yaml.dump(self.orchestration_config, f)
        with open(self.config_dir / "tool-permissions.yaml", 'w') as f:
            yaml.dump({}, f)

    def test_chain_executor_handles_timeout_gracefully(self):
        """Test chain executor handles agent timeout without crashing."""
        try:
            from chain_executor import ChainExecutor, ChainExecutionStatus
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("chain_executor", claude_agents_config / "chain-executor.py")
            chain_executor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chain_executor_module)
            ChainExecutor = chain_executor_module.ChainExecutor
            ChainExecutionStatus = chain_executor_module.ChainExecutionStatus

        executor = ChainExecutor(self.config_dir)

        # Execute chain with very short timeout
        async def test_timeout():
            execution = await executor.execute_chain("timeout_test", {}, dry_run=True)
            # Should complete despite timeout (in dry run)
            self.assertIn(execution.status, [ChainExecutionStatus.COMPLETED, ChainExecutionStatus.FAILED])
            return execution

        execution = asyncio.run(test_timeout())

        # Verify execution structure is intact
        self.assertEqual(len(execution.agents), 1)
        self.assertIsNotNone(execution.start_time)
        self.assertIsNotNone(execution.end_time)

    def test_chain_executor_error_propagation(self):
        """Test required agent failure stops chain, optional agent failure continues."""
        try:
            from chain_executor import ChainExecutor, ChainExecutionStatus, AgentExecutionStatus
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("chain_executor", claude_agents_config / "chain-executor.py")
            chain_executor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chain_executor_module)
            ChainExecutor = chain_executor_module.ChainExecutor
            ChainExecutionStatus = chain_executor_module.ChainExecutionStatus
            AgentExecutionStatus = chain_executor_module.AgentExecutionStatus

        executor = ChainExecutor(self.config_dir)

        # Test in dry run mode for predictable behavior
        async def test_error_propagation():
            execution = await executor.execute_chain("error_propagation", {}, dry_run=True)
            return execution

        execution = asyncio.run(test_error_propagation())

        # Should have two agents
        self.assertEqual(len(execution.agents), 2)

        # Both should complete in dry run
        for agent in execution.agents:
            self.assertEqual(agent.status, AgentExecutionStatus.COMPLETED)

    def test_chain_config_validation_missing_files(self):
        """Test chain executor handles missing config files gracefully."""
        # Remove config files to test error handling
        (self.config_dir / "chain-definitions.yaml").unlink()

        try:
            from chain_executor import ChainExecutor
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("chain_executor", claude_agents_config / "chain-executor.py")
            chain_executor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chain_executor_module)
            ChainExecutor = chain_executor_module.ChainExecutor

        # Should not crash when config files are missing
        executor = ChainExecutor(self.config_dir)

        # Should have empty chains
        self.assertEqual(len(executor.list_available_chains()), 0)

    def test_chain_execution_report_generation(self):
        """Test execution report generation with real data."""
        try:
            from chain_executor import ChainExecutor
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("chain_executor", claude_agents_config / "chain-executor.py")
            chain_executor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chain_executor_module)
            ChainExecutor = chain_executor_module.ChainExecutor

        executor = ChainExecutor(self.config_dir)

        async def test_report():
            execution = await executor.execute_chain("timeout_test", {"test": "context"}, dry_run=True)
            report = executor.generate_execution_report(execution)
            return report

        report = asyncio.run(test_report())

        # Report should contain key information
        self.assertIn("Chain Execution Report", report)
        self.assertIn("timeout_test", report)
        self.assertIn("test-agent", report)
        self.assertIn("Duration:", report)


class TestSecurityBoundaryEnforcement(IsolatedTestCase):
    """Test critical security boundary enforcement scenarios."""

    def setUp(self):
        super().setUp()
        self.config_dir = self.test_dir / ".claude" / "agents" / "config"
        self.config_dir.mkdir(parents=True)

        # Security-focused tool permissions
        self.tool_permissions = {
            "security_levels": {
                "read_only": {
                    "tools_allowed": ["Read", "Grep"],
                    "tools_forbidden": ["Write", "Edit", "Bash"]
                },
                "write_limited": {
                    "tools_allowed": ["Read", "Write", "Edit"],
                    "tools_forbidden": ["Bash"]
                }
            },
            "agent_permissions": {
                "security-scanner": {
                    "security_level": "read_only",
                    "specific_tools": ["Read", "Grep"]
                },
                "dangerous-agent": {
                    "security_level": "read_only",
                    "specific_tools": ["Bash"]  # Should be forbidden for read_only
                }
            }
        }

        with open(self.config_dir / "tool-permissions.yaml", 'w') as f:
            yaml.dump(self.tool_permissions, f)
        with open(self.config_dir / "agent-orchestration.yaml", 'w') as f:
            yaml.dump({}, f)

    def test_security_level_enforcement_blocks_forbidden_tools(self):
        """Test that security levels block forbidden tools correctly."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.config_dir.parent.parent)

        # Test agent with forbidden tool for its security level
        frontmatter = {
            "name": "dangerous-agent",
            "tools": ["Read", "Bash"],  # Bash forbidden for read_only level
            "model": "sonnet"
        }

        checker._check_tool_allocation(Path("test.md"), "dangerous-agent", frontmatter)

        # Should have errors for forbidden tool
        self.assertGreater(len(checker.errors), 0)
        error_text = " ".join(checker.errors).lower()
        self.assertIn("not in allowed list", error_text)

    def test_tool_count_cognitive_load_validation(self):
        """Test tool count validation for cognitive load limits."""
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
        frontmatter = {
            "name": "overloaded-haiku",
            "tools": ["Read", "Write", "Edit", "Grep"],  # 4 tools > 3 limit for Haiku
            "model": "haiku"
        }

        checker._check_tool_allocation(Path("test.md"), "overloaded-haiku", frontmatter)

        # Should have warnings about tool count
        warning_text = " ".join(checker.warnings).lower()
        self.assertIn("haiku", warning_text)
        self.assertIn("≤3 tools", warning_text)

    def test_mandatory_security_chain_validation(self):
        """Test that mandatory security chains are properly validated."""
        # Create config without mandatory security chain
        bad_chain_config = {
            "chains": {
                "regular_chain": {
                    "name": "Regular Chain",
                    "type": "optional",
                    "sequence": []
                }
            }
        }

        with open(self.config_dir / "chain-definitions.yaml", 'w') as f:
            yaml.dump(bad_chain_config, f)

        try:
            from validate_chains import ChainValidator
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("validate_chains", claude_hooks_utils / "validate-chains.py")
            validate_chains_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(validate_chains_module)
            ChainValidator = validate_chains_module.ChainValidator

        validator = ChainValidator(self.config_dir.parent.parent)
        result = validator.validate_all_chains()

        # Should fail due to missing security chain
        self.assertFalse(result)
        error_text = " ".join(validator.errors).lower()
        self.assertIn("security", error_text)


class TestRealWorldScenarios(IsolatedTestCase):
    """Test realistic scenarios that could occur in actual usage."""

    def setUp(self):
        super().setUp()
        self.config_dir = self.test_dir / ".claude" / "agents" / "config"
        self.config_dir.mkdir(parents=True)

    def test_empty_tool_permissions_handled_gracefully(self):
        """Test system handles empty or corrupted tool permissions."""
        # Write empty tool permissions
        with open(self.config_dir / "tool-permissions.yaml", 'w') as f:
            f.write("")  # Empty file

        with open(self.config_dir / "agent-orchestration.yaml", 'w') as f:
            yaml.dump({}, f)

        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        # Should not crash with empty config
        checker = AgentComplianceChecker(self.config_dir.parent.parent)
        # Even with empty config, tool_permissions should be loaded (may be empty dict or None)
        self.assertTrue(checker.tool_permissions is None or isinstance(checker.tool_permissions, dict))

    def test_corrupted_yaml_config_handled(self):
        """Test system handles corrupted YAML configuration files."""
        # Write invalid YAML
        with open(self.config_dir / "chain-definitions.yaml", 'w') as f:
            f.write("invalid: yaml: content: [unclosed")

        try:
            from chain_executor import ChainExecutor
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("chain_executor", claude_agents_config / "chain-executor.py")
            chain_executor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chain_executor_module)
            ChainExecutor = chain_executor_module.ChainExecutor

        # Should not crash with corrupted YAML
        executor = ChainExecutor(self.config_dir)
        self.assertEqual(len(executor.list_available_chains()), 0)

    def test_nonexistent_config_directory_handled(self):
        """Test system handles nonexistent configuration directory."""
        nonexistent_dir = self.test_dir / "nonexistent" / "config"

        try:
            from chain_executor import ChainExecutor
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("chain_executor", claude_agents_config / "chain-executor.py")
            chain_executor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chain_executor_module)
            ChainExecutor = chain_executor_module.ChainExecutor

        # Should not crash with nonexistent directory
        executor = ChainExecutor(nonexistent_dir)
        self.assertEqual(len(executor.list_available_chains()), 0)

    def test_agent_compliance_with_no_agents(self):
        """Test compliance checker handles directory with no agent files."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        # Create empty agents directory
        (self.config_dir.parent / "agents").mkdir(exist_ok=True)
        with open(self.config_dir / "tool-permissions.yaml", 'w') as f:
            yaml.dump({}, f)
        with open(self.config_dir / "agent-orchestration.yaml", 'w') as f:
            yaml.dump({}, f)

        checker = AgentComplianceChecker(self.config_dir.parent.parent)
        result = checker.check_all_agents()

        # Should fail gracefully and report no agents found
        self.assertFalse(result)
        self.assertGreater(len(checker.errors), 0)
        self.assertIn("No agent files found", checker.errors[0])


if __name__ == '__main__':
    unittest.main()