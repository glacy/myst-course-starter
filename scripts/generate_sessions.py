#!/usr/bin/env python3
"""
Script to generate markdown session files from planeamiento.json.

This script reads 'planeamiento.json', extracting content for each week,
and generates structured Markdown files with YAML frontmatter in the 'sessions/' directory.

Features:
- Generates contents as visual badges (using shields.io) before objectives.
- Safely handles existing files: skips by default, use --force to overwrite.
- Multilingual support: generates output in Spanish (es), English (en), or French (fr).

Multilingual Output:
The script supports generating session files in multiple languages using the --lang argument.
When a language is selected, the following elements are translated:
- Section headers (Objectives, Activities, Evaluation, References)
- Default titles and subtitles (when not provided in JSON)
- Modality labels (Presencial/In-person/Présentiel)
- Instructional text in objectives block

Note: The content from planeamiento.json (titles, objectives, activities, etc.) is used as-is.
Only the script-generated labels and default values are translated.

Usage:
    python scripts/generate_sessions.py [--lang {es|en|fr}] [--week N] [--force]
    
Examples:
    # Generate all sessions in Spanish (default)
    python scripts/generate_sessions.py
    
    # Generate all sessions in English
    python scripts/generate_sessions.py --lang en
    
    # Generate only week 1 in French
    python scripts/generate_sessions.py --lang fr --week 1
    
    # Overwrite existing files
    python scripts/generate_sessions.py --lang en --force
"""

import json
import os
import yaml
import re

# Configuration
JSON_FILE = 'planeamiento.json'
OUTPUT_DIR = 'sessions'

# Translations dictionary
# Maps language codes (es, en, fr) to translated strings for:
# - Section headers (objectives, activities, evaluation, references)
# - Default titles/subtitles when not provided in JSON
# - Modality labels
# - Instructional text in objectives block
TRANSLATIONS = {
    'es': {
        'session': 'Sesión',
        'week': 'Semana',
        'modality': 'Presencial',
        'objectives': 'Objetivos',
        'objectives_intro': 'Al completar esta lección, serás capaz de:',
        'activities': 'Actividades',
        'evaluation': 'Evaluación',
        'references': 'Referencias'
    },
    'en': {
        'session': 'Session',
        'week': 'Week',
        'modality': 'In-person',
        'objectives': 'Objectives',
        'objectives_intro': 'Upon completing this lesson, you will be able to:',
        'activities': 'Activities',
        'evaluation': 'Evaluation',
        'references': 'References'
    },
    'fr': {
        'session': 'Séance',
        'week': 'Semaine',
        'modality': 'Présentiel',
        'objectives': 'Objectifs',
        'objectives_intro': 'En complétant cette leçon, vous serez capable de :',
        'activities': 'Activités',
        'evaluation': 'Évaluation',
        'references': 'Références'
    }
}

import unicodedata

def generate_filename(week_num, title):
    """
    Generates a web-safe filename from the week number and title.
    
    Args:
        week_num (int): The week/session number.
        title (str): The session title.
        
    Returns:
        str: Filename like '01-session-title.md'.
    """
    # Normalize unicode characters (e.g., ó -> o)
    normalized_title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('ascii')
    
    # Sanitize title for filename
    safe_title = re.sub(r'[^\w\s-]', '', normalized_title).strip().lower()
    safe_title = re.sub(r'[-\s]+', '-', safe_title)
    return f"{int(week_num):02d}-{safe_title}.md"

import argparse

# ... existing imports ...

# ... existing constants and functions ...

def main():
    """
    Main function to generate session markdown files from planeamiento.json.
    
    Supports multilingual output via --lang argument. Translations are applied to:
    - Section headers, default values, and instructional text.
    - Content from JSON is used as-is (not translated).
    """
    parser = argparse.ArgumentParser(
        description='Generate markdown session files from planeamiento.json.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Generate all sessions in Spanish (default):
    python scripts/generate_sessions.py
  
  Generate all sessions in English:
    python scripts/generate_sessions.py --lang en
  
  Generate only week 1 in French:
    python scripts/generate_sessions.py --lang fr --week 1
  
  Overwrite existing files:
    python scripts/generate_sessions.py --lang en --force
        """
    )
    parser.add_argument('--week', type=int, help='Specific week number to generate (e.g., 1)')
    parser.add_argument('--force', action='store_true', help='Overwrite existing files')
    parser.add_argument('--lang', type=str, default='es', choices=['es', 'en', 'fr'],
                       help='Output language: es (Spanish), en (English), or fr (French). Default: es')
    args = parser.parse_args()
    
    # Get translations for selected language
    lang = args.lang
    t = TRANSLATIONS[lang]

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

    print(f"Reading {JSON_FILE}...")
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            full_data = json.load(f)
            # Support both new (dict with weeks) and old (list) schemas for backward compatibility
            if isinstance(full_data, dict) and 'weeks' in full_data:
                data = full_data['weeks']
                metadata = full_data.get('metadata', {})
            else:
                data = full_data
                metadata = {}
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    # Filter data if week argument is provided
    if args.week:
        print(f"Filtering for week {args.week}...")
        data = [entry for entry in data if entry.get('week') == args.week]
        if not data:
            print(f"No data found for week {args.week}")
            return

    # Defaults from metadata or fallback
    course_name = metadata.get('title', "your course name")
    authors_list = metadata.get('authors', ["your name"])
    # Ensure authors is a list of dicts for the frontmatter format
    if isinstance(authors_list, list) and authors_list and isinstance(authors_list[0], str):
        authors_fm = [{'name': a} for a in authors_list]
    else:
        authors_fm = [{'name': "your name"}]


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

            # YAML formatting
            yaml_frontmatter = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
            
            # Construct Markdown Body
            md_content = f"---\n{yaml_frontmatter}---\n\n"
            
            # Format Contents as Badges
            if content_list:
                # md_content += "## Contenidos\n\n" # Removed header for cleaner look with badges
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
                
                # Try to import generator from sibling
                import sys
                sys.path.append(os.path.dirname(os.path.abspath(__file__)))
                try:
                    from generate_activities import generate_filename as gen_act_filename
                except ImportError:
                    gen_act_filename = None
                
                for act_desc in act_list:
                    if gen_act_filename:
                        act_file = gen_act_filename(week_num, act_desc)
                        # Link to the activity file in activities/ directory
                        # Use relative path: ../activities/filename
                        link = f"[{act_desc}](../activities/{act_file})"
                        md_content += f"- {link}\n"
                    else:
                        md_content += f"- {act_desc}\n"
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
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            if os.path.exists(filepath) and not args.force:
                print(f"Skipping existing file: {filepath} (use --force to overwrite)")
                continue

            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            print(f"Generated: {filepath}")

        except Exception as e:
            print(f"Error processing week {entry.get('week')}: {e}")

if __name__ == "__main__":
    main()
