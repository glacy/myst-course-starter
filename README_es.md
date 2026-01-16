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


## Estructura del proyecto

### 1. Estructura de la Plantilla (Estado Inicial)
Antes de ejecutar los scripts de andamiaje, el repositorio contiene el motor central y la configuración:

```text
myst-course-starter/
├── assets/                # 🎨 Recursos estáticos (logos, imágenes)
├── scripts/               # 🛠️ Scripts de mantenimiento y automatización
├── tests/                 # 🧪 Pruebas unitarias para los scripts
├── planeamiento.json      # 📋 Datos estructurados del planeamiento (Tu Fuente de Verdad)
├── environment.yml        # 📦 Configuración del entorno reproducible
└── .github/               # 🤖 Flujos de automatización (CI/CD)
```

### 2. Estructura Andamiada (Después de Generar)
Al ejecutar `python3 scripts/scaffold_course.py`, se genera el siguiente contenido basado en tu `planeamiento.json`:

```text
myst-course-starter/
├── myst.yml               # ⚙️ Configuración del sitio auto-generada
├── programa.md            # 📄 Programa del curso auto-generado
├── sessions/              # 📚 Archivos Markdown de sesiones generados (Capítulos)
├── activities/            # ✍️ Esqueletos de actividades generados
├── examples/              # 🧩 Carpeta para ejemplos de referencia
└── exercises/             # ✍️ Carpeta para ejercicios propuestos
```

**Nota sobre la estructura de contenido:**
El curso sigue una arquitectura modular donde los contenidos prácticos no residen directamente en los archivos de sesión (`sessions/`), sino que se inyectan dinámicamente:
- **`examples/`**: Contiene ejemplos resueltos y casos de estudio.
- **`exercises/`**: Contiene los ejercicios propuestos, estructurados semánticamente mediante la directiva `{exercise}` de MyST.
Esta separación permite reutilizar componentes y facilita el mantenimiento.




## Inicio Rápido (Local)

Para garantizar un entorno de desarrollo consistente, este proyecto utiliza Anaconda/Miniconda.

### 1. Clonar el repositorio

```bash
git clone https://github.com/glacy/myst-course-starter.git
cd myst-course-starter
```

### 2. Configuración del entorno
```bash
# Crear el entorno desde el archivo de configuración
conda env create -f environment.yml

# Activar el entorno
conda activate myst-course-starter
```



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
### 3. Andamiaje del Curso (Automatizado)
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

### 4. Scripts Manuales/Individuales
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

### 5. Visor de Sílabo Interactivo

El **Visor de Sílabo (Syllabus Viewer)** es una herramienta complementaria para visualizar y editar el archivo `planeamiento.json`. Ahora está desacoplado de este repositorio y disponible como una aplicación alojada.

🚀 **Acceder al visor:** [https://glacy.github.io/syllabus-viewer/](https://glacy.github.io/syllabus-viewer/)

Úselo para:
- Editar visualmente la estructura de su curso.
- Exportar el `planeamiento.json` actualizado para usar con esta plantilla.
- Previsualizar el diseño de su sílabo.


## Despliegue

Esta plantilla está configurada para desplegar automáticamente en GitHub Pages utilizando GitHub Actions.

### Configuración en GitHub

1.  **Permisos**:
    -   Vaya a **Settings** > **Actions** > **General**.
    -   Bajo "Workflow permissions", seleccione **Read and write permissions**.
    -   Haga clic en **Save**.

2.  **GitHub Pages**:
    -   Vaya a **Settings** > **Pages**.
    -   Bajo "Build and deployment" > "Source", seleccione **GitHub Actions**.

Una vez configurado, cada push a la rama `main` activará un despliegue.

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
