# Suggested Commands for Claude Code Hooks Mastery

## Development Commands

```bash
# UV Package Management
uv run <script.py>              # Run UV single-file script
uv add <package>                # Add dependency (if using pyproject.toml)

# Git Operations (use gh CLI as specified in CLAUDE.md)
gh repo view                    # View repository information
gh issue list                   # List issues
gh pr create                    # Create pull request
git status                      # Check working directory status
git log --oneline -5            # Recent commits
```

## Claude Code Commands

```bash
# Custom Commands (from .claude/commands/)
/prime                          # Project analysis and understanding
/crypto_research               # Cryptocurrency research workflows
/cook                          # Advanced task execution
/update_status_line            # Dynamic status updates

# Output Style Commands
/output-style genui            # Beautiful HTML with styling
/output-style table-based      # Markdown tables
/output-style tts-summary      # Audio feedback
```

## System Commands (Darwin/macOS)

```bash
# File Operations
find . -name "*.py" -type f     # Find Python files
grep -r "pattern" .             # Search in files
ls -la                          # List files with details
cp source dest                  # Copy files
mv source dest                  # Move/rename files
chmod +x file                   # Make executable

# Process Management
ps aux | grep python           # Find Python processes
kill -9 <pid>                 # Force kill process
```

## Hook Testing

```bash
# View hook logs
cat logs/user_prompt_submit.json | jq '.'
cat logs/pre_tool_use.json | jq '.'
cat logs/stop.json | jq '.'

# Test individual hooks
echo '{"prompt":"test"}' | uv run .claude/hooks/user_prompt_submit.py
```
