"""
Script to inject a visible learning objectives block into markdown session files.

This script parses existing markdown files in 'sessions/', extracts 'learning_objectives'
from the YAML frontmatter, and inserts a formatted MyST note block (:::{note} Objetivos)
immediately after the frontmatter if it doesn't already exist.
"""

import os
import re
import yaml
import glob

SESSIONS_DIR = 'sessions'

def add_objectives_block(filepath):
    """
    Reads a markdown file, checks for objectives in frontmatter, and appends a visual block.
    
    Args:
        filepath (str): Path to the markdown file.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter
    match = re.search(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        print(f"No frontmatter found in {filepath}")
        return

    frontmatter_raw = match.group(1)
    
    try:
        data = yaml.safe_load(frontmatter_raw)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML in {filepath}: {e}")
        return

    objectives = data.get('learning_objectives', [])
    if not objectives:
        print(f"No learning_objectives in {filepath}")
        return

    # Check if block already exists
    if ":::{note} Objetivos" in content:
        print(f"Block already exists in {filepath}")
        return

    # Construct block
    block_lines = [":::{note} Objetivos", "Al completar esta lección, serás capaz de:"]
    for i, obj in enumerate(objectives, 1):
        block_lines.append(f"{i}. {obj}")
    block_lines.append(":::")
    block_text = "\n".join(block_lines) + "\n\n"

    # Insert after frontmatter
    end_of_frontmatter = match.end()
    new_content = content[:end_of_frontmatter] + "\n" + block_text + content[end_of_frontmatter:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Added objectives block to {filepath}")

def main():
    files = sorted(glob.glob(os.path.join(SESSIONS_DIR, '*.md')))
    for filepath in files:
        add_objectives_block(filepath)

if __name__ == "__main__":
    main()
