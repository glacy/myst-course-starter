[![deploy](https://github.com/glacy/myst-course-starter/actions/workflows/deploy.yml/badge.svg)](https://github.com/glacy/myst-course-starter/actions/workflows/deploy.yml)

**MyST Course Starter**

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/glacy/myst-course-starter)

🚀 **Official website (Compiled version):** [https://glacy.github.io/myst-course-starter](https://glacy.github.io/myst-course-starter)

---

## About this repository

This software functions as a **Course Generator Engine** and is designed to serve as a template for creating academic courses using [MyST Markdown](https://mystmd.org/).

Its primary role is to decouple **instructional design** from **technical implementation**. By defining your course structure in a single file (`planeamiento.json`), this software automatically:

1.  **Scaffolds structure**: Generates the folder hierarchy and markdown stubs for each session/week.
2.  **Synchronizes metadata**: Updates site configuration, titles, and navigation.
3.  **Powers the UI**: Feeds the interactive React-based "Syllabus Viewer" for students.

It is ideal for educators who want a "Compliance-as-Code" approach, ensuring that the course website, documentation, and student viewer always reflect the latest approved syllabus.

### Key Features
- **Semantic structure:** Driven by YAML frontmatter and JSON schemas.
- **Reproducibility:** Controlled environment with automated deployment.
- **Documentation as Code:** Changes to the syllabus are tracked via git and deployed via CI/CD.

## Cloud execution (recommended)

The easiest way to run this course is using **GitHub Codespaces**.
1. Click on the "Open in GitHub Codespaces" button above.
2. Wait for the environment to build (it will automatically install all dependencies).
3. Once the terminal is ready, the `frontmatter-academico` environment will be active.

### Best practices (pre-commit)

If you clone the repository locally, it is recommended to install git hooks for automatic validation:

```bash
# Once the conda environment is activated
pre-commit install
```
This will automatically validate the frontmatter when attempting to commit.

> **Note:** If you need to skip these validations in an emergency:
> - **Skip in a commit:** `git commit -n` (or `--no-verify`)
> - **Uninstall hooks:** `pre-commit uninstall`
> - **Disable configuration:** Rename the file: `mv .pre-commit-config.yaml .pre-commit-config.yaml.disabled`

## Project structure

```text
myst-course-starter/
├── assets/                # 🎨 Static resources (logos, images)
├── scripts/               # 🛠️ Maintenance and automation scripts
├── tests/                 # 🧪 Unit tests for scripts
├── myst.yml               # ⚙️ Site configuration and global metadata
├── programa.md            # 📄 Course program
├── planeamiento.json      # 📋 Structured planning data 
├── sessions/              # 📚 Course content (Chapters)
├── examples/              # 🧩 Reference examples
├── exercises/             # ✍️ Practical activities
└── .github/               # 🤖 Automation workflows (CI/CD)
```

**Note on content structure:**
The course follows a modular architecture where practical content does not reside directly in session files (`sessions/`), but is dynamically injected:
- **`examples/`**: Contains solved examples and case studies.
- **`exercises/`**: Contains proposed exercises, structured semantically using MyST's `{exercise}` directive.
This separation allows component reuse and facilitates maintenance.




## Reproducibility and local configuration

To ensure a consistent development environment, this project uses Anaconda/Miniconda.

### 1. Environment setup
```bash
# Create the environment from the configuration file
conda env create -f environment.yml

# Activate the environment
conda activate myst-course-starter
```

### 2. Verification and validation
Scripts are included to verify the integrity of the environment and content:

- **Verify technical environment:**
  ```bash
  # Linux / macOS / WSL
  ./scripts/verify_env.sh

  # Windows (PowerShell)
  .\scripts\verify_env.ps1
  ```
  Checks that all necessary tools (MyST, Pandoc, Python, etc.) are installed and accessible.

- **Validate frontmatter:**
  ```bash
  python3 scripts/validate_frontmatter.py
  ```
  Analyzes all files in `sessions/` to ensure they comply with the required metadata structure. **Emits warnings (not errors)** for optional fields such as `activities`, `evaluation`, and `references`, allowing more flexible validation.

- **Generate sessions table:**
  ```bash
  python3 scripts/generate_sessions_table_json.py
  ```
  Scans files in `sessions/` and automatically regenerates `sessions_table.md`.

- **Skeleton generation:**
  ```bash
  # Synchronize myst.yml and generate sessions
  python3 scripts/sync_myst.py
  python3 scripts/generate_sessions.py

  # Generate a specific week
  python3 scripts/generate_sessions.py --week 1
  
  # Generate sessions in different languages
  python3 scripts/generate_sessions.py --lang es  # Spanish (default)
  python3 scripts/generate_sessions.py --lang en  # English
  python3 scripts/generate_sessions.py --lang fr  # French
  ```
### 1. Course Scaffolding (Automated)
The `scaffold_course.py` script is the main entry point for generating the course structure. It orchestrates several steps to ensure a complete project setup:

```bash
python3 scripts/scaffold_course.py [--lang {es,en,fr}] [--force]
```

**What it does:**
1.  **Directory Verification**: Creates necessary folders (`sessions`, `activities`, `assets`, etc.).
2.  **Metadata Sync**: Creates `myst.yml` with title, authors, and configuration from `planeamiento.json`.
3.  **Program Generation**: Creates `programa.md` (syllabus entry point) with course details and schedule table.
4.  **Content Generation**:
    -   Generates session Markdown files (`sessions/`).
    -   Generates activity Markdown skeletons (`activities/`).
5.  **TOC Construction**: Builds a dynamic Table of Contents in `myst.yml`.
    -   **Localization**: "Week" labels are localized (e.g., "Semana 1").
    -   **Hidden Activities**: Activities are added to the build but hidden from the sidebar (`hidden: true`), accessible via links in session files.
6.  **Badge Injection**: Adds localized "Activity" badges (Duration, Difficulty) to activity files.
7.  **Overview Table**: Generates a summary table in `sessions_table.md`.

**Arguments:**
-   `--lang`: Selects the language for generated content, headers, and console output (default: `es`). Supported: `es`, `en`, `fr`.
-   `--force`: Overwrites existing files. **Includes an interactive confirmation prompt to prevent accidental data loss.**

### 2. Manual/Individual Scripts
If you need granular control, you can run individual scripts:

- **Generate Sessions:**
  ```bash
  python3 scripts/generate_sessions.py --lang en
  ```
- **Generate Activities:**
  ```bash
  python3 scripts/generate_activities.py --lang fr
  ```
- **Generate Program:**
  ```bash
  python3 scripts/generate_program.py --lang es
  ```
- **Inject Badges:**
  ```bash
  python3 scripts/inject_activity_header.py --lang en
  ```


### 3. Local server execution

Once the environment is configured and verified, you can start the development server:

```bash
myst start
```
The site will be available at `http://localhost:3000`.

### 4. Interactive Syllabus Viewer

The **Syllabus Viewer** is a companion tool to visualize and edit the `planeamiento.json` file. It is now decoupled from this repository and available as a hosted application.

🚀 **Access the viewer:** [https://glacy.github.io/syllabus-viewer/](https://glacy.github.io/syllabus-viewer/)

Use it to:
- Visually edit your course structure.
- Export the updated `planeamiento.json` to use with this template.
- Preview your syllabus layout.


## AI assistance

This project had the assistance of **Antigravity**, an advanced coding agent developed by Google Deepmind's team. Its role in development includes:

- **Refactoring and optimization**: Continuous improvement of code quality, ensuring consistency and adherence to best practices in Python, TypeScript, and React.
- **Environment maintenance**: Management of validation scripts, workflow automation (CI/CD), and dependency verification.
- **Dynamic documentation**: Generation and updating of technical documentation, such as this README, ensuring it reflects the current state of the project.
- **Development support**: Real-time assistance for error resolution, technology migration, and scaffolding of new components.
- **Pedagogical content prototyping**: Detailed writing of instructional material.


## License

This material is open.
- **Content:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Code:** MIT
