#!/usr/bin/env python3
"""
Mock hook infrastructure for testing Claude Code hooks without installation.

This module provides MockHookRunner and related utilities to simulate hook execution
with controlled responses, enabling reliable testing of hook behavior without
requiring uv or actual hook installation.

Following KISS/YAGNI: Simple classes with clear responsibilities.
"""

import json
import time
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable
from enum import Enum


class MockHookAction(Enum):
    """Possible hook actions for testing."""
    ALLOW = "allow"
    BLOCK = "block" 
    ERROR = "error"
    TIMEOUT = "timeout"


@dataclass
class MockHookResponse:
    """
    Represents a mock hook response for testing.
    
    Simple data structure to control hook behavior during tests.
    """
    action: MockHookAction
    reason: Optional[str] = None
    exit_code: int = 0
    stdout: str = ""
    stderr: str = ""
    delay_seconds: float = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_json(self) -> str:
        """Convert response to JSON format."""
        return json.dumps({
            'action': self.action.value,
            'reason': self.reason,
            'exit_code': self.exit_code,
            'stdout': self.stdout,
            'stderr': self.stderr,
            'metadata': self.metadata
        }, indent=2)


class MockHookRunner:
    """
    Mock hook execution system for testing without environmental dependencies.
    
    Simulates Claude Code hook behavior with controlled responses, enabling
    comprehensive testing of hook integration without requiring actual hooks.
    
    Usage:
        runner = MockHookRunner()
        runner.set_hook_response('pre_tool_use', MockHookResponse(MockHookAction.BLOCK))
        result = runner.run_hook('pre_tool_use', {'tool': 'Bash', 'input': {}})
    """
    
    def __init__(self):
        """Initialize mock hook runner."""
        self.hook_responses: Dict[str, MockHookResponse] = {}
        self.hook_calls: List[Dict[str, Any]] = []
        self.default_response = MockHookResponse(MockHookAction.ALLOW)
        
    def set_hook_response(self, hook_name: str, response: MockHookResponse):
        """
        Configure response for a specific hook.
        
        Args:
            hook_name: Name of the hook (e.g., 'pre_tool_use', 'post_tool_use')
            response: MockHookResponse to return when hook is called
        """
        self.hook_responses[hook_name] = response
    
    def set_default_response(self, response: MockHookResponse):
        """Set default response for hooks without specific configuration."""
        self.default_response = response
    
    def run_hook(self, hook_name: str, input_data: Dict[str, Any], 
                 timeout: float = 10.0) -> MockHookResponse:
        """
        Simulate running a hook with given input data.
        
        Args:
            hook_name: Name of the hook to run
            input_data: Input data to send to hook (simulated)
            timeout: Timeout in seconds (simulated)
            
        Returns:
            MockHookResponse with the configured response
        """
        # Record the call for verification
        call_record = {
            'hook_name': hook_name,
            'input_data': input_data.copy(),
            'timestamp': time.time(),
            'timeout': timeout
        }
        self.hook_calls.append(call_record)
        
        # Get configured response or default
        response = self.hook_responses.get(hook_name, self.default_response)
        
        # Simulate delay if specified
        if response.delay_seconds > 0:
            time.sleep(response.delay_seconds)
        
        # Simulate timeout
        if response.action == MockHookAction.TIMEOUT:
            raise TimeoutError(f"Mock hook {hook_name} timed out after {timeout}s")
        
        return response
    
    def get_hook_calls(self, hook_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get recorded hook calls for verification.
        
        Args:
            hook_name: Optional filter for specific hook name
            
        Returns:
            List of recorded hook calls
        """
        if hook_name is None:
            return self.hook_calls.copy()
        return [call for call in self.hook_calls if call['hook_name'] == hook_name]
    
    def clear_calls(self):
        """Clear recorded hook calls."""
        self.hook_calls.clear()
    
    def clear_responses(self):
        """Clear configured hook responses."""
        self.hook_responses.clear()
    
    def reset(self):
        """Reset all recorded calls and configured responses."""
        self.clear_calls()
        self.clear_responses()


class MockSafetyHook:
    """
    Specialized mock for safety hooks that need to evaluate tool calls.
    
    Provides convenient methods for testing safety logic without
    requiring the actual safety hook infrastructure.
    """
    
    def __init__(self, safety_logic_module=None):
        """
        Initialize safety hook mock.
        
        Args:
            safety_logic_module: Optional safety_logic module for real evaluation
        """
        self.runner = MockHookRunner()
        self.safety_logic = safety_logic_module
        self.auto_evaluate = False
        
    def enable_auto_evaluation(self, safety_logic_module):
        """
        Enable automatic safety evaluation using real safety logic.
        
        Args:
            safety_logic_module: The safety_logic module to use
        """
        self.safety_logic = safety_logic_module
        self.auto_evaluate = True
    
    def evaluate_tool_call(self, tool_name: str, tool_input: Dict[str, Any]) -> MockHookResponse:
        """
        Evaluate a tool call for safety and return appropriate response.
        
        Args:
            tool_name: Name of the tool being called
            tool_input: Input parameters for the tool
            
        Returns:
            MockHookResponse based on safety evaluation
        """
        if not self.auto_evaluate or not self.safety_logic:
            # Return configured response or default
            return self.runner.run_hook('pre_tool_use', {
                'tool': tool_name,
                'input': tool_input
            })
        
        # Use real safety logic for evaluation
        assessment = self.safety_logic.get_safety_assessment(tool_name, tool_input)
        
        if assessment['blocked']:
            response = MockHookResponse(
                action=MockHookAction.BLOCK,
                reason=assessment['reason'],
                exit_code=1,
                metadata={
                    'patterns_detected': assessment['patterns_detected'],
                    'warnings': assessment['warnings']
                }
            )
        else:
            response = MockHookResponse(
                action=MockHookAction.ALLOW,
                exit_code=0,
                metadata={
                    'patterns_detected': assessment['patterns_detected'],
                    'warnings': assessment['warnings']
                }
            )
        
        # Record the call
        self.runner.hook_calls.append({
            'hook_name': 'pre_tool_use',
            'input_data': {'tool': tool_name, 'input': tool_input},
            'timestamp': time.time(),
            'assessment': assessment,
            'response': response
        })
        
        return response
    
    def set_block_response(self, reason: str = "Blocked by mock safety hook"):
        """Convenience method to set blocking response."""
        self.runner.set_hook_response('pre_tool_use', MockHookResponse(
            action=MockHookAction.BLOCK,
            reason=reason,
            exit_code=1
        ))
    
    def set_allow_response(self, reason: str = "Allowed by mock safety hook"):
        """Convenience method to set allowing response.""" 
        self.runner.set_hook_response('pre_tool_use', MockHookResponse(
            action=MockHookAction.ALLOW,
            reason=reason,
            exit_code=0
        ))
    
    def set_error_response(self, error_msg: str = "Mock safety hook error"):
        """Convenience method to set error response."""
        self.runner.set_hook_response('pre_tool_use', MockHookResponse(
            action=MockHookAction.ERROR,
            reason=error_msg,
            exit_code=2,
            stderr=error_msg
        ))


def create_mock_hook_responses() -> Dict[str, MockHookResponse]:
    """
    Factory function to create common mock hook responses.
    
    Returns:
        Dictionary of commonly used mock responses
    """
    return {
        'allow_all': MockHookResponse(MockHookAction.ALLOW),
        'block_all': MockHookResponse(
            action=MockHookAction.BLOCK,
            reason="Blocked by test mock",
            exit_code=1
        ),
        'error_hook': MockHookResponse(
            action=MockHookAction.ERROR,
            reason="Hook execution error",
            exit_code=2,
            stderr="Mock hook error"
        ),
        'timeout_hook': MockHookResponse(
            action=MockHookAction.TIMEOUT,
            delay_seconds=1
        ),
        'slow_allow': MockHookResponse(
            action=MockHookAction.ALLOW,
            delay_seconds=0.5
        )
    }


# Convenience functions for common test scenarios
def create_blocking_hook_runner(reason: str = "Test block") -> MockHookRunner:
    """Create a hook runner that blocks all calls."""
    runner = MockHookRunner()
    runner.set_default_response(MockHookResponse(
        action=MockHookAction.BLOCK,
        reason=reason,
        exit_code=1
    ))
    return runner


def create_allowing_hook_runner() -> MockHookRunner:
    """Create a hook runner that allows all calls."""
    runner = MockHookRunner()
    runner.set_default_response(MockHookResponse(MockHookAction.ALLOW))
    return runner


def create_error_hook_runner(error_msg: str = "Test error") -> MockHookRunner:
    """Create a hook runner that errors on all calls."""
    runner = MockHookRunner()
    runner.set_default_response(MockHookResponse(
        action=MockHookAction.ERROR,
        reason=error_msg,
        exit_code=2,
        stderr=error_msg
    ))
    return runner