#!/usr/bin/env python3
"""Check PRP files for IN_PROGRESS status and warn if found.

This script is used by pre-commit to warn developers when they're
committing PRPs that are still in progress.
"""
import sys
import re
from pathlib import Path


def check_prp_status(files):
    """Check if any PRP files have IN_PROGRESS status.
    
    Args:
        files: List of file paths to check
        
    Returns:
        0 always (warnings don't block commits)
    """
    in_progress = []
    
    for file_path in files:
        path = Path(file_path)
        if path.exists() and path.suffix == '.md':
            try:
                content = path.read_text()
                # Look for Status: IN_PROGRESS pattern
                if re.search(r'^Status:\s*IN_PROGRESS', content, re.MULTILINE):
                    in_progress.append(file_path)
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
    
    if in_progress:
        print("\n⚠️  Warning: Committing PRPs with IN_PROGRESS status:")
        for file in in_progress:
            # Extract just the filename for cleaner output
            filename = Path(file).name
            print(f"  - {filename}")
        print("\nConsider updating status to:")
        print("  - COMPLETED if work is done and reviewed")
        print("  - PROPOSED if work hasn't started yet")
        print("  - OBSOLETE if no longer relevant\n")
    
    # Always return 0 to warn but not block
    return 0


if __name__ == "__main__":
    # Pre-commit passes file paths as arguments
    sys.exit(check_prp_status(sys.argv[1:]))