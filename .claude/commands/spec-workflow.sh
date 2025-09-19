#!/bin/bash

# spec-workflow.sh - Wrapper commands for PRP → Spec-Kit workflow
# Provides: /prp:to-spec, /prp:to-plan, /prp:validate commands

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TRANSFORMATION_SCRIPT="$PROJECT_ROOT/scripts/prp-to-speckit.sh"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[SPEC-WORKFLOW]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[SPEC-WORKFLOW]${NC} $1"
}

log_error() {
    echo -e "${RED}[SPEC-WORKFLOW]${NC} $1"
}

log_command() {
    echo -e "${BLUE}[COMMAND]${NC} $1"
}

# Show available commands
show_commands() {
    cat << EOF
Available Spec-Kit Workflow Commands:

${BLUE}/prp:to-spec${NC} [PRP_FILE]
    Transform PRP to spec-kit specification format
    Example: /prp:to-spec PRPs/prp-005-my-feature.md

${BLUE}/prp:to-plan${NC} [PRP_FILE]
    Transform PRP and proceed directly to /plan phase
    Example: /prp:to-plan PRPs/prp-005-my-feature.md

${BLUE}/prp:validate${NC} [SPEC_DIR]
    Validate KISS/YAGNI compliance in spec directory
    Example: /prp:validate specs/005-my-feature/

${BLUE}/prp:install-speckit${NC}
    Install spec-kit CLI tool in current project
    Runs: uvx --from git+https://github.com/github/spec-kit.git specify init . --ai claude

${BLUE}/prp:workflow-status${NC}
    Show current workflow status and next steps

Use any command with --help for detailed usage information.
EOF
}

# Install spec-kit CLI
install_speckit() {
    log_info "Installing spec-kit CLI tool..."

    if ! command -v uvx &> /dev/null; then
        log_error "uvx not found. Please install uvx first:"
        echo "  pip install uvx"
        return 1
    fi

    log_command "uvx --from git+https://github.com/github/spec-kit.git specify init . --ai claude --ignore-agent-tools"

    # Run the installation
    if uvx --from git+https://github.com/github/spec-kit.git specify init . --ai claude --ignore-agent-tools; then
        log_info "✅ Spec-kit installed successfully"
        log_info "Available commands: /constitution, /specify, /plan, /tasks, /implement"
        log_info "💡 With PRP integration, you'll typically skip /specify and /constitution"
        return 0
    else
        log_error "❌ Spec-kit installation failed"
        return 1
    fi
}

# Transform PRP to spec format
prp_to_spec() {
    local prp_file="$1"
    local feature_name=""
    local feature_number=""

    # Validate input
    if [ ! -f "$prp_file" ]; then
        log_error "PRP file not found: $prp_file"
        return 1
    fi

    # Extract feature info from filename
    if [[ $(basename "$prp_file") =~ prp-([0-9]+)-(.+)\.md ]]; then
        feature_number="${BASH_REMATCH[1]}"
        feature_name="${BASH_REMATCH[2]}"
    else
        log_error "PRP filename doesn't match pattern: prp-XXX-feature-name.md"
        return 1
    fi

    local output_dir="specs/${feature_number}-${feature_name}"

    log_info "Transforming PRP to spec-kit format..."
    log_info "  Input: $prp_file"
    log_info "  Output: $output_dir/"

    # Run transformation
    if "$TRANSFORMATION_SCRIPT" "$prp_file" "$output_dir"; then
        log_info "✅ Transformation successful"
        log_info "📁 Spec files created in: $output_dir/"
        log_info "📋 Next steps:"
        log_info "   1. cd $output_dir"
        log_info "   2. Run /plan to create technical plan"
        echo ""
        echo "Spec-kit workflow commands available:"
        echo "  /plan     - Create technical implementation plan"
        echo "  /tasks    - Break down into implementation tasks"
        echo "  /implement - Execute with TDD validation"
        return 0
    else
        log_error "❌ Transformation failed"
        return 1
    fi
}

# Transform PRP and proceed to planning
prp_to_plan() {
    local prp_file="$1"

    log_info "Transforming PRP and proceeding to planning phase..."

    # First transform to spec
    if ! prp_to_spec "$prp_file"; then
        return 1
    fi

    # Extract paths for next step
    local feature_name=""
    local feature_number=""
    if [[ $(basename "$prp_file") =~ prp-([0-9]+)-(.+)\.md ]]; then
        feature_number="${BASH_REMATCH[1]}"
        feature_name="${BASH_REMATCH[2]}"
    fi

    local spec_dir="specs/${feature_number}-${feature_name}"

    log_info "📋 Transformation complete. To continue with planning:"
    echo ""
    echo "Next steps:"
    echo "  1. cd $spec_dir"
    echo "  2. Review the generated spec.md"
    echo "  3. Run /plan to create technical implementation plan"
    echo ""
    echo "The spec.md contains all context from your PRP:"
    echo "  - Functional requirements (WHAT)"
    echo "  - Business value (WHY)"
    echo "  - Technical context for planning"
}

# Validate KISS/YAGNI compliance
prp_validate() {
    local spec_dir="$1"

    if [ ! -d "$spec_dir" ]; then
        log_error "Spec directory not found: $spec_dir"
        return 1
    fi

    log_info "Validating KISS/YAGNI compliance in $spec_dir..."

    if "$TRANSFORMATION_SCRIPT" --validate-kiss-yagni "$spec_dir"; then
        log_info "✅ Validation passed - No KISS/YAGNI violations detected"
        return 0
    else
        log_warn "⚠️  Validation found potential violations"
        log_info "Review the warnings above and consider simplifying the approach"
        return 1
    fi
}

# Show workflow status
workflow_status() {
    log_info "PRP → Spec-Kit Workflow Status"
    echo ""

    # Check if spec-kit is installed
    if [ -f "specify.sh" ] || [ -f "memory/constitution.md" ]; then
        echo "✅ Spec-kit: Installed"
    else
        echo "❌ Spec-kit: Not installed (run /prp:install-speckit)"
    fi

    # Check for PRP files
    local prp_count=$(find PRPs/ -name "prp-*.md" -not -name "prp-*template*" | wc -l | xargs)
    echo "📝 PRPs: $prp_count found"

    # Check for spec directories
    if [ -d "specs" ]; then
        local spec_count=$(find specs/ -mindepth 1 -maxdepth 1 -type d | wc -l | xargs)
        echo "📋 Specs: $spec_count directories in specs/"
    else
        echo "📋 Specs: None (no specs/ directory)"
    fi

    # Show recent PRPs
    echo ""
    echo "Recent PRPs:"
    find PRPs/ -name "prp-*.md" -not -name "*template*" | sort | tail -3 | while read -r prp; do
        local status="unknown"
        if grep -q "Status: PROPOSED" "$prp"; then
            status="PROPOSED"
        elif grep -q "Status: IN_PROGRESS" "$prp"; then
            status="IN_PROGRESS"
        elif grep -q "Status: COMPLETED" "$prp"; then
            status="COMPLETED"
        fi
        echo "  $(basename "$prp") [$status]"
    done

    echo ""
    echo "Available commands:"
    echo "  /prp:to-spec [PRP_FILE]    - Transform PRP to spec format"
    echo "  /prp:to-plan [PRP_FILE]    - Transform and proceed to planning"
    echo "  /prp:validate [SPEC_DIR]   - Validate KISS/YAGNI compliance"
}

# Main command dispatcher
main() {
    local command="${1:-}"

    case "$command" in
        "to-spec"|"prp:to-spec")
            shift
            if [ $# -eq 0 ]; then
                log_error "Usage: /prp:to-spec [PRP_FILE]"
                return 1
            fi
            prp_to_spec "$1"
            ;;
        "to-plan"|"prp:to-plan")
            shift
            if [ $# -eq 0 ]; then
                log_error "Usage: /prp:to-plan [PRP_FILE]"
                return 1
            fi
            prp_to_plan "$1"
            ;;
        "validate"|"prp:validate")
            shift
            if [ $# -eq 0 ]; then
                log_error "Usage: /prp:validate [SPEC_DIR]"
                return 1
            fi
            prp_validate "$1"
            ;;
        "install-speckit"|"prp:install-speckit")
            install_speckit
            ;;
        "workflow-status"|"prp:workflow-status"|"status")
            workflow_status
            ;;
        "help"|"--help"|"-h"|"")
            show_commands
            ;;
        *)
            log_error "Unknown command: $command"
            echo ""
            show_commands
            return 1
            ;;
    esac
}

# If script is being sourced, make functions available
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    # Being sourced - make functions available
    export -f prp_to_spec prp_to_plan prp_validate install_speckit workflow_status
    log_info "Spec-workflow commands loaded. Use /prp:to-spec, /prp:to-plan, /prp:validate"
else
    # Being executed directly
    main "$@"
fi