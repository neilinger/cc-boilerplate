#!/usr/bin/env python3
"""
Mock subprocess infrastructure for controlled command execution testing.

This module provides MockSubprocessRunner and utilities to simulate subprocess
execution with controlled results, enabling safe testing of bash commands
without executing dangerous operations.

Following KISS/YAGNI: Simple mock system focused on essential testing needs.
"""

import re
import time
import subprocess
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union, Callable
from unittest.mock import MagicMock


@dataclass 
class MockSubprocessResult:
    """
    Mock result for subprocess execution.
    
    Mimics subprocess.CompletedProcess interface for testing.
    """
    args: Union[str, List[str]]
    returncode: int
    stdout: str = ""
    stderr: str = ""
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def check_returncode(self):
        """Raise CalledProcessError if returncode is non-zero."""
        if self.returncode != 0:
            raise subprocess.CalledProcessError(
                self.returncode, self.args, self.stdout, self.stderr
            )


class MockSubprocessRunner:
    """
    Mock subprocess execution system for safe command testing.
    
    Provides controlled subprocess execution without running dangerous commands.
    Records all command attempts and returns configured responses.
    
    Usage:
        runner = MockSubprocessRunner()
        runner.add_command_response('ls', MockSubprocessResult(['ls'], 0, 'file1\nfile2'))
        result = runner.run(['ls'])
    """
    
    def __init__(self):
        """Initialize mock subprocess runner."""
        self.command_responses: Dict[str, MockSubprocessResult] = {}
        self.pattern_responses: List[tuple] = []  # (pattern, response)
        self.executed_commands: List[Dict[str, Any]] = []
        self.default_response = MockSubprocessResult([], 0)
        self.blocked_patterns: List[str] = []
        self.auto_block_dangerous = True
        
        # Default dangerous patterns to block
        self.dangerous_patterns = [
            r'\brm\s+.*-[a-z]*r[a-z]*f',  # rm -rf variants
            r'\bsudo\b',                   # sudo commands
            r'\bsu\b',                     # su commands  
            r'\bchmod\s+777',             # chmod 777
            r'\bdd\s+if=',                # dd commands
            r'\bmkfs\b',                  # filesystem creation
            r'\bfdisk\b',                 # disk partitioning
            r'>\s*/dev/',                 # writing to device files
            r'\bkill\s+-9\s+1\b',        # kill init process
            r'/etc/passwd',               # system files
            r'/etc/shadow',               # system files
        ]
    
    def add_command_response(self, command: str, response: MockSubprocessResult):
        """
        Configure response for specific command.
        
        Args:
            command: Command string to match (exact match)
            response: MockSubprocessResult to return
        """
        self.command_responses[command] = response
    
    def add_pattern_response(self, pattern: str, response: MockSubprocessResult):
        """
        Configure response for command pattern.
        
        Args:
            pattern: Regex pattern to match commands
            response: MockSubprocessResult to return
        """
        self.pattern_responses.append((re.compile(pattern), response))
    
    def set_default_response(self, response: MockSubprocessResult):
        """Set default response for unmatched commands."""
        self.default_response = response
    
    def block_pattern(self, pattern: str):
        """
        Add pattern to blocked command list.
        
        Args:
            pattern: Regex pattern to block
        """
        self.blocked_patterns.append(pattern)
    
    def run(self, args: Union[str, List[str]], **kwargs) -> MockSubprocessResult:
        """
        Mock subprocess.run() with controlled responses.
        
        Args:
            args: Command arguments (string or list)
            **kwargs: Additional arguments (captured for verification)
            
        Returns:
            MockSubprocessResult based on configured responses
            
        Raises:
            PermissionError: If command matches dangerous patterns and auto_block_dangerous is True
        """
        # Normalize command to string for pattern matching
        if isinstance(args, list):
            command_str = ' '.join(str(arg) for arg in args)
        else:
            command_str = str(args)
        
        # Record execution attempt
        execution_record = {
            'args': args,
            'command_str': command_str,
            'kwargs': kwargs.copy(),
            'timestamp': time.time()
        }
        self.executed_commands.append(execution_record)
        
        # Check blocked patterns first
        if self.auto_block_dangerous:
            for pattern in self.dangerous_patterns + self.blocked_patterns:
                if re.search(pattern, command_str, re.IGNORECASE):
                    raise PermissionError(
                        f"Dangerous command blocked by mock: {command_str} "
                        f"(matched pattern: {pattern})"
                    )
        
        # Check for exact command match
        if command_str in self.command_responses:
            response = self.command_responses[command_str]
            response.args = args
            return response
        
        # Check pattern matches
        for pattern, response in self.pattern_responses:
            if pattern.search(command_str):
                response.args = args
                return response
        
        # Return default response
        self.default_response.args = args
        return self.default_response
    
    def get_executed_commands(self, pattern: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get recorded command executions for verification.
        
        Args:
            pattern: Optional regex pattern to filter commands
            
        Returns:
            List of recorded command executions
        """
        if pattern is None:
            return self.executed_commands.copy()
        
        compiled_pattern = re.compile(pattern, re.IGNORECASE)
        return [
            cmd for cmd in self.executed_commands 
            if compiled_pattern.search(cmd['command_str'])
        ]
    
    def clear_executions(self):
        """Clear recorded command executions."""
        self.executed_commands.clear()
    
    def reset(self):
        """Reset all recorded executions and configured responses."""
        self.executed_commands.clear()
        self.command_responses.clear()
        self.pattern_responses.clear()
        self.blocked_patterns.clear()
    
    def disable_dangerous_blocking(self):
        """Disable automatic blocking of dangerous commands (use with caution)."""
        self.auto_block_dangerous = False
    
    def enable_dangerous_blocking(self):
        """Re-enable automatic blocking of dangerous commands."""
        self.auto_block_dangerous = True


class MockPopen:
    """
    Mock for subprocess.Popen class.
    
    Provides controlled simulation of process execution for testing.
    """
    
    def __init__(self, args, **kwargs):
        """Initialize mock process."""
        self.args = args
        self.kwargs = kwargs
        self.returncode = 0
        self.stdout = None
        self.stderr = None
        self._started = False
        self._finished = False
    
    def communicate(self, input=None, timeout=None):
        """Mock communicate method."""
        if not self._started:
            self._started = True
        self._finished = True
        return (self.stdout, self.stderr)
    
    def wait(self, timeout=None):
        """Mock wait method.""" 
        if not self._finished:
            self._finished = True
        return self.returncode
    
    def poll(self):
        """Mock poll method."""
        return self.returncode if self._finished else None
    
    def kill(self):
        """Mock kill method."""
        self.returncode = -9
        self._finished = True
    
    def terminate(self):
        """Mock terminate method."""
        self.returncode = -15
        self._finished = True


def create_safe_subprocess_responses() -> Dict[str, MockSubprocessResult]:
    """
    Factory function for common safe command responses.
    
    Returns:
        Dictionary of commonly used mock responses for safe commands
    """
    return {
        'ls': MockSubprocessResult(['ls'], 0, 'file1.txt\nfile2.txt\ndirectory1/'),
        'pwd': MockSubprocessResult(['pwd'], 0, '/Users/test/project'),
        'echo test': MockSubprocessResult(['echo', 'test'], 0, 'test'),
        'python --version': MockSubprocessResult(['python', '--version'], 0, 'Python 3.9.0'),
        'git status': MockSubprocessResult(['git', 'status'], 0, 'On branch main\nnothing to commit'),
        'whoami': MockSubprocessResult(['whoami'], 0, 'testuser'),
        'date': MockSubprocessResult(['date'], 0, 'Thu Jan  1 12:00:00 UTC 2025'),
    }


def create_error_responses() -> Dict[str, MockSubprocessResult]:
    """
    Factory function for common error command responses.
    
    Returns:
        Dictionary of commonly used error responses for testing
    """
    return {
        'ls /nonexistent': MockSubprocessResult(
            ['ls', '/nonexistent'], 1, '', 'ls: /nonexistent: No such file or directory'
        ),
        'cat /dev/null/file': MockSubprocessResult(
            ['cat', '/dev/null/file'], 1, '', 'cat: /dev/null/file: Not a directory'
        ),
        'python nonexistent.py': MockSubprocessResult(
            ['python', 'nonexistent.py'], 2, '', 'python: can\'t open file \'nonexistent.py\''
        ),
    }


def patch_subprocess_module(mock_runner: MockSubprocessRunner):
    """
    Create patches for subprocess module using mock runner.
    
    Args:
        mock_runner: MockSubprocessRunner to use for responses
        
    Returns:
        Dictionary of patches that can be applied with unittest.mock.patch
    """
    def mock_run(*args, **kwargs):
        return mock_runner.run(*args, **kwargs)
    
    def mock_popen(*args, **kwargs):
        # Create MockPopen instance
        process = MockPopen(*args, **kwargs)
        
        # Try to get response from runner
        try:
            result = mock_runner.run(*args, **kwargs)
            process.returncode = result.returncode
            process.stdout = result.stdout.encode() if kwargs.get('capture_output') else None
            process.stderr = result.stderr.encode() if kwargs.get('capture_output') else None
        except PermissionError:
            process.returncode = 1
            process.stderr = b"Command blocked by mock"
        
        return process
    
    return {
        'subprocess.run': mock_run,
        'subprocess.Popen': mock_popen,
        'subprocess.call': lambda *args, **kwargs: mock_runner.run(*args, **kwargs).returncode,
        'subprocess.check_call': lambda *args, **kwargs: mock_runner.run(*args, **kwargs).check_returncode(),
        'subprocess.check_output': lambda *args, **kwargs: mock_runner.run(*args, **kwargs).stdout.encode(),
    }


# Convenience functions for common test scenarios  
def create_safe_runner() -> MockSubprocessRunner:
    """Create a runner with safe command responses configured."""
    runner = MockSubprocessRunner()
    
    # Add common safe responses
    safe_responses = create_safe_subprocess_responses()
    for command, response in safe_responses.items():
        runner.add_command_response(command, response)
    
    return runner


def create_blocking_runner() -> MockSubprocessRunner:
    """Create a runner that blocks all commands."""
    runner = MockSubprocessRunner()
    runner.block_pattern(r'.*')  # Block everything
    return runner


def create_error_runner() -> MockSubprocessRunner:
    """Create a runner that returns errors for all commands.""" 
    runner = MockSubprocessRunner()
    runner.set_default_response(MockSubprocessResult(
        [], 1, '', 'Mock error: command failed'
    ))
    return runner