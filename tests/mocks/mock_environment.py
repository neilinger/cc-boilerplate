#!/usr/bin/env python3
"""
Mock environment infrastructure for isolated environment variable testing.

This module provides MockEnvironment and utilities to manage environment
variables in tests without affecting the real environment, enabling
proper test isolation and cleanup.

Following KISS/YAGNI: Simple environment management with clear responsibilities.
"""

import os
import copy
from typing import Dict, Optional, Set, Any, List
from dataclasses import dataclass, field
from contextlib import contextmanager


@dataclass
class EnvironmentChange:
    """
    Record of an environment variable change for tracking.
    
    Simple data structure to track what happened to environment variables.
    """
    action: str  # 'set', 'unset', 'change'
    key: str
    old_value: Optional[str]
    new_value: Optional[str]
    timestamp: float = field(default_factory=lambda: __import__('time').time())


class MockEnvironment:
    """
    Mock environment variable management for isolated testing.
    
    Provides controlled environment variable manipulation with automatic
    backup/restore capabilities and change tracking for verification.
    
    Usage:
        env = MockEnvironment()
        env.set('TEST_VAR', 'test_value')
        # ... run tests ...
        env.restore()  # Restores original environment
    """
    
    def __init__(self, isolated: bool = True):
        """
        Initialize mock environment.
        
        Args:
            isolated: If True, start with empty environment. If False, use current environment.
        """
        self.original_env: Dict[str, str] = {}
        self.mock_env: Dict[str, str] = {}
        self.changes: List[EnvironmentChange] = []
        self.protected_vars: Set[str] = set()
        self.blocked_vars: Set[str] = set()
        self.isolated = isolated
        
        # Backup original environment
        self._backup_environment()
        
        # Initialize mock environment
        if isolated:
            self.mock_env = {}
        else:
            self.mock_env = self.original_env.copy()
    
    def _backup_environment(self):
        """Backup current environment variables."""
        self.original_env = os.environ.copy()
    
    def _record_change(self, action: str, key: str, old_value: Optional[str], new_value: Optional[str]):
        """Record environment variable change."""
        change = EnvironmentChange(
            action=action,
            key=key,
            old_value=old_value,
            new_value=new_value
        )
        self.changes.append(change)
    
    def set(self, key: str, value: str):
        """
        Set environment variable.
        
        Args:
            key: Environment variable name
            value: Environment variable value
            
        Raises:
            PermissionError: If variable is protected or blocked
        """
        if key in self.blocked_vars:
            raise PermissionError(f"Environment variable {key} is blocked")
        
        if key in self.protected_vars and key in self.mock_env:
            raise PermissionError(f"Environment variable {key} is protected")
        
        old_value = self.mock_env.get(key)
        self.mock_env[key] = value
        
        action = 'change' if old_value is not None else 'set'
        self._record_change(action, key, old_value, value)
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get environment variable value.
        
        Args:
            key: Environment variable name
            default: Default value if not found
            
        Returns:
            Environment variable value or default
        """
        return self.mock_env.get(key, default)
    
    def unset(self, key: str):
        """
        Unset (remove) environment variable.
        
        Args:
            key: Environment variable name
            
        Raises:
            PermissionError: If variable is protected
        """
        if key in self.protected_vars:
            raise PermissionError(f"Environment variable {key} is protected")
        
        if key in self.blocked_vars:
            raise PermissionError(f"Environment variable {key} is blocked")
        
        old_value = self.mock_env.get(key)
        if old_value is not None:
            del self.mock_env[key]
            self._record_change('unset', key, old_value, None)
    
    def has(self, key: str) -> bool:
        """Check if environment variable exists."""
        return key in self.mock_env
    
    def keys(self) -> List[str]:
        """Get all environment variable names."""
        return list(self.mock_env.keys())
    
    def items(self) -> List[tuple]:
        """Get all environment variable key-value pairs."""
        return list(self.mock_env.items())
    
    def protect(self, key: str):
        """
        Protect environment variable from modification.
        
        Args:
            key: Environment variable name to protect
        """
        self.protected_vars.add(key)
    
    def block(self, key: str):
        """
        Block environment variable from being set or accessed.
        
        Args:
            key: Environment variable name to block
        """
        self.blocked_vars.add(key)
    
    def apply_to_os_environ(self):
        """
        Apply mock environment to os.environ.
        
        WARNING: This modifies the real environment. Use with caution.
        """
        os.environ.clear()
        os.environ.update(self.mock_env)
    
    def restore(self):
        """Restore original environment variables."""
        os.environ.clear()
        os.environ.update(self.original_env)
    
    def clear_changes(self):
        """Clear recorded changes."""
        self.changes.clear()
    
    def get_changes(self, action_filter: Optional[str] = None) -> List[EnvironmentChange]:
        """
        Get recorded environment changes.
        
        Args:
            action_filter: Optional filter for specific action type
            
        Returns:
            List of recorded changes
        """
        if action_filter is None:
            return self.changes.copy()
        return [change for change in self.changes if change.action == action_filter]
    
    def load_from_dict(self, env_dict: Dict[str, str], clear_existing: bool = False):
        """
        Load environment variables from dictionary.
        
        Args:
            env_dict: Dictionary of environment variables
            clear_existing: Whether to clear existing variables first
        """
        if clear_existing:
            old_keys = set(self.mock_env.keys())
            self.mock_env.clear()
            
            # Record clearing of old variables
            for key in old_keys:
                self._record_change('unset', key, self.original_env.get(key), None)
        
        # Set new variables
        for key, value in env_dict.items():
            old_value = self.mock_env.get(key)
            self.mock_env[key] = value
            
            action = 'change' if old_value is not None else 'set'
            self._record_change(action, key, old_value, value)
    
    def to_dict(self) -> Dict[str, str]:
        """Get current environment as dictionary."""
        return self.mock_env.copy()
    
    def reset_to_original(self):
        """Reset mock environment to original state."""
        old_keys = set(self.mock_env.keys())
        self.mock_env = self.original_env.copy()
        
        # Record the reset
        for key in old_keys:
            if key not in self.original_env:
                self._record_change('unset', key, self.mock_env.get(key), None)
        
        for key, value in self.original_env.items():
            if key not in old_keys or self.mock_env.get(key) != value:
                old_value = self.mock_env.get(key) if key in old_keys else None
                self._record_change('change' if old_value else 'set', key, old_value, value)


@contextmanager
def isolated_environment(env_vars: Optional[Dict[str, str]] = None):
    """
    Context manager for isolated environment testing.
    
    Args:
        env_vars: Optional dictionary of environment variables to set
        
    Usage:
        with isolated_environment({'TEST_VAR': 'test_value'}):
            # Test code runs with only TEST_VAR set
            assert os.environ.get('TEST_VAR') == 'test_value'
        # Original environment is restored
    """
    mock_env = MockEnvironment(isolated=True)
    
    if env_vars:
        mock_env.load_from_dict(env_vars)
    
    mock_env.apply_to_os_environ()
    
    try:
        yield mock_env
    finally:
        mock_env.restore()


@contextmanager
def modified_environment(env_vars: Dict[str, str]):
    """
    Context manager for temporarily modifying environment.
    
    Args:
        env_vars: Dictionary of environment variables to set/change
        
    Usage:
        with modified_environment({'DEBUG': 'true', 'API_KEY': 'test_key'}):
            # Test code runs with modified environment
            pass
        # Original environment is restored
    """
    mock_env = MockEnvironment(isolated=False)
    
    # Set the new variables
    for key, value in env_vars.items():
        mock_env.set(key, value)
    
    mock_env.apply_to_os_environ()
    
    try:
        yield mock_env
    finally:
        mock_env.restore()


def create_common_test_environments() -> Dict[str, Dict[str, str]]:
    """
    Factory function for common test environment configurations.
    
    Returns:
        Dictionary of named environment configurations
    """
    return {
        'development': {
            'ENV': 'development',
            'DEBUG': 'true',
            'LOG_LEVEL': 'DEBUG',
            'API_URL': 'http://localhost:8000'
        },
        'production': {
            'ENV': 'production',
            'DEBUG': 'false',
            'LOG_LEVEL': 'INFO',
            'API_URL': 'https://api.example.com'
        },
        'testing': {
            'ENV': 'test',
            'DEBUG': 'true',
            'LOG_LEVEL': 'INFO',
            'DATABASE_URL': 'sqlite:///:memory:',
            'DISABLE_AUTH': 'true'
        },
        'ci': {
            'CI': 'true',
            'ENV': 'test',
            'DEBUG': 'false',
            'LOG_LEVEL': 'WARNING',
            'PARALLEL_TESTS': 'true'
        },
        'minimal': {
            'PATH': '/usr/bin:/bin',
            'HOME': '/tmp/test_home'
        }
    }


def create_secure_environment() -> MockEnvironment:
    """
    Create environment with common security restrictions.
    
    Returns:
        MockEnvironment with security-focused configuration
    """
    env = MockEnvironment(isolated=True)
    
    # Block sensitive variables
    sensitive_vars = [
        'AWS_SECRET_ACCESS_KEY',
        'DATABASE_PASSWORD', 
        'API_SECRET_KEY',
        'PRIVATE_KEY',
        'SSH_PRIVATE_KEY',
        'OAUTH_CLIENT_SECRET'
    ]
    
    for var in sensitive_vars:
        env.block(var)
    
    # Protect system variables
    system_vars = ['PATH', 'HOME', 'USER', 'SHELL']
    for var in system_vars:
        if var in os.environ:
            env.set(var, os.environ[var])
            env.protect(var)
    
    return env


def patch_os_environ(mock_env: MockEnvironment):
    """
    Create patches for os.environ using mock environment.
    
    Args:
        mock_env: MockEnvironment to use for environment access
        
    Returns:
        Dictionary of patches that can be applied with unittest.mock.patch
    """
    class MockEnvironDict:
        def get(self, key, default=None):
            return mock_env.get(key, default)
        
        def __getitem__(self, key):
            value = mock_env.get(key)
            if value is None:
                raise KeyError(key)
            return value
        
        def __setitem__(self, key, value):
            mock_env.set(key, value)
        
        def __delitem__(self, key):
            mock_env.unset(key)
        
        def __contains__(self, key):
            return mock_env.has(key)
        
        def keys(self):
            return mock_env.keys()
        
        def items(self):
            return mock_env.items()
        
        def copy(self):
            return mock_env.to_dict()
        
        def update(self, other):
            if isinstance(other, dict):
                for key, value in other.items():
                    mock_env.set(key, value)
    
    return {
        'os.environ': MockEnvironDict(),
        'os.getenv': mock_env.get,
    }