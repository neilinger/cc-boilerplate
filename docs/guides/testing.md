# Testing Guide

This guide covers the comprehensive 3-tier testing architecture for cc-boilerplate, designed to balance security, reliability, and development velocity while following KISS/YAGNI principles.

## Overview of Testing Strategy

The cc-boilerplate project implements a **priority-based testing strategy** with three distinct tiers of testing, executed based on branch type and development context. This approach ensures security-critical components are always validated while optimizing CI resources and providing fast developer feedback.

### Design Principles

- **Security First**: Critical security tests never skipped regardless of context
- **Fast Feedback**: High-priority tests complete in <30 seconds for development velocity
- **Resource Efficiency**: Expensive tests only run when necessary (release branches)
- **KISS/YAGNI Compliance**: Simple, focused testing without over-engineering
- **Branch-Specific Testing**: Different test suites for different branch strategies

## Test Categories and Priorities

### 🔴 High Priority (Security Critical - Always Run)

**Purpose**: Prevent security vulnerabilities and system failures
**Execution**: All branches, all contexts, CI/CD mandatory
**Timeout**: <30 seconds total
**Success Criteria**: 100% pass rate required for any deployment

**Test Suites**:

- **Safety Hooks** (`test_safety_hooks.py`)
  - Dangerous command detection (rm -rf protection)
  - 30+ dangerous command patterns
  - File path validation and sanitization
  - Command argument parsing security

- **Hook Integration** (`test_hook_integration.py`)
  - Hook pipeline execution and error handling
  - End-to-end workflow validation
  - Error propagation and recovery
  - Context preservation across hooks

- **PRP Edge Cases** (`test_prp_edge_cases.py`)
  - PRP system security validation
  - Input sanitization and validation
  - Edge case handling for malformed inputs
  - System boundary protection

**Coverage Target**: 95% line coverage minimum

### 🟡 Medium Priority (Feature Reliability - Release Testing)

**Purpose**: Validate feature functionality and user experience
**Execution**: Release branches, main branch, PR to main
**Timeout**: <90 seconds total
**Success Criteria**: 95% pass rate, failures documented but not blocking

**Test Suites**:

- **TTS Providers** (`test_tts_providers.py`)
  For TTS provider details and fallback logic, see [TTS System Reference](../reference/tts-system.md#fallback-logic).

- **Integration Testing**
  - Status line generation
  - Output style formatting
  - Performance benchmarking
  - Cross-component communication

**Coverage Target**: 80% line coverage target

### 🟢 Low Priority (Extended Validation - Release Only)

**Purpose**: Comprehensive system validation and edge case coverage
**Execution**: Release branches only, manual testing
**Timeout**: <180 seconds total
**Success Criteria**: Best effort, failures inform improvement backlog

**Test Areas**:

- **External Dependencies**
  - Git command validation
  - GitHub CLI integration
  - System tool availability
  - Environment configuration testing

- **Performance and Load Testing**
  - Large file handling
  - Memory usage patterns
  - Concurrent operation testing
  - Resource cleanup validation

**Coverage Target**: 60% line coverage acceptable

### 🔵 Manual Priority (Human Validation)

**Purpose**: User experience and integration validation
**Execution**: Before major releases, manual only
**Timeline**: As needed

**Test Areas**:

- End-to-end workflow testing
- Documentation accuracy validation
- User acceptance scenarios
- Integration with Claude Code environment

## How to Run Different Test Suites

### Quick Security Validation (Development)

```bash
# Run individual high-priority tests
python3 tests/test_safety_hooks.py
python3 tests/test_hook_integration.py
python3 tests/test_prp_edge_cases.py

# Run all high-priority tests (recommended before commits)
python3 -m unittest discover tests/ -k "test_safety" -v
```

### Comprehensive Test Suite (Release Preparation)

```bash
# Run all available tests with detailed reporting
python3 tests/run_all_tests.py

# Run specific test categories
python3 -m unittest tests.test_tts_providers -v
```

### CI-Specific Testing

```bash
# Tier 1: Unit tests (CI always runs)
source .venv/bin/activate
python tests/test_safety_unit.py

# Tier 2: Integration tests (mocked)
python tests/test_ci_integration.py  # If available

# Legacy compatibility suite
python tests/run_all_tests.py
```

### Coverage Analysis

```bash
# Generate coverage report (when coverage tools are configured)
source .venv/bin/activate
coverage run -m unittest discover tests/
coverage report
coverage html  # Generate HTML report
```

## Testing Workflow for Developers

### Before Starting Development

1. **Environment Setup**:

   ```bash
   # Ensure test environment is ready
   uv sync --frozen
   source .venv/bin/activate
   python tests/test_base.py  # Validate environment
   ```

2. **Baseline Test Run**:

   ```bash
   # Ensure all tests pass before making changes
   python3 tests/run_all_tests.py
   ```

### During Development

1. **Continuous Validation**:

   ```bash
   # Run security tests after each significant change
   python3 tests/test_safety_hooks.py

   # Test specific functionality being developed
   python3 tests/test_[relevant_module].py
   ```

2. **Pre-Commit Testing**:

   ```bash
   # Required before any commit
   python3 tests/test_safety_hooks.py
   python3 tests/test_hook_integration.py
   python3 tests/test_prp_edge_cases.py
   ```

### Before Creating Pull Request

1. **Full Test Suite**:

   ```bash
   python3 tests/run_all_tests.py
   ```

2. **Manual Validation**:
   - Test key user scenarios
   - Verify documentation accuracy
   - Check for breaking changes

## Security Testing Approach

### Command Injection Protection

The safety hook system provides comprehensive protection against dangerous commands:

```python
# Example dangerous patterns detected:
# - rm -rf /
# - rm -rf ~
# - rm -rf .
# - chmod -R 777
# - find / -delete
# - dd if=/dev/zero of=/dev/sda
```

### Security Test Categories

For detailed security testing approaches and validation patterns, see [Security Guide](../guides/security.md#threat-protection).

### Running Security Tests

```bash
# High-priority security validation
python3 tests/test_safety_hooks.py
```

For complete security testing patterns and expected outputs, see [Security Guide](../guides/security.md#test-security).

## Integration Testing

### Hook Integration Pipeline

Tests the complete hook execution flow:

1. **Pre-tool Use Hook**:
   - Command validation and filtering
   - Context preparation
   - Security checks

2. **Tool Execution**:
   - Safe command execution
   - Output capture and filtering
   - Error handling

3. **Post-tool Use Hook**:
   - Result validation
   - Cleanup operations
   - Status reporting

### Integration Test Execution

```bash
# Run hook integration tests
python3 tests/test_hook_integration.py

# Example scenarios tested:
# - Normal command execution flow
# - Dangerous command blocking
# - Error recovery and reporting
# - Context preservation across hooks
```

## Local vs CI Testing Differences

### Local Development Testing

**Advantages**:

- Full system access for comprehensive testing
- Interactive debugging capabilities
- Custom environment configuration
- Manual validation scenarios

**Test Execution**:

```bash
# Local comprehensive testing
python3 tests/run_all_tests.py

# Local security validation
python3 tests/test_safety_hooks.py
```

### CI/CD Testing Environment

**Branch-Specific Behavior**:

| Branch Type | Tests Executed | Duration | CI Job |
|-------------|----------------|----------|--------|
| `feature/**` | Tier 1 Unit Tests | ~30s | `tier1-unit-tests` |
| `release/**` | Comprehensive Suite | ~15min | `comprehensive-tests` |
| PR to `main` | Enhanced Validation | ~20min | `enhanced-validation` |
| `main` push | Full + Deploy | ~10min | `production-deployment` |

**CI Environment Setup**:

```bash
# Standard CI test setup
uv python install 3.11
uv venv .venv
uv sync --frozen
source .venv/bin/activate
```

**CI-Specific Limitations**:

- No external API access (TTS providers may fail)
- Limited filesystem operations
- Timeout constraints (5-20 minutes)
- Mocked external dependencies

### Environment Variables

**Local Testing**:

```bash
export CI=false
export FULL_TESTING=true
export DEBUG_TESTS=true
```

**CI Testing**:

```bash
export CI=true
export FULL_TESTING=true  # Release branches only
export TIMEOUT_SECONDS=300
```

## Test Organization Structure

```
tests/
├── test_base.py                     # Environment validation
├── test_safety_unit.py              # Tier 1: Critical unit tests
├── test_ci_integration.py           # Tier 2A: CI integration
├── test_portable_functionality.py   # Tier 2B: Portable features
├── test_safety_hooks.py             # 🔴 Safety command detection
├── test_hook_integration.py         # 🔴 Hook pipeline testing
├── test_prp_edge_cases.py           # 🔴 PRP security validation
├── test_tts_providers.py            # 🟡 TTS provider fallback
├── run_all_tests.py                 # Test orchestrator
├── golden_dataset.py                # Test data and fixtures
└── mocks/                           # Mock implementations
    ├── mock_hooks.py
    ├── mock_subprocess.py
    ├── mock_filesystem.py
    └── mock_environment.py
```

## Test Execution Timeouts

**Performance Requirements**:

- **High Priority**: Must complete in <30 seconds total
- **Medium Priority**: Must complete in <90 seconds total
- **Low Priority**: Must complete in <180 seconds total
- **CI Job Timeout**: 5-20 minutes depending on branch type

**Timeout Handling**:

```python
# Tests automatically fail if they exceed timeout
try:
    result = subprocess.run(
        [sys.executable, str(test_file)],
        timeout=300  # 5 minute timeout
    )
except subprocess.TimeoutExpired:
    print(f"❌ Test suite timed out")
    return False
```

## Failure Response Protocol

### High Priority Failures (🔴)

- **Response**: Block all merges, immediate investigation required
- **Escalation**: Security team notification for safety hook failures
- **Resolution**: Must fix before any code deployment

### Medium Priority Failures (🟡)

- **Response**: Document issue, create tracking ticket
- **Escalation**: Allow merge with maintainer approval
- **Resolution**: Address in next sprint/release cycle

### Low Priority Failures (🟢)

- **Response**: Log for future improvement
- **Escalation**: Does not block development
- **Resolution**: Backlog for future enhancement

## Coverage Targets and Metrics

**Overall System Coverage**: 75% target across all priorities

**Priority-Based Coverage**:

- **High Priority**: 95% line coverage minimum (security critical)
- **Medium Priority**: 80% line coverage target (feature reliability)
- **Low Priority**: 60% line coverage acceptable (extended validation)

**Coverage Reporting**:

```bash
# Generate coverage metrics
python3 tests/run_all_tests.py

# Example output:
# 📊 COVERAGE ASSESSMENT
# ✅ Covered Safety Logic Unit Tests (Tier 1)
# ✅ Covered CI Integration Tests (Tier 2A)
# ✅ Covered Portable Functionality (Tier 2B)
# ✅ Covered Safety Hooks (rm command detection)
# ❌ Gap Hook Integration Pipeline
# Coverage: 6/8 areas (75.0%)
```

## Common Testing Scenarios

### Adding New Security Protection

1. **Add Test Case**:

   ```python
   def test_new_dangerous_pattern(self):
       """Test detection of new dangerous command pattern."""
       dangerous_cmd = "your_new_dangerous_command"
       self.assertTrue(is_dangerous_rm_command(dangerous_cmd))
   ```

2. **Update Implementation**:
   - Add pattern to safety hook
   - Ensure test passes
   - Verify no false positives

3. **Validate Integration**:

   ```bash
   python3 tests/test_safety_hooks.py
   python3 tests/test_hook_integration.py
   ```

### Testing New Feature Integration

1. **Create Feature Tests**:
   - Add to appropriate priority category
   - Follow naming convention: `test_[feature_name].py`
   - Include both positive and negative test cases

2. **Update Test Orchestrator**:

   ```python
   # Add to run_all_tests.py
   (tests_dir / "test_new_feature.py", "New Feature Testing", "MEDIUM PRIORITY"),
   ```

3. **CI Integration**:
   - Update `.github/workflows/ci-cd.yml` if needed
   - Test on feature branch first
   - Validate on release branch

### Debugging Test Failures

1. **Reproduce Locally**:

   ```bash
   # Run specific failing test
   python3 tests/test_failing_module.py -v

   # Enable debug output
   DEBUG_TESTS=true python3 tests/test_failing_module.py
   ```

2. **Check Environment**:

   ```bash
   # Validate test environment
   python3 tests/test_base.py

   # Check dependencies
   uv pip list
   ```

3. **Binary Search Debugging**:
   - Isolate failing test case
   - Add debug prints
   - Test incremental changes
   - Validate fix doesn't break other tests

## Best Practices

### Writing New Tests

1. **Follow Test Hierarchy**:
   - Security tests → High priority
   - Feature tests → Medium priority
   - Performance tests → Low priority

2. **Use Descriptive Names**:

   ```python
   def test_dangerous_rm_with_recursive_flag_and_root_path(self):
       """Test that rm -rf / is detected as dangerous."""
   ```

3. **Include Both Positive and Negative Cases**:

   ```python
   def test_safe_rm_commands_are_allowed(self):
       """Test that safe rm commands are not blocked."""
       safe_cmd = "rm single_file.txt"
       self.assertFalse(is_dangerous_rm_command(safe_cmd))
   ```

### Test Maintenance

1. **Regular Review**:
   - Update tests when features change
   - Remove obsolete test cases
   - Refactor duplicated test logic

2. **Performance Monitoring**:
   - Keep test execution time under targets
   - Optimize slow tests or move to lower priority
   - Monitor CI resource usage

3. **Coverage Monitoring**:
   - Review coverage reports regularly
   - Address coverage gaps in high-priority areas
   - Document intentional coverage exclusions

## Troubleshooting

### Common Issues

**"Tests pass locally but fail in CI"**:

- Check environment variables
- Verify dependency versions
- Look for race conditions
- Check file system differences

**"High priority tests timing out"**:

- Profile test execution
- Remove unnecessary operations
- Consider mocking external calls
- Optimize test setup/teardown

**"TTS tests failing without API keys"**:

- This is expected behavior
- TTS tests are medium priority
- Use mock providers for CI
- Document API key requirements

### Getting Help

1. **Review Documentation**:
   - [adr-003: Testing Strategy](../adr/adr-003-testing-strategy.md)
   - [Development Guide](development.md)
   - [Troubleshooting Guide](../troubleshooting.md)

2. **Check Test Logs**:

   ```bash
   # Detailed test output
   python3 tests/run_all_tests.py 2>&1 | tee test_output.log
   ```

3. **Create Issues**:
   - Use GitHub issues for bugs
   - Include test output and environment details
   - Tag with appropriate priority labels

---

**Remember**: Security first, simplicity always, test only what's needed now. The testing strategy balances comprehensive coverage with development velocity while never compromising on security.
