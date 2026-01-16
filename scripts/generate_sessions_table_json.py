#!/usr/bin/env python3
"""
Script to generate a markdown table of all sessions and their learning objectives.
Version: JSON Source (planeamiento.json)
"""
import json

import argparse
import sys

# Translations
TRANSLATIONS = {
    'es': {
        'generating': 'Generando {0} desde JSON...',
        'success': '✔ Tabla generada en {0}',
        'error': '✗ Error fatal: {0}',
        'header_title': 'Tabla de sesiones y resultados de aprendizaje',
        'col_week': 'Semana',
        'col_title': 'Título',
        'col_objectives': 'Resultados de aprendizaje'
    },
    'en': {
        'generating': 'Generating {0} from JSON...',
        'success': '✔ Table generated in {0}',
        'error': '✗ Fatal error: {0}',
        'header_title': 'Sessions and Learning Outcomes Table',
        'col_week': 'Week',
        'col_title': 'Title',
        'col_objectives': 'Learning Outcomes'
    },
    'fr': {
        'generating': 'Génération de {0} depuis JSON...',
        'success': '✔ Tableau généré dans {0}',
        'error': '✗ Erreur fatale: {0}',
        'header_title': 'Tableau des séances et objectifs d\'apprentissage',
        'col_week': 'Semaine',
        'col_title': 'Titre',
        'col_objectives': 'Objectifs d\'apprentissage'
    }
}

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

output_file = "sessions_table.md"
json_file = "planeamiento.json"

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument('--lang', default='es', choices=['es', 'en', 'fr'])
args = parser.parse_args()
t = TRANSLATIONS[args.lang]

print(f"{CYAN}{t['generating'].format(output_file)}{RESET}")

try:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"## {t['header_title']}\n\n")
        f.write(f"| {t['col_week']} | {t['col_title']} | {t['col_objectives']} |\n")
        f.write("|--------|--------|---------------------------|\n")

        with open(json_file, "r", encoding="utf-8") as jf:
            data = json.load(jf)

        # Sort data by week just in case
        #data['weeks'].sort(key=lambda x: x.get('week', 0))

        for entry in data['weeks']:
            week = entry.get('week', '')
            # Title is not explicitly in JSON structure in the same way as frontmatter.
            # The current generator infers it or uses "Sesión X" if not found in generate_sessions.py
            # But let's look at the content first line or similar logic. 
            # In generate_sessions.py logic: title = content_lines[0]
            title = entry.get('title', '')
            
            # Clean title (remove numbers like "1. ")
            # Simple logic to match generate_sessions.py mostly
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

    print(f"{GREEN}{t['success'].format(output_file)}{RESET}")
    
except Exception as e:
    print(f"{RED}{t['error'].format(e)}{RESET}")
    sys.exit(1)
