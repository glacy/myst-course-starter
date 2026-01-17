#!/usr/bin/env python3
import argparse
import os
import sys

# Add local directory to path to allow imports if running directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils import (
        load_json, TRANSLATIONS
    )
except ImportError:
    # Fallback for when running from root
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
    from utils import (
        load_json, TRANSLATIONS
    )

def run(lang: str = 'es', init: bool = False):
    """
    Generates programa.md.
    
    Args:
        lang (str): Language code.
        init (bool): Only create if missing.
    """
    output_file = 'programa.md'
    if init and os.path.exists(output_file):
        print(f"Skipping {output_file}: already exists (and --init flag used).")
        return

    t = TRANSLATIONS.get(lang, TRANSLATIONS['es'])
    
    try:
        data = load_json()
        metadata = data.get('metadata', {})
        weeks = data.get('weeks', [])
    except Exception as e:
        print(f"Error reading planeamiento.json: {e}")
        return

    # Extract metadata
    title = metadata.get('title', 'Course Title')
    semester = metadata.get('semester', 'Semester')
    university = metadata.get('university', 'University')
    code = metadata.get('code', 'CODE')
    description = metadata.get('description', 'No description provided.')
    authors = metadata.get('authors', [])
    author_name = authors[0] if isinstance(authors, list) and authors else "Instructor"

    # Define placeholders if not in translations (fallback)
    t.setdefault('placeholder_objectives', 'General course objectives will be detailed here.')
    t.setdefault('placeholder_methodology', 'Course methodology will be described here.')
    t.setdefault('placeholder_evaluation', 'Evaluation rules will be detailed here.')

    # Build Content
    md_content = f"""---
title: {title}
subtitle: {semester}
author: {author_name}
---

# {title}

|  |  |
| :--- | :--- |
| **{t.get('university', 'University')}** | {university} |
| **{t.get('code', 'Code')}** | {code} |
| **{t.get('semester', 'Semester')}** | {semester} |

## 📝 {t['description']}

{description}

## 🎯 {t['objectives']}

{t['placeholder_objectives']}

## 🧠 {t.get('methodology', 'Methodology')}

{t['placeholder_methodology']}

## 📊 {t['evaluation']}

{t['placeholder_evaluation']}

## 📅 {t.get('schedule', 'Schedule')}

"""
    # Append simple schedule from weeks
    if weeks:
        # Simple hack for translation of 'Code' to 'Week' equivalent in table header if needed
        # But let's just use generic or translated headers
        week_header = t.get('week', 'Week')
        
        md_content += f"| {week_header} | Title | Content |\n"
        md_content += "| :--- | :--- | :--- |\n"
        for w in weeks:
            num = w.get('week', '?')
            w_title = w.get('title', '')
            w_content = w.get('content', [])
            content_str = ", ".join(w_content) if isinstance(w_content, list) else str(w_content)
            # Escaping pipe in content just in case
            content_str = content_str.replace('|', '-')
            md_content += f"| {num} | {w_title} | {content_str} |\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✅ Generated {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Generate programa.md from planeamiento.json')
    parser.add_argument('--lang', default='es', choices=['es', 'en', 'fr'], help='Language for headers')
    parser.add_argument('--init', action='store_true', help='Only create if missing (do not overwrite)')
    args = parser.parse_args()
    
    run(lang=args.lang, init=args.init)

if __name__ == "__main__":
    main()
