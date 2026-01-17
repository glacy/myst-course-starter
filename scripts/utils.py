"""
Shared utilities and configuration for course scaffolding scripts.

Centralizes JSON loading, filename generation, translations and output paths.
"""

import json
import os
import re
import unicodedata
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

# Constants
JSON_FILE = 'planeamiento.json'
OUTPUT_DIR_SESSIONS = 'sessions'
OUTPUT_DIR_ACTIVITIES = 'activities'
OUTPUT_DIR_EXAMPLES = 'examples'
OUTPUT_DIR_EXERCISES = 'exercises'
OUTPUT_DIR_ASSETS = 'assets'
MYST_CONFIG_FILE = 'myst.yml'

# Translations
TRANSLATIONS = {
    'es': {
        # General
        'week': 'Semana',
        'session': 'Sesión',
        'success': '🎉 ¡Andamiaje del curso completado con éxito!',
        'run_hint': "   Ejecuta 'myst start' para previsualizar el curso.",
        'warning': "⚠️  ADVERTENCIA: Estás a punto de SOBREESCRIBIR todos los archivos generados (sesiones, actividades, programa).",
        'confirm': "¿Estás seguro de que deseas continuar? [y/N]: ",
        'abort': "❌ Operación cancelada por el usuario.",
        
        # Sessions
        'modality': 'Presencial',
        'objectives': 'Objetivos',
        'objectives_intro': 'Al completar esta lección, serás capaz de:',
        'activities': 'Actividades',
        'evaluation': 'Evaluación',
        'references': 'Referencias',
        
        # Activities
        'description': 'Descripción',
        'materials': 'Materiales',
        'instructions': 'Instrucciones',
        'default_objective': '[Definir objetivo específico de la actividad]',
        'default_material': '[Lista de materiales]',
        'step': 'Paso',
        'difficulty': 'Fundamental'
    },
    'en': {
        # General
        'week': 'Week',
        'session': 'Session',
        'success': '🎉 Course scaffolding completed successfully!',
        'run_hint': "   Run 'myst start' to preview the course.",
        'warning': "⚠️  WARNING: You are about to OVERWRITE all generated files (sessions, activities, program).",
        'confirm': "Are you sure you want to proceed? [y/N]: ",
        'abort': "❌ Operation cancelled by user.",
        
        # Sessions
        'modality': 'In-person',
        'objectives': 'Objectives',
        'objectives_intro': 'Upon completing this lesson, you will be able to:',
        'activities': 'Activities',
        'evaluation': 'Evaluation',
        'references': 'References',
        
        # Activities
        'description': 'Description',
        'materials': 'Materials',
        'instructions': 'Instructions',
        'default_objective': '[Define specific activity objective]',
        'default_material': '[List of materials]',
        'step': 'Step',
        'difficulty': 'Fundamental'
    },
    'fr': {
        # General
        'week': 'Semaine',
        'session': 'Séance',
        'success': '🎉 Échafaudage du cours terminé avec succès !',
        'run_hint': "   Exécutez 'myst start' pour prévisualiser le cours.",
        'warning': "⚠️  ATTENTION : Vous êtes sur le point d'ÉCRASER tous les fichiers générés (séances, activités, programme).",
        'confirm': "Êtes-vous sûr de vouloir continuer ? [y/N] : ",
        'abort': "❌ Opération annulée par l'utilisateur.",
        
        # Sessions
        'modality': 'Présentiel',
        'objectives': 'Objectifs',
        'objectives_intro': 'En complétant cette leçon, vous serez capable de :',
        'activities': 'Activités',
        'evaluation': 'Évaluation',
        'references': 'Références',
        
        # Activities
        'description': 'Description',
        'materials': 'Matériel',
        'instructions': 'Instructions',
        'default_objective': '[Définir l\'objectif spécifique de l\'activité]',
        'default_material': '[Liste du matériel]',
        'step': 'Étape',
        'difficulty': 'Fondamental'
    }
}

def load_json(filepath: str = JSON_FILE) -> Dict[str, Any]:
    """Reads and parses the JSON configuration file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Normalize structure: ensure we return a dict with 'weeks' and 'metadata'
    if isinstance(data, list):
        return {'weeks': data, 'metadata': {}}
    elif isinstance(data, dict):
        if 'weeks' not in data and 'metadata' not in data:
            # Maybe it's just the list inside a dict? unlikely based on code but safe fallback
             return {'weeks': [], 'metadata': {}}
        return data
    else:
        raise ValueError("Invalid JSON format")

def generate_filename(prefix: Union[int, str], title: str) -> str:
    """
    Generates a web-safe filename.
    
    Args:
        prefix (int|str): The week number or prefix.
        title (str): The content title or description.
        
    Returns:
        str: Filename like '01-slug-title.md'.
    """
    # Normalize unicode characters
    normalized = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('ascii')
    
    # Sanitize
    safe_slug = re.sub(r'[^\w\s-]', '', normalized).strip().lower()
    safe_slug = re.sub(r'[-\s]+', '-', safe_slug)
    
    # If title is very long (e.g. from description), truncate it
    # We use a heuristic: if it looks like a description (many words), truncate
    if len(safe_slug) > 50:
         safe_slug = "-".join(safe_slug.split('-')[:6])
    
    try:
        prefix_int = int(prefix)
        return f"{prefix_int:02d}-{safe_slug}.md"
    except ValueError:
        return f"{prefix}-{safe_slug}.md"

def get_translation(lang: str, key: str) -> str:
    """Retrieves a translation for a given key and language."""
    return TRANSLATIONS.get(lang, TRANSLATIONS['es']).get(key, key)

def save_yaml(filepath: str, data: Any) -> None:
    """Saves data to a YAML file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

def ensure_directory(path: str) -> None:
    """Creates a directory if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)
