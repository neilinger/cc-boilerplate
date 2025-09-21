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
Agent Description Format Fixer

This script systematically converts all agent descriptions to the required
ADR-007 compliant format:

ALWAYS use when: [specific trigger conditions]
NEVER use when: [anti-patterns to avoid]
Runs AFTER: [predecessor agents or "initial task"]
Hands off to: [next agents or "terminal"]

Usage:
    python fix-agent-descriptions.py [--dry-run] [--verbose]
"""

import os
import sys
import yaml
import re
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

class AgentDescriptionFixer:
    def __init__(self, claude_dir: Path):
        self.claude_dir = claude_dir
        self.agents_dir = claude_dir / "agents"
        self.fixes_applied = []
        self.errors = []

        # Transformation rules mapping agent types to structured descriptions
        self.transformation_rules = self._load_transformation_rules()

    def _load_transformation_rules(self) -> Dict:
        """Load transformation rules for different agent types"""
        return {
            # Language specialists
            "python-pro": {
                "always": "Python development, Python code optimization, modern Python patterns, async programming",
                "never": "Non-Python tasks, basic scripting that doesn't need expertise",
                "runs_after": "technical-researcher, requirements clarification",
                "hands_off": "test-automator, code-reviewer"
            },
            "rust-pro": {
                "always": "Rust development, systems programming, performance optimization, memory safety",
                "never": "Non-Rust tasks, high-level scripting",
                "runs_after": "technical-researcher, architecture decisions",
                "hands_off": "test-automator, code-reviewer"
            },
            "javascript-pro": {
                "always": "JavaScript/TypeScript development, Node.js, frontend frameworks",
                "never": "Non-JavaScript tasks, server-side only when backend expertise needed",
                "runs_after": "technical-researcher, requirements analysis",
                "hands_off": "test-automator, code-reviewer"
            },
            "react-pro": {
                "always": "React development, component architecture, state management, modern React patterns",
                "never": "Non-React tasks, backend development",
                "runs_after": "javascript-pro, UI/UX analysis",
                "hands_off": "test-automator, code-reviewer"
            },
            "nextjs-pro": {
                "always": "Next.js development, SSR/SSG, full-stack React applications",
                "never": "Non-Next.js tasks, basic React components",
                "runs_after": "react-pro, architecture decisions",
                "hands_off": "test-automator, deployment-engineer"
            },
            "vue-pro": {
                "always": "Vue.js development, composition API, Vue ecosystem",
                "never": "Non-Vue tasks, framework comparisons",
                "runs_after": "javascript-pro, frontend analysis",
                "hands_off": "test-automator, code-reviewer"
            },
            "angular-pro": {
                "always": "Angular development, TypeScript services, RxJS patterns",
                "never": "Non-Angular tasks, simple component work",
                "runs_after": "javascript-pro, enterprise architecture",
                "hands_off": "test-automator, code-reviewer"
            },
            "svelte-pro": {
                "always": "Svelte/SvelteKit development, reactive programming, component optimization",
                "never": "Non-Svelte tasks, complex state management",
                "runs_after": "javascript-pro, performance analysis",
                "hands_off": "test-automator, code-reviewer"
            },
            "go-pro": {
                "always": "Go development, concurrent programming, microservices, system tools",
                "never": "Non-Go tasks, UI development",
                "runs_after": "technical-researcher, system architecture",
                "hands_off": "test-automator, deployment-engineer"
            },
            "java-pro": {
                "always": "Java development, Spring ecosystem, enterprise applications",
                "never": "Non-Java tasks, simple scripting",
                "runs_after": "technical-researcher, enterprise architecture",
                "hands_off": "test-automator, code-reviewer"
            },
            "csharp-pro": {
                "always": ".NET development, C# optimization, enterprise applications",
                "never": "Non-.NET tasks, cross-platform when not .NET",
                "runs_after": "technical-researcher, enterprise architecture",
                "hands_off": "test-automator, code-reviewer"
            },
            "php-pro": {
                "always": "PHP development, Laravel/Symfony, web applications",
                "never": "Non-PHP tasks, modern alternatives available",
                "runs_after": "technical-researcher, web architecture",
                "hands_off": "test-automator, code-reviewer"
            },
            "ruby-pro": {
                "always": "Ruby development, Rails applications, Ruby ecosystem",
                "never": "Non-Ruby tasks, performance-critical applications",
                "runs_after": "technical-researcher, web architecture",
                "hands_off": "test-automator, code-reviewer"
            },
            "swift-pro": {
                "always": "Swift development, iOS applications, Apple ecosystem",
                "never": "Non-Apple development, cross-platform mobile",
                "runs_after": "technical-researcher, mobile architecture",
                "hands_off": "test-automator, mobile-deployment"
            },
            "kotlin-pro": {
                "always": "Kotlin development, Android applications, multiplatform",
                "never": "Non-Kotlin tasks, iOS-specific development",
                "runs_after": "technical-researcher, mobile architecture",
                "hands_off": "test-automator, mobile-deployment"
            },
            "cpp-pro": {
                "always": "C++ development, system programming, performance optimization",
                "never": "High-level scripting, web development",
                "runs_after": "technical-researcher, system architecture",
                "hands_off": "test-automator, code-reviewer"
            },
            "c-pro": {
                "always": "C development, embedded systems, low-level programming",
                "never": "High-level applications, object-oriented design",
                "runs_after": "technical-researcher, system architecture",
                "hands_off": "test-automator, code-reviewer"
            },

            # Domain specialists
            "ai-engineering-researcher": {
                "always": "AI/ML research, LLM developments, agent engineering, AI architecture",
                "never": "General software development, non-AI technical research",
                "runs_after": "initial research request",
                "hands_off": "technical-researcher, workflow-orchestrator"
            },
            "technical-researcher": {
                "always": "In-depth research, framework evaluation, technology analysis, feasibility studies",
                "never": "Simple questions, implementation tasks",
                "runs_after": "initial task",
                "hands_off": "adr-creator, implementation specialists"
            },
            "adr-creator": {
                "always": "Architectural decisions, technology choices, design patterns, technical decision documentation",
                "never": "Implementation details, non-architectural decisions",
                "runs_after": "technical-researcher, architecture analysis",
                "hands_off": "workflow-orchestrator, implementation specialists"
            },
            "smart-doc-generator": {
                "always": "Documentation creation/updates, README files, API docs, architectural overviews",
                "never": "Code implementation, testing, non-documentation tasks",
                "runs_after": "code implementation complete",
                "hands_off": "workflow-orchestrator"
            },
            "test-automator": {
                "always": "Test creation, coverage improvement, test automation setup, testing strategy",
                "never": "Code implementation, documentation, non-testing tasks",
                "runs_after": "code implementation complete",
                "hands_off": "code-reviewer, workflow-orchestrator"
            },
            "debugger": {
                "always": "Root cause analysis, complex debugging, fix implementation, error investigation",
                "never": "Simple errors, feature development",
                "runs_after": "error identification, test failures",
                "hands_off": "code-reviewer, test-automator"
            },
            "security-scanner": {
                "always": "Vulnerability scanning, security validation, OWASP compliance, security audits",
                "never": "Code implementation, non-security analysis",
                "runs_after": "code completion, dependency updates",
                "hands_off": "security-orchestrator, code-reviewer"
            },
            "pr-optimizer": {
                "always": "PR creation, GitHub workflow automation, PR optimization, code review preparation",
                "never": "Code implementation, non-GitHub tasks",
                "runs_after": "code completion, testing complete",
                "hands_off": "github-checker, workflow-orchestrator"
            },
            "dependency-manager": {
                "always": "Dependency updates, security alerts, package management, vulnerability fixes",
                "never": "Feature development, non-dependency tasks",
                "runs_after": "dependency analysis, security alerts",
                "hands_off": "security-scanner, test-automator"
            },
            "github-checker": {
                "always": "Repository maintenance, issue management, PR status, GitHub operations",
                "never": "Code implementation, complex analysis",
                "runs_after": "PR creation, issue creation",
                "hands_off": "pr-optimizer, workflow-orchestrator"
            },
            "context-engineer": {
                "always": "Context optimization, prompt improvement, memory management, agent performance tuning",
                "never": "Code implementation, non-context tasks",
                "runs_after": "agent performance issues, context bloat",
                "hands_off": "workflow-orchestrator, agent specialists"
            },

            # Database and infrastructure specialists
            "database-specialist": {
                "always": "Database design, query optimization, data modeling, migration strategies",
                "never": "Application logic, frontend development",
                "runs_after": "technical-researcher, data requirements analysis",
                "hands_off": "backend specialists, test-automator"
            },
            "devops-engineer": {
                "always": "Infrastructure automation, CI/CD pipelines, deployment strategies, monitoring",
                "never": "Application development, frontend tasks",
                "runs_after": "application completion, deployment requirements",
                "hands_off": "security-scanner, deployment-engineer"
            },
            "cloud-architect": {
                "always": "Cloud infrastructure design, scalability planning, cloud-native architecture",
                "never": "Local development, non-cloud solutions",
                "runs_after": "technical-researcher, scalability requirements",
                "hands_off": "devops-engineer, security-specialist"
            },
            "deployment-engineer": {
                "always": "Application deployment, production setup, release management",
                "never": "Development tasks, feature implementation",
                "runs_after": "application completion, testing complete",
                "hands_off": "monitoring-specialist, terminal"
            },

            # Content and marketing specialists
            "content-marketer": {
                "always": "Content strategy, marketing content, blog posts, social media content",
                "never": "Technical implementation, code development",
                "runs_after": "business requirements, marketing strategy",
                "hands_off": "seo-specialist, copywriter"
            },
            "seo-specialist": {
                "always": "SEO optimization, content strategy, search ranking improvement",
                "never": "Technical implementation, code development",
                "runs_after": "content-marketer, business-analyst",
                "hands_off": "technical-researcher, implementation specialists"
            },
            "copywriter": {
                "always": "Copy creation, content writing, marketing copy, user-facing text",
                "never": "Technical documentation, code implementation",
                "runs_after": "content-marketer, brand guidelines",
                "hands_off": "content-marketer, terminal"
            },
            "social-media-manager": {
                "always": "Social media strategy, content planning, community management",
                "never": "Technical implementation, non-social tasks",
                "runs_after": "content-marketer, brand strategy",
                "hands_off": "content-marketer, terminal"
            },

            # Business and analysis specialists
            "business-analyst": {
                "always": "Business requirements, process analysis, stakeholder needs, requirement gathering",
                "never": "Technical implementation, code development",
                "runs_after": "initial business request",
                "hands_off": "technical-researcher, workflow-orchestrator"
            },
            "product-manager": {
                "always": "Product strategy, feature prioritization, roadmap planning, user story creation",
                "never": "Technical implementation, detailed design",
                "runs_after": "business requirements, market analysis",
                "hands_off": "business-analyst, workflow-orchestrator"
            },
            "ui-ux-designer": {
                "always": "User interface design, user experience optimization, design systems",
                "never": "Backend development, technical implementation",
                "runs_after": "business requirements, user research",
                "hands_off": "frontend specialists, workflow-orchestrator"
            },

            # Analyzers
            "code-reviewer": {
                "always": "Code quality review, security analysis, best practices validation",
                "never": "Code implementation, feature development",
                "runs_after": "code implementation complete",
                "hands_off": "security-orchestrator (mandatory security chain)"
            },
            "test-coverage-analyzer": {
                "always": "Coverage analysis, gap identification, test quality assessment",
                "never": "Test implementation, code development",
                "runs_after": "test creation, coverage generation",
                "hands_off": "test-automator, workflow-orchestrator"
            },
            "work-completion-summary": {
                "always": "Task summaries, TTS announcements, progress reporting, completion validation",
                "never": "Implementation tasks, complex analysis",
                "runs_after": "task completion, workflow finish",
                "hands_off": "terminal"
            },
            "codebase-researcher": {
                "always": "Codebase analysis, pattern identification, architecture understanding",
                "never": "Code modification, implementation tasks",
                "runs_after": "initial research request",
                "hands_off": "technical-researcher, implementation specialists"
            },

            # Orchestrators
            "workflow-orchestrator": {
                "always": "Complex multi-step coordination, cross-cutting concerns, feature implementation requiring multiple domains",
                "never": "Simple single-domain tasks, analysis-only tasks",
                "runs_after": "complex task identification",
                "hands_off": "domain specialists based on needs"
            },
            "security-orchestrator": {
                "always": "Security-critical operations, mandatory security validation, comprehensive security review",
                "never": "Non-security tasks, initial development",
                "runs_after": "code-reviewer (mandatory security chain)",
                "hands_off": "security specialists, terminal"
            },

            # Root agents
            "meta-agent": {
                "always": "Agent creation, agent architecture decisions, system expansion",
                "never": "Feature implementation, regular development tasks",
                "runs_after": "agent system gaps identified",
                "hands_off": "workflow-orchestrator"
            }
        }

    def fix_all_agents(self, dry_run: bool = False) -> bool:
        """Fix all agent descriptions to comply with ADR-007 format"""
        agent_files = list(self.agents_dir.rglob("*.md"))
        agent_files = [f for f in agent_files if f.name != "README.md"]

        if not agent_files:
            self.errors.append("No agent files found")
            return False

        print(f"🔍 Processing {len(agent_files)} agent files...")

        for agent_file in agent_files:
            self._fix_agent_file(agent_file, dry_run)

        return len(self.errors) == 0

    def _fix_agent_file(self, agent_file: Path, dry_run: bool = False) -> None:
        """Fix individual agent file description format"""
        try:
            with open(agent_file, 'r') as f:
                content = f.read()

            # Parse frontmatter
            frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
            if not frontmatter_match:
                self.errors.append(f"{agent_file.name}: Missing or invalid frontmatter")
                return

            frontmatter_yaml = frontmatter_match.group(1)
            body_content = frontmatter_match.group(2)

            try:
                frontmatter = yaml.safe_load(frontmatter_yaml)
            except yaml.YAMLError as e:
                self.errors.append(f"{agent_file.name}: Invalid YAML frontmatter - {e}")
                return

            agent_name = frontmatter.get('name', agent_file.stem)

            # Check if description needs fixing
            description = frontmatter.get('description', '')

            # If already in correct format, skip
            if self._is_description_compliant(description):
                print(f"✅ {agent_name}: Already compliant")
                return

            # Transform description
            new_description = self._transform_description(agent_name, description)
            if not new_description:
                self.errors.append(f"{agent_name}: No transformation rule found")
                return

            # Update frontmatter with proper YAML block scalar
            frontmatter['description'] = new_description

            # Reconstruct file content with proper YAML formatting
            new_frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)

            # Fix the description to use YAML block scalar format
            new_frontmatter_yaml = new_frontmatter_yaml.replace(
                f"description: '{new_description}'",
                f"description: |\n  " + new_description.replace('\n', '\n  ')
            )
            new_frontmatter_yaml = new_frontmatter_yaml.replace(
                f'description: "{new_description}"',
                f"description: |\n  " + new_description.replace('\n', '\n  ')
            )
            new_frontmatter_yaml = new_frontmatter_yaml.replace(
                f"description: {new_description}",
                f"description: |\n  " + new_description.replace('\n', '\n  ')
            )

            new_content = f"---\n{new_frontmatter_yaml}---\n{body_content}"

            # Apply fix
            if not dry_run:
                with open(agent_file, 'w') as f:
                    f.write(new_content)

            self.fixes_applied.append(f"{agent_name}: Updated description format")
            print(f"🔧 {agent_name}: {'Would update' if dry_run else 'Updated'} description format")

        except Exception as e:
            self.errors.append(f"{agent_file.name}: Failed to process - {e}")

    def _is_description_compliant(self, description: str) -> bool:
        """Check if description follows the required format"""
        if isinstance(description, dict):
            description = str(description)

        required_patterns = ['ALWAYS use when:', 'NEVER use when:', 'Runs AFTER:', 'Hands off to:']
        return all(pattern in description for pattern in required_patterns)

    def _transform_description(self, agent_name: str, old_description: str) -> Optional[str]:
        """Transform old description to new format using transformation rules"""

        # Check if we have specific rules for this agent
        if agent_name in self.transformation_rules:
            rules = self.transformation_rules[agent_name]

            return f"""ALWAYS use when: {rules['always']}
NEVER use when: {rules['never']}
Runs AFTER: {rules['runs_after']}
Hands off to: {rules['hands_off']}"""

        # Generic transformation for unknown agents
        return self._generic_transform(agent_name, old_description)

    def _generic_transform(self, agent_name: str, old_description: str) -> str:
        """Generic transformation for agents without specific rules"""

        # Extract key functionality from old description
        if isinstance(old_description, dict):
            old_description = str(old_description)

        # Basic categorization
        always_use = f"{agent_name.replace('-', ' ')} tasks, domain-specific work"
        never_use = "Non-domain tasks, general development"
        runs_after = "requirements analysis, initial task"
        hands_off = "workflow-orchestrator, terminal"

        # Special handling for certain agent types
        if "pro" in agent_name:
            lang = agent_name.replace("-pro", "").title()
            always_use = f"{lang} development, {lang} code optimization"
            never_use = f"Non-{lang} tasks, general scripting"

        elif "specialist" in agent_name:
            domain = agent_name.replace("-specialist", "").replace("-", " ").title()
            always_use = f"{domain} tasks, specialized {domain} work"

        elif "analyzer" in agent_name:
            analysis_type = agent_name.replace("-analyzer", "").replace("-", " ")
            always_use = f"{analysis_type} analysis, {analysis_type} assessment"
            hands_off = "appropriate specialists, workflow-orchestrator"

        return f"""ALWAYS use when: {always_use}
NEVER use when: {never_use}
Runs AFTER: {runs_after}
Hands off to: {hands_off}"""

    def generate_report(self, dry_run: bool = False) -> str:
        """Generate transformation report"""
        report = []

        if dry_run:
            report.append("🔍 DRY RUN - Agent Description Format Fix Preview")
        else:
            report.append("🔧 Agent Description Format Fix Results")

        report.append("=" * 60)
        report.append(f"✅ Fixes applied: {len(self.fixes_applied)}")
        report.append(f"❌ Errors: {len(self.errors)}")
        report.append("")

        if self.fixes_applied:
            report.append("📝 Fixed Agents:")
            report.append("-" * 20)
            for fix in self.fixes_applied:
                report.append(f"  • {fix}")
            report.append("")

        if self.errors:
            report.append("❌ Errors:")
            report.append("-" * 10)
            for error in self.errors:
                report.append(f"  • {error}")
            report.append("")

        if not dry_run and self.fixes_applied:
            report.append("🎯 Next Steps:")
            report.append("-" * 12)
            report.append("  • Run compliance checker: ./scripts/agent-validation/check-agents.sh")
            report.append("  • Validate all agents work correctly")
            report.append("  • Commit changes if satisfied")

        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="Fix agent description formats for ADR-007 compliance")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying them")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")

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

    print(f"🏗️  Agent Description Format Fixer")
    print(f"📁 Processing agents in: {claude_dir}")
    print()

    fixer = AgentDescriptionFixer(claude_dir)
    success = fixer.fix_all_agents(args.dry_run)

    print()
    print(fixer.generate_report(args.dry_run))

    # Exit code for automation
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()