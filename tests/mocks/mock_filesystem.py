#!/usr/bin/env python3
"""
Mock file system infrastructure for safe file operation testing.

This module provides MockFileSystem and utilities to simulate file system
operations without side effects, enabling testing of file-based operations
in a controlled environment.

Following KISS/YAGNI: Simple in-memory file system mock for essential testing.
"""

import os
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Set
from dataclasses import dataclass, field


class MockFileSystemError(Exception):
    """Custom exception for mock file system errors."""
    pass


@dataclass
class MockFile:
    """
    Represents a file in the mock file system.
    
    Simple data structure to track file contents and metadata.
    """
    content: str = ""
    permissions: int = 0o644
    created_time: float = field(default_factory=time.time)
    modified_time: float = field(default_factory=time.time)
    is_executable: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def update_content(self, content: str):
        """Update file content and modification time."""
        self.content = content
        self.modified_time = time.time()
    
    def make_executable(self):
        """Make file executable."""
        self.is_executable = True
        self.permissions = 0o755
    
    def size(self) -> int:
        """Get file size in bytes."""
        return len(self.content.encode('utf-8'))


class MockFileSystem:
    """
    Mock file system for safe file operation testing.
    
    Provides in-memory file system simulation that tracks all file operations
    without affecting the real file system. Supports basic file operations
    like read, write, create, delete, and directory operations.
    
    Usage:
        fs = MockFileSystem()
        fs.write_file('/test/file.txt', 'content')
        content = fs.read_file('/test/file.txt')
    """
    
    def __init__(self, initial_files: Optional[Dict[str, str]] = None):
        """
        Initialize mock file system.
        
        Args:
            initial_files: Optional dict of path -> content for initial files
        """
        self.files: Dict[str, MockFile] = {}
        self.directories: Set[str] = {'/'}  # Root always exists
        self.operations: List[Dict[str, Any]] = []  # Track all operations
        self.blocked_paths: List[str] = []
        self.read_only_paths: List[str] = []
        
        # Initialize with any provided files
        if initial_files:
            for path, content in initial_files.items():
                self.write_file(path, content)
    
    def _normalize_path(self, path: Union[str, Path]) -> str:
        """Normalize path to consistent format."""
        path_str = str(path)
        if not path_str.startswith('/'):
            path_str = '/' + path_str.lstrip('./')
        return os.path.normpath(path_str)
    
    def _record_operation(self, operation: str, path: str, **kwargs):
        """Record file system operation for verification."""
        self.operations.append({
            'operation': operation,
            'path': path,
            'timestamp': time.time(),
            **kwargs
        })
    
    def _check_blocked(self, path: str):
        """Check if path is blocked."""
        for blocked in self.blocked_paths:
            if path.startswith(blocked):
                raise MockFileSystemError(f"Access to {path} is blocked")
    
    def _check_read_only(self, path: str):
        """Check if path is read-only for write operations."""
        for readonly in self.read_only_paths:
            if path.startswith(readonly):
                raise MockFileSystemError(f"Path {path} is read-only")
    
    def _ensure_parent_directory(self, path: str):
        """Ensure parent directory exists."""
        parent = os.path.dirname(path)
        if parent and parent != '/':
            self.directories.add(parent)
            self._ensure_parent_directory(parent)
    
    def write_file(self, path: str, content: str, permissions: int = 0o644):
        """
        Write content to a file.
        
        Args:
            path: File path to write
            content: Content to write
            permissions: File permissions (octal)
            
        Raises:
            MockFileSystemError: If path is blocked or read-only
        """
        path = self._normalize_path(path)
        self._check_blocked(path)
        self._check_read_only(path)
        
        self._record_operation('write', path, size=len(content))
        self._ensure_parent_directory(path)
        
        if path in self.files:
            self.files[path].update_content(content)
            self.files[path].permissions = permissions
        else:
            self.files[path] = MockFile(
                content=content,
                permissions=permissions,
                is_executable=permissions & 0o111 != 0
            )
    
    def read_file(self, path: str) -> str:
        """
        Read content from a file.
        
        Args:
            path: File path to read
            
        Returns:
            File content as string
            
        Raises:
            MockFileSystemError: If file doesn't exist or path is blocked
        """
        path = self._normalize_path(path)
        self._check_blocked(path)
        
        self._record_operation('read', path)
        
        if path not in self.files:
            raise MockFileSystemError(f"File not found: {path}")
        
        return self.files[path].content
    
    def file_exists(self, path: str) -> bool:
        """Check if file exists."""
        path = self._normalize_path(path)
        return path in self.files
    
    def directory_exists(self, path: str) -> bool:
        """Check if directory exists."""
        path = self._normalize_path(path)
        return path in self.directories
    
    def create_directory(self, path: str):
        """
        Create directory (and parent directories if needed).
        
        Args:
            path: Directory path to create
        """
        path = self._normalize_path(path)
        self._check_blocked(path)
        self._check_read_only(path)
        
        self._record_operation('mkdir', path)
        self._ensure_parent_directory(path)
        self.directories.add(path)
    
    def delete_file(self, path: str):
        """
        Delete a file.
        
        Args:
            path: File path to delete
            
        Raises:
            MockFileSystemError: If file doesn't exist or path is read-only
        """
        path = self._normalize_path(path)
        self._check_read_only(path)
        
        self._record_operation('delete', path)
        
        if path not in self.files:
            raise MockFileSystemError(f"File not found: {path}")
        
        del self.files[path]
    
    def list_directory(self, path: str) -> List[str]:
        """
        List contents of directory.
        
        Args:
            path: Directory path to list
            
        Returns:
            List of file/directory names in the directory
        """
        path = self._normalize_path(path)
        self._record_operation('listdir', path)
        
        if path not in self.directories:
            raise MockFileSystemError(f"Directory not found: {path}")
        
        contents = []
        path_prefix = path.rstrip('/') + '/'
        
        # Find files in this directory
        for file_path in self.files:
            if file_path.startswith(path_prefix):
                relative = file_path[len(path_prefix):]
                if '/' not in relative:  # Direct child, not subdirectory
                    contents.append(relative)
        
        # Find subdirectories
        for dir_path in self.directories:
            if dir_path.startswith(path_prefix) and dir_path != path:
                relative = dir_path[len(path_prefix):]
                if '/' not in relative:  # Direct child directory
                    contents.append(relative + '/')
        
        return sorted(contents)
    
    def get_file_info(self, path: str) -> Dict[str, Any]:
        """
        Get file information.
        
        Args:
            path: File path
            
        Returns:
            Dictionary with file metadata
        """
        path = self._normalize_path(path)
        
        if path not in self.files:
            raise MockFileSystemError(f"File not found: {path}")
        
        file_obj = self.files[path]
        return {
            'path': path,
            'size': file_obj.size(),
            'permissions': oct(file_obj.permissions),
            'created': file_obj.created_time,
            'modified': file_obj.modified_time,
            'is_executable': file_obj.is_executable,
            'metadata': file_obj.metadata.copy()
        }
    
    def copy_file(self, source: str, dest: str):
        """
        Copy file from source to destination.
        
        Args:
            source: Source file path
            dest: Destination file path
        """
        source = self._normalize_path(source)
        dest = self._normalize_path(dest)
        
        if source not in self.files:
            raise MockFileSystemError(f"Source file not found: {source}")
        
        self._check_read_only(dest)
        self._record_operation('copy', source, dest=dest)
        
        source_file = self.files[source]
        self.files[dest] = MockFile(
            content=source_file.content,
            permissions=source_file.permissions,
            is_executable=source_file.is_executable,
            metadata=source_file.metadata.copy()
        )
    
    def move_file(self, source: str, dest: str):
        """
        Move file from source to destination.
        
        Args:
            source: Source file path
            dest: Destination file path
        """
        self.copy_file(source, dest)
        self.delete_file(source)
        self._record_operation('move', source, dest=dest)
    
    def block_path(self, path: str):
        """Block access to path and all its children."""
        self.blocked_paths.append(self._normalize_path(path))
    
    def make_read_only(self, path: str):
        """Make path read-only (no writes/deletes)."""
        self.read_only_paths.append(self._normalize_path(path))
    
    def get_operations(self, operation_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get recorded file operations for verification.
        
        Args:
            operation_type: Optional filter for operation type
            
        Returns:
            List of recorded operations
        """
        if operation_type is None:
            return self.operations.copy()
        return [op for op in self.operations if op['operation'] == operation_type]
    
    def clear_operations(self):
        """Clear recorded operations."""
        self.operations.clear()
    
    def reset(self):
        """Reset file system to empty state."""
        self.files.clear()
        self.directories = {'/'}
        self.operations.clear()
        self.blocked_paths.clear()
        self.read_only_paths.clear()


def create_project_filesystem() -> MockFileSystem:
    """
    Create a mock file system with typical project structure.
    
    Returns:
        MockFileSystem pre-populated with common project files
    """
    initial_files = {
        '/README.md': '# Test Project\n\nA test project for mocking.',
        '/pyproject.toml': '[tool.poetry]\nname = "test-project"',
        '/.env.sample': 'API_KEY=your_key_here\nDEBUG=false',
        '/src/main.py': '#!/usr/bin/env python3\nprint("Hello, World!")',
        '/tests/test_main.py': 'import unittest\n\nclass TestMain(unittest.TestCase):\n    pass',
        '/.gitignore': '.env\n__pycache__/\n*.pyc',
        '/logs/app.log': 'INFO: Application started',
    }
    
    fs = MockFileSystem(initial_files)
    
    # Create additional directories
    fs.create_directory('/src')
    fs.create_directory('/tests') 
    fs.create_directory('/logs')
    fs.create_directory('/.claude/hooks')
    
    return fs


def create_protected_filesystem() -> MockFileSystem:
    """
    Create a file system with some protected/blocked paths.
    
    Returns:
        MockFileSystem with blocked and read-only paths configured
    """
    fs = create_project_filesystem()
    
    # Block sensitive paths
    fs.block_path('/etc')
    fs.block_path('/bin')
    fs.block_path('/root')
    
    # Make some paths read-only
    fs.make_read_only('/README.md')
    fs.make_read_only('/.gitignore')
    
    return fs


def patch_pathlib_and_os(mock_fs: MockFileSystem):
    """
    Create patches for pathlib and os modules using mock file system.
    
    Args:
        mock_fs: MockFileSystem to use for file operations
        
    Returns:
        Dictionary of patches that can be applied with unittest.mock.patch
    """
    def mock_read_text(self, encoding='utf-8', errors='strict'):
        return mock_fs.read_file(str(self))
    
    def mock_write_text(self, data, encoding='utf-8', errors='strict'):
        mock_fs.write_file(str(self), data)
    
    def mock_exists(self):
        return mock_fs.file_exists(str(self)) or mock_fs.directory_exists(str(self))
    
    def mock_is_file(self):
        return mock_fs.file_exists(str(self))
    
    def mock_is_dir(self):
        return mock_fs.directory_exists(str(self))
    
    def mock_mkdir(self, mode=0o777, parents=False, exist_ok=False):
        try:
            mock_fs.create_directory(str(self))
        except MockFileSystemError:
            if not exist_ok:
                raise
    
    return {
        'pathlib.Path.read_text': mock_read_text,
        'pathlib.Path.write_text': mock_write_text,
        'pathlib.Path.exists': mock_exists,
        'pathlib.Path.is_file': mock_is_file,
        'pathlib.Path.is_dir': mock_is_dir,
        'pathlib.Path.mkdir': mock_mkdir,
        'os.path.exists': lambda path: mock_fs.file_exists(path) or mock_fs.directory_exists(path),
        'os.path.isfile': lambda path: mock_fs.file_exists(path),
        'os.path.isdir': lambda path: mock_fs.directory_exists(path),
    }