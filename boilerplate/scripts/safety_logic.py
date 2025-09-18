#!/usr/bin/env python3
"""
Pure safety logic functions extracted from hooks for unit testing.

This module contains environment-agnostic safety validation logic that can be
tested independently of hook installation or subprocess execution.

Following KISS/YAGNI principles: simple functions, clear logic, no unnecessary complexity.
"""

import re
from typing import Dict, Any, List


def is_dangerous_rm_command(command: str) -> bool:
    """
    Comprehensive detection of dangerous rm commands.

    Args:
        command: Shell command string to check

    Returns:
        True if command contains dangerous rm patterns, False otherwise

    Examples:
        >>> is_dangerous_rm_command("rm -rf /")
        True
        >>> is_dangerous_rm_command("rm file.txt")
        False
        >>> is_dangerous_rm_command("echo rm -rf /")
        False
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


def is_safe_rm_command(command: str) -> bool:
    """
    Check if rm command is safe (specific files/directories, not dangerous paths).

    Args:
        command: Shell command string to check

    Returns:
        True if rm command appears safe, False otherwise

    Examples:
        >>> is_safe_rm_command("rm file.txt")
        True
        >>> is_safe_rm_command("rm -rf /tmp/specific_dir")
        True
        >>> is_safe_rm_command("rm -rf /")
        False
    """
    if not command or not isinstance(command, str):
        return False

    normalized = command.lower().strip()

    # Must be an rm command
    if not normalized.startswith('rm '):
        return False

    # If it's dangerous, it's not safe
    if is_dangerous_rm_command(command):
        return False

    # Additional checks for safe patterns
    safe_patterns = [
        r'\brm\s+[^-]',  # rm without flags (specific files)
        r'\brm\s+-[^rf]*\s+[^/~\*]',  # rm with safe flags and specific paths
        r'\brm\s+-r\s+[a-zA-Z0-9_\-/]+/[a-zA-Z0-9_\-/]+',  # rm -r with specific nested paths
        r'\brm\s+-rf\s+/tmp/[a-zA-Z0-9_\-/]+',  # rm -rf in /tmp with specific path
    ]

    for pattern in safe_patterns:
        if re.search(pattern, normalized):
            return True

    return False


def is_env_file_access(tool_name: str, tool_input: Dict[str, Any]) -> bool:
    """
    Check if any tool is trying to access .env files containing sensitive data.

    Args:
        tool_name: Name of the Claude Code tool being called
        tool_input: Input parameters for the tool

    Returns:
        True if tool is trying to access .env files, False otherwise

    Examples:
        >>> is_env_file_access("Read", {"file_path": ".env"})
        True
        >>> is_env_file_access("Read", {"file_path": ".env.sample"})
        False
        >>> is_env_file_access("Bash", {"command": "cat .env"})
        True
    """
    if not tool_name or not isinstance(tool_input, dict):
        return False

    if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write']:
        # Check file paths for file-based tools
        file_path = tool_input.get('file_path', '')
        if '.env' in file_path and not file_path.endswith('.env.sample'):
            return True

    elif tool_name == 'Bash':
        # Check bash commands for .env file access
        command = tool_input.get('command', '')
        # Pattern to detect .env file access (but allow .env.sample and .env.local)
        env_patterns = [
            r'\bcat\s+\.env\b(?!\.sample|\.local)',  # cat .env (but not .env.sample/.env.local)
            r'\bless\s+\.env\b(?!\.sample|\.local)',  # less .env
            r'\bhead\s+\.env\b(?!\.sample|\.local)',  # head .env
            r'\btail\s+\.env\b(?!\.sample|\.local)',  # tail .env
            r'\bgrep\s+.*\.env\b(?!\.sample|\.local)',  # grep something .env
            r'\bcp\s+\.env\s',  # cp .env (as source)
            r'\bmv\s+\.env\s',  # mv .env (as source)
            r'\brm\s+\.env\b(?!\.sample|\.local)',  # rm .env
            r'\becho\s+.*>\s*\.env\b(?!\.sample|\.local)',  # echo > .env
            r'\btouch\s+\.env\b(?!\.sample|\.local)',  # touch .env
        ]

        for pattern in env_patterns:
            if re.search(pattern, command):
                return True

    return False


def detect_command_injection_patterns(command: str) -> List[str]:
    """
    Detect potential command injection patterns in bash commands.

    Args:
        command: Shell command string to analyze

    Returns:
        List of detected injection patterns (empty if none found)

    Examples:
        >>> detect_command_injection_patterns("ls; rm -rf /")
        ['command_chaining']
        >>> detect_command_injection_patterns("ls $(dangerous_command)")
        ['command_substitution']
        >>> detect_command_injection_patterns("ls")
        []
    """
    if not command or not isinstance(command, str):
        return []

    patterns = []

    # Command chaining patterns
    if re.search(r'[;&|]+', command):
        if ';' in command:
            patterns.append('command_chaining_semicolon')
        if '&&' in command:
            patterns.append('command_chaining_and')
        if '||' in command:
            patterns.append('command_chaining_or')
        if '|' in command and '||' not in command:
            patterns.append('pipe_injection')

    # Command substitution patterns
    if re.search(r'\$\([^)]*\)', command):
        patterns.append('command_substitution_dollar')

    if re.search(r'`[^`]*`', command):
        patterns.append('command_substitution_backtick')

    # Variable expansion that could be dangerous
    if re.search(r'\$\{[^}]*\}', command):
        patterns.append('variable_expansion')

    return patterns


def validate_file_path_access(file_path: str, allowed_patterns: List[str] = None) -> bool:
    """
    Validate if file path access should be allowed.

    Args:
        file_path: Path to validate
        allowed_patterns: List of regex patterns for allowed paths

    Returns:
        True if access should be allowed, False otherwise

    Examples:
        >>> validate_file_path_access("/etc/passwd")
        False
        >>> validate_file_path_access("./project/file.txt")
        True
    """
    if not file_path:
        return False

    if allowed_patterns is None:
        # Default safe patterns - files within project directory
        allowed_patterns = [
            r'^\./[^/]',  # Relative paths starting with ./
            r'^[^/]',     # Relative paths not starting with /
            r'^/tmp/',    # Temporary files
            r'^/var/tmp/', # Temporary files
        ]

    # Dangerous patterns to always block
    dangerous_patterns = [
        r'^/etc/',     # System configuration
        r'^/bin/',     # System binaries
        r'^/sbin/',    # System binaries
        r'^/usr/bin/', # User binaries
        r'^/root/',    # Root home
        r'^/home/[^/]+/\.',  # Hidden files in user homes
        r'^\.\./.*/',  # Path traversal attempts
    ]

    # Block dangerous patterns first
    for pattern in dangerous_patterns:
        if re.search(pattern, file_path):
            return False

    # Allow if matches safe patterns
    for pattern in allowed_patterns:
        if re.search(pattern, file_path):
            return True

    return False


def get_safety_assessment(tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Comprehensive safety assessment for a tool call.

    Args:
        tool_name: Name of the Claude Code tool being called
        tool_input: Input parameters for the tool

    Returns:
        Dictionary with safety assessment results

    Examples:
        >>> result = get_safety_assessment("Bash", {"command": "rm -rf /"})
        >>> result['blocked']
        True
        >>> result['reason']
        'Dangerous rm command detected'
    """
    assessment = {
        'blocked': False,
        'reason': None,
        'warnings': [],
        'tool_name': tool_name,
        'patterns_detected': []
    }

    # Check .env file access
    if is_env_file_access(tool_name, tool_input):
        assessment['blocked'] = True
        assessment['reason'] = 'Access to .env files containing sensitive data is prohibited'
        assessment['patterns_detected'].append('env_file_access')
        return assessment

    # Check bash commands for various issues
    if tool_name == 'Bash':
        command = tool_input.get('command', '')

        # Check for dangerous rm commands
        if is_dangerous_rm_command(command):
            assessment['blocked'] = True
            assessment['reason'] = 'Dangerous rm command detected'
            assessment['patterns_detected'].append('dangerous_rm')
            return assessment

        # Check for command injection patterns
        injection_patterns = detect_command_injection_patterns(command)
        if injection_patterns:
            assessment['patterns_detected'].extend(injection_patterns)
            # For now, warn but don't block (could be made stricter)
            assessment['warnings'].append(f'Command injection patterns detected: {", ".join(injection_patterns)}')

    # Check file path access for file tools
    if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write']:
        file_path = tool_input.get('file_path', '')
        if file_path and not validate_file_path_access(file_path):
            assessment['blocked'] = True
            assessment['reason'] = f'File path access not allowed: {file_path}'
            assessment['patterns_detected'].append('unsafe_file_access')

    return assessment
