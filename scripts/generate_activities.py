#!/usr/bin/env python3
"""
Script to generate markdown activity files from planeamiento.json.

This script reads 'planeamiento.json', extracts the 'activities' field for each week,
and generates structured Markdown files in the 'activities/' directory.
"""

import argparse
import sys
import os

# Add local directory to path to allow imports if running directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils import (
        load_json, generate_filename, OUTPUT_DIR_ACTIVITIES, TRANSLATIONS
    )
except ImportError:
    # Fallback for when running from root
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
    from utils import (
        load_json, generate_filename, OUTPUT_DIR_ACTIVITIES, TRANSLATIONS
    )

def run(lang: str = 'es', force: bool = False):
    """
    Generates activity skeleton files.
    
    Args:
        lang (str): Language code.
        force (bool): Whether to overwrite existing files.
    """
    t = TRANSLATIONS.get(lang, TRANSLATIONS['es'])

    if not os.path.exists(OUTPUT_DIR_ACTIVITIES):
        os.makedirs(OUTPUT_DIR_ACTIVITIES)
        print(f"Created directory: {OUTPUT_DIR_ACTIVITIES}")

    print(f"Reading configuration...")
    try:
        full_data = load_json()
        weeks = full_data.get('weeks', [])
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    for entry in weeks:
        week_num = entry.get('week')
        if not week_num:
            continue

        raw_activity = entry.get('activities')
        if not raw_activity:
            continue

        # Normalize to list to handle single string or list of strings
        activities_list = []
        if isinstance(raw_activity, str):
            activities_list.append(raw_activity)
        elif isinstance(raw_activity, list):
            activities_list = raw_activity

        for i, activity_desc in enumerate(activities_list):
            filename = generate_filename(week_num, activity_desc)
            
            # Use title from description (first sentence or whole thing)
            title = activity_desc.split('.')[0]
            if len(title) > 60:
                title = title[:57] + "..."
            
            # Frontmatter
            md_content = f"""---
title: "{title}"
duration: "60 min"
modality: "{t['modality']}"
difficulty: "{t['difficulty']}"
---



## 📝 {t['description']}
{activity_desc}

## 🎯 {t['objectives']}
*   {t['default_objective']}

## 🛠️ {t['materials']}
*   {t['default_material']}

## 📄 {t['instructions']}
1.  [{t['step']} 1]
2.  [{t['step']} 2]
"""
            filepath = os.path.join(OUTPUT_DIR_ACTIVITIES, filename)

            if os.path.exists(filepath) and not force:
                print(f"Skipping existing file: {filepath} (use --force to overwrite)")
                continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            print(f"Generated: {filepath}")

def main():
    parser = argparse.ArgumentParser(description='Generate activity skeleton files from planeamiento.json.')
    parser.add_argument('--force', action='store_true', help='Overwrite existing files')
    parser.add_argument('--lang', default='es', choices=['es', 'en', 'fr'], help='Language for generated content')
    args = parser.parse_args()
    
    run(lang=args.lang, force=args.force)

if __name__ == "__main__":
    main()
