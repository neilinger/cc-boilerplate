#!/bin/bash

# generate-specs-from-prp.sh - Transform PRP content to spec-kit format with auto-architect
# Usage: ./scripts/generate-specs-from-prp.sh [PRP_FILE]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Functions
log_info() {
    echo -e "${GREEN}[SPEC-GEN]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[SPEC-GEN]${NC} $1"
}

log_error() {
    echo -e "${RED}[SPEC-GEN]${NC} $1"
}

log_command() {
    echo -e "${BLUE}[COMMAND]${NC} $1"
}

# Help function
show_help() {
    cat << EOF
generate-specs-from-prp.sh - Transform PRP content to spec-kit format with auto-architect

USAGE:
    $0 [PRP_FILE]

ARGUMENTS:
    PRP_FILE     Path to PRP markdown file

DESCRIPTION:
    Uses architect-review agent to automatically analyze the PRP and determine:
    - Whether feature needs single or multiple specs
    - What architectural components are required (frontend/backend/infrastructure)
    - Proper architectural boundaries and separation of concerns

EXAMPLES:
    # Auto-architect analysis
    $0 PRPs/prp-007-user-profile.md
    # → Agent determines: single spec for simple CRUD

    $0 PRPs/prp-008-auth-system.md
    # → Agent determines: multiple specs (frontend, backend, infrastructure)

NAMING CONVENTION:
    PRPs/prp-{3-digit-number}-{feature-name}.md
    →
    Single: specs/{3-digit-number}-{feature-name}/spec.md
    Multiple: specs/{3-digit-number}-{feature-name}-{component}/spec.md

EOF
}

# Use architect-review agent to analyze PRP and determine spec structure
analyze_with_architect() {
    local prp_file="$1"

    log_info "Using architect-review agent to analyze PRP structure..." >&2
    log_warn "Auto-architect analysis: Using heuristic until agent integration complete" >&2

    # Simple heuristic based on PRP content
    if grep -qi "frontend\|ui\|interface\|react\|vue\|angular" "$prp_file" && \
       grep -qi "backend\|api\|server\|database\|microservice" "$prp_file"; then
        echo '{"type": "multiple", "specs": ["frontend", "backend"], "reasoning": "Feature involves both UI and API components"}'
    elif grep -qi "infrastructure\|deployment\|docker\|kubernetes\|aws\|cloud" "$prp_file"; then
        if grep -qi "frontend\|backend" "$prp_file"; then
            echo '{"type": "multiple", "specs": ["frontend", "backend", "infrastructure"], "reasoning": "Full-stack feature with infrastructure requirements"}'
        else
            echo '{"type": "multiple", "specs": ["backend", "infrastructure"], "reasoning": "Backend feature with infrastructure requirements"}'
        fi
    else
        echo '{"type": "single", "reasoning": "Cohesive feature suitable for single specification"}'
    fi
}

# Extract PRP sequence number and feature name from filename
extract_prp_info() {
    local prp_file="$1"
    local filename=$(basename "$prp_file" .md)

    # Pattern: prp-XXX-feature-name
    if [[ $filename =~ ^prp-([0-9]{3})-(.+)$ ]]; then
        PRP_NUMBER="${BASH_REMATCH[1]}"
        FEATURE_NAME="${BASH_REMATCH[2]}"
        log_info "Extracted: Number=$PRP_NUMBER, Feature=$FEATURE_NAME"
    else
        log_error "PRP filename must match pattern: prp-XXX-feature-name.md"
        log_error "Got: $filename"
        return 1
    fi
}

# Extract content from PRP sections
extract_prp_section() {
    local prp_file="$1"
    local section="$2"

    case "$section" in
        "goal")
            awk '/^## Goal$/{flag=1; next} /^## /{flag=0} flag' "$prp_file"
            ;;
        "why")
            awk '/^## Why$/{flag=1; next} /^## /{flag=0} flag' "$prp_file"
            ;;
        "what")
            awk '/^## What$/{flag=1; next} /^## /{flag=0} flag' "$prp_file"
            ;;
        "context")
            awk '/^## All Needed Context$/{flag=1; next} /^## /{flag=0} flag' "$prp_file"
            ;;
        *)
            log_error "Unknown section: $section"
            return 1
            ;;
    esac
}

# Generate spec content from PRP
generate_spec_content() {
    local prp_file="$1"
    local component_name="$2"  # Empty for single spec, component name for multiple

    cat << EOF
# Feature Specification: $(extract_prp_section "$prp_file" "goal" | head -1 | sed 's/^.*Feature Goal.*: //')

## Overview

$(extract_prp_section "$prp_file" "goal")

## Business Value

$(extract_prp_section "$prp_file" "why")

## Functional Requirements

$(extract_prp_section "$prp_file" "what")

$(if [ -n "$component_name" ]; then
    echo "### Component Focus: $component_name"
    echo ""
    echo "This specification focuses on the **$component_name** component of the overall feature."
    echo ""
fi)

## Context and Constraints

$(extract_prp_section "$prp_file" "context")

---

> **Generated from PRP**: $(basename "$prp_file")
> **Generation Date**: $(date '+%Y-%m-%d %H:%M:%S')
$(if [ -n "$component_name" ]; then
    echo "> **Component**: $component_name"
fi)
>
> **Next Phase**: Use \`/plan\` to create technical implementation plan
EOF
}

# Create single spec
create_single_spec() {
    local prp_file="$1"
    local spec_dir="specs/${PRP_NUMBER}-${FEATURE_NAME}"
    local spec_file="$spec_dir/spec.md"

    log_info "Creating single spec: $spec_file"

    # Create directory
    mkdir -p "$spec_dir"

    # Generate spec content
    generate_spec_content "$prp_file" "" > "$spec_file"

    log_info "✅ Created: $spec_file"
    echo "$spec_file"
}

# Create multiple specs
create_multiple_specs() {
    local prp_file="$1"
    local components_json="$2"
    local created_specs=()

    # Parse components from JSON
    local components=($(echo "$components_json" | jq -r '.specs[]'))

    log_info "Creating ${#components[@]} specs for components: ${components[*]}"

    for component in "${components[@]}"; do
        local spec_dir="specs/${PRP_NUMBER}-${FEATURE_NAME}-${component}"
        local spec_file="$spec_dir/spec.md"

        log_info "Creating component spec: $spec_file"

        # Create directory
        mkdir -p "$spec_dir"

        # Generate spec content with component focus
        generate_spec_content "$prp_file" "$component" > "$spec_file"

        log_info "✅ Created: $spec_file"
        created_specs+=("$spec_file")
    done

    # Return all created specs
    printf '%s\n' "${created_specs[@]}"
}

# Create feature branch following naming convention
create_feature_branch() {
    local branch_name="feature/prp-${PRP_NUMBER}-${FEATURE_NAME}"

    log_info "Creating feature branch: $branch_name"

    # Check if branch already exists
    if git show-ref --verify --quiet "refs/heads/$branch_name"; then
        log_warn "Branch $branch_name already exists"
        git checkout "$branch_name"
    else
        git checkout -b "$branch_name"
        log_info "✅ Created and switched to branch: $branch_name"
    fi

    echo "$branch_name"
}

# Update PRP status
update_prp_status() {
    local prp_file="$1"
    local spec_files=("$@")
    spec_files=("${spec_files[@]:1}")  # Remove first element (prp_file)

    local today=$(date '+%Y-%m-%d')
    local spec_list=$(printf ', %s' "${spec_files[@]}")
    spec_list=${spec_list:2}  # Remove leading comma and space

    log_info "Updating PRP status to IN_PROGRESS"

    # Create a temporary file for safe editing
    local temp_file="/tmp/prp_update_$$"

    # Use awk for safer text replacement that handles special characters
    awk -v today="$today" -v spec_list="$spec_list" '
    /^Status: PROPOSED/ { gsub(/PROPOSED/, "IN_PROGRESS"); print; next }
    /^Status_Date: / { print "Status_Date: " today; next }
    /^Status_Note: / { print "Status_Note: Spec files created: " spec_list ". Ready for /plan phase."; next }
    { print }
    ' "$prp_file" > "$temp_file"

    # Replace original file
    mv "$temp_file" "$prp_file"

    log_info "✅ Updated PRP status"
}

# Main function
main() {
    local prp_file=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -*)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
            *)
                if [ -z "$prp_file" ]; then
                    prp_file="$1"
                else
                    log_error "Too many arguments. Only PRP_FILE is required."
                    show_help
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # Validate required arguments
    if [ -z "$prp_file" ]; then
        log_error "PRP_FILE is required"
        show_help
        exit 1
    fi

    # Validate input file exists
    if [ ! -f "$prp_file" ]; then
        log_error "PRP file not found: $prp_file"
        exit 1
    fi

    # Extract PRP info
    extract_prp_info "$prp_file"

    # Use architect agent to analyze and determine spec structure
    local spec_config=$(analyze_with_architect "$prp_file")

    log_info "Architect analysis complete"

    # Validate JSON
    if ! echo "$spec_config" | jq empty 2>/dev/null; then
        log_error "Invalid JSON from architect analysis"
        exit 1
    fi

    # Parse spec type
    local spec_type=$(echo "$spec_config" | jq -r '.type')
    local reasoning=$(echo "$spec_config" | jq -r '.reasoning')
    local created_specs=()

    log_info "Decision: $spec_type ($reasoning)"

    case "$spec_type" in
        "single")
            created_specs=($(create_single_spec "$prp_file"))
            ;;
        "multiple")
            created_specs=($(create_multiple_specs "$prp_file" "$spec_config"))
            ;;
        *)
            log_error "Invalid spec type: $spec_type (must be 'single' or 'multiple')"
            exit 1
            ;;
    esac

    # Create feature branch
    local branch_name=$(create_feature_branch)

    # Update PRP status
    update_prp_status "$prp_file" "${created_specs[@]}"

    # Summary
    log_info "🎉 Spec generation complete!"
    echo ""
    echo "📁 Created specs:"
    printf '   %s\n' "${created_specs[@]}"
    echo ""
    echo "🌿 Branch: $branch_name"
    echo "📋 PRP Status: IN_PROGRESS"
    echo "🧠 Architect Decision: $reasoning"
    echo ""
    echo "🚀 Next steps:"
    echo "   1. cd to a spec directory"
    echo "   2. Run /plan to create technical plan"
    echo "   3. Run /tasks to create implementation breakdown"
    echo "   4. Run /implement to execute with TDD"
}

# Run main function
main "$@"