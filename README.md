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
3. Once the terminal is ready, the `myst-course-starter` environment will be active.

## Project structure

### 1. Template Structure (Initial State)
Before running the scaffolding scripts, the repository contains the core engine and configuration:

```text
myst-course-starter/
├── assets/                # 🎨 Static resources (logos, images)
├── scripts/               # 🛠️ Maintenance and automation scripts
├── tests/                 # 🧪 Unit tests for scripts
├── planeamiento.json      # 📋 Structured planning data (Your Single Source of Truth)
├── environment.yml        # 📦 Reproducible environment configuration
└── .github/               # 🤖 Automation workflows (CI/CD)
```

### 2. Scaffolded Structure (After Generation)
Running `python3 scripts/scaffold_course.py` generates the following content based on your `planeamiento.json`:

```text
myst-course-starter/
├── myst.yml               # ⚙️ Auto-generated site configuration
├── programa.md            # 📄 Auto-generated Course Syllabus
├── sessions/              # 📚 Generated Session Markdown files (Chapters)
├── activities/            # ✍️ Generated Activity skeletons
├── examples/              # 🧩 Folder for reference examples
└── exercises/             # ✍️ Folder for proposed exercises
```

**Note on content structure:**
The course follows a modular architecture where practical content does not reside directly in session files (`sessions/`), but is dynamically injected:
- **`examples/`**: Contains solved examples and case studies.
- **`exercises/`**: Contains proposed exercises, structured semantically using MyST's `{exercise}` directive.
This separation allows component reuse and facilitates maintenance.




## Getting Started (Local)

To ensure a consistent development environment, this project uses Anaconda/Miniconda.

### 1. Clone the repository

```bash
git clone https://github.com/glacy/myst-course-starter.git
cd myst-course-starter
```

### 2. Environment setup
```bash
# Create the environment from the configuration file
conda env create -f environment.yml

# Activate the environment
conda activate myst-course-starter
```

### 3. Course Scaffolding (Automated)
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


### 4. Local server execution

Once the environment is configured and verified, you can start the development server:

```bash
myst start
```
The site will be available at `http://localhost:3000`.

### 5. Interactive Syllabus Viewer

The **Syllabus Viewer** is a companion tool to visualize and edit the `planeamiento.json` file. It is now decoupled from this repository and available as a hosted application.

🚀 **Access the viewer:** [https://glacy.github.io/syllabus-viewer/](https://glacy.github.io/syllabus-viewer/)

Use it to:
- Visually edit your course structure.
- Export the updated `planeamiento.json` to use with this template.
- Preview your syllabus layout.

### 6. Manual/Individual Scripts
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


### Internal script architecture (overview)

- Shared utilities live in `scripts/utils.py` (JSON loading, filenames, translations, output paths).
- The main orchestrator `scripts/scaffold_course.py` calls generator scripts as importable modules instead of via subprocess.
- Validation and overview helpers (`scripts/validate_frontmatter.py`, `scripts/generate_sessions_table_json.py`) reuse the same configuration and metadata as the generators.


## Deployment

This template is configured to deploy automatically to GitHub Pages using GitHub Actions.

### Configuration on GitHub

1.  **Permissions**:
    -   Go to **Settings** > **Actions** > **General**.
    -   Under "Workflow permissions", select **Read and write permissions**.
    -   Click **Save**.

2.  **GitHub Pages**:
    -   Go to **Settings** > **Pages**.
    -   Under "Build and deployment" > "Source", select **GitHub Actions**.

Once configured, every push to the `main` branch will trigger a deployment.

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
