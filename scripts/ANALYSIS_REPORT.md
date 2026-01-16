# Script Analysis Report

The following scripts were analyzed to determine if they are necessary for the course scaffolding process (`scaffold_course.py`).

## Core Scaffolding Scripts (KEEP)
These are actively used by the scaffolding process or essential for validation.
- `scaffold_course.py`: The main orchestrator.
- `generate_sessions.py`: Generates session markdown from JSON.
- `sync_myst.py`: Updates `myst.yml` metadata.
- `update_toc.py`: Updates the Table of Contents in `myst.yml`.
- `inject_activity_header.py`: Injects badges into activity files.
- `generate_sessions_table_json.py`: Generates the sessions overview table.
- `validate_frontmatter.py`: Essential for verifying the generated structure.
- `verify_env.sh` / `verify_env.ps1`: Environment verification.

## Legacy / Unused Scripts (RECOMMEND REMOVE)
These scripts appear to be part of previous workflows (e.g., separate evaluation files) or one-off migrations.

### Legacy Evaluation Workflow
These scripts assume a separate `evaluations/` directory, which is no longer part of the standard scaffold.
- `generate_evaluations.py`
- `link_components.py`
- `extract_evaluations.py`
- `fix_evaluation_titles.py`
- `update_myst_evaluations.py`

### One-off Migrations & Utilities
Scripts used for past refactoring or specific data fixes.
- `migrate_content.py`: Migration from `sessions_BKP`.
- `add_objectives_block.py`: Backfill script.
- `update_subtitles.py`: Mass update tool.
- `fix_decimals.py`: Formatting utility.
- `add_emojis.py`: Cosmetic utility.
- `sync_md_to_json.py`: Reverse sync (Markdown -> JSON), likely unused in the primary "JSON -> Site" flow.
- `hide_activities.py`: Utility for hiding content.

## Recommendation
It is safe to remove the scripts listed in "Legacy / Unused" to clean up the repository and reduce confusion. Make sure to backup `scripts/` before deletion if unsure.
