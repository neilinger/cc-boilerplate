#!/usr/bin/env python3
"""
Claude Code Delegation Validator

Validates agent delegation patterns to ensure proper flat delegation
and identifies delegation gaps. Addresses Issue #37.

Usage:
    python3 validate-delegation.py --log-file conversation.log
    python3 validate-delegation.py --interactive  # For real-time validation
    python3 validate-delegation.py --help
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime


@dataclass
class TaskCall:
    """Represents a Task tool invocation"""
    agent: str
    description: str
    timestamp: Optional[str] = None
    context_provided: bool = False


@dataclass
class DelegationReport:
    """Results of delegation validation"""
    total_tasks: int
    task_calls: List[TaskCall]
    specialists_used: Set[str]
    gaps_identified: List[str]
    delegation_efficiency: float
    violations: List[str]
    recommendations: List[str]


class DelegationValidator:
    """Validates agent delegation patterns"""

    def __init__(self, config_dir: Path = None):
        """Initialize validator with agent configuration"""
        self.config_dir = config_dir or Path(".claude/agents")
        self.available_agents = self._load_available_agents()
        self.delegation_gaps = self._load_delegation_gaps()

        # Pre-compile regex patterns for security
        self._compile_regex_patterns()

    def _load_available_agents(self) -> Set[str]:
        """Load list of available specialist agents"""
        agents = set()
        agent_dirs = ["specialists", "orchestrators", "analyzers"]

        for agent_dir in agent_dirs:
            agent_path = self.config_dir / agent_dir
            if agent_path.exists():
                for agent_file in agent_path.glob("*.md"):
                    if agent_file.name != "README.md":
                        agent_name = agent_file.stem
                        agents.add(agent_name)

        return agents

    def _load_delegation_gaps(self) -> List[str]:
        """Load known delegation gaps"""
        gaps_file = Path(".claude/memory/delegation-gaps.md")
        if not gaps_file.exists():
            return []

        gaps = []
        try:
            content = gaps_file.read_text()
            content = self._validate_input(content)
            # Extract gap titles using regex pattern (will be pre-compiled if available)
            if hasattr(self, 'gap_pattern'):
                gaps = self.gap_pattern.findall(content)
            else:
                # Fallback for cases where patterns not yet compiled
                gap_pattern = re.compile(r"### Gap: (.+)")
                gaps = gap_pattern.findall(content)
        except FileNotFoundError:
            print("Warning: Delegation gaps file not found", file=sys.stderr)
        except PermissionError:
            print("Warning: Permission denied reading delegation gaps file", file=sys.stderr)
        except UnicodeDecodeError as e:
            print(f"Warning: Could not decode delegation gaps file: {e}", file=sys.stderr)
        except re.error as e:
            print(f"Warning: Regex error in delegation gaps parsing: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Unexpected error loading delegation gaps: {e}", file=sys.stderr)

        return gaps

    def _compile_regex_patterns(self):
        """Pre-compile regex patterns for security"""
        try:
            self.gap_pattern = re.compile(r"### Gap: (.+)")
            self.task_pattern = re.compile(r'Task\([^)]*subagent_type\s*=\s*["\']([a-zA-Z0-9_-]+)["\']')
            self.desc_pattern = re.compile(r'description.*?["\']([^"\']*)["\']')
        except re.error as e:
            print(f"Error compiling regex patterns: {e}", file=sys.stderr)
            # Fallback to safe patterns
            self.gap_pattern = re.compile(r"### Gap: ([\w\s-]+)")
            self.task_pattern = re.compile(r'Task\(.*?subagent_type.*?([a-zA-Z0-9_-]+)')
            self.desc_pattern = re.compile(r'description.*?([\w\s-]+)')

    def _validate_input(self, content: str) -> str:
        """Validate and sanitize input content"""
        if not isinstance(content, str):
            raise ValueError("Input must be a string")

        # Limit content size to prevent DoS
        max_size = 10 * 1024 * 1024  # 10MB
        if len(content) > max_size:
            raise ValueError(f"Input too large: {len(content)} bytes (max: {max_size})")

        return content

    def parse_conversation_log(self, log_content: str) -> List[TaskCall]:
        """Parse conversation log for Task tool invocations"""
        task_calls = []

        try:
            # Validate and sanitize input
            log_content = self._validate_input(log_content)

            # Find all Task tool invocations using pre-compiled patterns
            for match in self.task_pattern.finditer(log_content):
                agent = match.group(1)

                # Validate agent name format
                if not re.match(r'^[a-zA-Z0-9_-]+$', agent):
                    continue  # Skip invalid agent names

                # Try to find description in nearby text
                start = max(0, match.start()-200)
                end = min(len(log_content), match.end()+200)
                context = log_content[start:end]

                desc_match = self.desc_pattern.search(context)
                description = desc_match.group(1) if desc_match else "No description"

                # Sanitize description
                description = description[:200] if description else "No description"

                # Check if context was provided
                context_provided = len(context.strip()) > 100

                task_calls.append(TaskCall(
                    agent=agent,
                    description=description,
                    context_provided=context_provided
                ))

        except ValueError as e:
            print(f"Warning: Input validation error: {e}", file=sys.stderr)
        except re.error as e:
            print(f"Warning: Regex processing error: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Unexpected error parsing log: {e}", file=sys.stderr)

        return task_calls

    def validate_delegation(self, task_calls: List[TaskCall]) -> DelegationReport:
        """Validate delegation patterns and identify issues"""
        violations = []
        recommendations = []
        gaps_identified = []

        # Check for direct delegation pattern
        for task_call in task_calls:
            # Check if agent exists
            if task_call.agent not in self.available_agents:
                gaps_identified.append(f"Unknown agent: {task_call.agent}")

            # Check if context was provided
            if not task_call.context_provided:
                violations.append(f"Insufficient context for {task_call.agent}")

        # Calculate delegation efficiency
        total_tasks = len(task_calls)
        delegated_tasks = len([t for t in task_calls if t.agent in self.available_agents])
        efficiency = (delegated_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Generate recommendations
        if efficiency < 80:
            recommendations.append("Consider creating specialists for frequently needed capabilities")

        if len(violations) > 0:
            recommendations.append("Provide more detailed context when delegating to agents")

        if len(set(t.agent for t in task_calls)) < 2 and total_tasks > 3:
            recommendations.append("Consider using more diverse specialist agents for complex tasks")

        return DelegationReport(
            total_tasks=total_tasks,
            task_calls=task_calls,
            specialists_used=set(t.agent for t in task_calls),
            gaps_identified=gaps_identified,
            delegation_efficiency=efficiency,
            violations=violations,
            recommendations=recommendations
        )

    def generate_report(self, report: DelegationReport) -> str:
        """Generate human-readable validation report"""
        output = []

        output.append("=" * 60)
        output.append("CLAUDE CODE DELEGATION VALIDATION REPORT")
        output.append("=" * 60)
        output.append("")

        # Summary
        output.append(f"📊 SUMMARY")
        output.append(f"   Total Tasks: {report.total_tasks}")
        output.append(f"   Tasks Delegated: {len(report.task_calls)}")
        output.append(f"   Specialists Used: {len(report.specialists_used)}")
        output.append(f"   Delegation Efficiency: {report.delegation_efficiency:.1f}%")
        output.append("")

        # Task Breakdown
        if report.task_calls:
            output.append("🎯 TASK DELEGATION BREAKDOWN")
            for i, task in enumerate(report.task_calls, 1):
                status = "✅" if task.agent in self.available_agents else "❌"
                context_status = "📋" if task.context_provided else "⚠️"
                output.append(f"   {i}. {status} {context_status} {task.agent}: {task.description}")
            output.append("")

        # Specialists Used
        if report.specialists_used:
            output.append("👥 SPECIALISTS UTILIZED")
            for agent in sorted(report.specialists_used):
                status = "✅" if agent in self.available_agents else "❌ (GAP)"
                output.append(f"   - {status} {agent}")
            output.append("")

        # Violations
        if report.violations:
            output.append("🚨 VIOLATIONS")
            for violation in report.violations:
                output.append(f"   ❌ {violation}")
            output.append("")

        # Gaps
        if report.gaps_identified:
            output.append("🕳️  DELEGATION GAPS")
            for gap in report.gaps_identified:
                output.append(f"   📝 {gap}")
            output.append("")

        # Recommendations
        if report.recommendations:
            output.append("💡 RECOMMENDATIONS")
            for rec in report.recommendations:
                output.append(f"   → {rec}")
            output.append("")

        # Status
        if report.violations:
            output.append("❌ DELEGATION VALIDATION FAILED")
        elif report.delegation_efficiency < 80:
            output.append("⚠️  DELEGATION EFFICIENCY LOW")
        else:
            output.append("✅ DELEGATION VALIDATION PASSED")

        output.append("")
        output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("=" * 60)

        return "\n".join(output)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Validate Claude Code agent delegation patterns"
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        help="Conversation log file to analyze"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode for real-time validation"
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=Path(".claude/agents"),
        help="Agent configuration directory"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file for validation report"
    )

    args = parser.parse_args()

    validator = DelegationValidator(args.config_dir)

    if args.interactive:
        print("Interactive delegation validation not yet implemented.")
        print("Use --log-file option for batch validation.")
        sys.exit(1)

    if not args.log_file:
        parser.print_help()
        sys.exit(1)

    if not args.log_file.exists():
        print(f"Error: Log file not found: {args.log_file}", file=sys.stderr)
        sys.exit(1)

    # Parse log file
    try:
        log_content = args.log_file.read_text()
        task_calls = validator.parse_conversation_log(log_content)
        report = validator.validate_delegation(task_calls)
        report_text = validator.generate_report(report)

        # Output report
        if args.output:
            args.output.write_text(report_text)
            print(f"Report written to: {args.output}")
        else:
            print(report_text)

        # Exit code based on validation results
        if report.violations:
            sys.exit(1)
        elif report.delegation_efficiency < 80:
            sys.exit(2)  # Warning level
        else:
            sys.exit(0)

    except Exception as e:
        print(f"Error processing log file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()