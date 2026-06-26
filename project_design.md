# Project Design for Excel Workbook Export

This repository now supports a structured, exportable Excel workbook model that separates sheet content, formula definitions, and export logic.

## Recommended project layout

- `workbook_manifest.json`: workbook metadata and sheet file list.
- `formula_library.json`: reusable formulas keyed by feature.
- `requests_sheet.json`: sheet definition for the Requests database.
- `dashboard_sheet.json`: sheet definition for the Dashboard view.
- `export_workbook.py`: export script that generates an `.xlsx` file from JSON definitions.
- `requirements.txt`: Python dependencies for the export script.

## Design principles

1. Separate data from formulas.
   - Data rows store values.
   - Column formulas and dashboard formulas reference formula keys.
2. Keep formulas reusable.
   - Use `formula_library.json` so formula updates happen in one place.
3. Treat each sheet as a separate artifact.
   - Each worksheet is its own JSON file for easy modifications.
4. Export from structured metadata.
   - A script reads the manifest and sheet files and writes a workbook.

## Workflow

1. Add or update a feature:
   - Update relevant sheet JSON file(s).
   - If the feature adds or changes formulas, add or update keys in `formula_library.json`.
2. Run export:
   - `python export_workbook.py`
3. Review the generated workbook.
4. Commit JSON/schema changes and keep the exported workbook separate if needed.

## Managing formula changes

- Use formula keys rather than hard-coded formulas inside sheet row definitions.
- Add descriptive names to the library like `daysOpen`, `totalRequests`, `openRequests`.
- If a formula changes for a new feature, update the template in one place.
- Optional: add parameters to formula templates for more advanced reuse.

## Export strategy

- The export script loads `workbook_manifest.json`.
- It reads every worksheet file to build tables and formulas.
- It creates real Excel formulas in the generated file.

## Benefits

- Easy to review and modify formulas in source control.
- One-source-of-truth for formulas.
- Clean separation between workbook structure and feature logic.
- Export-ready workbook generation for real project use.
