#!/bin/bash
# Pre-commit hook for agent compliance checking (optional)
#
# This script performs soft validation of agent changes during git commits.
# It provides gentle guidance but does not block commits (soft hook approach).
#
# To enable this hook:
#   ln -sf ../../scripts/agent-validation/pre-commit-agent-check.sh .git/hooks/pre-commit

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CLAUDE_HOOK_CONTEXT=true
STRICT_MODE=false  # Set to true to block commits on errors

echo -e "${BLUE}🔍 Claude Code Agent Compliance Check${NC}"
echo "================================================"

# Check if we're in a Claude Code project
if [[ ! -d ".claude/agents" ]]; then
    echo -e "${YELLOW}⚠️  No .claude/agents directory found${NC}"
    echo "   This doesn't appear to be a Claude Code project with agents"
    exit 0
fi

# Check for agent file changes
AGENT_FILES_CHANGED=$(git diff --cached --name-only | grep "\.claude/agents/.*\.md$" || true)

if [[ -z "$AGENT_FILES_CHANGED" ]]; then
    echo -e "${GREEN}✅ No agent files changed, skipping compliance check${NC}"
    exit 0
fi

echo -e "${BLUE}📝 Agent files being committed:${NC}"
echo "$AGENT_FILES_CHANGED" | sed 's/^/   • /'
echo

# Run compliance checker
echo -e "${BLUE}🔍 Running compliance checks...${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if python3 "$SCRIPT_DIR/agent-compliance-checker.py" --verbose; then
    echo -e "${GREEN}✅ All agent changes are compliant!${NC}"
    echo -e "${GREEN}   Commit proceeding...${NC}"
    exit 0
else
    COMPLIANCE_EXIT_CODE=$?

    echo
    echo -e "${YELLOW}⚠️  Agent compliance issues found${NC}"
    echo

    if [[ "$STRICT_MODE" == "true" ]]; then
        echo -e "${RED}❌ Strict mode enabled - commit blocked${NC}"
        echo -e "${RED}   Please fix compliance issues before committing${NC}"
        echo
        echo -e "${BLUE}💡 To bypass this check (not recommended):${NC}"
        echo -e "   git commit --no-verify"
        echo
        echo -e "${BLUE}🔧 To fix issues:${NC}"
        echo -e "   1. Review the compliance report above"
        echo -e "   2. Update agents according to ADR-007 and ADR-008"
        echo -e "   3. Run: python3 scripts/agent-validation/agent-compliance-checker.py"
        echo -e "   4. Commit again when compliant"
        exit $COMPLIANCE_EXIT_CODE
    else
        echo -e "${YELLOW}🔔 Soft Hook Mode: Commit proceeding with warnings${NC}"
        echo -e "${YELLOW}   Please consider addressing the compliance issues${NC}"
        echo
        echo -e "${BLUE}📚 Resources:${NC}"
        echo -e "   • ADR-007: Hierarchical Multi-Agent Architecture"
        echo -e "   • ADR-008: Cognitive Load Model Allocation"
        echo -e "   • docs/adr/ directory for details"
        echo
        echo -e "${BLUE}🔧 To check compliance manually:${NC}"
        echo -e "   python3 scripts/agent-validation/agent-compliance-checker.py --verbose"

        # Still exit 0 in soft mode to allow commit
        exit 0
    fi
fi
