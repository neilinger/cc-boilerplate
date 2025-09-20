#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Fix tools list formatting to be on a single line.
"""

import re
from pathlib import Path

def fix_agent_tools_formatting(file_path):
    """Fix tools formatting in a single agent file"""
    with open(file_path, 'r') as f:
        content = f.read()

    # Pattern to match tools line that continues to next line
    pattern = r'tools: ([^\n]+),\n  ([^\n]+)'

    def replace_tools(match):
        line1 = match.group(1)
        line2 = match.group(2)
        return f'tools: {line1}, {line2}'

    new_content = re.sub(pattern, replace_tools, content)

    if new_content != content:
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
        if fix_agent_tools_formatting(agent_file):
            print(f"✅ {agent_file.name}: Fixed tools formatting")
            fixed_count += 1

    print(f"\n🎯 Fixed {fixed_count} agent files")

if __name__ == "__main__":
    main()