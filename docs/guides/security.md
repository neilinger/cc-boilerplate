# Security

Pre-execution validation prevents dangerous commands.

## Threat Protection

**Dangerous Commands**: 30+ rm patterns blocked
**Environment Files**: .env access blocked
**Path Traversal**: System file access prevented
**Input Validation**: Command injection filtered

## Hook Details

**pre_tool_use.py** validates all tool execution:

- Exit code 0: Allow
- Exit code 1: Block dangerous command
- Exit code 2: Block .env access
- Exit code 3: Block path traversal

## Blocked Commands

**rm patterns**: `rm -rf /`, `rm -rf ~/*`, `rm --recursive --force`
**env files**: `cat .env`, `echo > .env` (allows .env.sample)
**system paths**: `/etc/*`, `../../../*`, `/root/*`

## Test Security

```bash
# Should be blocked
echo '{"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}' | uv run .claude/hooks/pre_tool_use.py

# Should be allowed
echo '{"tool_name": "Bash", "tool_input": {"command": "rm file.txt"}}' | uv run .claude/hooks/pre_tool_use.py
```

## Security Levels

**strict** - Block all patterns (production)
**moderate** - Warn and block (development)
**permissive** - Warn only (testing)

Set in .env: `SECURITY_LEVEL=strict`

## Audit Commands

```bash
# View security blocks
grep "BLOCKED" logs/security.log

# Security test
python tests/test_safety_hooks.py
```

## Known Issues

- Command obfuscation may bypass detection
- Indirect .env access through temp files
- Unicode character evasion

**Mitigations**: Pattern updates, defense layers, audit logs
