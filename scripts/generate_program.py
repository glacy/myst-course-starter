import argparse
import json
import os
import yaml

# Translations
TRANSLATIONS = {
    'es': {
        'university': 'Universidad',
        'code': 'Código',
        'semester': 'Semestre',
        'description': 'Descripción del Curso',
        'objectives': 'Objetivos Generales',
        'methodology': 'Metodología',
        'evaluation': 'Evaluación',
        'schedule': 'Cronograma',
        'placeholder_objectives': 'Los objetivos generales del curso se detallarán aquí.',
        'placeholder_methodology': 'La metodología del curso se describirá aquí.',
        'placeholder_evaluation': 'Las reglas de evaluación se detallarán aquí.',
        'generated_by': 'Generado automáticamente a partir de planeamiento.json'
    },
    'en': {
        'university': 'University',
        'code': 'Code',
        'semester': 'Semester',
        'description': 'Course Description',
        'objectives': 'General Objectives',
        'methodology': 'Methodology',
        'evaluation': 'Evaluation',
        'schedule': 'Schedule',
        'placeholder_objectives': 'General course objectives will be detailed here.',
        'placeholder_methodology': 'Course methodology will be described here.',
        'placeholder_evaluation': 'Evaluation rules will be detailed here.',
        'generated_by': 'Automatically generated from planeamiento.json'
    },
    'fr': {
        'university': 'Université',
        'code': 'Code',
        'semester': 'Semestre',
        'description': 'Description du Cours',
        'objectives': 'Objectifs Généraux',
        'methodology': 'Méthodologie',
        'evaluation': 'Évaluation',
        'schedule': 'Calendrier',
        'placeholder_objectives': 'Les objectifs généraux du cours seront détaillés ici.',
        'placeholder_methodology': 'La méthodologie du cours sera décrite ici.',
        'placeholder_evaluation': 'Les règles d\'évaluation seront détaillées ici.',
        'generated_by': 'Généré automatiquement à partir de planeamiento.json'
    }

}

def main():
    parser = argparse.ArgumentParser(description='Generate programa.md from planeamiento.json')
    parser.add_argument('--lang', default='es', choices=['es', 'en', 'fr'], help='Language for headers')
    parser.add_argument('--init', action='store_true', help='Only create if missing (do not overwrite)')
    args = parser.parse_args()
    
    output_file = 'programa.md'
    if args.init and os.path.exists(output_file):
        print(f"Skipping {output_file}: already exists (and --init flag used).")
        return

    t = TRANSLATIONS.get(args.lang, TRANSLATIONS['es'])
    
    try:
        with open('planeamiento.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
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

    # Build Content
    md_content = f"""---
title: {title}
subtitle: {semester}
author: {author_name}
---

# {title}

|  |  |
| :--- | :--- |
| **{t['university']}** | {university} |
| **{t['code']}** | {code} |
| **{t['semester']}** | {semester} |

## 📝 {t['description']}

{description}

## 🎯 {t['objectives']}

{t['placeholder_objectives']}

## 🧠 {t['methodology']}

{t['placeholder_methodology']}

## 📊 {t['evaluation']}

{t['placeholder_evaluation']}

## 📅 {t['schedule']}

"""
    # Append simple schedule from weeks
    if weeks:
        md_content += "| " + t['code'].replace('Code','Week').replace('Código', 'Semana').replace('Code', 'Semaine') + " | Title | Content |\n"
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

if __name__ == "__main__":
    main()
