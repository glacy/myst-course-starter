#!/usr/bin/env python3
"""
Script to generate a markdown table of all sessions and their learning objectives.
Version: JSON Source (planeamiento.json)
"""
import argparse
import sys
import os

# Add local directory to path to allow imports if running directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils import load_json, TRANSLATIONS
except ImportError:
    # Fallback for when running from root
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
    from utils import load_json, TRANSLATIONS

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

OUTPUT_FILE = "sessions_table.md"

def run(lang: str = 'es'):
    """
    Generates the sessions table markdown file.
    
    Args:
        lang (str): Language code.
    """
    t = TRANSLATIONS.get(lang, TRANSLATIONS['es'])
    
    print(f"{CYAN}{t.get('generating', 'Generating {0}...').format(OUTPUT_FILE)}{RESET}")

    try:
        data = load_json()
        weeks = data.get('weeks', [])
    except Exception as e:
        print(f"{RED}{t.get('error', 'Error: {0}').format(e)}{RESET}")
        return

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            header_title = t.get('header_title', 'Sessions Table')
            col_week = t.get('col_week', 'Week')
            col_title = t.get('col_title', 'Title')
            col_objectives = t.get('col_objectives', 'Objectives')
            
            f.write(f"## {header_title}\n\n")
            f.write(f"| {col_week} | {col_title} | {col_objectives} |\n")
            f.write("|--------|--------|---------------------------|\n")

            for entry in weeks:
                week = entry.get('week', '')
                title = entry.get('title', '')
                
                # Clean title (remove numbers like "1. ")
                if isinstance(title, str) and "." in title[:3]:
                     parts = title.split(".", 1)
                     if len(parts) > 1: title = parts[1].strip()

                objectives = entry.get('objectives', [])

                if isinstance(objectives, list):
                    formatted_objectives = "<ul>" + "".join([f"<li>{o}</li>" for o in objectives]) + "</ul>"
                elif objectives:
                    formatted_objectives = str(objectives)
                else:
                    formatted_objectives = ""

                # Escape pipes
                title = str(title).replace("|", "&#124;")
                formatted_objectives = formatted_objectives.replace("|", "&#124;")

                f.write(f"| {week} | {title} | {formatted_objectives} |\n")

        print(f"{GREEN}{t.get('success', 'Success').format(OUTPUT_FILE)}{RESET}")
    except Exception as e:
         print(f"{RED}Error writing file: {e}{RESET}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', default='es', choices=['es', 'en', 'fr'])
    args = parser.parse_args()
    run(lang=args.lang)

if __name__ == "__main__":
    main()
