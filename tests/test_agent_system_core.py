#!/usr/bin/env python3
"""
Agent System Core Tests - Priority 1 Critical Coverage

Tests the core agent system functionality introduced in PRP-004:
- Chain executor basic operations
- Agent compliance checking
- Chain validation logic

Following KISS/YAGNI: Test ONE behavior per test, use simple mocks,
focus on current implementation without over-engineering.
"""

import os
import sys
import unittest
import tempfile
import yaml
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


class TestChainExecutor(IsolatedTestCase):
    """Test chain executor core functionality."""

    def setUp(self):
        """Set up test environment with mock configs."""
        super().setUp()

        # Create mock config directory structure
        self.config_dir = self.test_dir / ".claude" / "agents" / "config"
        self.config_dir.mkdir(parents=True)

        # Mock chain definitions
        self.chain_config = {
            "chains": {
                "test_chain": {
                    "name": "Test Chain",
                    "description": "A test chain",
                    "type": "mandatory",
                    "sequence": [
                        {
                            "agent": "test-agent",
                            "role": "test_role",
                            "required": True,
                            "timeout_minutes": 5
                        }
                    ],
                    "validation_rules": ["test rule"]
                }
            }
        }

        # Mock orchestration config
        self.orchestration_config = {
            "orchestrators": {"test-orchestrator": {}},
            "categories": {
                "specialists": {
                    "agents": ["test-agent", "security-scanner"]
                }
            }
        }

        # Mock tool permissions
        self.tool_permissions = {
            "agent_permissions": {
                "test-agent": {
                    "security_level": "read_only",
                    "specific_tools": ["Read", "Task"]
                }
            }
        }

        # Write mock config files
        with open(self.config_dir / "chain-definitions.yaml", 'w') as f:
            yaml.dump(self.chain_config, f)
        with open(self.config_dir / "agent-orchestration.yaml", 'w') as f:
            yaml.dump(self.orchestration_config, f)
        with open(self.config_dir / "tool-permissions.yaml", 'w') as f:
            yaml.dump(self.tool_permissions, f)

    def test_chain_executor_initialization(self):
        """Test ChainExecutor initializes with config files."""
        # Import here to avoid circular imports
        try:
            from chain_executor import ChainExecutor
        except ImportError:
            # Try importing with full path
            import importlib.util
            spec = importlib.util.spec_from_file_location("chain_executor", claude_agents_config / "chain-executor.py")
            chain_executor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chain_executor_module)
            ChainExecutor = chain_executor_module.ChainExecutor

        executor = ChainExecutor(self.config_dir)

        # Verify configurations loaded
        self.assertIn("test_chain", executor.chain_definitions.get("chains", {}))
        self.assertIn("test-agent", executor._get_all_agents())
        self.assertEqual(len(executor.active_executions), 0)

    def test_validate_chain_definition_valid_chain(self):
        """Test validation passes for valid chain definition."""
        try:
            from chain_executor import ChainExecutor
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("chain_executor", claude_agents_config / "chain-executor.py")
            chain_executor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chain_executor_module)
            ChainExecutor = chain_executor_module.ChainExecutor

        executor = ChainExecutor(self.config_dir)
        result = executor.validate_chain_definition("test_chain")

        # Should have no errors for valid chain
        self.assertEqual(len(result["errors"]), 0)
        self.assertIsInstance(result["warnings"], list)

    def test_validate_chain_definition_missing_chain(self):
        """Test validation fails for non-existent chain."""
        try:
            from chain_executor import ChainExecutor
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("chain_executor", claude_agents_config / "chain-executor.py")
            chain_executor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chain_executor_module)
            ChainExecutor = chain_executor_module.ChainExecutor

        executor = ChainExecutor(self.config_dir)
        result = executor.validate_chain_definition("nonexistent_chain")

        # Should have error for missing chain
        self.assertGreater(len(result["errors"]), 0)
        self.assertIn("not found in definitions", result["errors"][0])

    def test_validate_chain_definition_missing_required_fields(self):
        """Test validation catches missing required fields."""
        # Create chain with missing fields
        bad_chain_config = {
            "chains": {
                "bad_chain": {
                    "name": "Bad Chain"
                    # Missing: description, type, sequence
                }
            }
        }

        with open(self.config_dir / "chain-definitions.yaml", 'w') as f:
            yaml.dump(bad_chain_config, f)

        try:
            from chain_executor import ChainExecutor
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("chain_executor", claude_agents_config / "chain-executor.py")
            chain_executor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chain_executor_module)
            ChainExecutor = chain_executor_module.ChainExecutor
        executor = ChainExecutor(self.config_dir)
        result = executor.validate_chain_definition("bad_chain")

        # Should catch missing required fields
        self.assertGreater(len(result["errors"]), 0)
        error_text = " ".join(result["errors"])
        self.assertIn("description", error_text)
        self.assertIn("type", error_text)
        self.assertIn("sequence", error_text)

    def test_validate_chain_sequence_missing_agent_field(self):
        """Test validation catches missing agent field in sequence."""
        # Create chain with bad sequence
        bad_sequence_config = {
            "chains": {
                "bad_sequence": {
                    "name": "Bad Sequence Chain",
                    "description": "Chain with bad sequence",
                    "type": "mandatory",
                    "sequence": [
                        {
                            "role": "test_role"
                            # Missing: agent field
                        }
                    ]
                }
            }
        }

        with open(self.config_dir / "chain-definitions.yaml", 'w') as f:
            yaml.dump(bad_sequence_config, f)

        try:
            from chain_executor import ChainExecutor
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("chain_executor", claude_agents_config / "chain-executor.py")
            chain_executor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chain_executor_module)
            ChainExecutor = chain_executor_module.ChainExecutor
        executor = ChainExecutor(self.config_dir)
        result = executor.validate_chain_definition("bad_sequence")

        # Should catch missing agent field
        self.assertGreater(len(result["errors"]), 0)
        self.assertIn("missing 'agent' field", " ".join(result["errors"]).lower())

    def test_get_all_agents_includes_orchestrators_and_specialists(self):
        """Test _get_all_agents returns agents from all categories."""
        try:
            from chain_executor import ChainExecutor
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("chain_executor", claude_agents_config / "chain-executor.py")
            chain_executor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chain_executor_module)
            ChainExecutor = chain_executor_module.ChainExecutor

        executor = ChainExecutor(self.config_dir)
        all_agents = executor._get_all_agents()

        # Should include orchestrator
        self.assertIn("test-orchestrator", all_agents)
        # Should include specialist agents
        self.assertIn("test-agent", all_agents)
        self.assertIn("security-scanner", all_agents)

    def test_list_available_chains(self):
        """Test listing available chain IDs."""
        try:
            from chain_executor import ChainExecutor
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("chain_executor", claude_agents_config / "chain-executor.py")
            chain_executor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chain_executor_module)
            ChainExecutor = chain_executor_module.ChainExecutor

        executor = ChainExecutor(self.config_dir)
        chains = executor.list_available_chains()

        self.assertIn("test_chain", chains)
        self.assertEqual(len(chains), 1)

    @patch('asyncio.sleep')  # Speed up test by mocking sleep
    async def test_execute_chain_dry_run(self):
        """Test chain execution in dry run mode."""
        try:
            from chain_executor import ChainExecutor
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("chain_executor", claude_agents_config / "chain-executor.py")
            chain_executor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chain_executor_module)
            ChainExecutor = chain_executor_module.ChainExecutor, ChainExecutionStatus

        executor = ChainExecutor(self.config_dir)
        context = {"test_context": "value"}

        execution = await executor.execute_chain("test_chain", context, dry_run=True)

        # Verify execution completed successfully
        self.assertEqual(execution.status, ChainExecutionStatus.COMPLETED)
        self.assertEqual(execution.chain_id, "test_chain")
        self.assertEqual(execution.context, context)
        self.assertEqual(len(execution.agents), 1)

        # Verify agent execution was simulated
        agent_exec = execution.agents[0]
        self.assertEqual(agent_exec.agent_name, "test-agent")
        self.assertEqual(agent_exec.role, "test_role")
        self.assertTrue(agent_exec.outputs.get("simulated", False))

    def test_execute_chain_nonexistent_chain_raises_error(self):
        """Test executing non-existent chain raises ValueError."""
        import asyncio
        try:
            from chain_executor import ChainExecutor
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("chain_executor", claude_agents_config / "chain-executor.py")
            chain_executor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chain_executor_module)
            ChainExecutor = chain_executor_module.ChainExecutor

        executor = ChainExecutor(self.config_dir)

        with self.assertRaises(ValueError) as cm:
            asyncio.run(executor.execute_chain("nonexistent", {}))

        self.assertIn("not found", str(cm.exception))


class TestAgentComplianceChecker(IsolatedTestCase):
    """Test agent compliance checking functionality."""

    def setUp(self):
        """Set up test environment with mock agent files."""
        super().setUp()

        # Create mock .claude directory structure
        self.claude_dir = self.test_dir / ".claude"
        self.agents_dir = self.claude_dir / "agents"
        self.config_dir = self.agents_dir / "config"
        self.specialists_dir = self.agents_dir / "specialists"

        for dir_path in [self.claude_dir, self.agents_dir, self.config_dir, self.specialists_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Mock tool permissions config
        self.tool_permissions = {
            "agent_permissions": {
                "test-agent": {
                    "security_level": "read_only",
                    "specific_tools": ["Read", "Task"]
                }
            }
        }

        # Mock orchestration config
        self.orchestration_config = {
            "categories": {
                "specialists": {
                    "agents": ["test-agent"]
                }
            }
        }

        # Write config files
        with open(self.config_dir / "tool-permissions.yaml", 'w') as f:
            yaml.dump(self.tool_permissions, f)
        with open(self.config_dir / "agent-orchestration.yaml", 'w') as f:
            yaml.dump(self.orchestration_config, f)

    def test_agent_compliance_checker_initialization(self):
        """Test AgentComplianceChecker initializes correctly."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.claude_dir)

        # Verify initialization
        self.assertEqual(checker.claude_dir, self.claude_dir)
        self.assertEqual(len(checker.errors), 0)
        self.assertEqual(len(checker.warnings), 0)

    def test_check_all_agents_no_agents_found(self):
        """Test checking when no agent files exist."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.claude_dir)
        result = checker.check_all_agents()

        # Should fail when no agents found
        self.assertFalse(result)
        self.assertGreater(len(checker.errors), 0)
        self.assertIn("No agent files found", checker.errors[0])

    def test_check_agent_file_valid_frontmatter(self):
        """Test checking agent file with valid frontmatter."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        # Create valid agent file
        agent_content = """---
name: test-agent
description: "ALWAYS use when: testing\nNEVER use when: production\nRuns AFTER: code-reviewer\nHands off to: None (terminal agent)"
model: sonnet
tools: ["Read", "Task"]
---

# Test Agent

This is a test agent.
"""

        agent_file = self.specialists_dir / "test-agent.md"
        with open(agent_file, 'w') as f:
            f.write(agent_content)

        checker = AgentComplianceChecker(self.claude_dir)
        result = checker.check_all_agents()

        # Should pass with valid agent
        self.assertTrue(result)
        self.assertEqual(len(checker.errors), 0)

    def test_check_agent_file_missing_frontmatter(self):
        """Test checking agent file without frontmatter."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        # Create agent file without frontmatter
        agent_content = """# Test Agent

This is a test agent without frontmatter.
"""

        agent_file = self.specialists_dir / "test-agent.md"
        with open(agent_file, 'w') as f:
            f.write(agent_content)

        checker = AgentComplianceChecker(self.claude_dir)
        result = checker.check_all_agents()

        # Should fail due to missing frontmatter
        self.assertFalse(result)
        self.assertGreater(len(checker.errors), 0)
        self.assertIn("Missing or invalid frontmatter", " ".join(checker.errors))

    def test_check_agent_file_missing_required_fields(self):
        """Test checking agent file missing required frontmatter fields."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        # Create agent file with incomplete frontmatter
        agent_content = """---
name: test-agent
# Missing description and model
---

# Test Agent
"""

        agent_file = self.specialists_dir / "test-agent.md"
        with open(agent_file, 'w') as f:
            f.write(agent_content)

        checker = AgentComplianceChecker(self.claude_dir)
        result = checker.check_all_agents()

        # Should fail due to missing required fields
        self.assertFalse(result)
        self.assertGreater(len(checker.errors), 0)
        error_text = " ".join(checker.errors)
        self.assertIn("Missing required field 'description'", error_text)
        self.assertIn("Missing required field 'model'", error_text)

    def test_check_hierarchical_placement_correct_directory(self):
        """Test agent in correct hierarchical directory."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        # security-scanner should be in specialists directory
        agent_content = """---
name: security-scanner
description: "ALWAYS use when: security scan needed"
model: sonnet
---

# Security Scanner
"""

        agent_file = self.specialists_dir / "security-scanner.md"
        with open(agent_file, 'w') as f:
            f.write(agent_content)

        checker = AgentComplianceChecker(self.claude_dir)
        checker._check_agent_file(agent_file)

        # Should pass - security-scanner belongs in specialists
        self.assertEqual(len(checker.errors), 0)

    def test_check_hierarchical_placement_wrong_directory(self):
        """Test agent in wrong hierarchical directory."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        # Create analyzers directory and put security-scanner there (wrong)
        analyzers_dir = self.agents_dir / "analyzers"
        analyzers_dir.mkdir()

        agent_content = """---
name: security-scanner
description: "ALWAYS use when: security scan needed"
model: sonnet
---

# Security Scanner
"""

        agent_file = analyzers_dir / "security-scanner.md"
        with open(agent_file, 'w') as f:
            f.write(agent_content)

        checker = AgentComplianceChecker(self.claude_dir)
        checker._check_agent_file(agent_file)

        # Should fail - security-scanner should be in specialists, not analyzers
        self.assertGreater(len(checker.errors), 0)
        self.assertIn("Should be in specialists/ directory", " ".join(checker.errors))

    def test_generate_report_no_issues(self):
        """Test report generation when no issues found."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.claude_dir)
        report = checker.generate_report()

        self.assertIn("All agents are compliant", report)

    def test_generate_report_with_errors(self):
        """Test report generation with errors and warnings."""
        try:
            from agent_compliance_checker import AgentComplianceChecker
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_compliance_checker", claude_hooks_utils / "agent-compliance-checker.py")
            agent_compliance_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_compliance_module)
            AgentComplianceChecker = agent_compliance_module.AgentComplianceChecker

        checker = AgentComplianceChecker(self.claude_dir)
        checker.errors.append("Test error")
        checker.warnings.append("Test warning")

        report = checker.generate_report()

        self.assertIn("Errors: 1", report)
        self.assertIn("Warnings: 1", report)
        self.assertIn("Test error", report)
        self.assertIn("Test warning", report)


class TestChainValidator(IsolatedTestCase):
    """Test chain validation functionality."""

    def setUp(self):
        """Set up test environment with mock chain configs."""
        super().setUp()

        # Create mock config directory structure
        self.claude_dir = self.test_dir / ".claude"
        self.config_dir = self.claude_dir / "agents" / "config"
        self.config_dir.mkdir(parents=True)

        # Mock configs - basic valid setup
        self.chain_definitions = {
            "chains": {
                "test_chain": {
                    "name": "Test Chain",
                    "description": "A test chain",
                    "type": "mandatory",
                    "sequence": [
                        {
                            "agent": "code-reviewer",
                            "role": "review",
                            "required": True
                        }
                    ],
                    "triggers": ["code modification", "dependency changes", "production deployment"],
                    "validation_rules": ["security_clearance must be approved"]
                },
                "security_validation": {
                    "name": "Security Validation Chain",
                    "description": "Mandatory security validation",
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
                }
            }
        }

        self.agent_orchestration = {
            "categories": {
                "analyzers": {
                    "agents": ["code-reviewer"]
                },
                "orchestrators": {
                    "agents": ["security-orchestrator"]
                }
            }
        }

        # Write configs
        with open(self.config_dir / "chain-definitions.yaml", 'w') as f:
            yaml.dump(self.chain_definitions, f)
        with open(self.config_dir / "agent-orchestration.yaml", 'w') as f:
            yaml.dump(self.agent_orchestration, f)
        with open(self.config_dir / "tool-permissions.yaml", 'w') as f:
            yaml.dump({}, f)  # Empty but valid

    def test_chain_validator_initialization(self):
        """Test ChainValidator initializes correctly."""
        try:
            from validate_chains import ChainValidator
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("validate_chains", claude_hooks_utils / "validate-chains.py")
            validate_chains_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(validate_chains_module)
            ChainValidator = validate_chains_module.ChainValidator

        validator = ChainValidator(self.claude_dir)

        # Verify configurations loaded
        self.assertIn("test_chain", validator.chain_definitions.get("chains", {}))
        self.assertEqual(len(validator.errors), 0)

    def test_validate_all_chains_valid_setup(self):
        """Test validation passes for valid chain setup."""
        try:
            from validate_chains import ChainValidator
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("validate_chains", claude_hooks_utils / "validate-chains.py")
            validate_chains_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(validate_chains_module)
            ChainValidator = validate_chains_module.ChainValidator

        validator = ChainValidator(self.claude_dir)
        result = validator.validate_all_chains()

        # Should pass with valid setup
        self.assertTrue(result)
        self.assertEqual(len(validator.errors), 0)

    def test_validate_chain_missing_required_fields(self):
        """Test validation catches missing required chain fields."""
        # Create invalid chain config
        bad_config = {
            "chains": {
                "bad_chain": {
                    "name": "Bad Chain"
                    # Missing: description, type, sequence
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
        validator = ChainValidator(self.claude_dir)
        result = validator.validate_all_chains()

        # Should fail with errors
        self.assertFalse(result)
        self.assertGreater(len(validator.errors), 0)
        error_text = " ".join(validator.errors)
        self.assertIn("Missing required field", error_text)

    def test_validate_chain_invalid_type(self):
        """Test validation catches invalid chain type."""
        # Create chain with invalid type
        bad_config = {
            "chains": {
                "bad_type_chain": {
                    "name": "Bad Type Chain",
                    "description": "Chain with invalid type",
                    "type": "invalid_type",  # Should be mandatory/optional/auto_trigger/manual_trigger
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
        validator = ChainValidator(self.claude_dir)
        result = validator.validate_all_chains()

        # Should fail with type error
        self.assertFalse(result)
        self.assertGreater(len(validator.errors), 0)
        self.assertIn("Invalid type 'invalid_type'", " ".join(validator.errors))

    def test_validate_chain_sequence_empty(self):
        """Test validation catches empty sequence."""
        # Create chain with empty sequence
        bad_config = {
            "chains": {
                "empty_sequence": {
                    "name": "Empty Sequence Chain",
                    "description": "Chain with empty sequence",
                    "type": "mandatory",
                    "sequence": []  # Empty sequence
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
        validator = ChainValidator(self.claude_dir)
        result = validator.validate_all_chains()

        # Should fail with sequence error
        self.assertFalse(result)
        self.assertGreater(len(validator.errors), 0)
        self.assertIn("Empty sequence", " ".join(validator.errors))

    def test_validate_chain_sequence_nonexistent_agent(self):
        """Test validation catches reference to non-existent agent."""
        # Create chain referencing non-existent agent
        bad_config = {
            "chains": {
                "nonexistent_agent": {
                    "name": "Non-existent Agent Chain",
                    "description": "Chain referencing non-existent agent",
                    "type": "mandatory",
                    "sequence": [
                        {
                            "agent": "non-existent-agent",
                            "role": "test"
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
        validator = ChainValidator(self.claude_dir)
        result = validator.validate_all_chains()

        # Should fail with agent not found error
        self.assertFalse(result)
        self.assertGreater(len(validator.errors), 0)
        self.assertIn("not found in orchestration config", " ".join(validator.errors))

    def test_generate_report_no_issues(self):
        """Test report generation when validation passes."""
        try:
            from validate_chains import ChainValidator
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("validate_chains", claude_hooks_utils / "validate-chains.py")
            validate_chains_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(validate_chains_module)
            ChainValidator = validate_chains_module.ChainValidator

        validator = ChainValidator(self.claude_dir)
        validator.validate_all_chains()
        report = validator.generate_report()

        self.assertIn("All chain configurations are valid", report)

    def test_generate_report_with_issues(self):
        """Test report generation with validation issues."""
        try:
            from validate_chains import ChainValidator
        except ImportError:
            import importlib.util
            spec = importlib.util.spec_from_file_location("validate_chains", claude_hooks_utils / "validate-chains.py")
            validate_chains_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(validate_chains_module)
            ChainValidator = validate_chains_module.ChainValidator

        validator = ChainValidator(self.claude_dir)
        validator.errors.append("Test error")
        validator.warnings.append("Test warning")

        report = validator.generate_report()

        self.assertIn("Errors: 1", report)
        self.assertIn("Warnings: 1", report)
        self.assertIn("Test error", report)
        self.assertIn("Test warning", report)


if __name__ == '__main__':
    unittest.main()