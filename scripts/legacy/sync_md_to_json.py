import glob
import yaml
import json
import re
from typing import Dict, Any, List

def main() -> None:
    """
    Synchronizes learning objectives from session markdown files to the planeamiento.json file.

    This script performs the following steps:
    1. Loads the existing `planeamiento.json` file.
    2. Iterates through all markdown files in the `sessions/` directory.
    3. Extracts the YAML frontmatter from each markdown file.
    4. Identifies the week number and learning objectives.
    5. Updates the corresponding week in the JSON data with the found objectives.
    6. Saves the updated data back to `planeamiento.json`.
    """
    json_path = 'planeamiento.json'
    
    # Load existing JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data: List[Dict[str, Any]] = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_path} not found. Please ensure the file exists in the root directory.")
        return
    except json.JSONDecodeError:
        print(f"Error: Failed to decode {json_path}. Please check if the file contains valid JSON.")
        return

    # Map week to index for faster lookup
    # Assuming 'week' is a unique identifier for each item in the list
    week_map: Dict[int, Dict[str, Any]] = {item['week']: item for item in data if 'week' in item}

    # Find all session markdown files
    files = sorted(glob.glob("sessions/*.md"))
    
    updates_count = 0

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract YAML frontmatter
            match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
            if match:
                fm = yaml.safe_load(match.group(1))
                if not fm:
                    continue

                # Get session number (week) and objectives
                week = fm.get('session', {}).get('number')
                objectives = fm.get('learning_objectives', [])
                
                if week and week in week_map:
                    # Update objectives in JSON if they exist in the markdown
                    if objectives:
                        week_map[week]['objectives'] = objectives
                        print(f"Synced Week {week}: Found {len(objectives)} objectives in {file_path}")
                        updates_count += 1
        except Exception as e:
            print(f"Warning: Failed to process {file_path}: {e}")

    # Save updated JSON
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {json_path}. Modified {updates_count} entries.")
    except Exception as e:
        print(f"Error: Failed to write to {json_path}: {e}")

if __name__ == "__main__":
    main()
