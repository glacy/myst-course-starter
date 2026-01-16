import glob
import re
import yaml
import os

import argparse

# Translations configuration
TRANSLATIONS = {
    'es': {
        'type': 'Tipo',
        'duration': 'Duración',
        'modality': 'Modalidad',
        'difficulty': 'Dificultad'
    },
    'en': {
        'type': 'Type',
        'duration': 'Duration',
        'modality': 'Modality',
        'difficulty': 'Difficulty'
    },
    'fr': {
        'type': 'Type',
        'duration': 'Durée',
        'modality': 'Modalité',
        'difficulty': 'Difficulté'
    }
}

def generate_badges(activity_data, lang='es'):
    """
    Generates markdown image badges based on activity metadata.
    """
    badges = []
    t = TRANSLATIONS.get(lang, TRANSLATIONS['es'])
    
    # Mapping keys to colors and labels
    # shielding.io format: label-message-color
    
    if 'type' in activity_data:
        val = str(activity_data['type']).replace('-', '--').replace(' ', '_')
        badges.append(f"![](https://img.shields.io/badge/{t['type']}-{val}-orange)")
        
    if 'duration' in activity_data:
        val = str(activity_data['duration']).replace('-', '--').replace(' ', '_')
        badges.append(f"![](https://img.shields.io/badge/{t['duration']}-{val}-yellow)")
        
    if 'modality' in activity_data:
        val = str(activity_data['modality']).replace('-', '--').replace(' ', '_')
        badges.append(f"![](https://img.shields.io/badge/{t['modality']}-{val}-blue)")
        
    if 'difficulty' in activity_data:
        val = str(activity_data['difficulty']).replace('-', '--').replace(' ', '_')
        color = 'green'
        if val.lower() in ['intermedio', 'intermediate']:
            color = 'yellow'
        elif val.lower() in ['avanzado', 'advanced', 'dificil']:
            color = 'red'
        badges.append(f"![](https://img.shields.io/badge/{t['difficulty']}-{val}-{color})")

    return " ".join(badges)

def process_file(filepath, lang='es'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to extract frontmatter
    # Matches starting ---, content, ending ---
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    
    if not match:
        print(f"Skipping {filepath}: No frontmatter found.")
        return

    frontmatter_raw = match.group(1)
    try:
        data = yaml.safe_load(frontmatter_raw)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML in {filepath}: {e}")
        return
    
    # Fallback: check if we have data in top level (simpler frontmatter) matches what generate_activities producs
    # generate_activities produces flat frontmatter: title, duration, modality, difficulty. 
    # The original script expected 'activity' key nested. 
    # Let's support both: direct keys or nested 'activity' dict.
    
    activity_data = {}
    if 'activity' in data:
        activity_data = data['activity']
    else:
        # Check for specific keys in root
        keys = ['type', 'duration', 'modality', 'difficulty']
        if any(k in data for k in keys):
            activity_data = {k: data[k] for k in keys if k in data}
    
    if not activity_data:
         # print(f"Skipping {filepath}: No activity metadata found.")
         # Silent skip to avoid noise on non-activity files if any
         return

    badges_line = generate_badges(activity_data, lang=lang)
    
    # Construct the marker line
    marker = "<!-- ACTIVITY-BADGES -->"
    new_badges_block = f"{marker}\n{badges_line}\n{marker}"

    # Check if we already have badges to replace
    # We look for the block between markers
    pattern = re.compile(f"{re.escape(marker)}.*?{re.escape(marker)}", re.DOTALL)
    
    if pattern.search(content):
        # Update existing badges
        new_content = pattern.sub(new_badges_block, content)
        action = "Updated"
    else:
        # Insert after frontmatter
        # match.end() gives the index after the closing ---
        # We want to insert strictly after the matches end index, which includes the newline
        end_index = match.end()
        new_content = content[:end_index] + "\n" + new_badges_block + "\n" + content[end_index:]
        action = "Injected"

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"{action} badges in {filepath}")
    else:
        print(f"No changes needed for {filepath}")

def main():
    parser = argparse.ArgumentParser(description='Inject badges into activity files.')
    parser.add_argument('--lang', default='es', choices=['es', 'en', 'fr'], help='Language for badge labels')
    args = parser.parse_args()
    
    files = sorted(glob.glob("activities/*.md"))
    print(f"Found {len(files)} activity files. Language: {args.lang}")
    for f in files:
        process_file(f, lang=args.lang)

if __name__ == "__main__":
    main()
