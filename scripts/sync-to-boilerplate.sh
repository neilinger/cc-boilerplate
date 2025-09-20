#!/usr/bin/env bash
set -euo pipefail

# CC-Boilerplate Development to Deliverable Sync Script
# Syncs development content (.claude/, docs/adr/, PRPs/) to boilerplate/ deliverable

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
    BACKUP=true
    STATS=true

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
            --no-backup)
                BACKUP=false
                shift
                ;;
            --no-stats)
                STATS=false
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

show_help() {
    cat << EOF
${BOLD}CC-Boilerplate Development to Deliverable Sync${RESET}

Synchronizes development content to boilerplate/ deliverable directory.

${BOLD}Usage:${RESET}
  $0 [OPTIONS]

${BOLD}Options:${RESET}
  --dry-run      Show what would be synced without making changes
  --verbose      Show detailed sync operations
  --no-backup    Skip creating backup before sync
  --no-stats     Skip showing before/after statistics
  -h, --help     Show this help message

${BOLD}What gets synced:${RESET}
  .claude/              → boilerplate/.claude/
  docs/adr/             → boilerplate/docs/adr/
  PRPs/                 → boilerplate/PRPs/
  setup.sh              → boilerplate/setup.sh
  .env.sample           → boilerplate/.env.sample
  .mcp.json.sample      → boilerplate/.mcp.json.sample

${BOLD}Examples:${RESET}
  $0                    # Full sync with backup
  $0 --dry-run          # Preview what would be synced
  $0 --verbose          # Show detailed operations
EOF
}

# Check prerequisites
check_prerequisites() {
    info "Checking prerequisites..."

    # Check we're in the right directory
    if [[ ! -f "scripts/sync-to-boilerplate.sh" ]]; then
        abort "Must be run from cc-boilerplate root directory"
    fi

    # Check required tools
    command -v rsync >/dev/null 2>&1 || abort "rsync is required but not installed"

    # Check source directories exist
    [[ -d ".claude" ]] || abort "Source directory .claude/ not found"
    [[ -d "docs/adr" ]] || abort "Source directory docs/adr/ not found"
    [[ -d "PRPs" ]] || abort "Source directory PRPs/ not found"

    # Create boilerplate directory if it doesn't exist
    if [[ ! -d "boilerplate" ]]; then
        if [[ "$DRY_RUN" == "true" ]]; then
            info "[DRY RUN] Would create boilerplate/ directory"
        else
            mkdir -p boilerplate
            success "Created boilerplate/ directory"
        fi
    fi

    success "Prerequisites check passed"
}

# Show statistics
show_stats() {
    if [[ "$STATS" == "false" ]]; then
        return
    fi

    local title="$1"
    echo ""
    echo "${BOLD}${title}${RESET}"
    echo "===================="

    echo ""
    echo "${BLUE}Agent Files:${RESET}"
    echo "  Development (.claude/agents/): $(find .claude/agents -name "*.md" 2>/dev/null | wc -l | tr -d ' ') files"
    echo "  Boilerplate: $(find boilerplate/.claude/agents -name "*.md" 2>/dev/null | wc -l | tr -d ' ') files"

    echo ""
    echo "${BLUE}Specialists:${RESET}"
    echo "  Development (.claude/agents/specialists/): $(ls .claude/agents/specialists/*.md 2>/dev/null | wc -l | tr -d ' ') files"
    echo "  Boilerplate: $(ls boilerplate/.claude/agents/specialists/*.md 2>/dev/null | wc -l | tr -d ' ') files"

    echo ""
    echo "${BLUE}ADRs:${RESET}"
    echo "  Development (docs/adr/): $(ls docs/adr/*.md 2>/dev/null | wc -l | tr -d ' ') files"
    echo "  Boilerplate: $(ls boilerplate/docs/adr/*.md 2>/dev/null | wc -l | tr -d ' ') files"

    echo ""
    echo "${BLUE}PRPs:${RESET}"
    echo "  Development (PRPs/): $(ls PRPs/*.md 2>/dev/null | wc -l | tr -d ' ') files"
    echo "  Boilerplate: Structure only (README, templates, code_reviews)"

    echo ""
    echo "${BLUE}CLAUDE.md Template:${RESET}"
    if [[ -f "CLAUDE.md" ]]; then
        echo "  Development: CLAUDE.md (exists)"
    else
        echo "  Development: CLAUDE.md (missing)"
    fi
    if [[ -f "boilerplate/CLAUDE.template.md" ]]; then
        echo "  Boilerplate: CLAUDE.template.md (exists)"
    else
        echo "  Boilerplate: CLAUDE.template.md (missing)"
    fi

    echo ""
    echo "${BLUE}Total MD Files:${RESET}"
    echo "  Development: $(find .claude docs/adr PRPs -name "*.md" 2>/dev/null | wc -l | tr -d ' ') files"
    echo "  Boilerplate: $(find boilerplate/.claude boilerplate/docs/adr boilerplate/PRPs -name "*.md" 2>/dev/null | wc -l | tr -d ' ') files + template"
    echo ""
}

# Create backup
create_backup() {
    if [[ "$BACKUP" == "false" ]]; then
        return
    fi

    if [[ ! -d "boilerplate" ]]; then
        info "No existing boilerplate/ to backup"
        return
    fi

    local backup_dir="boilerplate.backup.$(date +%Y%m%d_%H%M%S)"

    if [[ "$DRY_RUN" == "true" ]]; then
        info "[DRY RUN] Would create backup at $backup_dir"
    else
        info "Creating backup at $backup_dir..."
        cp -r boilerplate "$backup_dir"
        success "Backup created at $backup_dir"
    fi
}

# Sync a directory with detailed logging
sync_directory() {
    local src="$1"
    local dest="$2"
    local description="$3"

    if [[ ! -d "$src" ]]; then
        warn "Source directory $src does not exist, skipping"
        return
    fi

    if [[ "$VERBOSE" == "true" ]]; then
        info "Syncing $description: $src → $dest"
    fi

    # Create destination parent directory
    local dest_parent=$(dirname "$dest")
    if [[ ! -d "$dest_parent" ]]; then
        if [[ "$DRY_RUN" == "true" ]]; then
            [[ "$VERBOSE" == "true" ]] && info "[DRY RUN] Would create directory $dest_parent"
        else
            mkdir -p "$dest_parent"
            [[ "$VERBOSE" == "true" ]] && info "Created directory $dest_parent"
        fi
    fi

    # Perform sync
    local rsync_opts="-av --delete"
    if [[ "$DRY_RUN" == "true" ]]; then
        rsync_opts="$rsync_opts --dry-run"
    fi
    if [[ "$VERBOSE" == "false" ]]; then
        rsync_opts="$rsync_opts --quiet"
    fi

    if rsync $rsync_opts "$src/" "$dest/"; then
        if [[ "$DRY_RUN" == "true" ]]; then
            [[ "$VERBOSE" == "true" ]] && success "[DRY RUN] Would sync $description"
        else
            success "Synced $description"
        fi
    else
        abort "Failed to sync $description"
    fi
}

# Sync a single file
sync_file() {
    local src="$1"
    local dest="$2"
    local description="$3"

    if [[ ! -f "$src" ]]; then
        warn "Source file $src does not exist, skipping"
        return
    fi

    if [[ "$VERBOSE" == "true" ]]; then
        info "Syncing $description: $src → $dest"
    fi

    # Create destination directory if needed
    local dest_dir=$(dirname "$dest")
    if [[ ! -d "$dest_dir" ]]; then
        if [[ "$DRY_RUN" == "true" ]]; then
            [[ "$VERBOSE" == "true" ]] && info "[DRY RUN] Would create directory $dest_dir"
        else
            mkdir -p "$dest_dir"
            [[ "$VERBOSE" == "true" ]] && info "Created directory $dest_dir"
        fi
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        [[ "$VERBOSE" == "true" ]] && success "[DRY RUN] Would sync $description"
    else
        if cp "$src" "$dest"; then
            success "Synced $description"
        else
            abort "Failed to sync $description"
        fi
    fi
}

# Sync PRPs structure only (not actual PRP files)
sync_prps_structure() {
    info "Syncing PRPs structure (README, templates, code_reviews) to boilerplate..."

    if [[ ! -d "PRPs" ]]; then
        warn "Source directory PRPs/ does not exist, skipping"
        return
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        info "[DRY RUN] Would create boilerplate/PRPs/ structure"
        info "[DRY RUN] Would sync README.md, templates/, and code_reviews/"
    else
        # Create PRPs directory structure
        mkdir -p boilerplate/PRPs

        # Sync README.md if it exists
        if [[ -f "PRPs/README.md" ]]; then
            cp PRPs/README.md boilerplate/PRPs/README.md
            success "Synced PRPs/README.md"
        fi

        # Sync templates/ directory if it exists
        if [[ -d "PRPs/templates" ]]; then
            sync_directory "PRPs/templates" "boilerplate/PRPs/templates" "PRP templates"
        fi

        # Sync code_reviews/ directory if it exists
        if [[ -d "PRPs/code_reviews" ]]; then
            sync_directory "PRPs/code_reviews" "boilerplate/PRPs/code_reviews" "PRP code reviews"
        fi

        success "Synced PRPs structure (excluding actual PRP files)"
    fi
}

# Sync CLAUDE.md as template
sync_claude_template() {
    info "Syncing CLAUDE.md to boilerplate as CLAUDE.template.md..."

    if [[ ! -f "CLAUDE.md" ]]; then
        warn "Source file CLAUDE.md does not exist, skipping"
        return
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        info "[DRY RUN] Would copy CLAUDE.md to boilerplate/CLAUDE.template.md"
        info "[DRY RUN] Would replace project-specific references with placeholders"
    else
        # Copy CLAUDE.md as template
        cp CLAUDE.md boilerplate/CLAUDE.template.md

        # Replace project-specific references with placeholders
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' 's/cc-boilerplate/{{PROJECT_NAME}}/g' boilerplate/CLAUDE.template.md
        else
            # Linux
            sed -i 's/cc-boilerplate/{{PROJECT_NAME}}/g' boilerplate/CLAUDE.template.md
        fi

        success "Synced CLAUDE.md as CLAUDE.template.md"
    fi
}

# Clean data directory after .claude sync
clean_data_directory() {
    info "Cleaning boilerplate/.claude/data/ directory..."

    if [[ "$DRY_RUN" == "true" ]]; then
        info "[DRY RUN] Would remove all contents from boilerplate/.claude/data/"
    else
        if [[ -d "boilerplate/.claude/data" ]]; then
            find boilerplate/.claude/data -type f -delete 2>/dev/null || true
            find boilerplate/.claude/data -type d -empty -delete 2>/dev/null || true
            mkdir -p boilerplate/.claude/data
            success "Cleaned boilerplate/.claude/data/ directory"
        fi
    fi
}

# Perform the sync
perform_sync() {
    info "Starting synchronization..."

    # Sync .claude/ directory
    sync_directory ".claude" "boilerplate/.claude" "Claude Code configuration"

    # Clean data directory after .claude sync
    clean_data_directory

    # Sync docs/adr/ directory
    sync_directory "docs/adr" "boilerplate/docs/adr" "Architecture Decision Records"

    # Sync PRPs/ structure only (not actual PRP files)
    sync_prps_structure

    # Sync individual files
    sync_file "setup.sh" "boilerplate/setup.sh" "Setup script"
    sync_file ".env.sample" "boilerplate/.env.sample" "Environment template"
    sync_file ".mcp.json.sample" "boilerplate/.mcp.json.sample" "MCP configuration template"

    # Sync CLAUDE.md as template
    sync_claude_template

    # Sync scripts directory (needed for users)
    sync_directory "scripts" "boilerplate/scripts" "Scripts directory"

    # Ensure boilerplate manifest exists
    if [[ ! -f "boilerplate/.boilerplate-manifest.json" ]]; then
        warn "Boilerplate manifest not found - this may cause issues with updates"
    fi

    success "Synchronization completed!"
}

# Validate sync results
validate_sync() {
    if [[ "$DRY_RUN" == "true" ]]; then
        info "Skipping validation in dry-run mode"
        return
    fi

    info "Validating sync results..."

    local errors=0

    # Check critical directories exist
    for dir in ".claude/agents/specialists" ".claude/agents/analyzers" ".claude/agents/orchestrators" "docs/adr" "PRPs"; do
        if [[ ! -d "boilerplate/$dir" ]]; then
            warn "Missing directory: boilerplate/$dir"
            ((errors++))
        fi
    done

    # Check critical files exist
    for file in "setup.sh" ".env.sample" ".mcp.json.sample"; do
        if [[ ! -f "boilerplate/$file" ]]; then
            warn "Missing file: boilerplate/$file"
            ((errors++))
        fi
    done

    # Check we have specialists
    local specialist_count=$(ls boilerplate/.claude/agents/specialists/*.md 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$specialist_count" -lt 20 ]]; then
        warn "Only $specialist_count specialist agents found (expected 20+)"
        ((errors++))
    fi

    # Check we have ADRs
    local adr_count=$(ls boilerplate/docs/adr/*.md 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$adr_count" -lt 5 ]]; then
        warn "Only $adr_count ADRs found (expected 5+)"
        ((errors++))
    fi

    if [[ $errors -eq 0 ]]; then
        success "Validation passed - sync appears complete"
    else
        warn "Validation found $errors issues"
    fi
}

# Main execution
main() {
    setup_colors
    parse_args "$@"

    echo "${BOLD}========================================"
    echo "   CC-Boilerplate Development Sync"
    echo "========================================${RESET}"
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        warn "DRY RUN MODE - No changes will be made"
        echo ""
    fi

    check_prerequisites

    show_stats "BEFORE SYNC"

    create_backup
    perform_sync
    validate_sync

    show_stats "AFTER SYNC"

    echo ""
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "${BLUE}${BOLD}To perform the actual sync, run:${RESET}"
        echo "${GREEN}$0${RESET}"
    else
        echo "${GREEN}${BOLD}✅ Sync completed successfully!${RESET}"
        echo ""
        echo "${BLUE}Next steps:${RESET}"
        echo "1. Test with: ${GREEN}./scripts/init-boilerplate.sh${RESET}"
        echo "2. Commit changes: ${GREEN}git add boilerplate/ && git commit -m 'sync: update boilerplate with latest development'${RESET}"
    fi
    echo ""
}

# Run main function
main "$@"