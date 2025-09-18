#!/usr/bin/env python3
"""
URL Validation Tests - HIGH PRIORITY
Ensures all URLs in documentation are accessible and functional.
Critical for user experience - broken URLs waste user time and break trust.
"""

import re
import subprocess
import sys
import unittest
import urllib.request
import urllib.error
from pathlib import Path


class TestURLValidation(unittest.TestCase):
    """Test that all URLs in documentation are accessible."""

    def setUp(self):
        """Set up test fixtures."""
        self.repo_root = Path(__file__).parent.parent
        self.critical_urls = [
            "https://raw.githubusercontent.com/neilinger/cc-boilerplate/main/scripts/init-boilerplate.sh",
            "https://raw.githubusercontent.com/neilinger/cc-boilerplate/main/scripts/build-config.sh",
            "https://raw.githubusercontent.com/neilinger/cc-boilerplate/main/scripts/update-boilerplate.sh",
            "https://raw.githubusercontent.com/neilinger/cc-boilerplate/main/README.md",
            "https://raw.githubusercontent.com/neilinger/cc-boilerplate/main/CLAUDE.md",
        ]

    def test_critical_raw_github_urls(self):
        """Test that critical raw GitHub URLs are accessible."""
        for url in self.critical_urls:
            with self.subTest(url=url):
                try:
                    with urllib.request.urlopen(url, timeout=10) as response:
                        self.assertEqual(response.status, 200, f"URL should return 200: {url}")

                        # For script files, verify they start with shebang
                        if url.endswith('.sh'):
                            content = response.read().decode('utf-8')
                            self.assertTrue(content.startswith('#!/'),
                                          f"Script should start with shebang: {url}")

                        print(f"✓ {url}")

                except urllib.error.URLError as e:
                    self.fail(f"URL not accessible: {url} - Error: {e}")
                except Exception as e:
                    self.fail(f"Unexpected error accessing {url}: {e}")

    def test_readme_installation_urls(self):
        """Test all URLs mentioned in README.md installation sections."""
        readme_path = self.repo_root / "README.md"
        self.assertTrue(readme_path.exists(), "README.md must exist")

        with open(readme_path, 'r') as f:
            content = f.read()

        # Extract all https URLs from README
        urls = re.findall(r'https://[^\s\)]+', content)

        # Filter for raw.githubusercontent.com URLs (these are critical)
        github_raw_urls = [url for url in urls if 'raw.githubusercontent.com' in url]

        for url in github_raw_urls:
            with self.subTest(url=url):
                try:
                    with urllib.request.urlopen(url, timeout=10) as response:
                        self.assertEqual(response.status, 200, f"README URL should work: {url}")
                        print(f"✓ README URL: {url}")
                except Exception as e:
                    self.fail(f"README mentions broken URL: {url} - Error: {e}")

    def test_one_liner_installation_command(self):
        """Test that the one-liner installation command URLs work."""
        one_liner_patterns = [
            r'curl -sSL (https://raw\.githubusercontent\.com/[^\s]+/scripts/init-boilerplate\.sh)',
        ]

        readme_path = self.repo_root / "README.md"
        with open(readme_path, 'r') as f:
            content = f.read()

        for pattern in one_liner_patterns:
            matches = re.findall(pattern, content)
            self.assertTrue(matches, f"Should find one-liner URL pattern: {pattern}")

            for url in matches:
                with self.subTest(url=url):
                    try:
                        with urllib.request.urlopen(url, timeout=10) as response:
                            self.assertEqual(response.status, 200)

                            # Verify it's actually a bash script
                            content = response.read().decode('utf-8')
                            self.assertTrue(content.startswith('#!/usr/bin/env bash') or
                                          content.startswith('#!/bin/bash'),
                                          f"One-liner should download a bash script: {url}")

                            print(f"✓ One-liner URL works: {url}")

                    except Exception as e:
                        self.fail(f"One-liner installation URL broken: {url} - Error: {e}")

    def test_claude_md_urls(self):
        """Test URLs in CLAUDE.md are accessible."""
        claude_md_path = self.repo_root / "CLAUDE.md"
        if not claude_md_path.exists():
            self.skipTest("CLAUDE.md not found")

        with open(claude_md_path, 'r') as f:
            content = f.read()

        # Extract GitHub URLs (focus on raw.githubusercontent.com)
        github_urls = re.findall(r'https://raw\.githubusercontent\.com/[^\s\)]+', content)

        for url in github_urls:
            with self.subTest(url=url):
                try:
                    with urllib.request.urlopen(url, timeout=10) as response:
                        self.assertEqual(response.status, 200, f"CLAUDE.md URL should work: {url}")
                        print(f"✓ CLAUDE.md URL: {url}")
                except Exception as e:
                    self.fail(f"CLAUDE.md mentions broken URL: {url} - Error: {e}")

    def test_repository_accessibility(self):
        """Test that the repository itself is publicly accessible."""
        repo_urls = [
            "https://github.com/neilinger/cc-boilerplate",
            "https://api.github.com/repos/neilinger/cc-boilerplate",
        ]

        for url in repo_urls:
            with self.subTest(url=url):
                try:
                    with urllib.request.urlopen(url, timeout=10) as response:
                        self.assertEqual(response.status, 200, f"Repository URL should be accessible: {url}")
                        print(f"✓ Repository accessible: {url}")
                except Exception as e:
                    self.fail(f"Repository not publicly accessible: {url} - Error: {e}")


def run_url_validation_tests():
    """Run URL validation tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test class
    suite.addTests(loader.loadTestsFromTestCase(TestURLValidation))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("URL VALIDATION TESTS - HIGH PRIORITY")
    print("Ensuring all documentation URLs work correctly")
    print("=" * 60)

    result = run_url_validation_tests()

    print(f"\nURL Validation Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\nFAILURES (Broken URLs):")
        for test, traceback in result.failures:
            print(f"- {test}")
            print(f"  {traceback.split('AssertionError:')[-1].strip()}")

    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}")

    if result.wasSuccessful():
        print("\n🎉 All URLs working correctly!")
        print("Users can trust our installation instructions.")
    else:
        print("\n💥 CRITICAL: Broken URLs found!")
        print("User experience will be poor - fix immediately!")

    sys.exit(0 if result.wasSuccessful() else 1)