#!/usr/bin/env python3
"""
Script to synchronize session filenames in 'myst.yml'.

This script scans the 'sessions/' directory for files matching 'XX-*.md'.
It then updates the corresponding links in 'myst.yml' ensuring that the
Table of Contents points to the correct (sanitized) filenames on disk.
It uses regex to preserve the existing structure (comments, other children like activities).
"""

import glob
import re
import os
import sys

# Add local directory to path to allow imports if running directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils import OUTPUT_DIR_SESSIONS
except ImportError:
    # Fallback for when running from root
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
    from utils import OUTPUT_DIR_SESSIONS

MYST_FILE = 'myst.yml'

def main():
    if not os.path.exists(MYST_FILE):
        print(f"Error: {MYST_FILE} not found.")
        return

    with open(MYST_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Scanning {OUTPUT_DIR_SESSIONS} for updates...")
    
    updated_count = 0
    
    # Iterate through potential weeks (1 to 20 to be safe)
    # Or just glob all files in sessions
    session_files = sorted(glob.glob(os.path.join(OUTPUT_DIR_SESSIONS, '[0-9][0-9]-*.md')))
    
    for file_path in session_files:
        basename = os.path.basename(file_path)
        # Extract metadata from filename: "01-my-title.md" -> prefix "01-"
        match = re.match(r'^(\d{2})-', basename)
        if not match:
            continue
            
        prefix = match.group(1) # e.g., "01"
        
        # Regex to find the existing entry in myst.yml
        # Looking for: "file: sessions/01-old-name.md"
        # We match "file: sessions/01-.*\.md"
        
        folder_name = os.path.basename(OUTPUT_DIR_SESSIONS)
        pattern = fr'(file:\s*{folder_name}/)({prefix}-.*\.md)'
        
        # Perform replacement
        new_content = re.sub(pattern, f'\\g<1>{basename}', content)
        
        if new_content != content:
            print(f"Updating Week {prefix}: {basename}")
            content = new_content
            updated_count += 1
        
    if updated_count > 0:
        with open(MYST_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully updated {updated_count} links in {MYST_FILE}.")
    else:
        print("No changes needed in myst.yml.")

if __name__ == "__main__":
    main()
