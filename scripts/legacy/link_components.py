
import os
import re

def link_components():
    # Use relative path from script location to project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sessions_dir = os.path.join(base_dir, 'sessions')
    activities_dir = os.path.join(base_dir, 'activities')
    evaluations_dir = os.path.join(base_dir, 'evaluations')
    
    # 1. Map Session Num -> Activity Filename
    act_files = sorted([f for f in os.listdir(activities_dir) if f.endswith('.md')])
    act_map = {}
    for f in act_files:
        act_map[f[:2]] = f
        
    # 2. Map Session Num -> Evaluation Filename
    eval_files = sorted([f for f in os.listdir(evaluations_dir) if f.endswith('.md')])
    eval_map = {}
    for f in eval_files:
        eval_map[f[:2]] = f
        
    # 3. Process Sessions
    session_files = sorted([f for f in os.listdir(sessions_dir) if f.endswith('.md')])
    
    for filename in session_files:
        session_num = filename[:2]
        path = os.path.join(sessions_dir, filename)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        
        # Link Activity
        if session_num in act_map:
            act_file = act_map[session_num]
            link_text = f"\n\n👉 [Ir a la actividad](../activities/{act_file})"
            
            # Find Actividades header
            # We want to append the link at the end of the activities section, 
            # but before the next header (Evaluación or Referencias).
            
            # Logic: Find "## 🧪 Actividades"
            # Then find the next "## " header.
            # Compare indices.
            
            header_match = re.search(r'(## 🧪 Actividades)', content)
            if header_match:
                start_idx = header_match.end()
                
                # Find next header
                next_header = re.search(r'\n## ', content[start_idx:])
                
                if next_header:
                    insert_pos = start_idx + next_header.start()
                    # Check if link already exists to avoid dupes (simple check)
                    if act_file not in content[start_idx:insert_pos]:
                        content = content[:insert_pos] + link_text + "\n" + content[insert_pos:]
                        modified = True
                else:
                    # End of file? (Unlikely given Evaluations usually follows)
                    if act_file not in content[start_idx:]:
                         content = content + link_text + "\n"
                         modified = True

        # Re-read content or update logic indices could be tricky if we modify 'content'.
        # Since we modified 'content' string, we need to be careful with subsequent searches?
        # Python strings are immutable, 'content' is new. 
        # But 'header_match' for Evaluation needs to be run on the NEW content. Okay.
        
        # Link Evaluation
        if session_num in eval_map:
            eval_file = eval_map[session_num]
            link_text = f"\n\n👉 [Ir a la evaluación](../evaluations/{eval_file})"
             
            header_match = re.search(r'(## 📝 Evaluación)', content)
            if header_match:
                start_idx = header_match.end()
                # Find next header (Referencias)
                next_header = re.search(r'\n## ', content[start_idx:])
                
                if next_header:
                    insert_pos = start_idx + next_header.start()
                    if eval_file not in content[start_idx:insert_pos]:
                        content = content[:insert_pos] + link_text + "\n" + content[insert_pos:]
                        modified = True
                else:
                    # Likely Referencias is last, so this might be end of file or Referencias is after.
                    if eval_file not in content[start_idx:]:
                         content = content + link_text + "\n"
                         modified = True
                         
        if modified:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filename}")
            
if __name__ == "__main__":
    link_components()
