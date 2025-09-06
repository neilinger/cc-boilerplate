# Troubleshooting

Common issues and fixes.

## Quick Checks

```bash
uv --version
claude-code --version
chmod +x .claude/hooks/*.py
```

## Common Issues

**"Command not found: uv"**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

**"Hook execution failed"**  
Security hook blocked dangerous command. Check `logs/security.log`.

**"No module named 'dotenv'"**
```bash
cd .claude/hooks && uv sync
```

**".env file not found"**
```bash
cp .env.sample .env
# Edit with your API keys
```

**"Permission denied"**
```bash
chmod +x .claude/hooks/*.py
```

## TTS Issues

**No audio output**  
Check API keys: `echo $ELEVENLABS_API_KEY`  
Fallback to local: `TTS_DEFAULT_PROVIDER=pyttsx3`

**Commands blocked**  
Review security patterns, use alternative commands, or set `SECURITY_LEVEL=moderate`

**Hook timeout**  
Kill hanging processes: `pkill -f "hooks.*python"`  
Use local TTS: `TTS_DEFAULT_PROVIDER=pyttsx3`

**Import errors**  
Reinstall dependencies: `uv sync --reinstall`

**JSON errors**  
Test minimal input: `echo '{}' | uv run .claude/hooks/user_prompt_submit.py`

## Debug Mode

```bash
export DEBUG=true
grep "BLOCKED" logs/*.log
python tests/run_all_tests.py
```

### Legitimate Commands Blocked

**Symptoms**:
- Safe commands blocked by security hooks
- False positive security alerts
- Cannot execute necessary operations

**Diagnostic**:
```bash
# Test specific command blocking
echo '{"tool_name": "Bash", "tool_input": {"command": "YOUR_COMMAND"}}' | \
  uv run .claude/hooks/pre_tool_use.py --debug

# Review security patterns
grep -n "patterns\|dangerous" .claude/hooks/pre_tool_use.py
```

**Solutions**:
1. **Temporary bypass** (use carefully):
   ```bash
   # Set permissive mode temporarily
   export SECURITY_LEVEL=permissive
   ```

2. **Update security patterns**:
   ```python
   # In pre_tool_use.py, add to whitelist_patterns:
   whitelist_patterns = [
       r'rm -rf \./build/',     # Allow build directory cleanup
       r'rm -rf \./temp/',      # Allow temp directory cleanup
   ]
   ```

3. **Use alternative commands**:
   ```bash
   # Instead of: rm -rf ./build/*
   # Use: find ./build -type f -delete
   ```

### .env File Access Issues

**Symptoms**:
- Cannot read .env.sample
- Blocked from creating .env file
- Configuration files inaccessible

**Diagnostic**:
```bash
# Check .env file protection patterns
grep -A 10 "is_env_file_access" .claude/hooks/pre_tool_use.py

# Test .env access
echo '{"tool_name": "Read", "tool_input": {"file_path": ".env.sample"}}' | \
  uv run .claude/hooks/pre_tool_use.py
```

**Solutions**:
1. **Use allowed file extensions**:
   ```bash
   # These are allowed:
   .env.sample
   .env.template  
   .env.example
   
   # These are blocked:
   .env
   .environment
   ```

2. **Create .env from template**:
   ```bash
   # This works because it's a bash command, not direct .env access
   cp .env.sample .env
   ```

## Performance Issues

### Slow Hook Execution

**Symptoms**:
- Claude Code responses delayed
- Hook execution over 5 seconds
- High CPU usage during hooks

**Diagnostic**:
```bash
# Profile hook execution time
time echo '{"message": "test"}' | uv run .claude/hooks/notification.py

# Check system resources
top -p $(pgrep -f "claude-code")

# Test individual components
time uv run .claude/hooks/utils/tts/pyttsx3_tts.py --text "test"
```

**Solutions**:
1. **Optimize TTS provider selection**:
   ```bash
   # Use fastest local provider
   export TTS_DEFAULT_PROVIDER=pyttsx3
   ```

2. **Reduce hook complexity**:
   ```python
   # In hooks, add early returns:
   if not message_important:
       print(json.dumps({"status": "skipped"}))
       sys.exit(0)
   ```

3. **Cache frequently used data**:
   ```python
   # Cache API key validation
   @lru_cache(maxsize=1)
   def validate_api_key(key):
       # validation logic
   ```

### High Memory Usage

**Symptoms**:
- System running out of memory
- Claude Code becoming sluggish
- OS memory warnings

**Diagnostic**:
```bash
# Check memory usage
ps aux --sort=-%mem | head -10

# Monitor Claude Code specifically
ps -o pid,vsz,rss,comm -p $(pgrep claude-code)
```

**Solutions**:
1. **Limit concurrent hook executions**:
   ```json
   // settings.json
   {
     "hooks": {
       "max_concurrent": 2
     }
   }
   ```

2. **Clear hook caches**:
   ```bash
   # Clear UV cache
   uv cache clean

   # Clear Python cache
   find . -name "__pycache__" -exec rm -rf {} +
   ```

## Recovery Procedures

### Complete System Reset

**When to use**: System completely broken, multiple failures.

```bash
#!/bin/bash
echo "🔄 Starting CC-Boilerplate recovery..."

# 1. Backup current configuration
cp .env .env.backup 2>/dev/null
cp .claude/settings.json .claude/settings.json.backup 2>/dev/null

# 2. Reset hook permissions
chmod +x .claude/hooks/*.py

# 3. Reinstall UV dependencies
uv sync --reinstall

# 4. Reset configuration files
if [ ! -f .env ]; then
    cp .env.sample .env
    echo "⚠️  Please edit .env with your API keys"
fi

# 5. Test critical systems
echo "🧪 Testing critical systems..."
echo '{}' | uv run .claude/hooks/user_prompt_submit.py && echo "✅ user_prompt_submit"
echo '{"tool_name": "Bash", "tool_input": {"command": "echo test"}}' | uv run .claude/hooks/pre_tool_use.py && echo "✅ pre_tool_use"
echo '{"message": "test"}' | uv run .claude/hooks/notification.py && echo "✅ notification"

echo "✅ Recovery complete"
```

### Hook-Specific Recovery

**Individual hook failures**:

```bash
# Reset specific hook
hook_name="pre_tool_use"

# 1. Check hook integrity
python -m py_compile .claude/hooks/${hook_name}.py

# 2. Test hook with minimal input
echo '{}' | uv run .claude/hooks/${hook_name}.py

# 3. Reset hook permissions
chmod +x .claude/hooks/${hook_name}.py

# 4. Validate UV script header
head -10 .claude/hooks/${hook_name}.py
```

### Configuration Recovery

**Settings corruption**:

```bash
# Backup current (possibly corrupted) settings
mv .claude/settings.json .claude/settings.json.corrupted

# Create minimal working configuration
cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "user_prompt_submit": {"enabled": true},
    "pre_tool_use": {"enabled": true},
    "post_tool_use": {"enabled": true},
    "notification": {"enabled": true},
    "stop": {"enabled": true},
    "subagent_stop": {"enabled": true},
    "pre_compact": {"enabled": true},
    "session_start": {"enabled": true}
  },
  "security": {
    "dangerous_commands": true,
    "env_file_protection": true
  }
}
EOF

# Test configuration
python -c "import json; json.load(open('.claude/settings.json'))" && echo "✅ Valid JSON"
```

## Advanced Debugging

### Enable Debug Logging

```bash
# Global debug mode
export DEBUG=true
export VERBOSE=true

# Hook-specific debugging
export HOOK_DEBUG=true

# Security hook debugging
export SECURITY_DEBUG=true
```

### Log Analysis

```bash
# View recent hook executions
tail -50 logs/hooks.log | jq .

# Filter security events
grep "BLOCKED\|security" logs/*.log

# Analyze performance
grep "execution_time" logs/hooks.log | sort -k2 -n
```

### Network Debugging

```bash
# Test API connectivity
curl -I https://api.elevenlabs.io/v1/user
curl -I https://api.openai.com/v1/models

# Check network proxy settings
env | grep -i proxy

# Test DNS resolution
nslookup api.elevenlabs.io
```

### System Integration Testing

```bash
# Full system test
python tests/run_all_tests.py

# Security-specific tests
python tests/test_safety_hooks.py

# TTS integration tests
python tests/test_tts_providers.py
```

## Getting Additional Help

### Log Collection for Support

```bash
# Collect diagnostic information
cat > debug_info.txt << EOF
=== System Info ===
$(uv --version)
$(python --version)
$(which claude-code && claude-code --version)

=== Environment ===
$(env | grep -E "(API_KEY|TTS|USER|DEBUG)" | sed 's/=.*/=***/')

=== Hook Status ===
$(ls -la .claude/hooks/*.py | head -5)

=== Recent Logs ===
$(tail -20 logs/hooks.log 2>/dev/null || echo "No hook logs found")

=== Configuration ===
$(head -20 .claude/settings.json 2>/dev/null || echo "No settings.json found")
EOF

echo "Debug info collected in debug_info.txt"
```

### Common Diagnostic Questions

Before seeking help, please check:

1. **What version of Claude Code are you using?**
2. **What operating system and version?**
3. **What command or action triggered the issue?**
4. **What error messages do you see?**
5. **When did this issue start occurring?**
6. **Have you made any recent configuration changes?**

### Resources

- **Documentation**: [docs/](docs/) directory
- **Security Guide**: [docs/SECURITY.md](docs/SECURITY.md)
- **API Reference**: [docs/API.md](docs/API.md)
- **Test Suite**: `python tests/run_all_tests.py`

Remember: When in doubt, run the diagnostic commands and check the logs. Most issues have clear error messages that point to the solution.