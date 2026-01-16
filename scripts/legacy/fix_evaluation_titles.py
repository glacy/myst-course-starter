
import os
import re

def fix_titles():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    eval_dir = os.path.join(base_dir, 'evaluations')
    files = [f for f in os.listdir(eval_dir) if f.endswith('.md')]
    
    for filename in files:
        path = os.path.join(eval_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace 'title: "Evaluación Sesión' with 'title: "Evaluación Semana'
        # Be careful not to replace body text 'Sesión: 01' if user didn't ask, 
        # but user specifically said "en el campo `title` del frontmatter".
        
        # Regex for frontmatter title
        new_content = re.sub(r'^(title:\s*"Evaluación )Sesión', r'\1Semana', content, flags=re.MULTILINE)
        
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")

if __name__ == "__main__":
    fix_titles()
