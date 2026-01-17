#!/usr/bin/env python3
"""
Script to generate markdown session files from planeamiento.json.

This script reads 'planeamiento.json', extracting content for each week,
and generates structured Markdown files with YAML frontmatter in the 'sessions/' directory.
"""

import argparse
import sys
import os
import yaml

# Add local directory to path to allow imports if running directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils import (
        load_json, generate_filename, OUTPUT_DIR_SESSIONS, TRANSLATIONS
    )
except ImportError:
    # Fallback for when running from root
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
    from utils import (
        load_json, generate_filename, OUTPUT_DIR_SESSIONS, TRANSLATIONS
    )

def run(lang: str = 'es', week: int = None, force: bool = False):
    """
    Generates session markdown files.
    
    Args:
        lang (str): Language code ('es', 'en', 'fr').
        week (int, optional): Specific week to generate.
        force (bool): Whether to overwrite existing files.
    """
    t = TRANSLATIONS.get(lang, TRANSLATIONS['es'])

    if not os.path.exists(OUTPUT_DIR_SESSIONS):
        os.makedirs(OUTPUT_DIR_SESSIONS)
        print(f"Created directory: {OUTPUT_DIR_SESSIONS}")

    print(f"Reading configuration...")
    try:
        full_data = load_json()
        data = full_data.get('weeks', [])
        metadata = full_data.get('metadata', {})
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    # Filter data if week argument is provided
    if week:
        print(f"Filtering for week {week}...")
        data = [entry for entry in data if entry.get('week') == week]
        if not data:
            print(f"No data found for week {week}")
            return

    # Defaults from metadata or fallback
    course_name = metadata.get('title', "your course name")

    for entry in data:
        try:
            week_num = entry.get('week')
            if not week_num:
                continue
            
            # Content extraction
            content_list = entry.get('content', [])
            objectives = entry.get('objectives', [])
            activities = entry.get('activities', "")
            evaluation_list = entry.get('evaluation', [])
            references_list = entry.get('references', [])

            # Process Title (First item of content or generic)
            title = entry.get('title', f"{t['session']} {int(week_num)}")
            subtitle = entry.get('subtitle', f"{t['week']} {int(week_num)}")

            # Process Keywords (simple extraction from title)
            keywords = [word for word in title.split() if len(word) > 4]

            # Construct Frontmatter
            frontmatter = {
                'title': title,
                'subtitle': subtitle,
                'subject': course_name,
                'session': {
                    'number': int(week_num),
                    'duration': "TBD",
                    'modality': t['modality']
                },
                'keywords': keywords,
                'learning_objectives': objectives,
                'activities': activities,
                'evaluation': evaluation_list,
                'references': references_list
            }
            
            # Construct Markdown Body
            yaml_frontmatter = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
            
            md_content = f"---\n{yaml_frontmatter}---\n\n"
            
            # Format Contents as Badges
            if content_list:
                badges = []
                for item in content_list:
                     # Escape characters for shields.io: - -> --, _ -> __, space -> _
                     safe_item = item.replace('-', '--').replace('_', '__').replace(' ', '_').replace('?', '%3F')
                     # Use lightgrey color
                     badge_url = f"https://img.shields.io/badge/-{safe_item}-lightgrey"
                     badges.append(f"![]({badge_url})")
                md_content += " ".join(badges) + "\n\n"

            # Add Objectives Block
            if objectives:
                md_content += f":::{{note}} {t['objectives']}\n"
                md_content += f"{t['objectives_intro']}\n"
                for i, obj in enumerate(objectives, 1):
                    md_content += f"{i}. {obj}\n"
                md_content += ":::\n\n"
            

            # Helper to link activities
            if activities:
                md_content += f"## {t['activities']}\n\n"
                
                # Normalize to list
                act_list = []
                if isinstance(activities, str):
                    act_list.append(activities)
                elif isinstance(activities, list):
                    act_list = activities
                
                for act_desc in act_list:
                    # We use generate_filename from utils
                    act_file = generate_filename(week_num, act_desc)
                    # Link to the activity file in activities/ directory
                    link = f"[{act_desc}](../activities/{act_file})"
                    md_content += f"- {link}\n"

                md_content += "\n"
            
            if evaluation_list:
                md_content += f"## {t['evaluation']}\n\n"
                for eval_item in evaluation_list:
                    etype = eval_item.get('type', t['evaluation'])
                    desc = eval_item.get('description', '')
                    md_content += f"- **{etype}**: {desc}\n"
                md_content += "\n"
            
            if references_list:
                md_content += f"## {t['references']}\n\n"
                for ref in references_list:
                    text = ref.get('text', '')
                    pages = ref.get('pages', '')
                    ref_str = f"{text}"
                    if pages:
                        ref_str += f", {pages}"
                    md_content += f"- {ref_str}\n"
                md_content += "\n"

            # Write file
            filename = generate_filename(week_num, title)
            filepath = os.path.join(OUTPUT_DIR_SESSIONS, filename)
            
            if os.path.exists(filepath) and not force:
                print(f"Skipping existing file: {filepath} (use --force to overwrite)")
                continue

            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            print(f"Generated: {filepath}")

        except Exception as e:
            print(f"Error processing week {entry.get('week')}: {e}")

def main():
    """
    Main function to generate session markdown files from planeamiento.json.
    """
    parser = argparse.ArgumentParser(
        description='Generate markdown session files from planeamiento.json.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--week', type=int, help='Specific week number to generate (e.g., 1)')
    parser.add_argument('--force', action='store_true', help='Overwrite existing files')
    parser.add_argument('--lang', type=str, default='es', choices=['es', 'en', 'fr'],
                       help='Output language: es (Spanish), en (English), or fr (French). Default: es')
    args = parser.parse_args()
    
    run(lang=args.lang, week=args.week, force=args.force)

if __name__ == "__main__":
    main()
