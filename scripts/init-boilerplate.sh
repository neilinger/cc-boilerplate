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
    git subtree >/dev/null 2>&1
    if [[ $? -ne 129 ]]; then
        abort "Git subtree is required but not available"
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

# Get repository URL
get_repo_url() {
    local default_url="${CC_BOILERPLATE_REPO:-https://github.com/neilinger/cc-boilerplate.git}"

    echo ""
    info "Repository Configuration"
    echo "------------------------"
    read -r -p "Enter cc-boilerplate repository URL [$default_url]: " REPO_URL
    REPO_URL=${REPO_URL:-$default_url}

    read -r -p "Enter branch to use [main]: " BRANCH
    BRANCH=${BRANCH:-main}
}

# Check if boilerplate already exists
check_existing_boilerplate() {
    if [[ -d ".claude/boilerplate" ]]; then
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
}

# Create necessary directories
setup_directories() {
    info "Setting up directory structure..."
    mkdir -p .claude/project
    success "Directory structure created"
}

# Add git subtree
add_subtree() {
    info "Adding cc-boilerplate as git subtree..."

    # Add remote if it doesn't exist
    if ! git remote get-url cc-boilerplate >/dev/null 2>&1; then
        git remote add -f cc-boilerplate "$REPO_URL"
    else
        git fetch cc-boilerplate
    fi

    # Add subtree
    if git subtree add --prefix=.claude/boilerplate cc-boilerplate "$BRANCH" --squash; then
        success "Boilerplate added successfully"
    else
        abort "Failed to add boilerplate subtree"
    fi
}

# Create version file
create_version_file() {
    local commit_hash
    commit_hash=$(git ls-remote cc-boilerplate "$BRANCH" | cut -f1)
    local date
    date=$(date -u +"%Y-%m-%d")

    cat > .boilerplate-version <<EOF
{
  "version": "1.0.0",
  "commit": "${commit_hash:0:7}",
  "date": "$date",
  "branch": "$BRANCH",
  "repository": "$REPO_URL"
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

# Show completion message
show_completion() {
    echo ""
    echo "${GREEN}${BOLD}🎉 CC-Boilerplate Initialization Complete!${RESET}"
    echo ""
    info "What was set up:"
    echo "  📁 .claude/boilerplate/     - Core boilerplate files"
    echo "  📁 .claude/project/         - Your project customizations"
    echo "  📄 .boilerplate-version     - Version tracking"
    echo "  ⚙️  Updated .gitignore       - Ignore generated files"
    echo ""
    info "Next steps:"
    echo "  1. Edit .claude/project/CLAUDE.project.md for project-specific instructions"
    echo "  2. Edit .claude/project/settings.project.json for custom settings"
    echo "  3. Run 'scripts/build-config.sh' to generate merged configurations"
    echo "  4. Run 'scripts/update-boilerplate.sh' to pull future updates"
    echo ""
    info "Documentation: docs/SYNCHRONIZATION.md"
}

# Main execution
main() {
    setup_colors
    detect_os

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
