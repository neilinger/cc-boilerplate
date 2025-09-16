#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import sys
import re
from pathlib import Path

def is_dangerous_rm_command(command):
    """
    Comprehensive detection of dangerous rm commands.
    Matches various forms of rm -rf and similar destructive patterns.
    """
    if not command or not isinstance(command, str):
        return False

    # Normalize command by removing extra spaces and converting to lowercase
    normalized = ' '.join(command.lower().split())

    # Don't flag commands that are just printing or commenting rm commands
    if normalized.startswith('echo ') or normalized.startswith('#'):
        return False

    # Check for --no-preserve-root flag (extremely dangerous)
    if re.search(r'--no-preserve-root', normalized):
        return True

    # Check for command chaining/injection patterns with rm
    if re.search(r'\brm\s+.*-[a-z]*[rf]', normalized):  # If rm has r or f flags
        chaining_patterns = [
            r'&\s*$',           # Background execution: rm -rf / &
            r';\s*',            # Command chaining: rm -rf / ; echo done
            r'\|\|\s*',         # OR chaining: rm -rf / || echo
            r'&&\s*',           # AND chaining: rm -rf / && echo
            r'\|\s*(?!\s)',     # Pipe: rm -rf / | other_cmd
        ]

        for pattern in chaining_patterns:
            if re.search(pattern, normalized):
                return True

    # Check for dangerous rm commands anywhere in command chains/injections
    injection_patterns = [
        r';\s*rm\s+.*-[a-z]*[rf].*/',      # ; rm -rf /
        r'&&\s*rm\s+.*-[a-z]*[rf].*/',     # && rm -rf /
        r'\|\|\s*rm\s+.*-[a-z]*[rf].*/',   # || rm -rf /
        r'\|\s*rm\s+.*-[a-z]*[rf].*/',     # | rm -rf /
        r'\$\(.*rm\s+.*-[a-z]*[rf].*\)',   # $(rm -rf /)
        r'`.*rm\s+.*-[a-z]*[rf].*`',       # `rm -rf /`
    ]

    for pattern in injection_patterns:
        if re.search(pattern, normalized):
            return True

    # Check if command has both recursive and force flags (in any format)
    has_r_flag = bool(re.search(r'\brm\s+.*-[a-z]*r', normalized) or
                     re.search(r'\brm\s+.*--recursive', normalized))
    has_f_flag = bool(re.search(r'\brm\s+.*-[a-z]*f', normalized) or
                     re.search(r'\brm\s+.*--force', normalized))
    has_rf_flags = has_r_flag and has_f_flag

    # If it has both recursive and force flags, check for dangerous paths
    if has_rf_flags:
        dangerous_path_patterns = [
            r'\brm\s+.*\s+/$',          # rm -rf targeting root: rm -rf /
            r'\brm\s+.*\s+/\s*$',       # rm -rf targeting root exactly: rm -rf / (end)
            r'\brm\s+.*\s+/\*',         # rm -rf targeting root wildcard: rm -rf /*
            r'\brm\s+.*\s+~$',          # rm -rf targeting home: rm -rf ~
            r'\brm\s+.*\s+~/$',         # rm -rf targeting home path: rm -rf ~/
            r'\brm\s+.*\s+\$home\s*$',  # rm -rf targeting $HOME: rm -rf $HOME
            r'\brm\s+.*\s+\.\.$',       # rm -rf targeting parent: rm -rf ..
            r'\brm\s+.*\s+\.\./\.\.',   # rm -rf targeting multiple parents: rm -rf ../..
            r'\brm\s+.*\s+\.$',         # rm -rf targeting current: rm -rf .
            r'\brm\s+.*\s+\./$',        # rm -rf targeting current: rm -rf ./
            r'\brm\s+.*\s+\*$',         # rm -rf targeting wildcard: rm -rf *
            r'\brm\s+.*\s+\$\(.*\)',    # rm -rf with command substitution: rm -rf $(pwd)
            r'\brm\s+.*\s+`.*`',        # rm -rf with backticks: rm -rf `pwd`
        ]

        # Only dangerous if it matches a dangerous path pattern
        for pattern in dangerous_path_patterns:
            if re.search(pattern, normalized):
                return True

    # Also check for rm -r (without force) with dangerous paths
    elif re.search(r'\brm\s+.*-[a-z]*r', normalized):  # If rm has recursive flag
        simple_dangerous_patterns = [
            r'\brm\s+.*\s+/$',          # rm -r /
            r'\brm\s+.*\s+/\s*$',       # rm -r / (end)
            r'\brm\s+.*\s+~$',          # rm -r ~
            r'\brm\s+.*\s+\.\.$',       # rm -r ..
            r'\brm\s+.*\s+\.$',         # rm -r .
            r'\brm\s+.*\s+\*$',         # rm -r *
        ]

        for pattern in simple_dangerous_patterns:
            if re.search(pattern, normalized):
                return True

    return False

def is_env_file_access(tool_name, tool_input):
    """
    Check if any tool is trying to access .env files containing sensitive data.
    """
    if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write', 'Bash']:
        # Check file paths for file-based tools
        if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write']:
            file_path = tool_input.get('file_path', '')
            if '.env' in file_path and not file_path.endswith('.env.sample'):
                return True

        # Check bash commands for .env file access
        elif tool_name == 'Bash':
            command = tool_input.get('command', '')
            # Pattern to detect .env file access (but allow .env.sample)
            env_patterns = [
                r'\b\.env\b(?!\.sample)',  # .env but not .env.sample
                r'cat\s+.*\.env\b(?!\.sample)',  # cat .env
                r'less\s+.*\.env\b(?!\.sample)',  # less .env
                r'more\s+.*\.env\b(?!\.sample)',  # more .env
                r'head\s+.*\.env\b(?!\.sample)',  # head .env
                r'tail\s+.*\.env\b(?!\.sample)',  # tail .env
                r'grep\s+.*\.env\b(?!\.sample)',  # grep .env
                r'echo\s+.*>\s*\.env\b(?!\.sample)',  # echo > .env
                r'touch\s+.*\.env\b(?!\.sample)',  # touch .env
                r'cp\s+.*\.env\b(?!\.sample)',  # cp .env
                r'mv\s+.*\.env\b(?!\.sample)',  # mv .env
                r'rm\s+.*\.env\b(?!\.sample)',  # rm .env
            ]

            for pattern in env_patterns:
                if re.search(pattern, command):
                    return True

    return False

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})

        # Check for .env file access (blocks access to sensitive environment files)
        if is_env_file_access(tool_name, tool_input):
            print("BLOCKED: Access to .env files containing sensitive data is prohibited", file=sys.stderr)
            print("Use .env.sample for template files instead", file=sys.stderr)
            sys.exit(2)  # Exit code 2 blocks tool call and shows error to Claude

        # Check for dangerous rm -rf commands
        if tool_name == 'Bash':
            command = tool_input.get('command', '')

            # Block rm -rf commands with comprehensive pattern matching
            if is_dangerous_rm_command(command):
                print("BLOCKED: Dangerous rm command detected and prevented", file=sys.stderr)
                sys.exit(2)  # Exit code 2 blocks tool call and shows error to Claude

        # Ensure log directory exists
        log_dir = Path.cwd() / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / 'pre_tool_use.json'

        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Append new data
        log_data.append(input_data)

        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)

        sys.exit(0)

    except json.JSONDecodeError:
        # Gracefully handle JSON decode errors
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)

if __name__ == '__main__':
    main()
