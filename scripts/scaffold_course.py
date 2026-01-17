#!/usr/bin/env python3
"""
End-to-end course scaffolding orchestrator.

Reads planeamiento.json and coordinates all generator scripts to produce a
fully configured MyST course (myst.yml, programa.md, sessions, activities).
"""

import argparse
import sys
import os
from pathlib import Path

# Add local directory to path to allow imports if running directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils import (
        load_json, generate_filename, TRANSLATIONS, save_yaml,
        OUTPUT_DIR_SESSIONS, OUTPUT_DIR_ACTIVITIES, OUTPUT_DIR_EXAMPLES,
        OUTPUT_DIR_EXERCISES, OUTPUT_DIR_ASSETS, MYST_CONFIG_FILE
    )
    import generate_sessions
    import generate_activities
    import generate_program
    import sync_myst
    import update_toc
    import inject_activity_header
    import generate_sessions_table_json
except ImportError:
    # Fallback for when running from root
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
    from utils import (
        load_json, generate_filename, TRANSLATIONS, save_yaml,
        OUTPUT_DIR_SESSIONS, OUTPUT_DIR_ACTIVITIES, OUTPUT_DIR_EXAMPLES,
        OUTPUT_DIR_EXERCISES, OUTPUT_DIR_ASSETS, MYST_CONFIG_FILE
    )
    import generate_sessions
    import generate_activities
    import generate_program
    import sync_myst
    import update_toc
    import inject_activity_header
    import generate_sessions_table_json

def create_myst_config(lang: str):
    """Creates the myst.yml configuration file."""
    if Path(MYST_CONFIG_FILE).exists():
        return

    print("\n🚀 Creating default myst.yml...")
    
    t = TRANSLATIONS.get(lang, TRANSLATIONS['es'])
    default_title = "Course Title"
    default_subtitle = "Course Subtitle"
    default_author = "Author Name"
    
    try:
        data = load_json()
        metadata = data.get("metadata", {})
        default_title = metadata.get("title", default_title)
        default_subtitle = metadata.get("semester", default_subtitle)
        authors = metadata.get("authors", [])
        if isinstance(authors, list) and authors:
             default_author = authors[0]
        elif isinstance(authors, str):
             default_author = authors
        
        # Build TOC
        toc_entries = [{'file': 'programa.md'}]
        weeks = data.get('weeks', [])
        week_label = t['week']
        
        if weeks:
            for w in weeks:
                week_num = w.get('week')
                if not week_num: continue
                
                week_entry = {
                    'title': f"{week_label} {week_num}",
                    'children': [
                        {'file': f"sessions/{int(week_num):02d}-session.md"}
                    ]
                }
                
                # Add Activities
                raw_activities = w.get('activities')
                if raw_activities:
                    act_list = []
                    if isinstance(raw_activities, str):
                        act_list.append(raw_activities)
                    elif isinstance(raw_activities, list):
                        act_list = raw_activities
                    
                    for act_desc in act_list:
                        act_filename = generate_filename(week_num, act_desc)
                        week_entry['children'].append({
                            'file': f"activities/{act_filename}",
                            'hidden': True
                        })
                
                toc_entries.append(week_entry)

    except Exception as e:
        print(f"⚠️  Could not read metadata from planeamiento.json: {e}")
        toc_entries = [{'file': 'programa.md'}]

    myst_config = {
        'version': 1,
        'project': {
            'id': 'myst-course-starter',
            'title': default_title,
            'subtitle': default_subtitle,
            'authors': [{'name': default_author}],
            'github': 'https://github.com/glacy/myst-course-starter',
            'toc': toc_entries
        },
        'site': {
            'template': 'book-theme',
            'options': {
                'logo': 'assets/site_logo.svg',
                'logo_dark': 'assets/site_logo_dark.svg'
            },
            'title': default_title,
            'subtitle': default_subtitle,
            'actions': [
                {
                    'title': 'GitHub',
                    'url': 'https://github.com/glacy/myst-course-starter',
                    'icon': 'github'
                }
            ]
        }
    }
    
    save_yaml(MYST_CONFIG_FILE, myst_config)
    print("✅ Created myst.yml")

def main():
    parser = argparse.ArgumentParser(
        description="Scaffold the course structure from planeamiento.json"
    )
    parser.add_argument(
        "--force", 
        action="store_true", 
        help="Force overwrite of existing files"
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
    
    t = TRANSLATIONS.get(args.lang, TRANSLATIONS['es'])
    
    # Check for force flag with interactive confirmation
    if args.force:
        print(f"\n{t['warning']}")
        if args.yes:
             print(f"{t['confirm']} y (auto-confirmed)")
        else:
            response = input(f"{t['confirm']}").strip().lower()
            if response != 'y':
                print(f"{t['abort']}")
                sys.exit(0)
    
    print("🏗️  Starting course scaffolding process...")
    print(f"   Language: {args.lang}")
    print(f"   Force overwrite: {args.force}")

    # 0. Ensure myst.yml exists
    create_myst_config(args.lang)
    
    # 0.5 Ensure programa.md exists
    print("\n🚀 Generating programa.md...")
    generate_program.run(lang=args.lang, init=not args.force)
    print("✅ programa.md verification completed.")
    
    # 1. Create Directory Structure
    directories = [OUTPUT_DIR_SESSIONS, OUTPUT_DIR_ACTIVITIES, OUTPUT_DIR_EXAMPLES, OUTPUT_DIR_EXERCISES, OUTPUT_DIR_ASSETS]
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
    print("\n🚀 Synchronizing myst.yml metadata...")
    sync_myst.main()
    print("✅ myst.yml synchronized.")

    # 2. Generate Sessions
    print("\n🚀 Generating session files...")
    generate_sessions.run(lang=args.lang, force=args.force)
    print("✅ Session files generated.")

    # 3. Update Table of Contents
    print("\n🚀 Updating Table of Contents (TOC)...")
    update_toc.main()
    print("✅ TOC updated.")

    # 4. Generate Activities
    print("\n🚀 Generating activity skeletons...")
    generate_activities.run(lang=args.lang, force=args.force)
    print("✅ Activity skeletons generated.")

    # 5. Inject Activity Headers
    print("\n🚀 Injecting activity badges...")
    inject_activity_header.run(lang=args.lang)
    print("✅ Activity badges injected.")

    # 5. Generate Sessions Table
    print("\n🚀 Generating sessions table...")
    generate_sessions_table_json.run(lang=args.lang)
    print("✅ Sessions table generated.")

    print(f"\n{t['success']}")
    print(t['run_hint'])

if __name__ == "__main__":
    main()
