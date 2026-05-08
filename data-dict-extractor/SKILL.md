---
name: data-dict-extractor 
description: Generate Excel data dictionaries from Drupal 9/10 exported configuration. Use when working in a Drupal project that has a config sync directory and the user wants to document content types, taxonomy vocabularies, block types, media types, or paragraph types as spreadsheets. Triggers on requests like "generate a data dictionary", "document the content model", "create field documentation", "export Drupal fields to Excel", or similar.
---

# Drupal Data Dictionary

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
   If that fails, install them:
   ```bash
   pip install openpyxl pyyaml
   ```

4. **Run the script** from the project root:
   ```bash
   cd /path/to/project/root && python3 {skill_base_dir}/scripts/extract_data_dictionary.py \
     --sync-dir {sync_dir} \
     --prefix {prefix}
   ```
   `{skill_base_dir}` is the base directory shown at the top of this skill's context.

5. **Report** the five generated `.xlsx` files and their location.
