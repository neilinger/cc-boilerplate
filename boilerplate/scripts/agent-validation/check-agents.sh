#!/bin/bash
# Convenient developer script for agent compliance checking
#
# Usage:
#   ./check-agents.sh              # Basic compliance check
#   ./check-agents.sh --verbose    # Detailed report with suggestions
#   ./check-agents.sh --help       # Show help

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

show_help() {
    echo -e "${BLUE}Claude Code Agent Compliance Checker${NC}"
    echo "======================================="
    echo
    echo -e "${YELLOW}USAGE:${NC}"
    echo "  $0 [OPTIONS]"
    echo
    echo -e "${YELLOW}OPTIONS:${NC}"
    echo "  --verbose, -v    Show detailed report with suggestions"
    echo "  --help, -h       Show this help message"
    echo
    echo -e "${YELLOW}EXAMPLES:${NC}"
    echo "  $0              # Quick compliance check"
    echo "  $0 --verbose    # Detailed analysis"
    echo
    echo -e "${YELLOW}WHAT THIS CHECKS:${NC}"
    echo "  ✓ Hierarchical agent placement (orchestrators/, specialists/, analyzers/)"
    echo "  ✓ Tool allocation boundaries (3-7 tools per agent)"
    echo "  ✓ Model allocation (haiku≤3, sonnet≤7, opus=orchestration)"
    echo "  ✓ Description format (ALWAYS/NEVER/RUNS AFTER/HANDS OFF TO)"
    echo "  ✓ Security chain integration"
    echo "  ✓ Orchestration patterns"
    echo "  ✓ Agent chain configuration integrity"
    echo
    echo -e "${YELLOW}ARCHITECTURE REFERENCES:${NC}"
    echo "  📖 ADR-007: Hierarchical Multi-Agent Architecture"
    echo "  📖 ADR-008: Cognitive Load Model Allocation"
    echo "  ⚙️  Tool Permissions: .claude/agents/config/tool-permissions.yaml"
    echo "  🔗 Orchestration: .claude/agents/config/agent-orchestration.yaml"
}

# Parse arguments
VERBOSE=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo -e "${PURPLE}🤖 Claude Code Agent Compliance Checker${NC}"
echo "============================================="
echo

# Check if we're in the right directory
if [[ ! -d "$PROJECT_ROOT/.claude/agents" ]]; then
    echo -e "${RED}❌ Error: Could not find .claude/agents directory${NC}"
    echo "   Make sure you're running this from a Claude Code project"
    echo "   Current directory: $(pwd)"
    echo "   Looking for: $PROJECT_ROOT/.claude/agents"
    exit 1
fi

echo -e "${BLUE}📁 Project root: ${PROJECT_ROOT}${NC}"
echo -e "${BLUE}🔍 Checking agents in: .claude/agents/${NC}"
echo

# Change to project root for the compliance checker
cd "$PROJECT_ROOT"

# Count agent files
AGENT_COUNT=$(find .claude/agents -name "*.md" -not -name "README.md" | wc -l)
echo -e "${BLUE}📊 Found ${AGENT_COUNT} agent files to validate${NC}"
echo

# Run the compliance checker
echo -e "${BLUE}🔍 Running agent compliance analysis...${NC}"
echo

if $VERBOSE; then
    python3 "$SCRIPT_DIR/agent-compliance-checker.py" --verbose
    COMPLIANCE_EXIT_CODE=$?
else
    python3 "$SCRIPT_DIR/agent-compliance-checker.py"
    COMPLIANCE_EXIT_CODE=$?
fi

echo
echo -e "${BLUE}🔗 Running chain configuration validation...${NC}"
echo

if $VERBOSE; then
    python3 "$SCRIPT_DIR/validate-chains.py" --verbose
    CHAIN_EXIT_CODE=$?
else
    python3 "$SCRIPT_DIR/validate-chains.py"
    CHAIN_EXIT_CODE=$?
fi

# Combine exit codes - fail if either check fails
OVERALL_EXIT_CODE=$((COMPLIANCE_EXIT_CODE + CHAIN_EXIT_CODE))

echo
echo "============================================="

if [[ $OVERALL_EXIT_CODE -eq 0 ]]; then
    echo -e "${GREEN}🎉 SUCCESS: All agents and chains are compliant!${NC}"
    echo -e "${GREEN}   Your agent architecture follows ADR-007 and ADR-008${NC}"
    echo
    echo -e "${BLUE}💡 Next steps:${NC}"
    echo -e "   • Continue developing with confidence"
    echo -e "   • Consider setting up git hooks: ln -sf ../../scripts/agent-validation/pre-commit-agent-check.sh .git/hooks/pre-commit"
    echo -e "   • Add CI/CD validation using .claude/hooks/ci-agent-validation.yml"
else
    echo -e "${YELLOW}⚠️  COMPLIANCE ISSUES FOUND${NC}"
    echo -e "${YELLOW}   Some agents need attention to follow the architecture${NC}"
    echo
    echo -e "${BLUE}🔧 How to fix:${NC}"
    echo -e "   1. Review the issues listed above"
    echo -e "   2. Update agents according to the guidance"
    echo -e "   3. Run this script again to verify fixes"
    echo
    echo -e "${BLUE}📚 Resources:${NC}"
    echo -e "   • docs/adr/adr-007-agent-system-architecture.md"
    echo -e "   • docs/adr/adr-008-cognitive-load-model-allocation.md"
    echo -e "   • .claude/agents/config/tool-permissions.yaml"
    echo
    if ! $VERBOSE; then
        echo -e "${BLUE}💡 For detailed analysis:${NC}"
        echo -e "   $0 --verbose"
    fi
fi

echo
echo -e "${PURPLE}🤖 Agent compliance check complete${NC}"

# Exit with the combined exit code
exit $OVERALL_EXIT_CODE
