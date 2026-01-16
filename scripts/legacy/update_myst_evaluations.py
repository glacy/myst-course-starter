#!/usr/bin/env python3
"""
Script to automatically update myst.yml with evaluation file references.

This script scans the 'evaluations/' directory for markdown evaluation files and
automatically inserts references to them in the myst.yml configuration file.
The evaluations are inserted as hidden entries after the last file entry of each
corresponding week section.

The script:
1. Scans the evaluations/ directory for .md files
2. Maps week numbers (extracted from filenames like "01-evaluation.md") to evaluation files
3. Parses myst.yml to find week sections (identified by "title: Semana X")
4. Inserts evaluation file references after the last file entry in each week section
5. Marks evaluations as hidden: true so they are included but not shown in navigation

Usage:
    python scripts/update_myst_evaluations.py

Note: This script modifies myst.yml in place. It's recommended to commit changes
before running, or use version control to review modifications.
"""

import os
import re

def update_myst():
    """
    Update myst.yml to include evaluation files from the evaluations/ directory.
    
    This function:
    - Reads myst.yml and scans the evaluations/ directory
    - Maps week numbers to evaluation filenames (based on filename prefix, e.g., "01-*.md" -> week 1)
    - Finds week sections in myst.yml by detecting "title: Semana X" entries
    - Inserts evaluation file references after the last file entry in each week section
    - Marks evaluations as hidden: true to include them without showing in navigation
    
    The insertion logic:
    - Tracks the current week while scanning myst.yml
    - Records the last file entry line for each week
    - When a new week is detected or the table of contents ends, inserts the evaluation
      reference after the last file entry of the previous week
    - Inserts are applied in reverse order to preserve line indices
    
    Raises:
        No exceptions, but prints error messages if myst.yml is not found.
    """
    # Get paths relative to project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    myst_path = os.path.join(base_dir, 'myst.yml')
    eval_dir = os.path.join(base_dir, 'evaluations')
    
    # Check if myst.yml exists
    if not os.path.exists(myst_path):
        print(f"Error: {myst_path} not found.")
        return

    # Read myst.yml line by line for processing
    with open(myst_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Get all markdown files from evaluations directory
    if not os.path.exists(eval_dir):
        print(f"Warning: {eval_dir} directory not found. No evaluations to add.")
        return
        
    eval_files = sorted([f for f in os.listdir(eval_dir) if f.endswith('.md')])
    
    # Map week number to evaluation filename
    # Assumes evaluation files are named like "01-evaluation.md" where "01" is the week number
    week_map = {}
    for fname in eval_files:
        try:
            # Extract week number from first two characters of filename
            num = int(fname[:2])
            week_map[num] = fname
        except (ValueError, IndexError):
            # Skip files that don't start with a two-digit number
            pass
            
    # Scan myst.yml to find insertion points for evaluation files
    # Format: List of tuples (line_index_to_insert_after, text_to_insert)
    insertions = []
    
    current_week = None  # Track which week we're currently processing
    last_file_line = -1  # Track the last file entry line in the current week
    
    for idx, line in enumerate(lines):
        # 1. Detect new "Semana X" (Week Header) - marks the start of a new week section
        ws_match = re.search(r'^\s*-\s*title:\s*Semana\s*(\d+)', line)
        if ws_match:
            # If we were processing a previous week, insert its evaluation NOW
            # (before starting to track the new week)
            if current_week is not None and current_week in week_map:
                # Insert evaluation reference after the last file entry of the previous week
                indent = "      "  # Match YAML indentation structure
                text = f"{indent}- file: evaluations/{week_map[current_week]}\n{indent}  hidden: true\n"
                insertions.append((last_file_line, text))
            
            # Start tracking the new week
            current_week = int(ws_match.group(1))
            last_file_line = idx  # Fallback position if no files found in this week
            
        # 2. Detect End of Table of Contents section
        # When we hit a top-level key like "site:", we've left the TOC structure
        elif re.match(r'^site:', line):
            # Insert evaluation for the last week if we were tracking one
            if current_week is not None and current_week in week_map:
                indent = "      "
                text = f"{indent}- file: evaluations/{week_map[current_week]}\n{indent}  hidden: true\n"
                insertions.append((last_file_line, text))
            current_week = None  # Stop tracking weeks
            
        # 3. Detect File entry (children entries in the YAML structure)
        # Track the LAST file entry in the current week to append evaluation after it
        elif re.search(r'^\s*-\s*file:', line):
            if current_week is not None:
                last_file_line = idx  # Update position of last file entry

    print(f"Found {len(insertions)} evaluations to insert.")

    # Apply insertions in reverse order to preserve line indices
    # (inserting from end to beginning prevents index shifts)
    insertions.sort(key=lambda x: x[0], reverse=True)
    
    for line_idx, text in insertions:
        # Insert after the specified line (line_idx + 1)
        lines.insert(line_idx + 1, text)
        
    # Write updated content back to myst.yml
    with open(myst_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Updated myst.yml with evaluations.")

if __name__ == "__main__":
    update_myst()
