#!/usr/bin/env python3
"""
Script to generate markdown activity files from planeamiento.json.

This script reads 'planeamiento.json', extracts the 'activities' field for each week,
and generates structured Markdown files in the 'activities/' directory.
"""

import json
import os
import re
import argparse
import unicodedata

# Configuration
JSON_FILE = 'planeamiento.json'
OUTPUT_DIR = 'activities'

# Translations configuration
TRANSLATIONS = {
    'es': {
        'week': 'Semana',
        'description': 'Descripción',
        'objectives': 'Objetivos',
        'materials': 'Materiales',
        'instructions': 'Instrucciones',
        'default_objective': '[Definir objetivo específico de la actividad]',
        'default_material': '[Lista de materiales]',
        'step': 'Paso',
        'modality': 'Presencial',
        'difficulty': 'Fundamental'
    },
    'en': {
        'week': 'Week',
        'description': 'Description',
        'objectives': 'Objectives',
        'materials': 'Materials',
        'instructions': 'Instructions',
        'default_objective': '[Define specific activity objective]',
        'default_material': '[List of materials]',
        'step': 'Step',
        'modality': 'In-person',
        'difficulty': 'Fundamental'
    },
    'fr': {
        'week': 'Semaine',
        'description': 'Description',
        'objectives': 'Objectifs',
        'materials': 'Matériel',
        'instructions': 'Instructions',
        'default_objective': '[Définir l\'objectif spécifique de l\'activité]',
        'default_material': '[Liste du matériel]',
        'step': 'Étape',
        'modality': 'Présentiel',
        'difficulty': 'Fondamental'
    }
}

def generate_filename(week_num, description):
    """
    Generates a web-safe filename from the week number and activity description.
    Uses the first few words of the description as the slug.
    """
    # Take first 6 words for the title part
    words = description.split()[:6]
    slug_text = " ".join(words)
    
    # Normalize unicode characters
    normalized = unicodedata.normalize('NFKD', slug_text).encode('ascii', 'ignore').decode('ascii')
    
    # Sanitize
    safe_slug = re.sub(r'[^\w\s-]', '', normalized).strip().lower()
    safe_slug = re.sub(r'[-\s]+', '-', safe_slug)
    
    return f"{int(week_num):02d}-{safe_slug}.md"

def main():
    parser = argparse.ArgumentParser(description='Generate activity skeleton files from planeamiento.json.')
    parser.add_argument('--force', action='store_true', help='Overwrite existing files')
    parser.add_argument('--lang', default='es', choices=['es', 'en', 'fr'], help='Language for generated content')
    args = parser.parse_args()
    
    t = TRANSLATIONS.get(args.lang, TRANSLATIONS['es'])

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

    print(f"Reading {JSON_FILE}...")
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            weeks = data.get('weeks', [])
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
1.  {t['default_objective'].replace('[', '').replace(']', '')} 1
2.  {t['default_objective'].replace('[', '').replace(']', '')} 2
"""
            # Fixing the instruction placeholder to be simpler as per original code was [Paso 1]
            # Let's use the translation key 'step'
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
            filepath = os.path.join(OUTPUT_DIR, filename)

            if os.path.exists(filepath) and not args.force:
                print(f"Skipping existing file: {filepath} (use --force to overwrite)")
                continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            print(f"Generated: {filepath}")

if __name__ == "__main__":
    main()
