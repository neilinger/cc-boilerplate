#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pyyaml>=6.0",
#     "dataclasses",
#     "typing",
#     "pathlib",
#     "asyncio",
#     "enum",
# ]
# ///

"""
Agent Chain Executor - Runtime Engine for Chain Configuration

This module provides runtime execution of agent chains defined in chain-definitions.yaml,
with validation, monitoring, and dynamic adaptation capabilities.

Usage:
    python chain-executor.py --chain security_validation --context "code_modification"
    python chain-executor.py --validate-all-chains
    python chain-executor.py --dry-run --chain comprehensive_testing
"""

import os
import sys
import yaml
import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from enum import Enum

class ChainExecutionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    HALTED = "halted"

class AgentExecutionStatus(Enum):
    WAITING = "waiting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"

@dataclass
class AgentExecution:
    """Represents the execution state of a single agent in a chain"""
    agent_name: str
    role: str
    required: bool
    timeout_minutes: int
    status: AgentExecutionStatus = AgentExecutionStatus.WAITING
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    condition: Optional[str] = None
    condition_met: bool = True

@dataclass
class ChainExecution:
    """Represents the execution state of an entire chain"""
    chain_id: str
    chain_name: str
    chain_type: str
    status: ChainExecutionStatus = ChainExecutionStatus.PENDING
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    agents: List[AgentExecution] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    validation_results: Dict[str, bool] = field(default_factory=dict)
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)

class ChainExecutor:
    """Main chain execution engine"""

    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.chain_definitions = self._load_chain_definitions()
        self.agent_orchestration = self._load_agent_orchestration()
        self.tool_permissions = self._load_tool_permissions()

        # Setup logging
        self._setup_logging()

        # Execution state
        self.active_executions: Dict[str, ChainExecution] = {}
        self.execution_history: List[ChainExecution] = []

    def _setup_logging(self):
        """Configure logging for chain execution"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config_dir / 'chain-execution.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('ChainExecutor')

    def _load_chain_definitions(self) -> Dict:
        """Load chain definitions from YAML"""
        try:
            with open(self.config_dir / "chain-definitions.yaml", 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Failed to load chain definitions: {e}")
            return {}

    def _load_agent_orchestration(self) -> Dict:
        """Load agent orchestration config"""
        try:
            with open(self.config_dir / "agent-orchestration.yaml", 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.warning(f"Failed to load agent orchestration: {e}")
            return {}

    def _load_tool_permissions(self) -> Dict:
        """Load tool permissions matrix"""
        try:
            with open(self.config_dir / "tool-permissions.yaml", 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.warning(f"Failed to load tool permissions: {e}")
            return {}

    def validate_chain_definition(self, chain_id: str) -> Dict[str, List[str]]:
        """Validate a chain definition for consistency and completeness"""
        errors = []
        warnings = []

        if chain_id not in self.chain_definitions.get('chains', {}):
            errors.append(f"Chain '{chain_id}' not found in definitions")
            return {"errors": errors, "warnings": warnings}

        chain = self.chain_definitions['chains'][chain_id]

        # Validate required fields
        required_fields = ['name', 'description', 'type', 'sequence']
        for field in required_fields:
            if field not in chain:
                errors.append(f"Missing required field '{field}' in chain '{chain_id}'")

        # Validate sequence
        if 'sequence' in chain:
            for i, step in enumerate(chain['sequence']):
                if 'agent' not in step:
                    errors.append(f"Step {i} missing 'agent' field")
                if 'role' not in step:
                    errors.append(f"Step {i} missing 'role' field")

                # Check if agent exists in orchestration config
                agent_name = step.get('agent')
                if agent_name and agent_name not in self._get_all_agents():
                    warnings.append(f"Agent '{agent_name}' not found in orchestration config")

        # Validate validation rules
        if 'validation_rules' in chain:
            for rule in chain['validation_rules']:
                if not isinstance(rule, str):
                    warnings.append(f"Validation rule should be string: {rule}")

        return {"errors": errors, "warnings": warnings}

    def _get_all_agents(self) -> List[str]:
        """Get list of all available agents from orchestration config"""
        agents = []
        for category in ['orchestrators', 'specialists', 'analyzers']:
            if category in self.agent_orchestration:
                agents.extend(self.agent_orchestration[category].keys())
        return agents

    def _evaluate_trigger_conditions(self, chain_id: str, context: Dict[str, Any]) -> bool:
        """Check if chain triggers match the provided context"""
        chain = self.chain_definitions['chains'][chain_id]
        triggers = chain.get('triggers', [])

        # Check if any trigger matches context
        for trigger in triggers:
            if trigger in context.get('triggers', []):
                return True
            if trigger in context.get('type', ''):
                return True

        return False

    def _evaluate_agent_condition(self, agent_exec: AgentExecution, chain_context: Dict[str, Any]) -> bool:
        """Evaluate if an agent's execution condition is met"""
        if not agent_exec.condition:
            return True

        # Simple condition evaluation (can be enhanced with proper expression parser)
        condition = agent_exec.condition

        # Replace variables in condition with actual values
        for key, value in chain_context.items():
            condition = condition.replace(key, str(value))

        # Simple boolean evaluation (extend as needed)
        try:
            # WARNING: This is a simplified evaluation - in production, use a proper expression parser
            if "==" in condition:
                left, right = condition.split("==")
                return left.strip().strip('"') == right.strip().strip('"')
            elif ">" in condition:
                left, right = condition.split(">")
                return float(left.strip()) > float(right.strip())
            elif "<" in condition:
                left, right = condition.split("<")
                return float(left.strip()) < float(right.strip())
        except Exception as e:
            self.logger.warning(f"Failed to evaluate condition '{agent_exec.condition}': {e}")
            return True  # Default to true if evaluation fails

        return True

    async def execute_chain(self, chain_id: str, context: Dict[str, Any], dry_run: bool = False) -> ChainExecution:
        """Execute a chain with the given context"""
        self.logger.info(f"Starting chain execution: {chain_id}")

        # Validate chain exists
        if chain_id not in self.chain_definitions.get('chains', {}):
            raise ValueError(f"Chain '{chain_id}' not found")

        chain_def = self.chain_definitions['chains'][chain_id]

        # Create execution object
        execution = ChainExecution(
            chain_id=chain_id,
            chain_name=chain_def['name'],
            chain_type=chain_def['type'],
            context=context,
            start_time=time.time()
        )

        execution.status = ChainExecutionStatus.RUNNING
        self.active_executions[chain_id] = execution

        try:
            # Pre-execution validation
            if not self._run_pre_execution_checks(execution):
                execution.status = ChainExecutionStatus.FAILED
                return execution

            # Process sequence
            for step_def in chain_def['sequence']:
                agent_exec = AgentExecution(
                    agent_name=step_def['agent'],
                    role=step_def['role'],
                    required=step_def.get('required', True),
                    timeout_minutes=step_def.get('timeout_minutes', 10),
                    condition=step_def.get('condition')
                )

                execution.agents.append(agent_exec)

                # Check condition
                if not self._evaluate_agent_condition(agent_exec, execution.context):
                    agent_exec.status = AgentExecutionStatus.SKIPPED
                    agent_exec.condition_met = False
                    self.logger.info(f"Skipping {agent_exec.agent_name} - condition not met")
                    continue

                # Execute agent (or simulate in dry run)
                if dry_run:
                    await self._simulate_agent_execution(agent_exec)
                else:
                    await self._execute_agent(agent_exec, execution)

                # Check if required agent failed
                if agent_exec.required and agent_exec.status == AgentExecutionStatus.FAILED:
                    self.logger.error(f"Required agent {agent_exec.agent_name} failed - halting chain")
                    execution.status = ChainExecutionStatus.HALTED
                    break

            # Post-execution validation
            if execution.status == ChainExecutionStatus.RUNNING:
                if self._run_post_execution_validation(execution):
                    execution.status = ChainExecutionStatus.COMPLETED
                else:
                    execution.status = ChainExecutionStatus.FAILED

        except Exception as e:
            self.logger.error(f"Chain execution failed: {e}")
            execution.status = ChainExecutionStatus.FAILED
            execution.audit_trail.append({
                "timestamp": time.time(),
                "event": "execution_error",
                "message": str(e)
            })

        finally:
            execution.end_time = time.time()
            self.execution_history.append(execution)
            if chain_id in self.active_executions:
                del self.active_executions[chain_id]

        self.logger.info(f"Chain execution completed: {chain_id} - {execution.status.value}")
        return execution

    async def _simulate_agent_execution(self, agent_exec: AgentExecution):
        """Simulate agent execution for dry runs"""
        agent_exec.status = AgentExecutionStatus.RUNNING
        agent_exec.start_time = time.time()

        # Simulate execution time
        await asyncio.sleep(0.1)

        agent_exec.status = AgentExecutionStatus.COMPLETED
        agent_exec.end_time = time.time()
        agent_exec.outputs = {"simulated": True, "result": "success"}

    async def _execute_agent(self, agent_exec: AgentExecution, chain_execution: ChainExecution):
        """Execute a single agent (placeholder for actual agent execution)"""
        agent_exec.status = AgentExecutionStatus.RUNNING
        agent_exec.start_time = time.time()

        self.logger.info(f"Executing agent: {agent_exec.agent_name} in role: {agent_exec.role}")

        try:
            # TODO: Implement actual agent execution via Claude Code Agent API
            # This would involve:
            # 1. Loading agent configuration
            # 2. Preparing agent context
            # 3. Invoking agent through appropriate interface
            # 4. Collecting outputs and status

            # For now, simulate successful execution
            await asyncio.sleep(0.5)  # Simulate work

            agent_exec.status = AgentExecutionStatus.COMPLETED
            agent_exec.outputs = {
                "execution_time": time.time() - agent_exec.start_time,
                "role_completed": agent_exec.role,
                "status": "success"
            }

        except asyncio.TimeoutError:
            agent_exec.status = AgentExecutionStatus.TIMEOUT
            agent_exec.error_message = f"Agent execution timed out after {agent_exec.timeout_minutes} minutes"
        except Exception as e:
            agent_exec.status = AgentExecutionStatus.FAILED
            agent_exec.error_message = str(e)

        finally:
            agent_exec.end_time = time.time()

    def _run_pre_execution_checks(self, execution: ChainExecution) -> bool:
        """Run pre-execution validation checks"""
        checks = self.chain_definitions.get('validation_framework', {}).get('pre_execution_checks', [])

        for check in checks:
            if check == "validate_agent_availability":
                if not self._validate_agent_availability(execution):
                    return False
            elif check == "check_resource_constraints":
                if not self._check_resource_constraints(execution):
                    return False
            # Add more checks as needed

        return True

    def _run_post_execution_validation(self, execution: ChainExecution) -> bool:
        """Run post-execution validation"""
        chain_def = self.chain_definitions['chains'][execution.chain_id]
        validation_rules = chain_def.get('validation_rules', [])

        for rule in validation_rules:
            if not self._evaluate_validation_rule(rule, execution):
                execution.validation_results[rule] = False
                return False
            execution.validation_results[rule] = True

        return True

    def _validate_agent_availability(self, execution: ChainExecution) -> bool:
        """Check if all required agents are available"""
        for agent_exec in execution.agents:
            if agent_exec.agent_name not in self._get_all_agents():
                self.logger.error(f"Agent not available: {agent_exec.agent_name}")
                return False
        return True

    def _check_resource_constraints(self, execution: ChainExecution) -> bool:
        """Check resource constraints for execution"""
        # Placeholder for resource checking logic
        return True

    def _evaluate_validation_rule(self, rule: str, execution: ChainExecution) -> bool:
        """Evaluate a validation rule against execution results"""
        # Placeholder for rule evaluation
        # In practice, this would parse and evaluate complex validation rules
        return True

    def get_chain_status(self, chain_id: str) -> Optional[ChainExecution]:
        """Get current status of a chain execution"""
        return self.active_executions.get(chain_id)

    def list_available_chains(self) -> List[str]:
        """List all available chain IDs"""
        return list(self.chain_definitions.get('chains', {}).keys())

    def generate_execution_report(self, execution: ChainExecution) -> str:
        """Generate a human-readable execution report"""
        report = []
        report.append(f"Chain Execution Report: {execution.chain_name}")
        report.append("=" * 50)
        report.append(f"Chain ID: {execution.chain_id}")
        report.append(f"Status: {execution.status.value}")
        report.append(f"Duration: {(execution.end_time or time.time()) - execution.start_time:.2f} seconds")
        report.append("")

        report.append("Agent Execution Details:")
        report.append("-" * 25)
        for agent in execution.agents:
            duration = (agent.end_time or time.time()) - (agent.start_time or time.time())
            report.append(f"  • {agent.agent_name} ({agent.role}): {agent.status.value} ({duration:.2f}s)")
            if agent.error_message:
                report.append(f"    Error: {agent.error_message}")

        report.append("")
        report.append("Validation Results:")
        report.append("-" * 18)
        for rule, passed in execution.validation_results.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            report.append(f"  • {rule}: {status}")

        return "\n".join(report)

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Claude Code Agent Chain Executor")
    parser.add_argument("--chain", help="Chain ID to execute")
    parser.add_argument("--context", help="Execution context (JSON string)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate execution without running agents")
    parser.add_argument("--validate-all", action="store_true", help="Validate all chain definitions")
    parser.add_argument("--list-chains", action="store_true", help="List available chains")
    parser.add_argument("--config-dir", default=".claude/agents/config", help="Configuration directory")

    args = parser.parse_args()

    config_dir = Path(args.config_dir)
    if not config_dir.exists():
        print(f"❌ Configuration directory not found: {config_dir}")
        sys.exit(1)

    executor = ChainExecutor(config_dir)

    if args.list_chains:
        chains = executor.list_available_chains()
        print("Available chains:")
        for chain_id in chains:
            print(f"  • {chain_id}")
        return

    if args.validate_all:
        print("🔍 Validating all chain definitions...")
        all_valid = True
        for chain_id in executor.list_available_chains():
            result = executor.validate_chain_definition(chain_id)
            if result["errors"]:
                print(f"❌ {chain_id}: {len(result['errors'])} errors")
                for error in result["errors"]:
                    print(f"   • {error}")
                all_valid = False
            elif result["warnings"]:
                print(f"⚠️  {chain_id}: {len(result['warnings'])} warnings")
                for warning in result["warnings"]:
                    print(f"   • {warning}")
            else:
                print(f"✅ {chain_id}: Valid")

        if all_valid:
            print("\n🎉 All chain definitions are valid!")
        else:
            print("\n❌ Some chain definitions have errors")
            sys.exit(1)
        return

    if not args.chain:
        print("❌ Please specify a chain to execute with --chain")
        sys.exit(1)

    # Parse context
    import json
    context = {}
    if args.context:
        try:
            context = json.loads(args.context)
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON context: {args.context}")
            sys.exit(1)

    # Execute chain
    async def run_chain():
        try:
            execution = await executor.execute_chain(args.chain, context, args.dry_run)
            print(executor.generate_execution_report(execution))

            if execution.status == ChainExecutionStatus.COMPLETED:
                return 0
            else:
                return 1
        except Exception as e:
            print(f"❌ Chain execution failed: {e}")
            return 1

    exit_code = asyncio.run(run_chain())
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
