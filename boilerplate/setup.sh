#!/bin/bash
# CC-Boilerplate Setup Script
# Configures the boilerplate for a new project

set -e  # Exit on error

echo "======================================"
echo "      CC-Boilerplate Setup"
echo "======================================"
echo ""

# Check for required commands
command -v uv >/dev/null 2>&1 || {
    echo "L Error: UV is required but not installed."
    echo "Install from: https://docs.astral.sh/uv/"
    exit 1
}

# Check if running inside Claude Code environment or if claude command is available
if [ -n "$CLAUDE_CODE_SESSION" ] || [ -n "$CLAUDE_ENV" ] || command -v claude >/dev/null 2>&1; then
    echo "✓ Claude Code environment detected"
else
    echo "L Error: Claude Code is required but not installed."
    echo "Install from: https://docs.anthropic.com/en/docs/claude-code"
    echo "Or run this script from inside an active Claude Code session"
    exit 1
fi

command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1 || {
    echo "⚠️  Warning: Python is not installed."
    echo "Some features (PRP status checking) will not work without Python."
    echo "Install from: https://www.python.org/"
}

# Get project configuration
echo "📋 Project Configuration"
echo "------------------------"
read -p "Enter your project name [cc-boilerplate]: " PROJECT_NAME
PROJECT_NAME=${PROJECT_NAME:-cc-boilerplate}

read -p "Enter your name (for TTS personalization): " USER_NAME
if [ -z "$USER_NAME" ]; then
    echo "L Error: User name is required for personalization"
    exit 1
fi

# Optional API keys
echo ""
echo "= API Keys (Optional - press Enter to skip)"
echo "--------------------------------------------"
read -p "OpenAI API Key: " OPENAI_KEY
read -p "Anthropic API Key: " ANTHROPIC_KEY
read -p "ElevenLabs API Key: " ELEVENLABS_KEY
read -p "ElevenLabs Voice ID: " ELEVENLABS_VOICE_ID

# Create .env from template
if [ -f .env.sample ]; then
    echo ""
    echo "⚙️ Creating .env configuration..."
    cp .env.sample .env

    # Update with user inputs
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/\"Your Name\"/\"$USER_NAME\"/g" .env
        sed -i '' "s/cc-boilerplate/$PROJECT_NAME/g" .env

        # Update API keys if provided
        [ ! -z "$OPENAI_KEY" ] && sed -i '' "s/OPENAI_API_KEY=\"\"/OPENAI_API_KEY=\"$OPENAI_KEY\"/g" .env
        [ ! -z "$ANTHROPIC_KEY" ] && sed -i '' "s/ANTHROPIC_API_KEY=\"\"/ANTHROPIC_API_KEY=\"$ANTHROPIC_KEY\"/g" .env
        [ ! -z "$ELEVENLABS_KEY" ] && sed -i '' "s/ELEVENLABS_API_KEY=\"\"/ELEVENLABS_API_KEY=\"$ELEVENLABS_KEY\"/g" .env
        [ ! -z "$ELEVENLABS_VOICE_ID" ] && sed -i '' "s/ELEVENLABS_VOICE_ID=\"\"/ELEVENLABS_VOICE_ID=\"$ELEVENLABS_VOICE_ID\"/g" .env
    else
        # Linux
        sed -i "s/\"Your Name\"/\"$USER_NAME\"/g" .env
        sed -i "s/cc-boilerplate/$PROJECT_NAME/g" .env

        # Update API keys if provided
        [ ! -z "$OPENAI_KEY" ] && sed -i "s/OPENAI_API_KEY=\"\"/OPENAI_API_KEY=\"$OPENAI_KEY\"/g" .env
        [ ! -z "$ANTHROPIC_KEY" ] && sed -i "s/ANTHROPIC_API_KEY=\"\"/ANTHROPIC_API_KEY=\"$ANTHROPIC_KEY\"/g" .env
        [ ! -z "$ELEVENLABS_KEY" ] && sed -i "s/ELEVENLABS_API_KEY=\"\"/ELEVENLABS_API_KEY=\"$ELEVENLABS_KEY\"/g" .env
        [ ! -z "$ELEVENLABS_VOICE_ID" ] && sed -i "s/ELEVENLABS_VOICE_ID=\"\"/ELEVENLABS_VOICE_ID=\"$ELEVENLABS_VOICE_ID\"/g" .env
    fi

    echo " Created .env configuration"
else
    echo "�  Warning: .env.sample not found, skipping .env creation"
fi

# Create .mcp.json if ElevenLabs key provided
if [ ! -z "$ELEVENLABS_KEY" ] && [ -f .mcp.json.sample ]; then
    cp .mcp.json.sample .mcp.json
    echo " Created .mcp.json for ElevenLabs MCP server"
fi

# Update README with project name
if [ -f README.md ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/CC-Boilerplate/$PROJECT_NAME/g" README.md
        sed -i '' "s/cc-boilerplate/$PROJECT_NAME/g" README.md
    else
        sed -i "s/CC-Boilerplate/$PROJECT_NAME/g" README.md
        sed -i "s/cc-boilerplate/$PROJECT_NAME/g" README.md
    fi
    echo " Updated README.md with project name"
fi

# Create required directories if they don't exist
mkdir -p logs output
touch logs/.gitkeep output/.gitkeep

# Initialize git if not already initialized
if [ ! -d .git ]; then
    echo ""
    echo "🔧 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit from cc-boilerplate"
    echo " Git repository initialized"
fi

echo ""
echo "======================================"
echo "         Setup Complete!"
echo "======================================"
echo ""
echo "📋 Project Configuration:"
echo "   Name: $PROJECT_NAME"
echo "   User: $USER_NAME"
[ ! -z "$OPENAI_KEY" ] && echo "   OpenAI API: Configured"
[ ! -z "$ANTHROPIC_KEY" ] && echo "   Anthropic API: Configured"
[ ! -z "$ELEVENLABS_KEY" ] && echo "   ElevenLabs API: Configured"
echo ""
echo "📁 Files Created:"
echo "   .env (from .env.sample)"
[ ! -z "$ELEVENLABS_KEY" ] && echo "   .mcp.json (from .mcp.json.sample)"
echo "   logs/.gitkeep"
echo "   output/.gitkeep"
echo ""
echo "🚀 Next Steps:"
echo "  1. Review your .env configuration"
echo "  2. Start Claude Code: claude ."
echo "  3. Try the pre-configured hooks and agents"
echo "  4. Use /agents to explore available sub-agents"
echo "  5. Use meta-agent to create project-specific agents"
echo ""
echo "📚 Learn More:"
echo "  " See CLAUDE.md for development principles"
echo "  " All 8 hooks are pre-configured and active"
echo "  " 8 output styles available via /output-style"
echo "  " 4 status line versions in .claude/status_lines/"
echo ""
echo "Happy coding with Claude Code! <�"
