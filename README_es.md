[![deploy](https://github.com/glacy/myst-course-starter/actions/workflows/deploy.yml/badge.svg)](https://github.com/glacy/myst-course-starter/actions/workflows/deploy.yml)

**MyST Course Starter**

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/glacy/myst-course-starter)

🚀 **Sitio web oficial (Versión compilada):** [https://glacy.github.io/myst-course-starter](https://glacy.github.io/myst-course-starter)

---

## Acerca de este repositorio

Este software funciona como un **Motor Generador de Cursos** y está diseñado para servir como plantilla para crear cursos académicos utilizando [MyST Markdown](https://mystmd.org/).

Su función principal es desacoplar el **diseño instruccional** de la **implementación técnica**. Al definir la estructura de su curso en un solo archivo (`planeamiento.json`), este software automáticamente:

1.  **Andamia la estructura**: Genera la jerarquía de carpetas y los borradores en markdown para cada sesión/semana.
2.  **Sincroniza metadatos**: Actualiza la configuración del sitio, títulos y navegación.
3.  **Alimenta la UI**: Nutre el "Visor de Sílabo" interactivo basado en React para los estudiantes.

Es ideal para educadores que desean un enfoque de "Compliance-as-Code", asegurando que el sitio web del curso, la documentación y el visor para estudiantes siempre reflejen el último sílabo aprobado.

### Características Clave
- **Estructura semántica:** Impulsada por frontmatter YAML y esquemas JSON.
- **Reproducibilidad:** Entorno controlado con despliegue automatizado.
- **Documentación como Código:** Los cambios en el sílabo se rastrean vía git y se despliegan mediante CI/CD.

## Ejecución en la nube (recomendado)

La forma más sencilla de ejecutar este curso es utilizando **GitHub Codespaces**.
1. Haga clic en el botón "Open in GitHub Codespaces" de arriba.
2. Espere a que el entorno se construya (instalará automáticamente todas las dependencias).
3. Una vez lista la terminal, el entorno `frontmatter-academico` estará activo.

### Buenas prácticas (pre-commit)

Si clonas el repositorio localmente, se recomienda instalar los hooks de git para validación automática:

```bash
# Una vez activado el entorno conda
pre-commit install
```
Esto validará el frontmatter automáticamente al intentar hacer un commit.

> **Nota:** Si necesitas omitir estas validaciones en una emergencia:
> - **Omitir en un commit:** `git commit -n` (o `--no-verify`)
> - **Desinstalar hooks:** `pre-commit uninstall`
> - **Desactivar configuración:** Renombra el archivo: `mv .pre-commit-config.yaml .pre-commit-config.yaml.disabled`

## Estructura del proyecto

```text
myst-course-starter/
├── assets/                # 🎨 Recursos estáticos (logos, imágenes)
├── scripts/               # 🛠️ Scripts de mantenimiento y automatización
├── tests/                 # 🧪 Pruebas unitarias para los scripts
├── myst.yml               # ⚙️ Configuración del sitio y metadatos globales
├── programa.md            # 📄 Programa del curso
├── planeamiento.json      # 📋 Datos estructurados del planeamiento 
├── sessions/              # 📚 Contenido del curso (Capítulos)
├── examples/              # 🧩 Ejemplos de referencia
├── exercises/             # ✍️ Actividades prácticas
└── .github/               # 🤖 Flujos de automatización (CI/CD)
```

**Nota sobre la estructura de contenido:**
El curso sigue una arquitectura modular donde los contenidos prácticos no residen directamente en los archivos de sesión (`sessions/`), sino que se inyectan dinámicamente:
- **`examples/`**: Contiene ejemplos resueltos y casos de estudio.
- **`exercises/`**: Contiene los ejercicios propuestos, estructurados semánticamente mediante la directiva `{exercise}` de MyST.
Esta separación permite reutilizar componentes y facilita el mantenimiento.




## Reproducibilidad y configuración local

Para garantizar un entorno de desarrollo consistente, este proyecto utiliza Anaconda/Miniconda.

### 1. Configuración del entorno
```bash
# Crear el entorno desde el archivo de configuración
conda env create -f environment.yml

# Activar el entorno
conda activate myst-course-starter
```

### 2. Verificación y validación
Se incluyen scripts para verificar la integridad del entorno y el contenido:

- **Verificar entorno técnico:**
  ```bash
  # Linux / macOS / WSL
  ./scripts/verify_env.sh

  # Windows (PowerShell)
  .\scripts\verify_env.ps1
  ```
  Comprueba que todas las herramientas necesarias (MyST, Pandoc, Python, etc.) estén instaladas y accesibles.

- **Validar frontmatter:**
  ```bash
  python3 scripts/validate_frontmatter.py
  ```
  Analiza todos los archivos en `sessions/` para asegurar que cumplen con la estructura de metadatos requerida. **Emite advertencias (no errores)** para campos opcionales como `activities`, `evaluation` y `references`, permitiendo una validación más flexible.

- **Generar tabla de sesiones:**
  ```bash
  python3 scripts/generate_sessions_table_json.py
  ```
  Escanea los archivos en `sessions/` y regenera automáticamente `sessions_table.md`.

- **Generación de skeleton:**
  ```bash
  # Sincronizar myst.yml y generar sesiones
  python3 scripts/sync_myst.py
  python3 scripts/generate_sessions.py

  # Generar una semana específica
  python3 scripts/generate_sessions.py --week 1
  
  # Generar sesiones en diferentes idiomas
  python3 scripts/generate_sessions.py --lang es  # Español (por defecto)
  python3 scripts/generate_sessions.py --lang en  # Inglés
  python3 scripts/generate_sessions.py --lang fr  # Francés
  ```
### 1. Andamiaje del Curso (Automatizado)
El script `scaffold_course.py` es el punto de entrada principal para generar la estructura del curso. Orquesta varios pasos para asegurar una configuración completa del proyecto:

```bash
python3 scripts/scaffold_course.py [--lang {es,en,fr}] [--force]
```

**Lo que hace:**
1.  **Verificación de Directorios**: Crea las carpetas necesarias (`sessions`, `activities`, `assets`, etc.).
2.  **Sincronización de Metadatos**: Crea `myst.yml` con el título, autores y configuración desde `planeamiento.json`.
3.  **Generación del Programa**: Crea `programa.md` (punto de entrada del sílabo) con detalles del curso y tabla cronograma.
4.  **Generación de Contenido**:
    -   Genera archivos Markdown de sesiones (`sessions/`).
    -   Genera esqueletos Markdown para las actividades (`activities/`).
5.  **Construcción del TOC**: Crea una Tabla de Contenidos dinámica en `myst.yml`.
    -   **Localización**: Las etiquetas de "Semana" están localizadas (ej. "Semana 1", "Week 1").
    -   **Actividades Ocultas**: Las actividades se agregan a la construcción pero se ocultan de la barra lateral (`hidden: true`), accesibles vía enlaces en las sesiones.
6.  **Inyección de Insignias**: Agrega badges localizados (Duración, Dificultad) a los archivos de actividad.
7.  **Tabla de Resumen**: Genera una tabla resumen en `sessions_table.md`.

**Argumentos:**
-   `--lang`: Selecciona el idioma para el contenido generado, encabezados y mensajes de consola (por defecto: `es`). Soportado: `es`, `en`, `fr`.
-   `--force`: Sobrescribe archivos existentes. **Incluye una confirmación interactiva para prevenir la pérdida accidental de datos.**

### 2. Scripts Manuales/Individuales
Si necesitas control granular, puedes ejecutar scripts individuales:

- **Generar Sesiones:**
  ```bash
  python3 scripts/generate_sessions.py --lang en
  ```
- **Generar Actividades:**
  ```bash
  python3 scripts/generate_activities.py --lang fr
  ```
- **Generar Programa:**
  ```bash
  python3 scripts/generate_program.py --lang es
  ```
- **Inyectar Badges:**
  ```bash
  python3 scripts/inject_activity_header.py --lang en
  ```

### 3. Ejecución del servidor local

Una vez configurado y verificado el entorno, puedes iniciar el servidor de desarrollo:

```bash
myst start
```
El sitio estará disponible en `http://localhost:3000`.

### 4. Visor de Sílabo Interactivo

El **Visor de Sílabo (Syllabus Viewer)** es una herramienta complementaria para visualizar y editar el archivo `planeamiento.json`. Ahora está desacoplado de este repositorio y disponible como una aplicación alojada.

🚀 **Acceder al visor:** [https://glacy.github.io/syllabus-viewer/](https://glacy.github.io/syllabus-viewer/)

Úselo para:
- Editar visualmente la estructura de su curso.
- Exportar el `planeamiento.json` actualizado para usar con esta plantilla.
- Previsualizar el diseño de su sílabo.


## Asistencia de IA

Este proyecto contó con la asistencia de **Antigravity**, un agente de codificación avanzado desarrollado por el equipo de Google Deepmind. Su papel en el desarrollo incluye:

- **Refactorización y optimización**: Mejora continua de la calidad del código, asegurando consistencia y adherencia a las mejores prácticas en Python, TypeScript y React.
- **Mantenimiento del entorno**: Gestión de scripts de validación, automatización de flujos de trabajo (CI/CD) y verificación de dependencias.
- **Documentación dinámica**: Generación y actualización de documentación técnica, como este README, asegurando que refleje el estado actual del proyecto.
- **Soporte en desarrollo**: Asistencia en tiempo real para la resolución de errores, migración de tecnologías y scaffolding de nuevos componentes.
- **Prototipado de contenido pedagógico**: Redacción detallada de material instruccional.


## Licencia

Este material es abierto.
- **Contenido:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Código:** MIT
