
import os
import yaml
import re

def extract_evaluations():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sessions_dir = os.path.join(base_dir, 'sessions')
    files = sorted([f for f in os.listdir(sessions_dir) if f.endswith('.md')])
    
    print("| Session | Type | Description |")
    print("|---|---|---|")
    
    for filename in files:
        path = os.path.join(sessions_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract YAML frontmatter
        match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1))
                evaluations = frontmatter.get('evaluation', [])
                if isinstance(evaluations, list):
                    for ev in evaluations:
                        etype = ev.get('type', 'Unknown')
                        desc = ev.get('description', 'No description')
                        print(f"| {filename[:2]} | {etype} | {desc} |")
                else:
                     print(f"| {filename[:2]} | Unknown | {evaluations} |")
            except Exception as e:
                print(f"| {filename[:2]} | Error | {e} |")

if __name__ == "__main__":
    extract_evaluations()
