#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Clean duplicate content in agent description blocks.
"""

import re
from pathlib import Path

def clean_agent_file(file_path):
    """Clean duplicate content in agent file description"""
    with open(file_path, 'r') as f:
        content = f.read()

    # Find and fix duplicate content in description block
    pattern = r'(description: \|\n(?:  [^\n]*\n){4})(\n  NEVER use when:.*?\n  Hands off to:.*?)\'?'

    match = re.search(pattern, content, re.DOTALL)
    if match:
        # Keep only the first instance
        clean_description = match.group(1).rstrip()
        new_content = content[:match.start()] + clean_description + content[match.end():]

        with open(file_path, 'w') as f:
            f.write(new_content)
        return True
    return False

def main():
    claude_dir = Path('.claude')
    if not claude_dir.exists():
        print("❌ .claude directory not found")
        return

    agents_dir = claude_dir / 'agents'
    agent_files = list(agents_dir.rglob('*.md'))
    agent_files = [f for f in agent_files if f.name != 'README.md']

    fixed_count = 0

    for agent_file in agent_files:
        if clean_agent_file(agent_file):
            print(f"✅ {agent_file.name}: Cleaned duplicated content")
            fixed_count += 1

    print(f"\n🎯 Cleaned {fixed_count} agent files")

if __name__ == "__main__":
    main()