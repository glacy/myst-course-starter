
import os
import yaml
import re

def generate_evaluations():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sessions_dir = os.path.join(base_dir, 'sessions')
    eval_dir = os.path.join(base_dir, 'evaluations')
    
    # Map for filenames based on session number
    # I'll generate filenames dynamically: XX-[type]-[keword].md
    # But I need keywords. I'll use a simple mapping or heuristics.
    # Simpler: just use the session number and type and a generic name if I can't extract a keyword, 
    # OR use the filenames I proposed in the plan.
    
    proposed_filenames = {
        '01': '01-formativa-conversion.md',
        '02': '02-sumativa-quiz.md',
        '03': '03-formativa-vectores.md',
        '04': '04-formativa-dcl.md',
        '05': '05-sumativa-informe-centrifugacion.md',
        '06': '06-sumativa-problemario-energia.md',
        '07': '07-formativa-caso-ergonomia.md',
        '08': '08-formativa-densidad.md',
        '09': '09-sumativa-proyecto-biorreactor.md',
        '10': '10-sumativa-reporte-viscosidad.md',
        '11': '11-formativa-exposicion-reynolds.md',
        '12': '12-formativa-problemas-electrostatica.md',
        '13': '13-sumativa-taller-circuitos.md',
        '14': '14-formativa-mapa-magnetismo.md',
        '15': '15-sumativa-cuestionario-espectroscopia.md',
        '16': '16-sumativa-proyecto-final.md'
    }

    files = sorted([f for f in os.listdir(sessions_dir) if f.endswith('.md')])
    
    for filename in files:
        session_num = filename[:2]
        path = os.path.join(sessions_dir, filename)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1))
                evaluations = frontmatter.get('evaluation', [])
                # Handle list or single dict
                if isinstance(evaluations, list) and evaluations:
                    ev = evaluations[0]
                elif isinstance(evaluations, dict):
                    ev = evaluations
                else:
                    print(f"Skipping {filename}: No valid evaluation found.")
                    continue
                    
                etype = ev.get('type', 'Unknown')
                desc = ev.get('description', 'Actividad de evaluación.')
                
                target_filename = proposed_filenames.get(session_num, f"{session_num}-evaluacion.md")
                target_path = os.path.join(eval_dir, target_filename)
                
                # Create content
                md_content = f"""---
title: "Evaluación Sesión {session_num}"
type: {etype}
---

# {etype}: {desc}

**Sesión:** {session_num}
**Tipo:** {etype}

## 📝 Descripción
{desc}

## 🎯 Objetivos de Evaluación
*   Verificar la comprensión de los conceptos clave de la sesión.
*   Aplicar los conocimientos a situaciones prácticas de biotecnología.

## 📄 Instrucciones
1.  Lea detenidamente el enunciado.
2.  Resuelva los problemas o desarrolle el tema solicitado.
3.  Entregue su respuesta en el formato indicado.

---
"""
                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                print(f"Generated {target_filename}")
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    generate_evaluations()
