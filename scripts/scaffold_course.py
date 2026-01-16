#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
from pathlib import Path

def run_step(description, command, check=True):
    """Runs a command and prints a status description."""
    print(f"\n🚀 {description}...")
    try:
        subprocess.run(command, check=check, text=True)
        print(f"✅ {description} completed.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during: {description}")
        print(f"   Command: {' '.join(command)}")
        sys.exit(e.returncode)

def main():
    parser = argparse.ArgumentParser(
        description="Scaffold the course structure from planeamiento.json"
    )
    parser.add_argument(
        "--force", 
        action="store_true", 
        help="Force overwrite of existing files (passed to generate_sessions.py)"
    )
    parser.add_argument(
        "--lang",
        default="en",
        choices=["es", "en", "fr"],
        help="Language for generated content (default: en)"
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Automatically answer 'yes' to confirmation prompts"
    )
    
    args = parser.parse_args()
    
    # Ensure planeamiento.json exists
    if not Path("planeamiento.json").exists():
        print("❌ planeamiento.json not found in the root directory.")
        sys.exit(1)
    # Translations
    TRANSLATIONS = {
        'es': {
            'week': 'Semana',
            'success': '🎉 ¡Andamiaje del curso completado con éxito!',
            'run_hint': "   Ejecuta 'myst start' para previsualizar el curso.",
            'warning': "⚠️  ADVERTENCIA: Estás a punto de SOBREESCRIBIR todos los archivos generados (sesiones, actividades, programa).",
            'confirm': "¿Estás seguro de que deseas continuar? [y/N]: ",
            'abort': "❌ Operación cancelada por el usuario."
        },
        'en': {
            'week': 'Week',
            'success': '🎉 Course scaffolding completed successfully!',
            'run_hint': "   Run 'myst start' to preview the course.",
            'warning': "⚠️  WARNING: You are about to OVERWRITE all generated files (sessions, activities, program).",
            'confirm': "Are you sure you want to proceed? [y/N]: ",
            'abort': "❌ Operation cancelled by user."
        },
        'fr': {
            'week': 'Semaine',
            'success': '🎉 Échafaudage du cours terminé avec succès !',
            'run_hint': "   Exécutez 'myst start' pour prévisualiser le cours.",
            'warning': "⚠️  ATTENTION : Vous êtes sur le point d'ÉCRASER tous les fichiers générés (séances, activités, programme).",
            'confirm': "Êtes-vous sûr de vouloir continuer ? [y/N] : ",
            'abort': "❌ Opération annulée par l'utilisateur."
        }
    }
    
    # Check for force flag with interactive confirmation
    if args.force:
        t_warn = TRANSLATIONS.get(args.lang, TRANSLATIONS['es'])
        print(f"\n{t_warn['warning']}")
        if args.yes:
             print(f"{t_warn['confirm']} y (auto-confirmed)")
        else:
            response = input(f"{t_warn['confirm']}").strip().lower()
            if response != 'y':
                print(f"{t_warn['abort']}")
                sys.exit(0)
    
    print("🏗️  Starting course scaffolding process...")
    print(f"   Language: {args.lang}")
    print(f"   Force overwrite: {args.force}")

    # 0. Ensure myst.yml exists
    if not Path("myst.yml").exists():
        print("\n🚀 Creating default myst.yml...")
        
        # Try to read metadata from planeamiento.json
        import json
        
        # Add scripts dir to path to import generate_activities
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        try:
            from generate_activities import generate_filename
        except ImportError:
            # Fallback if running from proper context or issues
            try:
                from generate_activities import generate_filename
            except ImportError:
                print("⚠️ Could not import generate_filename. Activities won't be in TOC.")
                generate_filename = None

        default_title = "Course Title"
        default_subtitle = "Course Subtitle"
        default_author = "Author Name"
        toc_content = "  toc:\n    - file: programa.md\n"
        
        try:
            with open("planeamiento.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                metadata = data.get("metadata", {})
                default_title = metadata.get("title", default_title)
                default_subtitle = metadata.get("semester", default_subtitle)
                authors = metadata.get("authors", [])
                if isinstance(authors, list) and authors:
                     default_author = authors[0]
                elif isinstance(authors, str):
                     default_author = authors
                
                # Build TOC from weeks
                weeks = data.get('weeks', [])
                week_label = TRANSLATIONS.get(args.lang, TRANSLATIONS['es'])['week']
                
                if weeks:
                    for w in weeks:
                        week_num = w.get('week')
                        # Use a placeholder filename that update_toc.py will recognize (XX-*.md)
                        # We use 'session' as a generic name, update_toc will fix it to the real filename
                        toc_content += f"    - title: {week_label} {week_num}\n"
                        toc_content += f"      children:\n"
                        toc_content += f"      - file: sessions/{int(week_num):02d}-session.md\n"
                        
                        # Add Activities
                        if generate_filename:
                            raw_activities = w.get('activities')
                            if raw_activities:
                                act_list = []
                                if isinstance(raw_activities, str):
                                    act_list.append(raw_activities)
                                elif isinstance(raw_activities, list):
                                    act_list = raw_activities
                                
                                for act_desc in act_list:
                                    act_filename = generate_filename(week_num, act_desc)
                                    toc_content += f"      - file: activities/{act_filename}\n"
                                    toc_content += f"        hidden: true\n"


        except Exception as e:
            print(f"⚠️  Could not read metadata from planeamiento.json: {e}")

        default_myst = f"""version: 1
project:
  id: myst-course-starter
  title: {default_title}
  subtitle: {default_subtitle}
  authors:
    - name: {default_author}
  github: https://github.com/glacy/myst-course-starter
{toc_content}site:
  template: book-theme
  options:
    logo: assets/site_logo.svg
    logo_dark: assets/site_logo_dark.svg
  title: {default_title}
  subtitle: {default_subtitle}
  actions:
    - title: GitHub
      url: https://github.com/glacy/myst-course-starter
      icon: github
"""
        with open("myst.yml", "w") as f:
            f.write(default_myst)
        print("✅ Created myst.yml")
    
    # 0.5 Ensure programa.md exists
    prog_cmd = ["python3", "scripts/generate_program.py", "--lang", args.lang]
    if not args.force:
        prog_cmd.append("--init")
    run_step("Generating programa.md", prog_cmd)
    
    # 1. Create Directory Structure
    directories = ["sessions", "activities", "examples", "exercises", "assets"]
    print("\n🚀 Verifying directory structure...")
    for d in directories:
        p = Path(d)
        if not p.exists():
            p.mkdir(parents=True)
            print(f"   Created directory: {d}/")
        else:
            print(f"   Directory exists: {d}/")
    print("✅ Directory structure verification completed.")

    # 2. Sync Myst Metadata
    run_step("Synchronizing myst.yml metadata", ["python3", "scripts/sync_myst.py"])

    # 2. Generate Sessions
    gen_cmd = ["python3", "scripts/generate_sessions.py", "--lang", args.lang]
    if args.force:
        gen_cmd.append("--force")
    run_step("Generating session files", gen_cmd)

    # 3. Update Table of Contents
    run_step("Updating Table of Contents (TOC)", ["python3", "scripts/update_toc.py"])

    # 4. Generate Activities
    act_cmd = ["python3", "scripts/generate_activities.py", "--lang", args.lang]
    if args.force:
        act_cmd.append("--force")
    run_step("Generating activity skeletons", act_cmd)

    # 5. Inject Activity Headers
    run_step("Injecting activity badges", ["python3", "scripts/inject_activity_header.py", "--lang", args.lang])

    # 5. Generate Sessions Table
    run_step("Generating sessions table", ["python3", "scripts/generate_sessions_table_json.py", "--lang", args.lang])

    t = TRANSLATIONS.get(args.lang, TRANSLATIONS['es'])
    print(f"\n{t['success']}")
    print(t['run_hint'])

if __name__ == "__main__":
    main()
