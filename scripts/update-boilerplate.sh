#!/usr/bin/env bash
set -euo pipefail

# CC-Boilerplate Update Script
# Pulls updates from cc-boilerplate while preserving project customizations

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

# Cleanup function for trap
cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 && -n "${BACKUP_DIR:-}" ]]; then
        warn "Update failed. Attempting rollback..."
        rollback_changes
    fi
    exit $exit_code
}

# Set trap for cleanup
trap cleanup EXIT

# Check requirements
check_requirements() {
    command -v git >/dev/null 2>&1 || abort "Git is required but not installed"
    command -v jq >/dev/null 2>&1 || abort "jq is required but not installed"

    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        abort "Not in a git repository"
    fi

    if [[ ! -f ".boilerplate-version" ]]; then
        abort "Boilerplate not initialized. Run scripts/init-boilerplate.sh first"
    fi

    # Check if this is the source cc-boilerplate repository
    if [[ -d "boilerplate" && -f "boilerplate/CLAUDE.template.md" ]]; then
        info "Detected source cc-boilerplate repository"
        SELF_HOSTED=true
    elif [[ ! -d ".claude/boilerplate" ]]; then
        abort "Boilerplate directory not found. Run scripts/init-boilerplate.sh first"
    else
        SELF_HOSTED=false
    fi
}

# Parse command line arguments
parse_args() {
    DRY_RUN=false
    FORCE=false
    BRANCH=""
    SELF_HOSTED=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --force)
                FORCE=true
                shift
                ;;
            --branch)
                BRANCH="$2"
                shift 2
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
CC-Boilerplate Update Script

Usage: $0 [OPTIONS]

Options:
  --dry-run          Show what would be updated without making changes
  --force            Force update even if working directory is not clean
  --branch BRANCH    Update from specific branch (default: current tracking branch)
  -h, --help         Show this help message

Examples:
  $0                 # Update from current tracking branch
  $0 --dry-run       # Show what would be updated
  $0 --branch main   # Update from main branch
  $0 --force         # Force update with uncommitted changes
EOF
}

# Read current version info
read_version_info() {
    if ! VERSION_INFO=$(jq -r '.' .boilerplate-version 2>/dev/null); then
        abort "Failed to read .boilerplate-version file"
    fi

    CURRENT_VERSION=$(echo "$VERSION_INFO" | jq -r '.version // "unknown"')
    CURRENT_COMMIT=$(echo "$VERSION_INFO" | jq -r '.commit // "unknown"')
    CURRENT_BRANCH=$(echo "$VERSION_INFO" | jq -r '.branch // "main"')
    REPO_URL=$(echo "$VERSION_INFO" | jq -r '.repository // "https://github.com/neilinger/cc-boilerplate.git"')

    # Use specified branch or current tracking branch
    BRANCH=${BRANCH:-$CURRENT_BRANCH}
}

# Check for uncommitted changes
check_working_directory() {
    if [[ "$FORCE" == "false" && -n $(git status --porcelain) ]]; then
        warn "You have uncommitted changes:"
        git status --short
        echo ""
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            abort "Update cancelled"
        fi
    fi
}

# Check if remote exists and fetch latest
fetch_remote() {
    info "Fetching latest changes from cc-boilerplate..."

    if ! git remote get-url cc-boilerplate >/dev/null 2>&1; then
        warn "Remote 'cc-boilerplate' not found. Adding it..."
        git remote add cc-boilerplate "$REPO_URL"
    fi

    if git fetch cc-boilerplate "$BRANCH"; then
        success "Remote fetched successfully"
    else
        abort "Failed to fetch from cc-boilerplate remote"
    fi
}

# Get remote commit info
get_remote_info() {
    if [[ "$SELF_HOSTED" == "true" ]]; then
        # For self-hosted (source repo), get latest release tag
        REMOTE_TAG=$(gh api repos/neilinger/cc-boilerplate/releases/latest --jq '.tag_name' 2>/dev/null || echo "v1.6.0")
        REMOTE_COMMIT=$(git rev-parse HEAD 2>/dev/null || abort "Cannot get current commit")
        REMOTE_COMMIT_SHORT=${REMOTE_COMMIT:0:7}
        info "Self-hosted repository - current version: $CURRENT_VERSION, latest release: $REMOTE_TAG"

        # For self-hosted, check if we're ahead of the release tag
        if [[ "$CURRENT_VERSION" == "$REMOTE_TAG" ]]; then
            success "Already at latest release version ($CURRENT_VERSION)"
            exit 0
        fi
    else
        REMOTE_COMMIT=$(git rev-parse cc-boilerplate/"$BRANCH" 2>/dev/null || abort "Branch $BRANCH not found on remote")
        REMOTE_COMMIT_SHORT=${REMOTE_COMMIT:0:7}

        # Check if already up to date
        if [[ "$CURRENT_COMMIT" == "$REMOTE_COMMIT_SHORT" ]]; then
            success "Already up to date (commit: $CURRENT_COMMIT)"
            exit 0
        fi
    fi
}

# Create backup
create_backup() {
    local timestamp
    timestamp=$(date -u +"%Y%m%d_%H%M%S")
    BACKUP_DIR=".claude/backups/backup_$timestamp"

    info "Creating backup at $BACKUP_DIR..."
    mkdir -p "$BACKUP_DIR"

    if [[ "$SELF_HOSTED" == "true" ]]; then
        # For self-hosted, backup the actual .claude content
        [[ -d ".claude/agents" ]] && cp -r .claude/agents "$BACKUP_DIR/"
        [[ -d ".claude/commands" ]] && cp -r .claude/commands "$BACKUP_DIR/"
        [[ -d ".claude/hooks" ]] && cp -r .claude/hooks "$BACKUP_DIR/"
    else
        # Backup current boilerplate subtree
        [[ -d ".claude/boilerplate" ]] && cp -r .claude/boilerplate "$BACKUP_DIR/"
    fi

    # Backup current version file
    cp .boilerplate-version "$BACKUP_DIR/"

    # Backup current generated configs if they exist
    [[ -f "CLAUDE.md" ]] && cp CLAUDE.md "$BACKUP_DIR/"
    [[ -f ".claude/settings.json" ]] && cp .claude/settings.json "$BACKUP_DIR/"

    success "Backup created at $BACKUP_DIR"
}

# Rollback changes
rollback_changes() {
    if [[ -z "${BACKUP_DIR:-}" || ! -d "$BACKUP_DIR" ]]; then
        warn "No backup found for rollback"
        return 1
    fi

    warn "Rolling back changes..."

    if [[ "$SELF_HOSTED" == "true" ]]; then
        # For self-hosted, restore actual .claude content
        [[ -d "$BACKUP_DIR/agents" ]] && { rm -rf .claude/agents; cp -r "$BACKUP_DIR/agents" .claude/; }
        [[ -d "$BACKUP_DIR/commands" ]] && { rm -rf .claude/commands; cp -r "$BACKUP_DIR/commands" .claude/; }
        [[ -d "$BACKUP_DIR/hooks" ]] && { rm -rf .claude/hooks; cp -r "$BACKUP_DIR/hooks" .claude/; }
    else
        # Restore boilerplate subtree
        [[ -d "$BACKUP_DIR/boilerplate" ]] && { rm -rf .claude/boilerplate; cp -r "$BACKUP_DIR/boilerplate" .claude/; }
    fi

    # Restore version file
    cp "$BACKUP_DIR/.boilerplate-version" .

    # Restore generated configs
    [[ -f "$BACKUP_DIR/CLAUDE.md" ]] && cp "$BACKUP_DIR/CLAUDE.md" .
    [[ -f "$BACKUP_DIR/settings.json" ]] && cp "$BACKUP_DIR/settings.json" .claude/

    success "Rollback completed"
}

# Show what would be updated (dry run)
show_dry_run() {
    echo ""
    info "DRY RUN - Changes that would be made:"
    echo "  Current commit: $CURRENT_COMMIT"
    echo "  Remote commit:  $REMOTE_COMMIT_SHORT"
    echo "  Branch:         $BRANCH"
    echo ""
    info "Files that would be updated:"

    # Show diff summary
    if git diff --name-only cc-boilerplate/"$BRANCH" .claude/boilerplate/ 2>/dev/null | head -10; then
        echo ""
    else
        echo "  (Unable to determine specific file changes)"
    fi

    info "To perform the update, run without --dry-run"
    exit 0
}

# Perform the actual update
perform_update() {
    if [[ "$SELF_HOSTED" == "true" ]]; then
        info "Self-hosted repository - updating to latest release version..."

        # For self-hosted, sync content from boilerplate/ to .claude/
        info "Syncing boilerplate content to .claude/ directories..."

        # Update agents
        if [[ -d "boilerplate/.claude/agents" ]]; then
            if command -v rsync >/dev/null 2>&1; then
                rsync -av --delete "boilerplate/.claude/agents/" ".claude/agents/" || abort "Failed to sync agents"
            else
                rm -rf .claude/agents && cp -r "boilerplate/.claude/agents" ".claude/agents" || abort "Failed to sync agents"
            fi
            success "Agents updated"
        fi

        # Update commands
        if [[ -d "boilerplate/.claude/commands" ]]; then
            if command -v rsync >/dev/null 2>&1; then
                rsync -av --delete "boilerplate/.claude/commands/" ".claude/commands/" || abort "Failed to sync commands"
            else
                rm -rf .claude/commands && cp -r "boilerplate/.claude/commands" ".claude/commands" || abort "Failed to sync commands"
            fi
            success "Commands updated"
        fi

        # Update hooks
        if [[ -d "boilerplate/.claude/hooks" ]]; then
            if command -v rsync >/dev/null 2>&1; then
                rsync -av --delete "boilerplate/.claude/hooks/" ".claude/hooks/" || abort "Failed to sync hooks"
            else
                rm -rf .claude/hooks && cp -r "boilerplate/.claude/hooks" ".claude/hooks" || abort "Failed to sync hooks"
            fi
            success "Hooks updated"
        fi

        # Update CLAUDE.md template if newer
        if [[ -f "boilerplate/CLAUDE.template.md" ]]; then
            if [[ ! -f "CLAUDE.md" || "boilerplate/CLAUDE.template.md" -nt "CLAUDE.md" ]]; then
                cp "boilerplate/CLAUDE.template.md" "CLAUDE.md.new"
                # Replace placeholder
                sed -i.bak "s/{{PROJECT_NAME}}/cc-boilerplate/g" "CLAUDE.md.new"
                rm "CLAUDE.md.new.bak"
                mv "CLAUDE.md.new" "CLAUDE.md"
                success "CLAUDE.md updated from template"
            fi
        fi

        success "Self-hosted boilerplate content updated successfully"
    else
        info "Updating boilerplate from commit $CURRENT_COMMIT to $REMOTE_COMMIT_SHORT..."

        # Use git subtree pull to update
        if git subtree pull --prefix=.claude/boilerplate cc-boilerplate "$BRANCH" --squash; then
            success "Boilerplate updated successfully"
        else
            abort "Failed to update boilerplate subtree"
        fi
    fi
}

# Update version file
update_version_file() {
    local date
    date=$(date -u +"%Y-%m-%d")

    if [[ "$SELF_HOSTED" == "true" ]]; then
        # For self-hosted, use the latest release tag
        local new_version="$REMOTE_TAG"

        cat > .boilerplate-version <<EOF
{
  "version": "$new_version",
  "commit": "$REMOTE_COMMIT_SHORT",
  "date": "$date",
  "branch": "$BRANCH",
  "repository": "$REPO_URL",
  "previous_commit": "$CURRENT_COMMIT",
  "updated_from": "$CURRENT_VERSION",
  "self_hosted": true,
  "note": "This is the source cc-boilerplate repository"
}
EOF
        success "Version updated to $new_version (latest release)"
    else
        # Read current version and increment patch version
        local version_parts
        IFS='.' read -ra version_parts <<< "$CURRENT_VERSION"
        local major=${version_parts[0]:-1}
        local minor=${version_parts[1]:-0}
        local patch=${version_parts[2]:-0}

        # Increment patch version
        ((patch++))
        local new_version="$major.$minor.$patch"

        cat > .boilerplate-version <<EOF
{
  "version": "$new_version",
  "commit": "$REMOTE_COMMIT_SHORT",
  "date": "$date",
  "branch": "$BRANCH",
  "repository": "$REPO_URL",
  "previous_commit": "$CURRENT_COMMIT",
  "updated_from": "$CURRENT_VERSION"
}
EOF
        success "Version updated to $new_version"
    fi
}

# Rebuild configurations
rebuild_configs() {
    info "Rebuilding configurations..."

    # Look for build-config.sh in multiple locations
    local build_script=""
    if [[ "$SELF_HOSTED" == "true" && -f "scripts/build-config.sh" ]]; then
        build_script="scripts/build-config.sh"
    elif [[ -f ".claude/boilerplate/scripts/build-config.sh" ]]; then
        build_script=".claude/boilerplate/scripts/build-config.sh"
    elif [[ -f "scripts/build-config.sh" ]]; then
        build_script="scripts/build-config.sh"
    else
        warn "build-config.sh not found. You'll need to rebuild configurations manually."
        return 0
    fi

    if "$build_script"; then
        success "Configurations rebuilt successfully"
    else
        warn "Configuration rebuild failed. Check manually."
    fi
}

# Handle CLAUDE.md template updates
update_claude_template() {
    info "Checking for CLAUDE.md template updates..."

    # Determine template location based on hosting type
    local template_file=""
    if [[ "$SELF_HOSTED" == "true" && -f "boilerplate/CLAUDE.template.md" ]]; then
        template_file="boilerplate/CLAUDE.template.md"
    elif [[ -f ".claude/boilerplate/CLAUDE.template.md" ]]; then
        template_file=".claude/boilerplate/CLAUDE.template.md"
    else
        info "No CLAUDE.template.md found in boilerplate, skipping"
        return 0
    fi

    # Extract project name from existing configs or use fallback
    local project_name="my-project"
    if [[ -f ".env" ]]; then
        project_name=$(grep "^PROJECT_NAME=" .env 2>/dev/null | cut -d'=' -f2 | tr -d '"' || echo "my-project")
    fi

    if [[ -f "CLAUDE.md" ]]; then
        # Existing CLAUDE.md found - create backup and offer template
        local backup_name="CLAUDE.md.backup.$(date +%Y%m%d_%H%M%S)"
        cp CLAUDE.md "$backup_name"
        warn "Existing CLAUDE.md detected during update!"
        info "  - Backup created: $backup_name"
        info "  - New template saved as: CLAUDE.md.boilerplate"

        # Save template separately for manual merge
        cp "$template_file" CLAUDE.md.boilerplate

        # Replace placeholders in the boilerplate version
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/{{PROJECT_NAME}}/$project_name/g" CLAUDE.md.boilerplate
        else
            sed -i "s/{{PROJECT_NAME}}/$project_name/g" CLAUDE.md.boilerplate
        fi

        echo ""
        warn "📋 MANUAL MERGE REQUIRED:"
        echo "     The boilerplate CLAUDE.md has been updated with new features"
        echo "     including Dynamic Agent Discovery enforcement."
        echo ""
        echo "     Please use Claude Code to merge:"
        echo "     - Your existing: CLAUDE.md"
        echo "     - New features from: CLAUDE.md.boilerplate"
        echo "     - Especially the new Dynamic Agent Discovery section"
        echo ""
        echo "     After merging, you can delete CLAUDE.md.boilerplate"
        echo ""
    else
        # No existing CLAUDE.md - safe to create from template
        cp "$template_file" CLAUDE.md

        # Replace placeholder with actual project name
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/{{PROJECT_NAME}}/$project_name/g" CLAUDE.md
        else
            sed -i "s/{{PROJECT_NAME}}/$project_name/g" CLAUDE.md
        fi

        success "Created CLAUDE.md from updated template"
    fi
}

# Show completion message
show_completion() {
    local new_version
    new_version=$(jq -r '.version' .boilerplate-version)

    echo ""
    echo "${GREEN}${BOLD}🎉 Boilerplate Update Complete!${RESET}"
    echo ""
    info "Update summary:"
    echo "  ⬆️  Version:     $CURRENT_VERSION → $new_version"
    echo "  📝 Commit:      $CURRENT_COMMIT → $REMOTE_COMMIT_SHORT"
    echo "  🌿 Branch:      $BRANCH"
    echo "  📁 Backup:      $BACKUP_DIR"
    echo ""
    info "Next steps:"
    echo "  1. Review changes in .claude/boilerplate/"
    echo "  2. If CLAUDE.md.boilerplate exists, merge it with your CLAUDE.md"
    echo "  3. Test your project to ensure compatibility"
    echo "  4. Update your project customizations if needed"
    echo "  5. If issues occur, rollback with: cp -r $BACKUP_DIR/* ."
    echo ""
    info "View changes: git log --oneline .claude/boilerplate/"
}

# Main execution
main() {
    setup_colors

    echo "${BOLD}======================================"
    echo "      CC-Boilerplate Update"
    echo "======================================${RESET}"
    echo ""

    parse_args "$@"
    check_requirements
    read_version_info
    check_working_directory
    fetch_remote
    get_remote_info

    if [[ "$DRY_RUN" == "true" ]]; then
        show_dry_run
    fi

    create_backup
    perform_update
    update_version_file
    rebuild_configs
    update_claude_template
    show_completion
}

# Run main function
main "$@"
