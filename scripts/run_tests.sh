#!/bin/bash
#
# Simple test runner script for PRP system
# Compatible with UV and standard Python environments
#

set -e

echo "PRP System Test Runner"
echo "====================="

# Check if we're in the right directory
if [[ ! -d "PRPs" ]]; then
    echo "Error: Run this script from the project root (where PRPs/ directory exists)"
    exit 1
fi

# Ensure scripts directory is in Python path
export PYTHONPATH="${PWD}/scripts:${PWD}/tests:${PYTHONPATH}"

echo "Running PRP validation tests..."

# Try UV first, fallback to regular Python
if command -v uv >/dev/null 2>&1; then
    echo "Using UV to run tests..."
    uv run python scripts/test_prp_system.py
else
    echo "UV not found, using system Python..."
    python scripts/test_prp_system.py
fi

echo ""
echo "To validate individual PRPs:"
echo "  uv run python scripts/validate_prp.py PRPs/your_prp.md"
echo "  # or: python scripts/validate_prp.py PRPs/your_prp.md"
echo ""
echo "To validate all PRPs in directory:"
echo "  uv run python scripts/validate_prp.py PRPs/"
echo "  # or: python scripts/validate_prp.py PRPs/"