#!/bin/bash
# Install spec-kit using official uvx installer

set -e

# Color setup
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📦 Installing spec-kit...${NC}"

# Check for required tools
command -v uvx >/dev/null 2>&1 || {
    echo -e "${RED}❌ Error: uvx is required but not installed.${NC}"
    echo "Install uv first: https://docs.astral.sh/uv/"
    exit 1
}

command -v jq >/dev/null 2>&1 || {
    echo -e "${RED}❌ Error: jq is required but not installed.${NC}"
    echo "Install jq: brew install jq (macOS) or apt-get install jq (Linux)"
    exit 1
}

# Determine manifest location
MANIFEST_FILE=""
if [ -f "boilerplate/.boilerplate-manifest.json" ]; then
    MANIFEST_FILE="boilerplate/.boilerplate-manifest.json"
elif [ -f ".boilerplate-manifest.json" ]; then
    MANIFEST_FILE=".boilerplate-manifest.json"
else
    echo -e "${RED}❌ Error: Could not find .boilerplate-manifest.json${NC}"
    exit 1
fi

# Read version and configuration from manifest
if ! jq -e '.dependencies."spec-kit"' "$MANIFEST_FILE" > /dev/null; then
    echo -e "${YELLOW}⚠️  No spec-kit dependency found in manifest${NC}"
    exit 0
fi

VERSION=$(jq -r '.dependencies."spec-kit".version' "$MANIFEST_FILE")
REPO="git+https://github.com/github/spec-kit.git"

echo -e "${BLUE}Installing spec-kit ${VERSION}...${NC}"

# Remove existing .specify directory if it exists
if [ -d ".specify" ]; then
    echo -e "${YELLOW}⚠️  Backing up existing .specify directory...${NC}"
    mv .specify ".specify.backup.$(date +%s)"
fi

# Use headless installation with version pinning
echo -e "${BLUE}Running: uvx --from ${REPO}@${VERSION} specify init . --ai claude --ignore-agent-tools${NC}"

uvx --from "${REPO}@${VERSION}" specify init . \
  --ai claude \
  --ignore-agent-tools || {
    echo -e "${RED}❌ Spec-kit installation failed${NC}"
    exit 1
}

# Validate installation
echo -e "${BLUE}Validating installation...${NC}"

VALIDATION_DIRS=($(jq -r '.dependencies."spec-kit".validation.required_dirs[]' "$MANIFEST_FILE"))
VALIDATION_FILES=($(jq -r '.dependencies."spec-kit".validation.required_files[]' "$MANIFEST_FILE"))

for dir in "${VALIDATION_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo -e "${RED}❌ Required directory not found: $dir${NC}"
        exit 1
    fi
done

for file in "${VALIDATION_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ Required file not found: $file${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ Spec-kit ${VERSION} installed successfully${NC}"

# Update .boilerplate-version if it exists
if [ -f ".boilerplate-version" ]; then
    echo -e "${BLUE}Updating .boilerplate-version...${NC}"
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Add or update spec-kit dependency in .boilerplate-version
    jq --arg version "$VERSION" --arg timestamp "$TIMESTAMP" '
        .dependencies = (.dependencies // {}) |
        .dependencies."spec-kit" = {
            "version": $version,
            "installed_at": $timestamp
        }
    ' .boilerplate-version > .boilerplate-version.tmp && \
    mv .boilerplate-version.tmp .boilerplate-version

    echo -e "${GREEN}✅ Updated .boilerplate-version${NC}"
fi

echo -e "${GREEN}🎉 Spec-kit installation complete!${NC}"
echo -e "${BLUE}Available Claude Code commands: /plan, /tasks, /implement${NC}"