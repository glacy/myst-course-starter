
import os
import re

def migrate_content():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_dir = os.path.join(base_dir, 'sessions_BKP')
    target_dir = os.path.join(base_dir, 'sessions')
    
    # List all markdown files in source directory
    files = [f for f in os.listdir(source_dir) if f.endswith('.md')]
    
    for filename in files:
        source_path = os.path.join(source_dir, filename)
        target_path = os.path.join(target_dir, filename)
        
        if not os.path.exists(target_path):
            print(f"Skipping {filename}: Target file not found.")
            continue
            
        print(f"Processing {filename}...")
        
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                source_content = f.read()
                
            with open(target_path, 'r', encoding='utf-8') as f:
                target_content = f.read()
                
            # Extract content from source
            # Start after ::: {note} Objetivos ... :::
            start_marker = r':::\{note\} Objetivos\s*.*?\s*:::'
            match_start = re.search(start_marker, source_content, re.DOTALL)
            
            if not match_start:
                print(f"  Warning: Could not find 'Objetivos' block in {filename} source.")
                continue
                
            start_pos = match_start.end()
            
            # Find end position (Actividades, Ejercicios, Referencias, Evaluacion)
            # We look for the first occurrence of any of these headers
            end_markers = [
                r'\n#+\s+Actividades',
                r'\n#+\s+Ejercicios',
                r'\n#+\s+Referencias',
                r'\n#+\s+Evaluación'
            ]
            
            end_pos = len(source_content)
            for marker in end_markers:
                match_end = re.search(marker, source_content[start_pos:])
                if match_end:
                    current_end_pos = start_pos + match_end.start()
                    if current_end_pos < end_pos:
                        end_pos = current_end_pos
            
            extracted_content = source_content[start_pos:end_pos].strip()
            
            if not extracted_content:
                print(f"  Warning: No content extracted from {filename}.")
                continue
                
            # Insert into target
            # Find insertion point: after Objetivos block and before Actividades
            # Assuming target has Actividades header. If not, append before References or at end.
            
            target_start_marker = r':::\{note\} Objetivos\s*.*?\s*:::'
            target_match_start = re.search(target_start_marker, target_content, re.DOTALL)

            if not target_match_start:
                 print(f"  Warning: Could not find 'Objetivos' block in {filename} target.")
                 continue

            insertion_point = target_match_start.end()
            
            # Check if content is already there (heuristic check)
            # If the extracted starts with characters present right after insertion point, skip
            # But safer to just insert cleanly. 
            # We need to make sure we don't double insert.
            
            # Construct new content
            # Add some newlines for spacing
            new_content = target_content[:insertion_point] + "\n\n" + extracted_content + "\n\n" + target_content[insertion_point:]
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            print(f"  Successfully migrated content for {filename}.")
            
        except Exception as e:
            print(f"  Error processing {filename}: {e}")

if __name__ == "__main__":
    migrate_content()
