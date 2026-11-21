---
name: data-dict-extractor
description: Generate Excel data dictionaries from Drupal 9/10 exported configuration. Use when working in a Drupal project that has a config sync directory and the user wants to document content types, taxonomy vocabularies, block types, media types, or paragraph types as spreadsheets. Triggers on requests like "generate a data dictionary", "document the content model", "create field documentation", "export Drupal fields to Excel", or similar.
---

# Drupal Data Dictionary

## Requirements

Python 3 with openpyxl and PyYAML; a shell, read access to an exported Drupal configuration directory, and write access to the chosen output directory. A running Drupal site, DDEV, and service credentials are not required for this local extraction.

Resolve `SKILL_DIR` to the absolute directory containing the loaded `SKILL.md`, using the skill location supplied by the agent or locating this file. Set it explicitly (for example, `SKILL_DIR="/path/to/installed/data-dict-extractor"`); do not derive it from the project working directory. Run project-relative commands from the working project and use `"$SKILL_DIR/..."` for companions.

## Safety and review

Configuration exports can include confidential architecture, field labels/help text, and embedded secrets. Select only the configuration needed and keep source and workbooks in authorized local storage. A human reviews the command, output prefix, and existing filenames before execution because workbooks are overwritten. Review generated values, sheet links, and possible spreadsheet formulas before opening or sharing. Do not upload source configuration or private workbooks to a public AI model; a human owns the final content-model interpretation and delivery.

Outside a verified secure sandbox, a human must read and understand unreviewed shell commands and generated code before execution. Always review MCP data-changing operations if an MCP alternative is used. Use least privilege; tool installation requires Security Team review and verification of upstream identity. Personal information requires approved tooling integrated with its source system; confidential information requires specifically approved tools; non-public information requires tools that neither train on nor retain it. Never send sensitive non-public data to public AI models. Stop when eligibility is unknown. An AI check does not replace human self-review before sharing, publishing, or handing work to another reviewer.


Runs the bundled `scripts/extract_data_dictionary.py` against a Drupal config export to produce five Excel workbooks documenting all field definitions.

## Output files

Five `.xlsx` files are generated in the project root (directory containing the sync dir):
- `{prefix}-content-types.xlsx`
- `{prefix}-taxonomy-vocabularies.xlsx`
- `{prefix}-block-types.xlsx`
- `{prefix}-media-types.xlsx`
- `{prefix}-paragraph-types.xlsx`

## Workflow

1. **Gather configuration** — before running, ask the user:
   - **Sync directory**: path to the Drupal config export directory, relative to the project root (default: `sync`)
   - **Output prefix**: short identifier used to name the output files (suggest the project/site name, default: `az-gov`)

2. **Locate project root** — confirm the sync directory exists at the path given. If the current working directory is not the project root, find it (check parent directories or ask the user).

3. **Check dependencies** — verify Python packages are available:
   ```bash
   python3 -c "import openpyxl, yaml"
   ```
   If packages are missing, report them; after setup is authorized and package identity is reviewed, use a project virtual environment:
   ```bash
   python3 -m pip install openpyxl pyyaml
   ```

4. **Run the script** from the project root:
   ```bash
   cd "/path/to/project/root" && python3 "$SKILL_DIR/scripts/extract_data_dictionary.py" \
     --sync-dir {sync_dir} \
     --prefix {prefix}
   ```
   `SKILL_DIR` is the resolved loaded-skill directory described in Requirements.

5. **Report** the five generated `.xlsx` files and their location.
