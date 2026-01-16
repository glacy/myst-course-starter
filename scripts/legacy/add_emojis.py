
import os
import re

def add_emojis():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, 'sessions')
    files = [f for f in os.listdir(target_dir) if f.endswith('.md')]
    
    replacements = [
        (r'^##\s+Actividades', '## 🧪 Actividades'),
        (r'^##\s+Evaluación', '## 📝 Evaluación'),
        (r'^##\s+Referencias', '## 📚 Referencias'),
    ]
    
    for filename in files:
        path = os.path.join(target_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        for pattern, replacement in replacements:
            # Check if emoji is already there to avoid double emoji
            # We assume if the header already has an emoji it might not match exactly "## Actividades" 
            # but usually it's "## 🧪 Actividades".
            # My regex `^##\s+Actividades` checks for strict start, so "## 🧪 Actividades" won't match, which is good.
            # But what if there are trailing spaces?
            
            new_content = re.sub(pattern, replacement, new_content, flags=re.MULTILINE)
            
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")
        else:
            print(f"No changes for {filename}")

if __name__ == "__main__":
    add_emojis()
