#!/usr/bin/env bash
set -euo pipefail

# Ensure Homebrew git is used (includes git-subtree on macOS)
export PATH="/opt/homebrew/bin:$PATH"

# CC-Boilerplate Initialization Script
# Initializes cc-boilerplate in new or existing projects using git subtree

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

# OS detection
detect_os() {
    case "$OSTYPE" in
        darwin*) OS="macOS" ;;
        linux*)  OS="Linux" ;;
        *)       echo "${RED}❌ Unsupported OS: $OSTYPE${RESET}" && exit 1 ;;
    esac
}

# Error handling
abort() {
    echo "${RED}❌ $1${RESET}" >&2
    exit 1
}

# Success message
success() {
    echo "${GREEN}✅ $1${RESET}"
}

# Info message
info() {
    echo "${BLUE}ℹ️  $1${RESET}"
}

# Warning message
warn() {
    echo "${YELLOW}⚠️  $1${RESET}"
}

# Check required tools
check_requirements() {
    info "Checking requirements..."

    # Check git
    command -v git >/dev/null 2>&1 || abort "Git is required but not installed"

    # Check git subtree (exit code 129 is expected when called without args)
    set +e
    git subtree >/dev/null 2>&1
    local exit_code=$?
    set -e
    if [[ $exit_code -ne 129 ]]; then
        abort "Git subtree is required but not available (got exit code $exit_code, expected 129)"
    fi

    # Check jq
    command -v jq >/dev/null 2>&1 || abort "jq is required but not installed. Install with: brew install jq"

    success "All requirements met"
}

# Check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        warn "Not in a git repository. Initializing git repository..."
        git init
        success "Git repository initialized"
    fi
}

# Check for clean working directory
check_clean_workdir() {
    if [[ -n $(git status --porcelain 2>/dev/null) ]]; then
        warn "You have uncommitted changes:"
        git status --short
        echo ""
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            abort "Initialization cancelled"
        fi
    fi
}

# Get latest release tag
get_latest_tag() {
    local repo_url="$1"
    local latest_tag

    # Extract owner/repo from URL
    local repo_path
    repo_path=$(echo "$repo_url" | sed -E 's|^https://github\.com/([^/]+/[^/]+)\.git$|\1|')

    # Try to get latest release tag via GitHub API
    if command -v curl >/dev/null 2>&1; then
        latest_tag=$(curl -s "https://api.github.com/repos/$repo_path/releases/latest" | grep '"tag_name":' | cut -d'"' -f4 2>/dev/null)
    fi

    # Fall back to git ls-remote if API fails
    if [[ -z "$latest_tag" ]]; then
        latest_tag=$(git ls-remote --tags --refs "$repo_url" | grep -o 'refs/tags/v[0-9]*\.[0-9]*\.[0-9]*$' | sed 's|refs/tags/||' | sort -V | tail -1 2>/dev/null)
    fi

    # Ultimate fallback to main
    echo "${latest_tag:-main}"
}

# Get repository URL
get_repo_url() {
    local default_url="${CC_BOILERPLATE_REPO:-https://github.com/neilinger/cc-boilerplate.git}"

    echo ""
    success "Setup is working correctly! Almost done..."
    echo ""

    if [ "$INTERACTIVE" = false ]; then
        # Non-interactive mode - explain and use defaults
        info "🤖 Auto-configuration Mode (piped execution detected)"
        echo "------------------------"
        echo ""
        success "Installing CC-Boilerplate - Claude Code enhancement toolkit"
        echo ""
        info "What this adds to your project:"
        echo "  • AI agents for documentation, testing, security, and development"
        echo "  • Automated quality checks and security validation"
        echo "  • Enhanced Claude Code commands and workflows"
        echo "  • Intelligent task orchestration and coordination"
        echo ""
        info "Using default configuration:"
        echo "  📦 Repository: neilinger/cc-boilerplate (official)"
        local default_branch
        default_branch=$(get_latest_tag "$default_url")
        echo "  🔖 Version: $default_branch (latest stable)"
        echo "  📁 Location: .claude/boilerplate/"
        echo ""
        REPO_URL="$default_url"
        BRANCH="$default_branch"
        success "Configuration set automatically"
    else
        # Interactive mode - existing prompting code
        info "Repository Configuration (Step 6/9)"
        echo "------------------------"
        echo "${BLUE}💡 Press ENTER to use defaults, or type custom values${RESET}"
        echo ""
        read -r -p "${BOLD}Repository URL [${default_url}]: ${RESET}" REPO_URL
        REPO_URL=${REPO_URL:-$default_url}

        local default_branch
        default_branch=$(get_latest_tag "$REPO_URL")
        read -r -p "${BOLD}Version to use [$default_branch]: ${RESET}" BRANCH
        BRANCH=${BRANCH:-$default_branch}

        echo ""
        success "Configuration set: $(basename "$REPO_URL") (branch: $BRANCH)"
    fi
}

# Check if boilerplate already exists
check_existing_boilerplate() {
    if [[ -d ".claude/boilerplate" ]]; then
        if [ "$INTERACTIVE" = false ]; then
            # Non-interactive mode - clean exit with guidance
            local current_dir="$(pwd)"
            local claude_cmd="$(detect_claude_command)"

            echo ""
            info "CC-Boilerplate detected - already installed ✓"
            echo ""
            echo "${BOLD}${BLUE}Ready to use:${RESET}"
            echo "  ${BOLD}${GREEN}${claude_cmd} ${current_dir}${RESET}"
            echo ""
            echo "Then type ${BOLD}${GREEN}/code-quality${RESET} to test"
            echo ""
            exit 0
        else
            # Interactive mode - ask user
            warn "Boilerplate directory already exists at .claude/boilerplate"
            read -p "Remove and reinitialize? (y/N): " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                rm -rf .claude/boilerplate
                git remote remove cc-boilerplate 2>/dev/null || true
                success "Existing boilerplate removed"
            else
                abort "Initialization cancelled"
            fi
        fi
    fi
}

# Create necessary directories
setup_directories() {
    info "Setting up directory structure..."
    mkdir -p .claude/project
    mkdir -p .claude/boilerplate
    success "Directory structure created"
}

# Safely merge documentation (PRPs, ADRs) without overwriting existing project files
merge_documentation() {
    local source_dir="$1"

    info "Merging documentation (preserving existing project files)..."

    # Handle PRPs directory - only add missing boilerplate PRPs
    if [[ -d "$source_dir/PRPs" ]]; then
        if [[ -d "PRPs" ]]; then
            # Project already has PRPs - selectively add only missing boilerplate PRPs
            info "Found existing PRPs directory - merging selectively..."
            mkdir -p .claude/boilerplate/PRPs

            # Copy boilerplate PRPs to staging area, then selectively merge
            cp -r "$source_dir/PRPs/"* .claude/boilerplate/PRPs/ 2>/dev/null || true

            # Copy boilerplate PRPs that don't exist in project
            for prp_file in "$source_dir/PRPs"/*.md; do
                if [[ -f "$prp_file" ]]; then
                    local filename=$(basename "$prp_file")
                    if [[ ! -f "PRPs/$filename" ]]; then
                        info "Adding boilerplate PRP: $filename"
                        cp "$prp_file" "PRPs/"
                    fi
                fi
            done

            # Copy boilerplate PRP subdirectories that don't exist
            for prp_dir in "$source_dir/PRPs"/*/; do
                if [[ -d "$prp_dir" ]]; then
                    local dirname=$(basename "$prp_dir")
                    if [[ ! -d "PRPs/$dirname" ]]; then
                        info "Adding boilerplate PRP directory: $dirname"
                        cp -r "$prp_dir" "PRPs/"
                    fi
                fi
            done
        else
            # No existing PRPs - copy all boilerplate PRPs
            info "No existing PRPs found - copying all boilerplate PRPs..."
            cp -r "$source_dir/PRPs" ./
            # Also copy to boilerplate staging
            cp -r "$source_dir/PRPs" .claude/boilerplate/
        fi
    fi

    # Handle docs/adr directory - only add missing boilerplate ADRs
    if [[ -d "$source_dir/docs" ]]; then
        if [[ -d "docs" ]]; then
            # Project already has docs - selectively add missing ADRs
            info "Found existing docs directory - merging selectively..."
            mkdir -p docs/adr
            mkdir -p .claude/boilerplate/docs

            # Copy boilerplate docs to staging
            cp -r "$source_dir/docs/"* .claude/boilerplate/docs/ 2>/dev/null || true

            # Copy missing boilerplate ADRs
            if [[ -d "$source_dir/docs/adr" ]]; then
                for adr_file in "$source_dir/docs/adr"/*.md; do
                    if [[ -f "$adr_file" ]]; then
                        local filename=$(basename "$adr_file")
                        if [[ ! -f "docs/adr/$filename" ]]; then
                            info "Adding boilerplate ADR: $filename"
                            cp "$adr_file" "docs/adr/"
                        fi
                    fi
                done
            fi
        else
            # No existing docs - copy all boilerplate docs
            info "No existing docs found - copying all boilerplate docs..."
            cp -r "$source_dir/docs" ./
            # Also copy to boilerplate staging
            cp -r "$source_dir/docs" .claude/boilerplate/
        fi
    fi

    # Handle templates directory - needed for config building
    if [[ -d "$source_dir/templates" ]]; then
        info "Copying configuration templates..."
        mkdir -p .claude/boilerplate/templates
        cp -r "$source_dir/templates/"* .claude/boilerplate/templates/ 2>/dev/null || true
    fi

    success "Documentation merged safely (existing project files preserved)"
}

# Install boilerplate content
add_subtree() {
    info "Installing cc-boilerplate content..."

    # Create temp directory for clone
    local temp_dir
    temp_dir=$(mktemp -d)

    # Clone the repository to temp directory
    info "Downloading boilerplate from $REPO_URL (version: $BRANCH)..."
    if ! git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$temp_dir"; then
        abort "Failed to download boilerplate from $REPO_URL"
    fi

    # Get commit hash from the cloned repository
    local commit_hash
    commit_hash=$(cd "$temp_dir" && git rev-parse HEAD)

    # Copy only the boilerplate subdirectory content (PRESERVING EXISTING PROJECT FILES)
    if [[ -d "$temp_dir/boilerplate" ]]; then
        info "Extracting boilerplate content..."

        # CRITICAL: Install .claude content directly AND keep reference copy
        if [[ -d "$temp_dir/boilerplate/.claude" ]]; then
            if command -v rsync >/dev/null 2>&1; then
                # Main installation: Copy directly to .claude/ for immediate Claude access
                if ! rsync -a "$temp_dir/boilerplate/.claude/" .claude/; then
                    abort "Failed to copy .claude content to main directory"
                fi
                # Reference copy: Keep copy in .claude/boilerplate/ for build-config.sh
                if ! rsync -a "$temp_dir/boilerplate/.claude/" .claude/boilerplate/.claude/; then
                    abort "Failed to copy .claude boilerplate reference"
                fi
            else
                # Enable dotglob to include hidden files
                shopt -s dotglob
                # Main installation
                if ! cp -r "$temp_dir/boilerplate/.claude/"* .claude/; then
                    abort "Failed to copy .claude content to main directory"
                fi
                # Reference copy
                mkdir -p .claude/boilerplate/.claude
                if ! cp -r "$temp_dir/boilerplate/.claude/"* .claude/boilerplate/.claude/; then
                    abort "Failed to copy .claude boilerplate reference"
                fi
                shopt -u dotglob
            fi
        fi

        # Copy scripts directory (needed for build-config.sh, etc.)
        if [[ -d "$temp_dir/boilerplate/scripts" ]]; then
            if command -v rsync >/dev/null 2>&1; then
                rsync -a "$temp_dir/boilerplate/scripts/" .claude/boilerplate/scripts/
            else
                mkdir -p .claude/boilerplate/scripts
                cp -r "$temp_dir/boilerplate/scripts/"* .claude/boilerplate/scripts/
            fi
        fi

        # SELECTIVELY merge PRPs and ADRs (only add missing ones, don't overwrite)
        merge_documentation "$temp_dir/boilerplate"

        # Copy essential project root files from the source repository
        info "Setting up project root files..."

        # Copy setup.sh to project root (where it should be executed)
        if [[ -f "$temp_dir/setup.sh" ]]; then
            cp "$temp_dir/setup.sh" ./setup.sh
            chmod +x ./setup.sh
        fi

        # Copy sample configuration files to project root
        [[ -f "$temp_dir/.env.sample" ]] && cp "$temp_dir/.env.sample" ./.env.sample
        [[ -f "$temp_dir/.mcp.json.sample" ]] && cp "$temp_dir/.mcp.json.sample" ./.mcp.json.sample

        # Handle CLAUDE.md template
        if [[ -f "$temp_dir/boilerplate/CLAUDE.template.md" ]]; then
            if [[ -f ./CLAUDE.md ]]; then
                # Existing CLAUDE.md found - create backup and advise
                local backup_name="CLAUDE.md.backup.$(date +%Y%m%d_%H%M%S)"
                cp ./CLAUDE.md "$backup_name"
                warn "Existing CLAUDE.md detected!"
                info "  - Backup created: $backup_name"
                info "  - New template saved as: CLAUDE.md.boilerplate"

                # Save template separately for manual merge
                cp "$temp_dir/boilerplate/CLAUDE.template.md" ./CLAUDE.md.boilerplate

                # Replace placeholders in the boilerplate version
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    sed -i '' "s/{{PROJECT_NAME}}/${PROJECT_NAME:-my-project}/g" ./CLAUDE.md.boilerplate
                else
                    sed -i "s/{{PROJECT_NAME}}/${PROJECT_NAME:-my-project}/g" ./CLAUDE.md.boilerplate
                fi

                echo ""
                echo "  📋 MANUAL MERGE REQUIRED:"
                echo "     Please use Claude Code to merge:"
                echo "     - Your existing: CLAUDE.md"
                echo "     - New features from: CLAUDE.md.boilerplate"
                echo "     - Especially the new Dynamic Agent Discovery section"
                echo ""
            else
                # No existing CLAUDE.md - safe to create
                cp "$temp_dir/boilerplate/CLAUDE.template.md" ./CLAUDE.md
                # Replace placeholder with actual project name
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    sed -i '' "s/{{PROJECT_NAME}}/${PROJECT_NAME:-my-project}/g" ./CLAUDE.md
                else
                    sed -i "s/{{PROJECT_NAME}}/${PROJECT_NAME:-my-project}/g" ./CLAUDE.md
                fi
                success "Created CLAUDE.md from template"
            fi
        fi

        success "Boilerplate content and project files installed successfully"
    else
        abort "Boilerplate directory not found in repository"
    fi

    # Clean up temp directory
    rm -rf "$temp_dir"

    # Store commit hash for version file
    export BOILERPLATE_COMMIT_HASH="$commit_hash"
}

# Create version file
create_version_file() {
    local commit_hash="${BOILERPLATE_COMMIT_HASH:-unknown}"
    local date
    date=$(date -u +"%Y-%m-%d")
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    cat > .boilerplate-version <<EOF
{
  "version": "$BRANCH",
  "commit": "${commit_hash:0:7}",
  "date": "$date",
  "branch": "$BRANCH",
  "repository": "$REPO_URL",
  "initialized_at": "$timestamp",
  "dependencies": {
    "spec-kit": {
      "version": "pending",
      "installed_at": null
    }
  }
}
EOF

    success "Version tracking file created"
}

# Run initial config build
build_initial_config() {
    info "Building initial configuration..."

    # Check if build-config.sh exists
    if [[ -f ".claude/boilerplate/scripts/build-config.sh" ]]; then
        .claude/boilerplate/scripts/build-config.sh
    elif [[ -f "scripts/build-config.sh" ]]; then
        scripts/build-config.sh
    else
        warn "build-config.sh not found. You'll need to run it manually after setup."
    fi
}

# Create sample project customization
create_sample_customization() {
    info "Creating sample project customization..."

    cat > .claude/project/CLAUDE.project.md <<EOF
<!-- Project-specific CLAUDE.md customizations -->
## Project-Specific Guidelines

- This is a sample customization
- Add your project-specific instructions here
- These will be merged with the base CLAUDE.md template

## Domain-Specific Rules

<!-- Add domain-specific rules here -->
<!-- Examples:
- Use TypeScript for all new code
- Follow React Hooks patterns
- API calls use fetch with async/await
-->
EOF

    cat > .claude/project/settings.project.json <<EOF
{
  "__PROJECT_CUSTOM_PERMISSIONS__": [
    "Bash(docker:*)",
    "Bash(npm run:*)"
  ],
  "__PROJECT_CUSTOM_SETTINGS__": {
    "projectName": "$(basename "$(pwd)")",
    "customOutputStyle": "default"
  },
  "__PROJECT_CUSTOM_HOOKS__": {}
}
EOF

    success "Sample customizations created in .claude/project/"
}

# Add to gitignore
update_gitignore() {
    local gitignore_entries=(
        ".claude/build/"
        "*.backup.*"
        ".boilerplate-version.backup"
    )

    info "Updating .gitignore..."

    if [[ ! -f .gitignore ]]; then
        touch .gitignore
    fi

    for entry in "${gitignore_entries[@]}"; do
        if ! grep -q "^${entry}$" .gitignore 2>/dev/null; then
            echo "$entry" >> .gitignore
        fi
    done

    success ".gitignore updated"
}

# Detect Claude Code command
detect_claude_command() {
    if command -v claude >/dev/null 2>&1; then
        echo "claude"
    elif command -v claude-code >/dev/null 2>&1; then
        echo "claude-code"
    else
        echo "claude"  # default assumption
    fi
}

# Show completion message
show_completion() {
    local current_dir="$(pwd)"
    local claude_cmd="$(detect_claude_command)"

    echo ""
    echo "${GREEN}${BOLD}✅ CC-Boilerplate Installed Successfully!${RESET}"
    echo ""
    echo "${BOLD}📁 Location: ${current_dir}${RESET}"
    echo ""

    # Complete setup workflow
    echo "${BOLD}${BLUE}Complete setup with these steps:${RESET}"
    echo ""
    echo "  ${BOLD}1.${RESET} Run the project setup script:"
    echo "     ${BOLD}${GREEN}./setup.sh${RESET}"
    echo ""
    echo "  ${BOLD}2.${RESET} Open Claude Code in this directory:"
    echo "     ${BOLD}${GREEN}${claude_cmd} ${current_dir}${RESET}"
    echo ""
    echo "  ${BOLD}3.${RESET} Test it works - type this command:"
    echo "     ${BOLD}${GREEN}/code-quality${RESET}"
    echo ""
    echo "  ${BOLD}4.${RESET} You'll see a menu = success! 🎉"
    echo ""
    echo "${BLUE}The setup.sh script configures your project (name, API keys, TTS) and integrates${RESET}"
    echo "${BLUE}the boilerplate into your existing project structure.${RESET}"
    echo ""

    # Offer to run setup automatically for interactive mode
    if [[ "$INTERACTIVE" == "true" ]]; then
        echo "${YELLOW}Would you like to run ./setup.sh now? (recommended)${RESET}"
        read -p "Run setup script? (Y/n): " run_setup
        run_setup=${run_setup:-Y}

        if [[ "$run_setup" =~ ^[Yy]$ ]]; then
            echo ""
            echo "${GREEN}🚀 Running project setup...${RESET}"
            echo ""
            if [[ -f ./setup.sh ]]; then
                bash ./setup.sh
            else
                warn "Setup script not found. Please run ./setup.sh manually later."
            fi
        else
            echo ""
            echo "${YELLOW}Remember to run ./setup.sh when you're ready!${RESET}"
        fi
    fi

    # Create verification file
    echo "$(date): CC-Boilerplate ready" > .claude/.cc-installed
}

# Main execution
main() {
    setup_colors
    detect_os

    # Detect if running via pipe/non-interactive (like curl | bash)
    if [ -t 0 ]; then
        INTERACTIVE=true
    else
        INTERACTIVE=false
        echo "${BOLD}${BLUE}🚀 Installing Claude Code Boilerplate...${RESET}"
        echo "This enhances your project with AI-powered development tools"
        echo ""
    fi

    echo "${BOLD}======================================"
    echo "    CC-Boilerplate Initialization"
    echo "======================================${RESET}"
    echo ""

    info "Running on $OS"

    check_requirements
    check_git_repo
    check_clean_workdir
    get_repo_url
    check_existing_boilerplate
    setup_directories
    add_subtree
    create_version_file
    create_sample_customization
    update_gitignore
    build_initial_config
    show_completion
}

# Run main function
main "$@"
