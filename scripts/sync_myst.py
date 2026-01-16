#!/usr/bin/env python3
"""
Script to synchronize myst.yml with metadata from planeamiento.json.

This script updates the project title, subtitle, author, and copyright information
in 'myst.yml' to ensure consistency with the centralized course metadata.
It uses regex patterns to preserve existing comments and structure in the YAML file.
"""

import json
import re
import os

JSON_FILE = 'planeamiento.json'
MYST_FILE = 'myst.yml'

def main():
    if not os.path.exists(JSON_FILE) or not os.path.exists(MYST_FILE):
        print("Missing planeamiento.json or myst.yml")
        return

    # Read Metadata
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            metadata = data.get('metadata', {})
            if not metadata:
                print("No metadata found in planeamiento.json")
                return
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    # Extract values
    code = metadata.get('code', 'CODE')
    title = metadata.get('title', 'Course Title')
    semester = metadata.get('semester', 'Semester')
    authors = metadata.get('authors', ['Author'])
    author_name = authors[0] if isinstance(authors, list) and authors else "Author"
    university = metadata.get('university', 'University')
    
    # Construct strings
    project_title = f"{code}" # Or maybe "{title}"? myst.yml currently uses code as title. Let's stick to Code or Title? 
    # Current myst.yml: title: FI1105. 
    # Let's use Code for title, and Semester for subtitle, consistent with current.
    
    project_subtitle = semester
    site_title = code
    site_subtitle = semester
    
    # Copyright needs year
    year = re.search(r'\d{4}', semester)
    year_str = year.group(0) if year else "202X"
    copyright_str = f"© {year_str} {author_name}. Distribuido bajo licencia Creative Commons."

    print(f"Syncing {MYST_FILE} with metadata:")
    print(f"  Title: {project_title}")
    print(f"  Subtitle: {project_subtitle}")
    print(f"  Author: {author_name}")

    with open(MYST_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex Replacements
    # 1. Update project.title
    # Look for "  title: .*" inside project block? Or just generic?
    # YAML structure: 
    # project:
    #   title: ...
    # Warning: simple regex replacement might change other titles.
    # We need to be careful.
    
    # Replace project title (indented under project)
    content = re.sub(r'(^project:\s*\n\s+title:).+', f'\\1 {project_title}', content, flags=re.MULTILINE)
    
    # Replace project subtitle
    content = re.sub(r'(^project:\s*\n(?:.*\n)*?\s+subtitle:).+', f'\\1 {project_subtitle}', content, flags=re.MULTILINE)

    # Replace site title/subtitle (usually at bottom)
    content = re.sub(r'(^site:\s*\n\s+title:).+', f'\\1 {site_title}', content, flags=re.MULTILINE)
    content = re.sub(r'(^site:\s*\n(?:.*\n)*?\s+subtitle:).+', f'\\1 {site_subtitle}', content, flags=re.MULTILINE)

    # Replace author (first one)
    #   authors:
    #   - name: Escuela de Física
    content = re.sub(r'(\s+authors:\s*\n\s+-\s+name:).+', f'\\1 {author_name}', content, flags=re.MULTILINE)

    with open(MYST_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Done.")

if __name__ == "__main__":
    main()
