#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///

"""
Fix description newline formatting in agent files.

This script fixes the YAML format issue where descriptions have embedded
newlines causing incorrect formatting in frontmatter.
"""

import os
import re
import yaml
from pathlib import Path

def fix_agent_description(file_path):
    """Fix description formatting in a single agent file"""
    with open(file_path, 'r') as f:
        content = f.read()

    # Parse frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not frontmatter_match:
        return False, "Missing frontmatter"

    frontmatter_yaml = frontmatter_match.group(1)
    body_content = frontmatter_match.group(2)

    # Check if description has embedded newlines in quotes
    if not re.search(r"description: '[^']*\n[^']*'", frontmatter_yaml):
        return False, "No embedded newlines found"

    # Parse YAML
    try:
        frontmatter = yaml.safe_load(frontmatter_yaml)
    except yaml.YAMLError as e:
        return False, f"YAML error: {e}"

    # Get the description
    description = frontmatter.get('description', '')
    if not description:
        return False, "No description found"

    # Ensure description uses block scalar format
    frontmatter['description'] = description

    # Convert back to YAML with custom formatting
    new_yaml_lines = []
    yaml_lines = yaml.dump(frontmatter, default_flow_style=False).strip().split('\n')

    i = 0
    while i < len(yaml_lines):
        line = yaml_lines[i]
        if line.startswith('description:'):
            # Replace with block scalar format
            new_yaml_lines.append('description: |')
            # Add description lines with proper indentation
            desc_lines = description.split('\n')
            for desc_line in desc_lines:
                new_yaml_lines.append(f'  {desc_line}')
        else:
            new_yaml_lines.append(line)
        i += 1

    # Reconstruct file
    new_frontmatter = '\n'.join(new_yaml_lines)
    new_content = f"---\n{new_frontmatter}\n---\n{body_content}"

    # Write back
    with open(file_path, 'w') as f:
        f.write(new_content)

    return True, "Fixed"

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
        success, message = fix_agent_description(agent_file)
        if success:
            print(f"✅ {agent_file.name}: {message}")
            fixed_count += 1
        elif "No embedded newlines found" not in message:
            print(f"⚠️  {agent_file.name}: {message}")

    print(f"\n🎯 Fixed {fixed_count} agent files")

if __name__ == "__main__":
    main()