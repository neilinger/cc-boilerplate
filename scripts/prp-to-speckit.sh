#!/bin/bash

# prp-to-speckit.sh - Transform PRP data to spec-kit format
# Usage: ./scripts/prp-to-speckit.sh [PRP_FILE] [OUTPUT_DIR] [--test]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Help function
show_help() {
    cat << EOF
prp-to-speckit.sh - Transform PRP data to spec-kit format

USAGE:
    $0 [PRP_FILE] [OUTPUT_DIR] [OPTIONS]

ARGUMENTS:
    PRP_FILE     Path to PRP markdown file
    OUTPUT_DIR   Directory to create spec-kit files

OPTIONS:
    --test                Run transformation tests
    --validate-kiss-yagni Check KISS/YAGNI compliance
    --dry-run            Show what would be done without creating files
    -h, --help           Show this help

EXAMPLES:
    # Transform prp-004 to spec-kit format
    $0 PRPs/prp-004-agent-system-redesign.md specs/004-agent-system/

    # Test transformation functions
    $0 --test

    # Validate KISS/YAGNI compliance
    $0 --validate-kiss-yagni specs/004-agent-system/

EOF
}

# Extract PRP sections using yq (if available) or fallback to sed/awk
extract_prp_section() {
    local prp_file="$1"
    local section="$2"

    # Try to extract YAML frontmatter if present
    if head -n 20 "$prp_file" | grep -q "^---$"; then
        # Has YAML frontmatter
        case "$section" in
            "goal")
                sed -n '/^## Goal$/,/^## /p' "$prp_file" | head -n -1 | tail -n +2
                ;;
            "why")
                sed -n '/^## Why$/,/^## /p' "$prp_file" | head -n -1 | tail -n +2
                ;;
            "what")
                sed -n '/^## What$/,/^## /p' "$prp_file" | head -n -1 | tail -n +2
                ;;
            "context")
                sed -n '/^## All Needed Context$/,/^## /p' "$prp_file" | head -n -1 | tail -n +2
                ;;
            "validation")
                sed -n '/^## Validation Loop$/,/^## /p' "$prp_file" | head -n -1 | tail -n +2
                ;;
            *)
                log_error "Unknown section: $section"
                return 1
                ;;
        esac
    else
        log_error "PRP file does not have proper structure"
        return 1
    fi
}

# Transform PRP Goal section to spec-kit specification format
transform_to_specification() {
    local prp_file="$1"
    local output_file="$2"

    log_info "Transforming PRP to specification format..."

    cat > "$output_file" << EOF
# Feature Specification

## Overview

$(extract_prp_section "$prp_file" "goal")

## Business Value

$(extract_prp_section "$prp_file" "why")

## Functional Requirements

$(extract_prp_section "$prp_file" "what")

## Context and Constraints

$(extract_prp_section "$prp_file" "context")

---

> **Generated from PRP**: This specification was automatically transformed from $(basename "$prp_file")
>
> **Next Phase**: Use \`/plan\` to create technical implementation plan
EOF

    log_info "Specification created: $output_file"
}

# Create constitution from CLAUDE.md and ADRs
create_constitution() {
    local output_dir="$1"
    local constitution_file="$output_dir/constitution.md"

    log_info "Creating constitution from CLAUDE.md and ADRs..."

    mkdir -p "$(dirname "$constitution_file")"

    cat > "$constitution_file" << EOF
# Project Constitution

## Development Principles

### From CLAUDE.md

$(if [ -f "$PROJECT_ROOT/CLAUDE.md" ]; then
    # Extract key principles from CLAUDE.md
    sed -n '/## Two Golden Rules/,/## /p' "$PROJECT_ROOT/CLAUDE.md" | head -n -1
fi)

### Architecture Decisions

$(if [ -d "$PROJECT_ROOT/docs/adr" ]; then
    echo "**Relevant ADRs:**"
    find "$PROJECT_ROOT/docs/adr" -name "adr-*.md" | sort | while read -r adr; do
        title=$(grep "^# " "$adr" | head -n 1 | sed 's/^# //')
        echo "- [$title]($adr)"
    done
fi)

### Quality Standards

- **KISS**: Keep It Simple, Stupid - Use the easiest way that works
- **YAGNI**: You Aren't Gonna Need It - Build only what's needed now
- **Context Engineering**: Automatic discovery over manual specification
- **Validation Gates**: KISS/YAGNI checks at each phase transition

---

> **Generated from**: CLAUDE.md and ADR documents
>
> **Purpose**: Establishes non-negotiable principles for spec-kit workflow
EOF

    log_info "Constitution created: $constitution_file"
}

# Validate KISS/YAGNI compliance
validate_kiss_yagni() {
    local spec_dir="$1"
    local violations=0

    log_info "Validating KISS/YAGNI compliance in $spec_dir..."

    # Check for over-engineering indicators
    for file in "$spec_dir"/*.md; do
        if [ -f "$file" ]; then
            log_info "Checking $(basename "$file")..."

            # Check for complexity indicators
            if grep -qi "microservice\|distributed\|scalable\|enterprise\|framework" "$file"; then
                log_warn "Potential YAGNI violation in $(basename "$file"): Complex patterns detected"
                violations=$((violations + 1))
            fi

            # Check for premature optimization
            if grep -qi "performance\|optimization\|cache\|redis\|memcache" "$file"; then
                log_warn "Potential YAGNI violation in $(basename "$file"): Premature optimization detected"
                violations=$((violations + 1))
            fi

            # Check for over-abstraction
            if grep -qi "abstract\|interface\|factory\|builder\|strategy" "$file"; then
                log_warn "Potential KISS violation in $(basename "$file"): Over-abstraction detected"
                violations=$((violations + 1))
            fi
        fi
    done

    if [ $violations -eq 0 ]; then
        log_info "✅ KISS/YAGNI validation passed"
        return 0
    else
        log_warn "⚠️  KISS/YAGNI validation found $violations potential violations"
        return 1
    fi
}

# Test transformation functions
run_tests() {
    log_info "Running transformation tests..."

    local test_prp="/tmp/test-prp.md"
    local test_output="/tmp/test-spec"

    # Create test PRP
    cat > "$test_prp" << 'EOF'
---
name: "Test PRP"
---

## Goal

**Feature Goal**: Test feature for validation

**Deliverable**: Test deliverable

## Why

- Test business value
- Test integration

## What

Test user-visible behavior

## All Needed Context

Test context information

## Validation Loop

Test validation approach
EOF

    # Test transformation
    mkdir -p "$test_output"

    if transform_to_specification "$test_prp" "$test_output/spec.md"; then
        log_info "✅ Transformation test passed"
    else
        log_error "❌ Transformation test failed"
        return 1
    fi

    if create_constitution "$test_output"; then
        log_info "✅ Constitution test passed"
    else
        log_error "❌ Constitution test failed"
        return 1
    fi

    # Cleanup
    rm -rf "$test_prp" "$test_output"

    log_info "All tests passed!"
    return 0
}

# Main function
main() {
    local prp_file=""
    local output_dir=""
    local dry_run=false
    local test_mode=false
    local validate_mode=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --test)
                test_mode=true
                shift
                ;;
            --validate-kiss-yagni)
                validate_mode=true
                shift
                ;;
            --dry-run)
                dry_run=true
                shift
                ;;
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
                elif [ -z "$output_dir" ]; then
                    output_dir="$1"
                else
                    log_error "Too many arguments"
                    show_help
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # Handle special modes
    if [ "$test_mode" = true ]; then
        run_tests
        exit $?
    fi

    if [ "$validate_mode" = true ]; then
        if [ -z "$prp_file" ]; then
            log_error "Validation mode requires spec directory"
            exit 1
        fi
        validate_kiss_yagni "$prp_file"
        exit $?
    fi

    # Validate required arguments
    if [ -z "$prp_file" ] || [ -z "$output_dir" ]; then
        log_error "PRP_FILE and OUTPUT_DIR are required"
        show_help
        exit 1
    fi

    # Validate input file exists
    if [ ! -f "$prp_file" ]; then
        log_error "PRP file not found: $prp_file"
        exit 1
    fi

    # Create output directory
    if [ "$dry_run" = false ]; then
        mkdir -p "$output_dir"
    else
        log_info "DRY RUN: Would create directory $output_dir"
    fi

    # Perform transformation
    if [ "$dry_run" = false ]; then
        transform_to_specification "$prp_file" "$output_dir/spec.md"
        create_constitution "$output_dir"

        log_info "Transformation complete!"
        log_info "Next steps:"
        log_info "  1. cd $output_dir"
        log_info "  2. Run /plan to create technical plan"
        log_info "  3. Run /tasks to create implementation breakdown"
        log_info "  4. Run /implement to execute with TDD"
    else
        log_info "DRY RUN: Would transform $prp_file to $output_dir/spec.md"
        log_info "DRY RUN: Would create constitution at $output_dir/constitution.md"
    fi
}

# Run main function
main "$@"