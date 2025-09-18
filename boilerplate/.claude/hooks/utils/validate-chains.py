#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pyyaml>=6.0",
#     "pathlib",
#     "argparse",
# ]
# ///

"""
Chain Configuration Validator

Validates agent chain configurations for consistency, completeness,
and compliance with architectural principles.

Usage:
    python validate-chains.py [--verbose] [--fix-issues]
"""

import os
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

class ChainValidator:
    def __init__(self, claude_dir: Path):
        self.claude_dir = claude_dir
        self.config_dir = claude_dir / "agents" / "config"
        self.errors = []
        self.warnings = []
        self.suggestions = []

        # Load configurations
        self.chain_definitions = self._load_chain_definitions()
        self.agent_orchestration = self._load_agent_orchestration()
        self.tool_permissions = self._load_tool_permissions()

    def _load_chain_definitions(self) -> Dict:
        """Load chain definitions"""
        try:
            with open(self.config_dir / "chain-definitions.yaml", 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.errors.append(f"Failed to load chain-definitions.yaml: {e}")
            return {}

    def _load_agent_orchestration(self) -> Dict:
        """Load agent orchestration config"""
        try:
            with open(self.config_dir / "agent-orchestration.yaml", 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.errors.append(f"Failed to load agent-orchestration.yaml: {e}")
            return {}

    def _load_tool_permissions(self) -> Dict:
        """Load tool permissions matrix"""
        try:
            with open(self.config_dir / "tool-permissions.yaml", 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.errors.append(f"Failed to load tool-permissions.yaml: {e}")
            return {}

    def validate_all_chains(self) -> bool:
        """Validate all chain configurations"""
        if not self.chain_definitions:
            self.errors.append("No chain definitions found or failed to load")
            return False

        print(f"🔍 Validating {len(self.chain_definitions.get('chains', {}))} chain definitions...")

        # Validate each chain
        for chain_id, chain_def in self.chain_definitions.get('chains', {}).items():
            self._validate_chain(chain_id, chain_def)

        # Validate chain system integrity
        self._validate_chain_system_integrity()

        # Validate security requirements
        self._validate_security_requirements()

        return len(self.errors) == 0

    def _validate_chain(self, chain_id: str, chain_def: Dict) -> None:
        """Validate individual chain configuration"""
        # Required fields
        required_fields = ['name', 'description', 'type', 'sequence']
        for field in required_fields:
            if field not in chain_def:
                self.errors.append(f"Chain '{chain_id}': Missing required field '{field}'")

        # Validate chain type
        valid_types = ['mandatory', 'optional', 'auto_trigger', 'manual_trigger']
        chain_type = chain_def.get('type')
        if chain_type and chain_type not in valid_types:
            self.errors.append(f"Chain '{chain_id}': Invalid type '{chain_type}'. Must be one of: {valid_types}")

        # Validate sequence
        if 'sequence' in chain_def:
            self._validate_chain_sequence(chain_id, chain_def['sequence'])

        # Validate triggers
        if 'triggers' in chain_def:
            self._validate_chain_triggers(chain_id, chain_def['triggers'])

        # Validate validation rules
        if 'validation_rules' in chain_def:
            self._validate_validation_rules(chain_id, chain_def['validation_rules'])

    def _validate_chain_sequence(self, chain_id: str, sequence: List[Dict]) -> None:
        """Validate chain sequence configuration"""
        if not sequence:
            self.errors.append(f"Chain '{chain_id}': Empty sequence")
            return

        agent_names = self._get_all_available_agents()

        for i, step in enumerate(sequence):
            step_id = f"Chain '{chain_id}', step {i+1}"

            # Required step fields
            if 'agent' not in step:
                self.errors.append(f"{step_id}: Missing 'agent' field")
                continue

            if 'role' not in step:
                self.errors.append(f"{step_id}: Missing 'role' field")

            agent_name = step['agent']

            # Check if agent exists
            if agent_name not in agent_names:
                self.errors.append(f"{step_id}: Agent '{agent_name}' not found in orchestration config")

            # Validate timeout
            timeout = step.get('timeout_minutes', 10)
            if not isinstance(timeout, (int, float)) or timeout <= 0:
                self.warnings.append(f"{step_id}: Invalid timeout '{timeout}', should be positive number")

            # Validate required field
            required = step.get('required', True)
            if not isinstance(required, bool):
                self.warnings.append(f"{step_id}: 'required' should be boolean, got {type(required)}")

            # Check condition syntax
            condition = step.get('condition')
            if condition and not self._validate_condition_syntax(condition):
                self.warnings.append(f"{step_id}: Potentially invalid condition syntax: '{condition}'")

            # Validate input/output references
            self._validate_step_io_references(step_id, step, sequence[:i])

    def _validate_condition_syntax(self, condition: str) -> bool:
        """Basic validation of condition syntax"""
        # Simple checks for common operators
        valid_operators = ['==', '!=', '>', '<', '>=', '<=', 'true', 'false']
        return any(op in condition for op in valid_operators)

    def _validate_step_io_references(self, step_id: str, step: Dict, previous_steps: List[Dict]) -> None:
        """Validate that input references point to valid previous outputs"""
        inputs = step.get('inputs', [])
        if not inputs:
            return

        # Collect all available outputs from previous steps
        available_outputs = set()
        for prev_step in previous_steps:
            available_outputs.update(prev_step.get('outputs', []))

        # Check if all inputs are available
        for input_ref in inputs:
            if input_ref not in available_outputs:
                self.warnings.append(f"{step_id}: Input '{input_ref}' not produced by previous steps")

    def _validate_chain_triggers(self, chain_id: str, triggers: List[str]) -> None:
        """Validate chain trigger configurations"""
        if not triggers:
            self.warnings.append(f"Chain '{chain_id}': No triggers defined")
            return

        # Common trigger patterns
        valid_trigger_patterns = [
            'code modification', 'new file creation', 'dependency changes',
            'new feature implementation', 'test coverage below threshold',
            'explicit testing request', 'public API changes', 'architecture modifications',
            'release preparation', 'production deployment'
        ]

        for trigger in triggers:
            if not any(pattern in trigger.lower() for pattern in valid_trigger_patterns):
                self.suggestions.append(f"Chain '{chain_id}': Unusual trigger pattern '{trigger}' - verify intent")

    def _validate_validation_rules(self, chain_id: str, rules: List[str]) -> None:
        """Validate chain validation rules"""
        if not rules:
            self.warnings.append(f"Chain '{chain_id}': No validation rules defined")
            return

        for rule in rules:
            if not isinstance(rule, str):
                self.errors.append(f"Chain '{chain_id}': Validation rule must be string, got {type(rule)}")
            elif len(rule.strip()) < 10:
                self.warnings.append(f"Chain '{chain_id}': Very short validation rule: '{rule}'")

    def _get_all_available_agents(self) -> Set[str]:
        """Get set of all available agent names"""
        agents = set()

        # Get orchestrators
        if 'orchestrators' in self.agent_orchestration:
            agents.update(self.agent_orchestration['orchestrators'].keys())

        # Get agents from categories section
        if 'categories' in self.agent_orchestration:
            for category_data in self.agent_orchestration['categories'].values():
                if 'agents' in category_data:
                    agents.update(category_data['agents'])

        return agents

    def _validate_chain_system_integrity(self) -> None:
        """Validate overall chain system integrity"""
        chains = self.chain_definitions.get('chains', {})

        # Check for mandatory security chain
        security_chains = [cid for cid, cdef in chains.items()
                          if cdef.get('type') == 'mandatory' and 'security' in cid.lower()]

        if not security_chains:
            self.errors.append("No mandatory security chain found - security validation is required")

        # Check for chain coverage of critical operations
        critical_operations = ['code modification', 'dependency changes', 'production deployment']
        covered_operations = set()

        for chain_def in chains.values():
            triggers = chain_def.get('triggers', [])
            for trigger in triggers:
                for op in critical_operations:
                    if op in trigger.lower():
                        covered_operations.add(op)

        missing_coverage = set(critical_operations) - covered_operations
        if missing_coverage:
            self.warnings.append(f"Missing chain coverage for critical operations: {missing_coverage}")

        # Check for circular dependencies
        self._check_chain_circular_dependencies(chains)

    def _check_chain_circular_dependencies(self, chains: Dict) -> None:
        """Check for circular dependencies in chain handoffs"""
        # Build handoff graph
        handoff_graph = {}
        for chain_id, chain_def in chains.items():
            handoffs = []
            # Extract handoff information from sequence or other config
            # This is simplified - in practice, you'd parse the actual handoff logic
            handoff_graph[chain_id] = handoffs

        # Simple cycle detection (can be enhanced)
        visited = set()
        rec_stack = set()

        def has_cycle(node):
            if node in rec_stack:
                return True
            if node in visited:
                return False

            visited.add(node)
            rec_stack.add(node)

            for neighbor in handoff_graph.get(node, []):
                if has_cycle(neighbor):
                    return True

            rec_stack.remove(node)
            return False

        for chain_id in chains:
            if chain_id not in visited:
                if has_cycle(chain_id):
                    self.errors.append(f"Circular dependency detected involving chain '{chain_id}'")

    def _validate_security_requirements(self) -> None:
        """Validate security-specific chain requirements"""
        chains = self.chain_definitions.get('chains', {})

        # Ensure security validation chain exists and is properly configured
        security_chain = chains.get('security_validation')
        if not security_chain:
            self.errors.append("Missing 'security_validation' chain - required for compliance")
            return

        # Check security chain sequence
        sequence = security_chain.get('sequence', [])
        required_security_agents = ['code-reviewer', 'security-orchestrator']

        security_agents_in_chain = [step.get('agent') for step in sequence]
        for required_agent in required_security_agents:
            if required_agent not in security_agents_in_chain:
                self.errors.append(f"Security chain missing required agent: '{required_agent}'")

        # Check that security-orchestrator is marked as required
        for step in sequence:
            if step.get('agent') == 'security-orchestrator' and not step.get('required', True):
                self.errors.append("security-orchestrator must be marked as required in security chain")

    def generate_report(self, verbose: bool = False) -> str:
        """Generate validation report"""
        report = []

        # Summary
        total_issues = len(self.errors) + len(self.warnings) + len(self.suggestions)
        if total_issues == 0:
            report.append("✅ All chain configurations are valid!")
            return "\n".join(report)

        report.append(f"📊 Chain Configuration Validation Report")
        report.append(f"{'=' * 50}")
        report.append(f"🚨 Errors: {len(self.errors)}")
        report.append(f"⚠️  Warnings: {len(self.warnings)}")
        report.append(f"💡 Suggestions: {len(self.suggestions)}")
        report.append("")

        # Errors (must fix)
        if self.errors:
            report.append("🚨 ERRORS (Must Fix):")
            report.append("-" * 25)
            for error in self.errors:
                report.append(f"  • {error}")
            report.append("")

        # Warnings (should fix)
        if self.warnings:
            report.append("⚠️  WARNINGS (Should Fix):")
            report.append("-" * 27)
            for warning in self.warnings:
                report.append(f"  • {warning}")
            report.append("")

        # Suggestions (consider)
        if self.suggestions and verbose:
            report.append("💡 SUGGESTIONS (Consider):")
            report.append("-" * 28)
            for suggestion in self.suggestions:
                report.append(f"  • {suggestion}")
            report.append("")

        # Guidance
        report.append("🔧 REMEDIATION GUIDANCE:")
        report.append("-" * 25)
        report.append("  • Review chain-definitions.yaml for syntax and completeness")
        report.append("  • Ensure all referenced agents exist in agent-orchestration.yaml")
        report.append("  • Validate that mandatory security chains are properly configured")
        report.append("  • Check for circular dependencies in chain handoffs")
        report.append("  • Verify input/output references between chain steps")

        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="Validate agent chain configurations")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output including suggestions")
    parser.add_argument("--fix-issues", action="store_true", help="Attempt to auto-fix some issues (future feature)")

    args = parser.parse_args()

    # Find .claude directory
    current_dir = Path.cwd()
    claude_dir = None

    for parent in [current_dir] + list(current_dir.parents):
        potential_claude = parent / ".claude"
        if potential_claude.exists() and (potential_claude / "agents").exists():
            claude_dir = potential_claude
            break

    if not claude_dir:
        print("❌ Error: Could not find .claude/agents directory")
        print("   Run this script from within a Claude Code project")
        sys.exit(1)

    print(f"🔗 Claude Code Chain Configuration Validator")
    print(f"📁 Checking chains in: {claude_dir}")
    print()

    validator = ChainValidator(claude_dir)
    is_valid = validator.validate_all_chains()

    print(validator.generate_report(args.verbose))

    if args.fix_issues:
        print("\n🔧 Auto-fix functionality coming in future version...")

    # Exit code for CI/CD integration
    sys.exit(0 if is_valid else 1)

if __name__ == "__main__":
    main()
