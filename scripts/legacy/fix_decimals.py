
import os
import re

def fix_decimals():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    examples_dir = os.path.join(base_dir, 'examples')
    exclude_files = ['07-biomecanica-brazo.md'] # User manually edited this
    
    files = [f for f in os.listdir(examples_dir) if f.endswith('.md') and f not in exclude_files]
    
    for filename in files:
        path = os.path.join(examples_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Strategy: Convert English (1,234.56) to Spanish (1.234,56)
        
        # 1. Protect thousands separators (comma followed by 3 digits)
        # We use a placeholder
        # Check for 1,234 (comma surrounded by digits, usually 3 after)
        # Be careful not to match 0,588 if that was intended as decimal, but in "English source" it shouldn't be.
        # In English source, 0,588 is not a number key unless it's a list "0, 588" (space)
        # or "Something 0,588" (unlikely)
        # Standard english thousand is 1,000. 
        
        def replace_thousand(match):
            return match.group(1) + "||DOT||" + match.group(2)
            
        # Match digit, comma, 3 digits, NOT followed by another digit (to avoid matching inside longer sequences if any)
        # But 1,000,000 has multiple.
        # Simple approach: Replace comma between digits if followed by 3 digits?
        # Let's assume standard English usage in my generation.
        
        # Step 1: Comma to Placeholder (Thousands)
        # Regex: Digit + Comma + 3 Digits.
        # Iterate until no changes to handle 1,000,000
        content_step1 = re.sub(r'(\d),(\d{3})', replace_thousand, content)
        while content_step1 != content:
            content = content_step1
            content_step1 = re.sub(r'(\d),(\d{3})', replace_thousand, content)
            
        # Step 2: Dot to Comma (Decimal)
        # Regex: Digit + Dot + Digit
        content = re.sub(r'(\d)\.(\d)', r'\1,\2', content)
        
        # Step 3: Placeholder to Dot (Thousands)
        content = content.replace("||DOT||", ".")
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Processed {filename}")
        
if __name__ == "__main__":
    fix_decimals()
