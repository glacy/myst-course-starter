import os
import re

def hide_activities():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    myst_path = os.path.join(base_dir, 'myst.yml')
    
    with open(myst_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Check if this line is an activity file
        if re.search(r'^\s*-\s*file:\s*activities/', line):
            # Check if next line is already hidden
            # Be careful with index out of bounds
            if i + 1 < len(lines):
                next_line = lines[i+1]
                if 'hidden: true' in next_line:
                    # Already hidden, move on
                    pass
                else:
                    # Not hidden, insert hidden: true
                    # Use same indentation as the file line but with spaces instead of dash
                    # The file line is "      - file: ..."
                    # We want "        hidden: true"
                    # Indentation of "- file:" is usually 6 spaces.
                    # "      - file:" -> 6 spaces + "- file:"
                    # We want to align hidden with file key? No, MyST yaml format:
                    # - file: path
                    #   hidden: true
                    # So 2 extra spaces from the dash position?
                    
                    # line: "      - file: ..."
                    # Match whitespace before dash
                    match = re.search(r'^(\s*)-\s*file:', line)
                    if match:
                        indent = match.group(1) # "      "
                        # We need "      " + "  hidden: true" ?
                        # Actually, usually it is:
                        # - file: foo
                        #   hidden: true
                        # The 'h' lines up with 'f'.
                        # "- file" -> dash is at col X. 'f' is at col X+2.
                        # So 'hidden' should start at col X+2.
                        # Indent of line is match.group(1).
                        # We append "  hidden: true\n" directly?
                        # Wait, let's look at evaluations.
                        # "      - file: evaluations/..."
                        # "        hidden: true"
                        # "      " has 6 spaces.
                        # "        " has 8 spaces.
                        
                        insertion = f"{indent}  hidden: true\n"
                        new_lines.append(insertion)
            else:
                 # End of file case
                 match = re.search(r'^(\s*)-\s*file:', line)
                 if match:
                    indent = match.group(1)
                    insertion = f"{indent}  hidden: true\n"
                    new_lines.append(insertion)
        i += 1
        
    with open(myst_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Added hidden: true to activities.")

if __name__ == "__main__":
    hide_activities()
