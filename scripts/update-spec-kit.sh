#!/bin/bash
# Update spec-kit to version specified in manifest

set -e

# Color setup
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Updating spec-kit...${NC}"

# Check for required tools
command -v jq >/dev/null 2>&1 || {
    echo -e "${RED}❌ Error: jq is required but not installed.${NC}"
    echo "Install jq: brew install jq (macOS) or apt-get install jq (Linux)"
    exit 1
}

# Determine manifest and version file locations
MANIFEST_FILE=""
if [ -f "boilerplate/.boilerplate-manifest.json" ]; then
    MANIFEST_FILE="boilerplate/.boilerplate-manifest.json"
elif [ -f ".boilerplate-manifest.json" ]; then
    MANIFEST_FILE=".boilerplate-manifest.json"
else
    echo -e "${RED}❌ Error: Could not find .boilerplate-manifest.json${NC}"
    exit 1
fi

if [ ! -f ".boilerplate-version" ]; then
    echo -e "${RED}❌ Error: .boilerplate-version not found${NC}"
    echo "This script should be run from a project initialized with cc-boilerplate"
    exit 1
fi

# Check if spec-kit dependency exists
if ! jq -e '.dependencies."spec-kit"' "$MANIFEST_FILE" > /dev/null; then
    echo -e "${YELLOW}⚠️  No spec-kit dependency found in manifest${NC}"
    exit 0
fi

# Get current and target versions
CURRENT=$(jq -r '.dependencies."spec-kit".version // "none"' .boilerplate-version 2>/dev/null)
TARGET=$(jq -r '.dependencies."spec-kit".version' "$MANIFEST_FILE")

echo -e "${BLUE}Current version: ${CURRENT}${NC}"
echo -e "${BLUE}Target version:  ${TARGET}${NC}"

if [ "$CURRENT" = "$TARGET" ]; then
    echo -e "${GREEN}✅ Spec-kit already at version $TARGET${NC}"
    exit 0
fi

# Confirm update
if [ "$CURRENT" != "none" ] && [ "$CURRENT" != "pending" ]; then
    echo ""
    echo -e "${YELLOW}⚠️  This will update spec-kit from $CURRENT to $TARGET${NC}"
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Update cancelled"
        exit 0
    fi
fi

# Backup existing .specify if it exists
if [ -d ".specify" ]; then
    BACKUP_DIR=".specify.backup.$(date +%s)"
    echo -e "${YELLOW}📦 Backing up existing .specify to $BACKUP_DIR${NC}"
    mv .specify "$BACKUP_DIR"
fi

# Install new version using our install script
echo -e "${BLUE}Installing spec-kit version $TARGET...${NC}"

# Check if install script exists
if [ ! -f "scripts/install-spec-kit.sh" ]; then
    echo -e "${RED}❌ Error: scripts/install-spec-kit.sh not found${NC}"
    echo "Cannot update spec-kit without install script"
    exit 1
fi

# Run install script
if ./scripts/install-spec-kit.sh; then
    echo -e "${GREEN}✅ Spec-kit updated successfully to version $TARGET${NC}"

    # Clean up old backup if update was successful
    if [ -d "$BACKUP_DIR" ]; then
        echo -e "${BLUE}Cleaning up backup directory...${NC}"
        rm -rf "$BACKUP_DIR"
    fi
else
    echo -e "${RED}❌ Spec-kit update failed${NC}"

    # Restore backup if available
    if [ -d "$BACKUP_DIR" ]; then
        echo -e "${YELLOW}🔄 Restoring backup...${NC}"
        rm -rf .specify 2>/dev/null || true
        mv "$BACKUP_DIR" .specify
        echo -e "${GREEN}✅ Backup restored${NC}"
    fi

    exit 1
fi

echo -e "${GREEN}🎉 Spec-kit update complete!${NC}"
echo -e "${BLUE}Available Claude Code commands: /plan, /tasks, /implement${NC}"