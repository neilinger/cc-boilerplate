#!/usr/bin/env python3
"""
Mock infrastructure for comprehensive testing without environmental dependencies.

This module provides mock utilities for testing Claude Code hooks, subprocess
execution, file system operations, and environment variables without side effects.

Following KISS/YAGNI: Simple, focused mocking utilities that enable reliable testing
in both CI and local environments.

Available Mock Systems:
- MockHookRunner: Simulates hook execution with controlled responses
- MockSubprocessRunner: Controlled subprocess execution for testing
- MockFileSystem: Safe file system operations without side effects
- MockEnvironment: Environment variable management with isolation
"""

from .mock_hooks import MockHookRunner, MockHookResponse, MockHookAction, MockSafetyHook
from .mock_subprocess import MockSubprocessRunner, MockSubprocessResult
from .mock_filesystem import MockFileSystem, MockFileSystemError
from .mock_environment import MockEnvironment, isolated_environment

__all__ = [
    'MockHookRunner',
    'MockHookResponse',
    'MockHookAction',
    'MockSafetyHook',
    'MockSubprocessRunner',
    'MockSubprocessResult',
    'MockFileSystem',
    'MockFileSystemError',
    'MockEnvironment',
    'isolated_environment',
]

__version__ = '1.0.0'