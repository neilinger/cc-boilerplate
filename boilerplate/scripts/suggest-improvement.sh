#!/usr/bin/env bash
set -euo pipefail

# CC-Boilerplate Improvement Suggestion Helper
# Makes it easy to suggest improvements back to cc-boilerplate upstream

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

# Show help
show_help() {
    cat <<EOF
CC-Boilerplate Improvement Suggestion Helper

Usage: $0 [FILE_PATH] [OPTIONS]

Examples:
  $0                                    # General suggestion
  $0 .claude/hooks/my-useful-hook.py   # Suggest specific file
  $0 --idea "Auto-detect project type" # Suggest an idea

Options:
  --idea TEXT    Suggest an idea without a file
  -h, --help     Show this help message

This script helps you easily suggest improvements to cc-boilerplate upstream.
EOF
}

# Generate GitHub issue URL
generate_issue_url() {
    local title="$1"
    local body="$2"
    local base_url="https://github.com/neilinger/cc-boilerplate/issues/new"

    # URL encode title and body
    local encoded_title encoded_body
    encoded_title=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$title'''))" 2>/dev/null || echo "$title")
    encoded_body=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$body'''))" 2>/dev/null || echo "$body")

    echo "${base_url}?title=${encoded_title}&body=${encoded_body}&labels=enhancement"
}

# Suggest a file
suggest_file() {
    local file_path="$1"

    if [[ ! -f "$file_path" ]]; then
        echo "${RED}❌ File not found: $file_path${RESET}" >&2
        exit 1
    fi

    echo "${BLUE}📝 Suggesting file: $file_path${RESET}"
    echo ""

    # Get file info
    local file_size line_count
    file_size=$(wc -c < "$file_path")
    line_count=$(wc -l < "$file_path")

    # Read first few lines for context
    local preview
    preview=$(head -20 "$file_path" | sed 's/^/    /')

    # Generate issue content
    local title="Enhancement: Add $(basename "$file_path")"
    local body="## Suggested Improvement

**File**: \`$file_path\`
**Size**: $file_size bytes, $line_count lines

## Description
I found this useful addition in my project that might benefit cc-boilerplate users.

## File Preview
\`\`\`
$preview
$([ $line_count -gt 20 ] && echo "    ... (truncated)")
\`\`\`

## Why This Would Be Useful
[Please describe why this would benefit other cc-boilerplate users]

## Testing
- [ ] Tested in my project
- [ ] Works with current cc-boilerplate structure
- [ ] No breaking changes

---
*Suggested via cc-boilerplate suggest-improvement.sh*"

    local url
    url=$(generate_issue_url "$title" "$body")

    echo "${GREEN}✅ Issue URL generated!${RESET}"
    echo ""
    echo "Click this link to open a pre-filled GitHub issue:"
    echo "${BLUE}$url${RESET}"
    echo ""
    echo "Or copy the content below and paste it manually:"
    echo ""
    echo "${YELLOW}Title:${RESET} $title"
    echo ""
    echo "${YELLOW}Body:${RESET}"
    echo "$body"
}

# Suggest an idea
suggest_idea() {
    local idea="$1"

    echo "${BLUE}💡 Suggesting idea: $idea${RESET}"
    echo ""

    local title="Enhancement: $idea"
    local body="## Suggested Enhancement

**Idea**: $idea

## Description
[Please describe your idea in detail]

## Why This Would Be Useful
[Please explain how this would benefit cc-boilerplate users]

## Possible Implementation
[Optional: Any thoughts on how this could be implemented]

---
*Suggested via cc-boilerplate suggest-improvement.sh*"

    local url
    url=$(generate_issue_url "$title" "$body")

    echo "${GREEN}✅ Issue URL generated!${RESET}"
    echo ""
    echo "Click this link to open a pre-filled GitHub issue:"
    echo "${BLUE}$url${RESET}"
    echo ""
    echo "Or copy the content below and paste it manually:"
    echo ""
    echo "${YELLOW}Title:${RESET} $title"
    echo ""
    echo "${YELLOW}Body:${RESET}"
    echo "$body"
}

# General suggestion
suggest_general() {
    echo "${BLUE}💬 Creating general improvement suggestion${RESET}"
    echo ""

    local title="Enhancement Request"
    local body="## Suggested Enhancement

[Please describe your improvement idea]

## Current Situation
[What currently happens or what's missing]

## Proposed Solution
[How you think this could be improved]

## Why This Would Be Useful
[How this would benefit cc-boilerplate users]

---
*Suggested via cc-boilerplate suggest-improvement.sh*"

    local url
    url=$(generate_issue_url "$title" "$body")

    echo "${GREEN}✅ Issue URL generated!${RESET}"
    echo ""
    echo "Click this link to open a pre-filled GitHub issue:"
    echo "${BLUE}$url${RESET}"
    echo ""
    echo "${YELLOW}Tip:${RESET} You can also suggest specific files with:"
    echo "  $0 path/to/your/useful/file.py"
}

# Main function
main() {
    setup_colors

    echo "${BOLD}======================================"
    echo "   CC-Boilerplate Improvement Helper"
    echo "======================================${RESET}"
    echo ""

    # Parse arguments
    case "${1:-}" in
        -h|--help)
            show_help
            exit 0
            ;;
        --idea)
            if [[ -z "${2:-}" ]]; then
                echo "${RED}❌ --idea requires a description${RESET}" >&2
                exit 1
            fi
            suggest_idea "$2"
            ;;
        "")
            suggest_general
            ;;
        *)
            if [[ "$1" == --* ]]; then
                echo "${RED}❌ Unknown option: $1${RESET}" >&2
                echo "Use --help for usage information" >&2
                exit 1
            fi
            suggest_file "$1"
            ;;
    esac
}

# Run main function
main "$@"