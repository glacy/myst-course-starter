
"""
Update session subtitles based on a predefined mapping related to their content.
"""

import os
import re

SESSIONS_DIR = "/home/glacy/biotec/sessions"

# Mapping based on filename prefix
SUBTITLE_MAP = {
    "01": "Sistema Internacional de Unidades",
    "02": "Desplazamiento, velocidad y aceleración",
    "03": "Vectores y definición de fuerza",
    "04": "Leyes de Newton y diagramas de cuerpo libre",
    "05": "Cinemática rotacional y movimiento circular",
    "06": "Trabajo, energía mecánica y potencia",
    "07": "Equilibrio de cuerpos rígidos",
    "08": "Densidad, presión y principio de Arquímedes",
    "09": "Ecuación de Bernoulli y fluido ideal",
    "10": "Viscosidad y ley de Poiseuille",
    "11": "Número de Reynolds y fuerza de arrastre",
    "12": "Carga eléctrica y ley de Coulomb",
    "13": "Circuitos eléctricos y potencial de membrana",
    "14": "Campos magnéticos y biomagnetismo",
    "15": "Reflexión, refracción y espectroscopía",
    "16": "Instrumentos ópticos y resolución"
}

def update_subtitle(filepath, new_subtitle):
    with open(filepath, "r") as f:
        content = f.read()

    # Regex to find subtitle field
    pattern = r"^(subtitle:).*?$"
    
    # Check if subtitle exists
    if re.search(pattern, content, re.MULTILINE):
        # Update existing
        # We need to quote the subtitle if it contains colons or special chars used in YAML, 
        # but for these simple strings it should be fine. 
        # Just in case, let's wrap in quotes if likely needed, or just let it be.
        # "Desplazamiento, Velocidad..." is fine without quotes.
        new_content = re.sub(pattern, f"subtitle: {new_subtitle}", content, count=1, flags=re.MULTILINE)
    else:
        # Insert after title
        new_content = re.sub(r"^(title:.*?)$", f"\\1\nsubtitle: {new_subtitle}", content, count=1, flags=re.MULTILINE)

    if content != new_content:
        with open(filepath, "w") as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(filepath)} -> {new_subtitle}")
    else:
        print(f"No changes for {os.path.basename(filepath)}")

def main():
    print(f"Updating subtitles in {SESSIONS_DIR}...")
    for filename in sorted(os.listdir(SESSIONS_DIR)):
        if filename.endswith(".md") and filename[0].isdigit():
            prefix = filename[:2]
            if prefix in SUBTITLE_MAP:
                new_subtitle = SUBTITLE_MAP[prefix]
                full_path = os.path.join(SESSIONS_DIR, filename)
                update_subtitle(full_path, new_subtitle)
            else:
                print(f"Skipping {filename} (no mapping found)")

if __name__ == "__main__":
        main()
