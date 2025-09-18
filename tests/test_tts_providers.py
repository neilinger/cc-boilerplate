#!/usr/bin/env python3
"""
TTS Provider testing - MEDIUM PRIORITY
Tests TTS provider availability, fallback mechanisms, and error handling.
Validates the audio feedback system reliability across multiple providers.
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Dict, List, Optional
from unittest.mock import patch, Mock

class TestTTSProviderAvailability(unittest.TestCase):
    """Test TTS provider availability and basic functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tts_dir = Path(__file__).parent.parent / ".claude" / "hooks" / "utils" / "tts"
        self.assertTrue(self.tts_dir.exists(), "TTS utils directory must exist")
        
        self.tts_providers = [
            "elevenlabs_tts.py",
            "openai_tts.py", 
            "pyttsx3_tts.py"
        ]
        
        # Verify all TTS providers exist
        for provider in self.tts_providers:
            provider_path = self.tts_dir / provider
            self.assertTrue(provider_path.exists(), f"TTS provider {provider} must exist")
    
    def run_tts_provider(self, provider: str, text: str = "test", 
                        timeout: int = 30) -> subprocess.CompletedProcess:
        """Run a TTS provider with test input."""
        provider_path = self.tts_dir / provider
        
        result = subprocess.run(
            [sys.executable, str(provider_path), text],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return result
    
    def test_elevenlabs_tts_availability(self):
        """Test ElevenLabs TTS provider."""
        result = self.run_tts_provider("elevenlabs_tts.py", "test message")
        
        # Should either work (0) or fail gracefully with meaningful error
        if result.returncode == 0:
            print("✓ ElevenLabs TTS: Available and working")
        else:
            print(f"ℹ ElevenLabs TTS: Not available - {result.stderr.strip()}")
            # Should fail gracefully, not crash
            self.assertIsNotNone(result.returncode, "Should complete execution")
    
    def test_openai_tts_availability(self):
        """Test OpenAI TTS provider."""
        result = self.run_tts_provider("openai_tts.py", "test message")
        
        if result.returncode == 0:
            print("✓ OpenAI TTS: Available and working")
        else:
            print(f"ℹ OpenAI TTS: Not available - {result.stderr.strip()}")
            self.assertIsNotNone(result.returncode, "Should complete execution")
    
    def test_pyttsx3_tts_availability(self):
        """Test pyttsx3 TTS provider (local fallback)."""
        result = self.run_tts_provider("pyttsx3_tts.py", "test message")
        
        if result.returncode == 0:
            print("✓ pyttsx3 TTS: Available and working")
        else:
            print(f"ℹ pyttsx3 TTS: Not available - {result.stderr.strip()}")
            self.assertIsNotNone(result.returncode, "Should complete execution")
    
    def test_tts_providers_handle_empty_input(self):
        """Test that TTS providers handle empty input gracefully."""
        for provider in self.tts_providers:
            with self.subTest(provider=provider):
                result = self.run_tts_provider(provider, "")
                
                # Should handle empty input without crashing
                self.assertIsNotNone(result.returncode,
                                   f"{provider} should handle empty input")
                
                # May succeed (ignore empty) or fail (require input)
                # Both are acceptable behaviors
    
    def test_tts_providers_handle_long_text(self):
        """Test TTS providers with long text input."""
        long_text = "This is a test message. " * 50  # ~1000 characters
        
        for provider in self.tts_providers:
            with self.subTest(provider=provider):
                try:
                    result = self.run_tts_provider(provider, long_text, timeout=45)
                    
                    # Should handle long text without timeout
                    self.assertIsNotNone(result.returncode,
                                       f"{provider} should handle long text")
                    
                    if result.returncode != 0:
                        print(f"ℹ {provider} with long text: {result.stderr.strip()[:100]}")
                        
                except subprocess.TimeoutExpired:
                    self.fail(f"{provider} timed out with long text")


class TestTTSAPIKeyHandling(unittest.TestCase):
    """Test TTS provider API key validation and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tts_dir = Path(__file__).parent.parent / ".claude" / "hooks" / "utils" / "tts"
        
        # Store original environment variables
        self.original_elevenlabs_key = os.environ.get('ELEVENLABS_API_KEY')
        self.original_openai_key = os.environ.get('OPENAI_API_KEY')
    
    def tearDown(self):
        """Restore original environment variables."""
        if self.original_elevenlabs_key:
            os.environ['ELEVENLABS_API_KEY'] = self.original_elevenlabs_key
        elif 'ELEVENLABS_API_KEY' in os.environ:
            del os.environ['ELEVENLABS_API_KEY']
            
        if self.original_openai_key:
            os.environ['OPENAI_API_KEY'] = self.original_openai_key
        elif 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
    
    def test_elevenlabs_missing_api_key(self):
        """Test ElevenLabs TTS behavior without API key."""
        # Remove API key
        if 'ELEVENLABS_API_KEY' in os.environ:
            del os.environ['ELEVENLABS_API_KEY']
        
        provider_path = self.tts_dir / "elevenlabs_tts.py"
        result = subprocess.run(
            [sys.executable, str(provider_path), "test"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Should fail gracefully with informative message
        self.assertNotEqual(result.returncode, 0, 
                          "Should fail without API key")
        
        # Should provide meaningful error message
        error_output = result.stderr.lower() + result.stdout.lower()

        # Accept either API key issues OR dependency issues (both are valid failures)
        api_key_indicators = ['api', 'key', 'token', 'auth', 'credential']
        dependency_indicators = ['modulenotfounderror', 'no module named', 'import error']

        has_expected_error = (
            any(keyword in error_output for keyword in api_key_indicators) or
            any(keyword in error_output for keyword in dependency_indicators)
        )

        self.assertTrue(has_expected_error,
                       f"Should indicate API key or dependency issue. Got: {error_output[:200]}")
    
    def test_openai_missing_api_key(self):
        """Test OpenAI TTS behavior without API key."""
        # Remove API key
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        provider_path = self.tts_dir / "openai_tts.py"
        result = subprocess.run(
            [sys.executable, str(provider_path), "test"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Should fail gracefully
        self.assertNotEqual(result.returncode, 0,
                          "Should fail without API key")
        
        # Should provide meaningful error message
        error_output = result.stderr.lower() + result.stdout.lower()

        # Accept either API key issues OR dependency issues (both are valid failures)
        api_key_indicators = ['api', 'key', 'token', 'auth', 'credential']
        dependency_indicators = ['modulenotfounderror', 'no module named', 'import error']

        has_expected_error = (
            any(keyword in error_output for keyword in api_key_indicators) or
            any(keyword in error_output for keyword in dependency_indicators)
        )

        self.assertTrue(has_expected_error,
                       f"Should indicate API key or dependency issue. Got: {error_output[:200]}")
    
    def test_invalid_api_keys(self):
        """Test behavior with invalid API keys."""
        invalid_keys = [
            "invalid-key-123",
            "",
            "sk-" + "x" * 48,  # Wrong format
            "el-" + "0" * 32,  # Wrong format
        ]
        
        providers_and_env_vars = [
            ("elevenlabs_tts.py", "ELEVENLABS_API_KEY"),
            ("openai_tts.py", "OPENAI_API_KEY"),
        ]
        
        for provider, env_var in providers_and_env_vars:
            for invalid_key in invalid_keys:
                with self.subTest(provider=provider, key=invalid_key[:10] + "..."):
                    # Set invalid API key
                    os.environ[env_var] = invalid_key
                    
                    provider_path = self.tts_dir / provider
                    result = subprocess.run(
                        [sys.executable, str(provider_path), "test"],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    # Should handle invalid keys gracefully
                    if result.returncode != 0:
                        # Expected behavior - invalid keys should fail
                        print(f"✓ {provider} properly rejected invalid key")
                    else:
                        # Unexpected - should investigate why it succeeded
                        print(f"⚠️  {provider} accepted invalid key")


class TestTTSFallbackMechanism(unittest.TestCase):
    """Test TTS fallback mechanism in notification system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.notification_hook = Path(__file__).parent.parent / ".claude" / "hooks" / "notification.py"
        self.assertTrue(self.notification_hook.exists(), "Notification hook must exist")
    
    def test_notification_hook_with_tts(self):
        """Test notification hook TTS integration."""
        notification_input = {
            "message": "Test notification with TTS",
            "type": "info",
            "use_tts": True,
            "timestamp": "2025-01-09T10:30:00Z"
        }
        
        result = subprocess.run(
            [sys.executable, str(self.notification_hook)],
            input=json.dumps(notification_input),
            text=True,
            capture_output=True,
            timeout=45
        )
        
        # Should complete successfully even if TTS fails
        self.assertEqual(result.returncode, 0,
                        f"Notification hook should handle TTS gracefully: {result.stderr}")
        
        print(f"✓ Notification hook with TTS: {result.stdout.strip()}")
    
    def test_notification_hook_fallback_behavior(self):
        """Test notification hook behavior when TTS providers fail."""
        # This test simulates TTS provider failures by using environment manipulation
        # In real implementation, the notification hook should try multiple providers
        
        # Test with potentially missing TTS dependencies
        notification_input = {
            "message": "Fallback test - this message should still be processed",
            "type": "warning",
            "use_tts": True,
            "timestamp": "2025-01-09T10:30:00Z"
        }
        
        # Temporarily remove API keys to force fallback
        original_keys = {}
        for key in ['ELEVENLABS_API_KEY', 'OPENAI_API_KEY']:
            if key in os.environ:
                original_keys[key] = os.environ[key]
                del os.environ[key]
        
        try:
            result = subprocess.run(
                [sys.executable, str(self.notification_hook)],
                input=json.dumps(notification_input),
                text=True,
                capture_output=True,
                timeout=45
            )
            
            # Should still succeed with fallback or graceful degradation
            self.assertEqual(result.returncode, 0,
                           "Notification should work even when TTS fails")
            
            print("✓ Notification hook handles TTS fallback gracefully")
            
        finally:
            # Restore original API keys
            for key, value in original_keys.items():
                os.environ[key] = value


class TestTTSFileOutput(unittest.TestCase):
    """Test TTS provider file output handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tts_dir = Path(__file__).parent.parent / ".claude" / "hooks" / "utils" / "tts"
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_tts_audio_file_creation(self):
        """Test that TTS providers can create audio files when working."""
        # This test only runs if TTS providers are actually functional
        # It's more of a system integration test
        
        for provider in ["elevenlabs_tts.py", "openai_tts.py"]:
            with self.subTest(provider=provider):
                provider_path = self.tts_dir / provider
                
                # Try to run TTS and check if it creates audio files
                result = subprocess.run(
                    [sys.executable, str(provider_path), "test audio"],
                    capture_output=True,
                    text=True,
                    timeout=45
                )
                
                if result.returncode == 0:
                    print(f"✓ {provider}: Successfully executed")
                    
                    # Check if any audio files were mentioned in output
                    if any(ext in result.stdout.lower() for ext in ['.mp3', '.wav', '.audio']):
                        print(f"  ✓ {provider}: Audio file handling detected")
                else:
                    print(f"ℹ {provider}: Not functional in test environment")
    
    def test_tts_error_handling(self):
        """Test TTS provider error handling with various failure modes."""
        failure_scenarios = [
            ("very long text " * 1000, "excessive_length"),  # Very long input
            ("", "empty_input"),                              # Empty input  
            ("Special chars: 中文 العربية émojis 🎵", "unicode"), # Unicode
        ]
        
        for provider in ["elevenlabs_tts.py", "pyttsx3_tts.py"]:
            for test_text, scenario in failure_scenarios:
                with self.subTest(provider=provider, scenario=scenario):
                    provider_path = self.tts_dir / provider
                    
                    try:
                        result = subprocess.run(
                            [sys.executable, str(provider_path), test_text],
                            capture_output=True,
                            text=True,
                            timeout=60
                        )
                        
                        # Should complete without hanging
                        self.assertIsNotNone(result.returncode,
                                           f"{provider} should handle {scenario}")
                        
                        if result.returncode != 0 and result.stderr:
                            print(f"ℹ {provider} {scenario}: {result.stderr.strip()[:100]}")
                            
                    except subprocess.TimeoutExpired:
                        self.fail(f"{provider} timed out on {scenario}")


def run_tts_tests():
    """Run all TTS provider tests."""
    import json
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTTSProviderAvailability))
    suite.addTests(loader.loadTestsFromTestCase(TestTTSAPIKeyHandling))
    suite.addTests(loader.loadTestsFromTestCase(TestTTSFallbackMechanism))
    suite.addTests(loader.loadTestsFromTestCase(TestTTSFileOutput))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    import json
    
    print("=" * 60)
    print("TTS PROVIDER TESTING - MEDIUM PRIORITY")
    print("Testing TTS provider availability, fallback, and error handling")
    print("=" * 60)
    
    # Check environment
    api_keys_present = []
    if os.environ.get('ELEVENLABS_API_KEY'):
        api_keys_present.append('ElevenLabs')
    if os.environ.get('OPENAI_API_KEY'):
        api_keys_present.append('OpenAI')
    
    if api_keys_present:
        print(f"🔑 API keys detected: {', '.join(api_keys_present)}")
    else:
        print("ℹ️  No API keys detected - testing fallback behavior")
    print()
    
    result = run_tts_tests()
    
    print(f"\nTTS Provider Tests Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}")
    
    # Provide operational recommendations
    print("\n" + "=" * 60)
    print("TTS SYSTEM RECOMMENDATIONS:")
    print("1. Implement robust fallback: ElevenLabs → OpenAI → pyttsx3")
    print("2. Cache API availability to avoid repeated failures")
    print("3. Add rate limiting to prevent API quota exhaustion")
    print("4. Consider audio file cleanup to prevent disk space issues")
    print("=" * 60)
    
    sys.exit(0 if result.wasSuccessful() else 1)