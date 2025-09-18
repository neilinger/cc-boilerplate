#!/usr/bin/env python3
"""
Comprehensive test runner for cc-boilerplate project.
Runs all test suites and provides coverage overview with priorities.
"""

import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

def run_test_suite(test_file: Path, description: str, priority: str) -> Tuple[bool, Dict]:
    """Run a test suite and return success status with details."""
    print(f"\n{'='*60}")
    print(f"Running {description} ({priority})")
    print(f"File: {test_file}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        execution_time = time.time() - start_time
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        success = result.returncode == 0
        
        return success, {
            'returncode': result.returncode,
            'execution_time': execution_time,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
        
    except subprocess.TimeoutExpired:
        execution_time = time.time() - start_time
        print(f"❌ Test suite timed out after {execution_time:.1f} seconds")
        return False, {
            'returncode': -1,
            'execution_time': execution_time,
            'error': 'timeout'
        }
    except Exception as e:
        execution_time = time.time() - start_time
        print(f"❌ Test suite failed with exception: {e}")
        return False, {
            'returncode': -2,
            'execution_time': execution_time,
            'error': str(e)
        }

def extract_test_stats(output: str) -> Dict:
    """Extract test statistics from unittest output."""
    stats = {
        'tests_run': 0,
        'failures': 0,
        'errors': 0,
        'skipped': 0
    }
    
    lines = output.split('\n')
    for line in lines:
        line = line.strip()
        if 'Tests run:' in line:
            # Parse "Tests run: X, Failures: Y, Errors: Z, Skipped: W" format
            parts = line.split(',')
            for part in parts:
                part = part.strip()
                if 'Tests run:' in part:
                    stats['tests_run'] = int(part.split(':')[1].strip())
                elif 'Failures:' in part:
                    stats['failures'] = int(part.split(':')[1].strip())
                elif 'Errors:' in part:
                    stats['errors'] = int(part.split(':')[1].strip())
                elif 'Skipped:' in part:
                    stats['skipped'] = int(part.split(':')[1].strip())
        
        # Alternative format parsing
        elif line.startswith(('FAIL:', 'ERROR:', 'SKIP:')):
            if line.startswith('FAIL:'):
                stats['failures'] += 1
            elif line.startswith('ERROR:'):
                stats['errors'] += 1
            elif line.startswith('SKIP:'):
                stats['skipped'] += 1
    
    return stats

def main():
    """Run all test suites and provide comprehensive report."""
    print("CC-BOILERPLATE COMPREHENSIVE TEST SUITE")
    print("="*60)
    print("Running all available tests with priority-based reporting")
    
    tests_dir = Path(__file__).parent
    
    # Define test suites with priorities
    test_suites = [
        # HIGH PRIORITY - Security and Core Functionality
        (tests_dir / "test_url_validation.py", "URL Validation Testing (Critical UX)", "HIGH PRIORITY"),
        (tests_dir / "test_safety_unit.py", "Safety Unit Testing (Tier 1)", "HIGH PRIORITY"),
        (tests_dir / "test_ci_integration.py", "CI Integration Testing (Tier 2A)", "HIGH PRIORITY"),
        (tests_dir / "test_portable_functionality.py", "Portable Functionality Testing (Tier 2B)", "HIGH PRIORITY"),
        (tests_dir / "test_safety_hooks.py", "Safety Hook Testing", "HIGH PRIORITY"),
        (tests_dir / "test_hook_integration.py", "Hook Integration Testing", "HIGH PRIORITY"),
        (tests_dir / "test_prp_edge_cases.py", "PRP Edge Case Testing", "HIGH PRIORITY"),
        
        # MEDIUM PRIORITY - Features and Reliability
        (tests_dir / "test_tts_providers.py", "TTS Provider Testing", "MEDIUM PRIORITY"),
        
        # EXISTING TESTS - Already implemented
        (Path(__file__).parent.parent / "scripts" / "test_prp_system.py", "PRP System Testing", "EXISTING"),
    ]
    
    # Filter to only existing test files
    available_tests = [(test_file, desc, priority) for test_file, desc, priority in test_suites if test_file.exists()]
    missing_tests = [(test_file, desc, priority) for test_file, desc, priority in test_suites if not test_file.exists()]
    
    if missing_tests:
        print(f"\n⚠️  Missing test files:")
        for test_file, desc, priority in missing_tests:
            print(f"   - {desc} ({priority}): {test_file}")
        print()
    
    print(f"Found {len(available_tests)} available test suites")
    
    # Run all available tests
    results = []
    total_start_time = time.time()
    
    for test_file, description, priority in available_tests:
        success, details = run_test_suite(test_file, description, priority)
        results.append((description, priority, success, details))
    
    total_execution_time = time.time() - total_start_time
    
    # Generate comprehensive report
    print("\n" + "="*80)
    print("COMPREHENSIVE TEST REPORT")
    print("="*80)
    
    # Summary by priority
    high_priority_results = [(desc, success, details) for desc, priority, success, details in results if priority == "HIGH PRIORITY"]
    medium_priority_results = [(desc, success, details) for desc, priority, success, details in results if priority == "MEDIUM PRIORITY"]
    existing_results = [(desc, success, details) for desc, priority, success, details in results if priority == "EXISTING"]
    
    print(f"\n🔴 HIGH PRIORITY TESTS ({len(high_priority_results)} suites)")
    print("-" * 40)
    high_success = 0
    high_total_tests = 0
    for desc, success, details in high_priority_results:
        status = "✅ PASS" if success else "❌ FAIL"
        time_str = f"{details.get('execution_time', 0):.1f}s"
        print(f"{status} {desc} ({time_str})")
        
        # Extract test statistics
        if 'stdout' in details:
            stats = extract_test_stats(details['stdout'])
            if stats['tests_run'] > 0:
                high_total_tests += stats['tests_run']
                print(f"     Tests: {stats['tests_run']}, Failures: {stats['failures']}, Errors: {stats['errors']}")
        
        if success:
            high_success += 1
    
    print(f"\n🟡 MEDIUM PRIORITY TESTS ({len(medium_priority_results)} suites)")
    print("-" * 40)
    medium_success = 0
    medium_total_tests = 0
    for desc, success, details in medium_priority_results:
        status = "✅ PASS" if success else "❌ FAIL"
        time_str = f"{details.get('execution_time', 0):.1f}s"
        print(f"{status} {desc} ({time_str})")
        
        if 'stdout' in details:
            stats = extract_test_stats(details['stdout'])
            if stats['tests_run'] > 0:
                medium_total_tests += stats['tests_run']
                print(f"     Tests: {stats['tests_run']}, Failures: {stats['failures']}, Errors: {stats['errors']}")
        
        if success:
            medium_success += 1
    
    print(f"\n⚪ EXISTING TESTS ({len(existing_results)} suites)")
    print("-" * 40)
    existing_success = 0
    existing_total_tests = 0
    for desc, success, details in existing_results:
        status = "✅ PASS" if success else "❌ FAIL"
        time_str = f"{details.get('execution_time', 0):.1f}s"
        print(f"{status} {desc} ({time_str})")
        
        if 'stdout' in details:
            stats = extract_test_stats(details['stdout'])
            if stats['tests_run'] > 0:
                existing_total_tests += stats['tests_run']
                print(f"     Tests: {stats['tests_run']}, Failures: {stats['failures']}, Errors: {stats['errors']}")
        
        if success:
            existing_success += 1
    
    # Overall statistics
    total_suites = len(results)
    total_success = sum(1 for _, _, success, _ in results if success)
    success_rate = (total_success / total_suites * 100) if total_suites > 0 else 0
    
    print(f"\n📊 OVERALL STATISTICS")
    print("-" * 40)
    print(f"Total test suites run: {total_suites}")
    print(f"Successful suites: {total_success}")
    print(f"Failed suites: {total_suites - total_success}")
    print(f"Success rate: {success_rate:.1f}%")
    print(f"Total execution time: {total_execution_time:.1f} seconds")
    
    # Individual test counts
    print(f"\nIndividual test counts:")
    print(f"High priority tests: {high_total_tests}")
    print(f"Medium priority tests: {medium_total_tests}")
    print(f"Existing tests: {existing_total_tests}")
    print(f"Total individual tests: {high_total_tests + medium_total_tests + existing_total_tests}")
    
    # Coverage assessment
    print(f"\n🎯 COVERAGE ASSESSMENT")
    print("-" * 40)
    
    coverage_areas = {
        "Safety Logic Unit Tests (Tier 1)": high_priority_results[0][1] if len(high_priority_results) > 0 else False,
        "CI Integration Tests (Tier 2A)": high_priority_results[1][1] if len(high_priority_results) > 1 else False,
        "Portable Functionality (Tier 2B)": high_priority_results[2][1] if len(high_priority_results) > 2 else False,
        "Safety Hooks (rm command detection)": high_priority_results[3][1] if len(high_priority_results) > 3 else False,
        "Hook Integration Pipeline": high_priority_results[4][1] if len(high_priority_results) > 4 else False,
        "PRP Edge Case Validation": high_priority_results[5][1] if len(high_priority_results) > 5 else False,
        "TTS Provider Fallback": medium_priority_results[0][1] if len(medium_priority_results) > 0 else False,
        "PRP System Core": existing_results[0][1] if len(existing_results) > 0 else False,
    }
    
    for area, tested in coverage_areas.items():
        status = "✅ Covered" if tested else "❌ Gap"
        print(f"{status} {area}")
    
    covered_areas = sum(1 for tested in coverage_areas.values() if tested)
    coverage_percent = (covered_areas / len(coverage_areas) * 100)
    print(f"\nCoverage: {covered_areas}/{len(coverage_areas)} areas ({coverage_percent:.1f}%)")
    
    # Critical issues summary
    critical_failures = []
    for desc, priority, success, details in results:
        if priority == "HIGH PRIORITY" and not success:
            critical_failures.append(desc)
    
    if critical_failures:
        print(f"\n🚨 CRITICAL FAILURES")
        print("-" * 40)
        for failure in critical_failures:
            print(f"❌ {failure}")
        print("\nThese failures affect core security and functionality!")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS")
    print("-" * 40)
    
    if high_success == len(high_priority_results):
        print("✅ All high priority tests passing - core system is secure")
    else:
        print("⚠️  High priority test failures need immediate attention")
    
    if medium_success < len(medium_priority_results):
        print("ℹ️  Medium priority improvements available for better reliability")
    
    missing_test_areas = [
        "Status Line Testing",
        "Log Management Testing", 
        "External Dependency Testing (git, gh commands)",
        "Performance/Load Testing"
    ]
    
    if missing_test_areas:
        print(f"\nTest gaps to consider:")
        for area in missing_test_areas:
            print(f"  - {area}")
    
    print(f"\n{'='*80}")
    
    # Exit code based on critical test results
    if critical_failures:
        print("❌ CRITICAL TESTS FAILED - Review required")
        return 1
    elif total_success == total_suites:
        print("✅ ALL TESTS PASSED - System is well tested")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED - Review recommended")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)