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
Agent Compliance Checker - Soft Hook System for Drift Prevention

This script validates that Claude Code agents follow the hierarchical
multi-agent architecture defined in ADR-007 and ADR-008.

Usage:
    python agent-compliance-checker.py [--fix] [--verbose]

Features:
- Validates agent structure and metadata
- Checks tool allocation boundaries
- Monitors description format adherence
- Ensures model allocation follows cognitive load rules
- Validates orchestration chain integrity
- Provides developer-friendly suggestions
"""

import os
import sys
import yaml
import re
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

class AgentComplianceChecker:
    def __init__(self, claude_dir: Path):
        self.claude_dir = claude_dir
        self.agents_dir = claude_dir / "agents"
        self.config_dir = self.agents_dir / "config"
        self.errors = []
        self.warnings = []
        self.suggestions = []

        # Load configuration
        self.tool_permissions = self._load_tool_permissions()
        self.orchestration_config = self._load_orchestration_config()

    def _load_tool_permissions(self) -> Dict:
        """Load tool permissions matrix"""
        try:
            with open(self.config_dir / "tool-permissions.yaml", 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.errors.append(f"Failed to load tool-permissions.yaml: {e}")
            return {}

    def _load_orchestration_config(self) -> Dict:
        """Load orchestration configuration"""
        try:
            with open(self.config_dir / "agent-orchestration.yaml", 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.errors.append(f"Failed to load agent-orchestration.yaml: {e}")
            return {}

    def check_all_agents(self) -> bool:
        """Check all agents for compliance"""
        agent_files = list(self.agents_dir.rglob("*.md"))
        agent_files = [f for f in agent_files if f.name != "README.md"]

        if not agent_files:
            self.errors.append("No agent files found")
            return False

        print(f"🔍 Checking {len(agent_files)} agent files...")

        for agent_file in agent_files:
            self._check_agent_file(agent_file)

        return len(self.errors) == 0

    def _check_agent_file(self, agent_file: Path) -> None:
        """Check individual agent file for compliance"""
        try:
            with open(agent_file, 'r') as f:
                content = f.read()

            # Parse frontmatter
            frontmatter = self._parse_frontmatter(content)
            if not frontmatter:
                self.errors.append(f"{agent_file.name}: Missing or invalid frontmatter")
                return

            agent_name = frontmatter.get('name', agent_file.stem)

            # Run compliance checks
            self._check_hierarchical_placement(agent_file, agent_name)
            self._check_frontmatter_structure(agent_file, frontmatter)
            self._check_tool_allocation(agent_file, agent_name, frontmatter)
            self._check_model_allocation(agent_file, agent_name, frontmatter)
            self._check_description_format(agent_file, frontmatter)
            self._check_orchestration_chains(agent_file, frontmatter)

        except Exception as e:
            self.errors.append(f"{agent_file.name}: Failed to parse - {e}")

    def _parse_frontmatter(self, content: str) -> Optional[Dict]:
        """Parse YAML frontmatter from markdown"""
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return None

        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return None

    def _check_hierarchical_placement(self, agent_file: Path, agent_name: str) -> None:
        """Check if agent is in correct hierarchical directory"""
        relative_path = agent_file.relative_to(self.agents_dir)
        directory = relative_path.parts[0] if len(relative_path.parts) > 1 else "root"

        expected_dirs = {
            "orchestrators": ["workflow-orchestrator", "security-orchestrator", "code-lifecycle-manager"],
            "specialists": ["security-scanner", "test-automator", "smart-doc-generator", "debugger",
                           "pr-optimizer", "dependency-manager", "technical-researcher", "adr-creator",
                           "ai-engineering-researcher", "context-engineer", "github-checker"],
            "analyzers": ["code-reviewer", "test-coverage-analyzer", "work-completion-summary", "codebase-researcher"],
            "root": ["meta-agent", "the-librarian"]
        }

        # Find expected directory for agent
        expected_dir = None
        for dir_name, agents in expected_dirs.items():
            if agent_name in agents:
                expected_dir = dir_name
                break

        if expected_dir and expected_dir != directory:
            if expected_dir == "root":
                self.errors.append(f"{agent_name}: Should be in root directory, not {directory}/")
            else:
                self.errors.append(f"{agent_name}: Should be in {expected_dir}/ directory, not {directory}/")

    def _check_frontmatter_structure(self, agent_file: Path, frontmatter: Dict) -> None:
        """Check frontmatter structure compliance"""
        required_fields = ['name', 'description', 'model']
        agent_name = frontmatter.get('name', agent_file.stem)

        for field in required_fields:
            if field not in frontmatter:
                self.errors.append(f"{agent_name}: Missing required field '{field}' in frontmatter")

        # Check if description uses new format
        description = frontmatter.get('description', '')
        if isinstance(description, str) and not description.strip().startswith('ALWAYS use when:'):
            self.warnings.append(f"{agent_name}: Description should use new format with 'ALWAYS use when:', 'NEVER use when:', etc.")

    def _check_tool_allocation(self, agent_file: Path, agent_name: str, frontmatter: Dict) -> None:
        """Check tool allocation compliance"""
        tools = frontmatter.get('tools', [])
        agent_name = frontmatter.get('name', agent_name)

        if not tools:
            # Some agents might not specify tools (full access)
            return

        if isinstance(tools, str):
            tools = [t.strip() for t in tools.split(',')]

        # Check tool count (3-7 tools principle)
        tool_count = len(tools)
        model = frontmatter.get('model', 'sonnet')

        if model == 'haiku' and tool_count > 3:
            self.warnings.append(f"{agent_name}: Haiku model should have ≤3 tools, has {tool_count}")
        elif model == 'sonnet' and tool_count > 7:
            self.warnings.append(f"{agent_name}: Sonnet model should have ≤7 tools, has {tool_count}")

        # Check for restricted tools
        if agent_name in self.tool_permissions.get('agent_permissions', {}):
            allowed_tools = self.tool_permissions['agent_permissions'][agent_name].get('specific_tools', [])
            for tool in tools:
                if tool == 'Task':  # Task is generally allowed
                    continue
                if not any(self._tool_matches_pattern(tool, pattern) for pattern in allowed_tools):
                    self.errors.append(f"{agent_name}: Tool '{tool}' not in allowed list")

    def _tool_matches_pattern(self, tool: str, pattern: str) -> bool:
        """Check if tool matches permission pattern"""
        if pattern == tool:
            return True
        if pattern.endswith('*'):
            return tool.startswith(pattern[:-1])
        return False

    def _check_model_allocation(self, agent_file: Path, agent_name: str, frontmatter: Dict) -> None:
        """Check model allocation follows cognitive load rules"""
        model = frontmatter.get('model', 'sonnet')
        tools = frontmatter.get('tools', [])

        if isinstance(tools, str):
            tools = [t.strip() for t in tools.split(',')]

        tool_count = len(tools) if tools else 0

        # Cognitive load rules
        if model == 'haiku':
            if tool_count > 3:
                self.warnings.append(f"{agent_name}: Haiku should have ≤3 tools for low cognitive load")
        elif model == 'opus':
            # Opus should be for orchestration or high complexity
            if agent_name not in ['workflow-orchestrator', 'meta-agent', 'technical-researcher']:
                self.suggestions.append(f"{agent_name}: Consider if Opus is needed - reserved for orchestration/high complexity")

    def _check_description_format(self, agent_file: Path, frontmatter: Dict) -> None:
        """Check description format compliance"""
        description = frontmatter.get('description', '')
        agent_name = frontmatter.get('name', agent_file.stem)

        if isinstance(description, str):
            # Old format check
            if not any(phrase in description for phrase in ['ALWAYS use when:', 'NEVER use when:']):
                self.warnings.append(f"{agent_name}: Should use new description format with ALWAYS/NEVER triggers")
        elif isinstance(description, dict) or '|' in str(description):
            # New format - check for required patterns
            desc_str = str(description)
            required_patterns = ['ALWAYS use when:', 'NEVER use when:', 'Runs AFTER:', 'Hands off to:']

            for pattern in required_patterns:
                if pattern not in desc_str:
                    self.warnings.append(f"{agent_name}: Missing '{pattern}' in description")

    def _check_orchestration_chains(self, agent_file: Path, frontmatter: Dict) -> None:
        """Check orchestration chain integrity"""
        description = str(frontmatter.get('description', ''))
        agent_name = frontmatter.get('name', agent_file.stem)

        # Check for mandatory security chain
        if agent_name == 'code-reviewer':
            if 'security-orchestrator' not in description:
                self.errors.append(f"{agent_name}: Must hand off to security-orchestrator (mandatory security chain)")

        # Check for valid handoff targets
        handoff_match = re.search(r'Hands off to: ([^\\n]+)', description)
        if handoff_match:
            handoff_agents = [name.strip() for name in handoff_match.group(1).split(',')]
            for target in handoff_agents:
                if target not in ['workflow-orchestrator', 'security-orchestrator', 'test-coverage-analyzer',
                                'adr-creator', 'pr-optimizer', 'None (terminal agent)']:
                    self.suggestions.append(f"{agent_name}: Handoff to '{target}' - verify agent exists")

    def generate_report(self, verbose: bool = False) -> str:
        """Generate compliance report"""
        report = []

        # Summary
        total_issues = len(self.errors) + len(self.warnings) + len(self.suggestions)
        if total_issues == 0:
            report.append("✅ All agents are compliant with hierarchical architecture!")
            return "\\n".join(report)

        report.append(f"📊 Agent Compliance Report")
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
        report.append("  • Review ADR-007 (Hierarchical Multi-Agent Architecture)")
        report.append("  • Check tool-permissions.yaml for allowed tools")
        report.append("  • Use cognitive load model allocation (haiku≤3, sonnet≤7, opus=orchestration)")
        report.append("  • Follow ALWAYS/NEVER/RUNS AFTER/HANDS OFF TO description format")
        report.append("  • Ensure security chain integration for critical agents")

        return "\\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="Check agent compliance with hierarchical architecture")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output including suggestions")
    parser.add_argument("--fix", action="store_true", help="Attempt to auto-fix some issues (future feature)")

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

    print(f"🏗️  Claude Code Agent Compliance Checker")
    print(f"📁 Checking agents in: {claude_dir}")
    print()

    checker = AgentComplianceChecker(claude_dir)
    is_compliant = checker.check_all_agents()

    print(checker.generate_report(args.verbose))

    if args.fix:
        print("\\n🔧 Auto-fix functionality coming in future version...")

    # Exit code for CI/CD integration
    sys.exit(0 if is_compliant else 1)

if __name__ == "__main__":
    main()
