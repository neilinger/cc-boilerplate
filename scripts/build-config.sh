#!/usr/bin/env bash
set -euo pipefail

# CC-Boilerplate Configuration Builder
# Merges base templates with project customizations

# Color setup
setup_colors() {
    if [[ -t 1 ]] && command -v tput >/dev/null 2>&1; then
        RED=$(tput setaf 1)
        GREEN=$(tput setaf 2)
        BLUE=$(tput setaf 4)
        YELLOW=$(tput setaf 3)
        BOLD=$(tput bold)
        RESET=$(tput sgr0)
    else
        RED="" GREEN="" BLUE="" YELLOW="" BOLD="" RESET=""
    fi
}

# Error handling
abort() {
    echo "${RED}❌ $1${RESET}" >&2
    exit 1
}

success() {
    echo "${GREEN}✅ $1${RESET}"
}

info() {
    echo "${BLUE}ℹ️  $1${RESET}"
}

warn() {
    echo "${YELLOW}⚠️  $1${RESET}"
}

# Parse command line arguments
parse_args() {
    DRY_RUN=false
    VERBOSE=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                abort "Unknown option: $1"
                ;;
        esac
    done
}

# Show help
show_help() {
    cat <<EOF
CC-Boilerplate Configuration Builder

Usage: $0 [OPTIONS]

Options:
  --dry-run     Show what would be generated without writing files
  --verbose     Show detailed merge process
  -h, --help    Show this help message

Examples:
  $0                    # Build configurations
  $0 --dry-run          # Show what would be generated
  $0 --verbose          # Verbose rebuild
EOF
}

# Check requirements
check_requirements() {
    command -v jq >/dev/null 2>&1 || abort "jq is required but not installed"

    # Check for required directories and files
    [[ -d ".claude/boilerplate" ]] || abort "Boilerplate not found. Run init-boilerplate.sh first"

    # Check for template files with helpful error messages
    if [[ ! -f ".claude/boilerplate/.claude/settings.template.json" ]]; then
        echo "❌ Settings template not found at: .claude/boilerplate/.claude/settings.template.json"
        echo "📁 Contents of .claude/boilerplate/:"
        ls -la .claude/boilerplate/ 2>/dev/null || echo "   Directory not found or empty"
        echo "📁 Contents of .claude/boilerplate/.claude/:"
        ls -la .claude/boilerplate/.claude/ 2>/dev/null || echo "   Directory not found or empty"
        abort "Settings template not found. Boilerplate installation may be incomplete."
    fi

    if [[ ! -f ".claude/boilerplate/templates/CLAUDE.template.md" ]]; then
        echo "❌ CLAUDE template not found at: .claude/boilerplate/templates/CLAUDE.template.md"
        echo "📁 Contents of .claude/boilerplate/templates/:"
        ls -la .claude/boilerplate/templates/ 2>/dev/null || echo "   Directory not found or empty"
        abort "CLAUDE template not found. Boilerplate installation may be incomplete."
    fi

    # Create project directory if it doesn't exist
    mkdir -p .claude/project

    # Create build directory
    mkdir -p .claude/build
}

# Atomic file replacement
safe_replace() {
    local target="$1"
    local content="$2"

    if [[ "$DRY_RUN" == "true" ]]; then
        info "Would write to $target (${#content} characters)"
        return 0
    fi

    local tmpfile
    tmpfile=$(mktemp "${target}.tmp.XXXXXX")
    echo "$content" > "$tmpfile"

    if mv "$tmpfile" "$target"; then
        [[ "$VERBOSE" == "true" ]] && info "Generated $target"
    else
        rm -f "$tmpfile"
        abort "Failed to write $target"
    fi
}

# Merge JSON files with jq
merge_json_settings() {
    local base_template=".claude/boilerplate/.claude/settings.template.json"
    local project_settings=".claude/project/settings.project.json"
    local output=".claude/settings.json"

    info "Merging JSON settings..."

    # Create default project settings if they don't exist
    if [[ ! -f "$project_settings" ]]; then
        cat > "$project_settings" <<EOF
{
  "__PROJECT_CUSTOM_PERMISSIONS__": [],
  "__PROJECT_CUSTOM_SETTINGS__": {},
  "__PROJECT_CUSTOM_HOOKS__": {}
}
EOF
        [[ "$VERBOSE" == "true" ]] && info "Created default $project_settings"
    fi

    # Validate JSON files
    jq empty "$base_template" || abort "Invalid JSON in $base_template"
    jq empty "$project_settings" || abort "Invalid JSON in $project_settings"

    # Merge JSON with custom logic for project placeholders
    local merged_json
    merged_json=$(jq -s '
        .[0] as $base | .[1] as $project |
        $base |
        # Merge permissions
        .permissions.allow += ($project.__PROJECT_CUSTOM_PERMISSIONS__ // []) |
        del(.permissions.__PROJECT_CUSTOM_PERMISSIONS__) |
        # Merge custom settings
        . * ($project.__PROJECT_CUSTOM_SETTINGS__ // {}) |
        del(.__PROJECT_CUSTOM_SETTINGS__) |
        # Merge custom hooks
        .hooks = (.hooks + ($project.__PROJECT_CUSTOM_HOOKS__ // {})) |
        del(.hooks.__PROJECT_CUSTOM_HOOKS__)
    ' "$base_template" "$project_settings")

    if [[ -z "$merged_json" ]]; then
        abort "Failed to merge JSON settings"
    fi

    # Validate merged JSON
    echo "$merged_json" | jq empty || abort "Generated invalid JSON"

    safe_replace "$output" "$merged_json"
    success "JSON settings merged → $output"
}

# Extract section between markers
extract_section() {
    local file="$1"
    local start_marker="$2"
    local end_marker="$3"

    if [[ ! -f "$file" ]]; then
        return 0
    fi

    sed -n "/$start_marker/,/$end_marker/p" "$file" | sed '1d;$d'
}

# Merge Markdown files with section markers
merge_markdown() {
    local base_template=".claude/boilerplate/templates/CLAUDE.template.md"
    local project_md=".claude/project/CLAUDE.project.md"
    local output="CLAUDE.md"

    info "Merging Markdown configuration..."

    # Read base template
    local base_content
    base_content=$(cat "$base_template")

    # Extract project customizations if they exist
    local project_content=""
    if [[ -f "$project_md" ]]; then
        project_content=$(cat "$project_md")
        [[ "$VERBOSE" == "true" ]] && info "Found project customizations in $project_md"
    fi

    # Replace the project section placeholder with actual content
    local merged_content
    if [[ -n "$project_content" ]]; then
        merged_content=$(echo "$base_content" | sed "
            /<!-- BEGIN PROJECT -->/,/<!-- END PROJECT -->/c\\
$project_content
        ")
    else
        merged_content="$base_content"
    fi

    safe_replace "$output" "$merged_content"
    success "Markdown configuration merged → $output"
}

# Merge YAML files (manual approach since yq is not available)
merge_yaml() {
    local base_file=".claude/boilerplate/templates/.pre-commit-config.template.yaml"
    local project_file=".claude/project/.pre-commit-config.project.yaml"
    local output=".pre-commit-config.yaml"

    # Skip if base template doesn't exist
    if [[ ! -f "$base_file" ]]; then
        [[ "$VERBOSE" == "true" ]] && info "No pre-commit template found, skipping YAML merge"
        return 0
    fi

    info "Merging YAML configuration..."

    # For now, just copy base if no project customizations exist
    if [[ ! -f "$project_file" ]]; then
        cp "$base_file" "$output"
    else
        # Simple concatenation approach - could be enhanced with yq
        {
            cat "$base_file"
            echo ""
            echo "# Project-specific additions:"
            cat "$project_file"
        } > "$output"
    fi

    success "YAML configuration merged → $output"
}

# Validate generated files
validate_generated_files() {
    info "Validating generated files..."

    local errors=0

    # Validate JSON
    if [[ -f ".claude/settings.json" ]]; then
        if jq empty .claude/settings.json 2>/dev/null; then
            [[ "$VERBOSE" == "true" ]] && success "settings.json is valid"
        else
            warn "Generated settings.json is invalid"
            ((errors++))
        fi
    fi

    # Check Markdown structure
    if [[ -f "CLAUDE.md" ]]; then
        if grep -q "# CLAUDE.md" CLAUDE.md; then
            [[ "$VERBOSE" == "true" ]] && success "CLAUDE.md structure looks good"
        else
            warn "Generated CLAUDE.md may have structural issues"
            ((errors++))
        fi
    fi

    # Check for leftover markers
    for file in CLAUDE.md .claude/settings.json; do
        if [[ -f "$file" ]] && grep -q "__PROJECT_CUSTOM" "$file" 2>/dev/null; then
            warn "Found unresolved placeholders in $file"
            ((errors++))
        fi
    done

    if [[ $errors -eq 0 ]]; then
        success "All generated files validated successfully"
    else
        warn "$errors validation issues found"
        return 1
    fi
}

# Create manifest of generated files
create_manifest() {
    local manifest=".claude/build/manifest.json"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    local files=()
    [[ -f "CLAUDE.md" ]] && files+=("CLAUDE.md")
    [[ -f ".claude/settings.json" ]] && files+=(".claude/settings.json")
    [[ -f ".pre-commit-config.yaml" ]] && files+=(".pre-commit-config.yaml")

    local manifest_content
    manifest_content=$(jq -n \
        --arg timestamp "$timestamp" \
        --argjson files "$(printf '%s\n' "${files[@]}" | jq -R . | jq -s .)" \
        '{
            generated_at: $timestamp,
            generated_files: $files,
            source_template_dir: ".claude/boilerplate",
            source_project_dir: ".claude/project"
        }')

    safe_replace "$manifest" "$manifest_content"
    [[ "$VERBOSE" == "true" ]] && success "Build manifest created → $manifest"
}

# Show dry run summary
show_dry_run_summary() {
    echo ""
    info "DRY RUN - Files that would be generated:"
    echo "  📄 CLAUDE.md                    - Merged project instructions"
    echo "  ⚙️  .claude/settings.json       - Merged Claude settings"
    echo "  📝 .pre-commit-config.yaml     - Pre-commit configuration"
    echo "  📊 .claude/build/manifest.json  - Build manifest"
    echo ""
    info "Source files:"
    echo "  📁 .claude/boilerplate/         - Base templates"
    echo "  📁 .claude/project/             - Project customizations"
    echo ""
    info "To generate files, run without --dry-run"
}

# Check for update reminders
check_update_reminder() {
    if [[ -f ".boilerplate-version" ]]; then
        # Check if version file is older than 90 days
        if [[ $(find .boilerplate-version -mtime +90 2>/dev/null) ]]; then
            echo ""
            echo "${YELLOW}💡 Update Available${RESET}"
            echo "   Your boilerplate hasn't been updated in 90+ days."
            echo "   Check for updates: ${BLUE}scripts/update-boilerplate.sh --dry-run${RESET}"
            echo ""
        fi
    fi
}

# Show completion summary
show_completion() {
    echo ""
    echo "${GREEN}${BOLD}🏗️  Configuration Build Complete!${RESET}"
    echo ""
    info "Generated files:"

    if [[ -f "CLAUDE.md" ]]; then
        local claude_size
        claude_size=$(wc -c < CLAUDE.md)
        echo "  📄 CLAUDE.md (${claude_size} bytes)"
    fi

    if [[ -f ".claude/settings.json" ]]; then
        local settings_size
        settings_size=$(wc -c < .claude/settings.json)
        echo "  ⚙️  .claude/settings.json (${settings_size} bytes)"
    fi

    if [[ -f ".pre-commit-config.yaml" ]]; then
        local precommit_size
        precommit_size=$(wc -c < .pre-commit-config.yaml)
        echo "  📝 .pre-commit-config.yaml (${precommit_size} bytes)"
    fi

    echo ""
    info "Customization files:"
    echo "  📝 .claude/project/CLAUDE.project.md      - Edit for project instructions"
    echo "  ⚙️  .claude/project/settings.project.json - Edit for custom settings"
    echo ""
    info "Next time you update boilerplate, run this script again to rebuild"

    # Check for gentle update reminder
    check_update_reminder
}

# Main execution
main() {
    setup_colors

    echo "${BOLD}======================================"
    echo "    CC-Boilerplate Config Builder"
    echo "======================================${RESET}"
    echo ""

    parse_args "$@"
    check_requirements

    if [[ "$DRY_RUN" == "true" ]]; then
        show_dry_run_summary
        exit 0
    fi

    merge_json_settings
    merge_markdown
    merge_yaml
    validate_generated_files
    create_manifest
    show_completion
}

# Run main function
main "$@"
