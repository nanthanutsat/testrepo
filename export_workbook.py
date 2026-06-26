import json
from pathlib import Path
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).parent


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def apply_table(ws, table):
    columns = table["columns"]
    rows = table.get("rows", [])

    # Write headers
    for col_idx, column in enumerate(columns, start=1):
        ws.cell(row=1, column=col_idx, value=column["header"])

    for row_idx, row in enumerate(rows, start=2):
        values = row.get("values", {})
        for col_idx, column in enumerate(columns, start=1):
            key = column["key"]
            value = values.get(key)
            if isinstance(value, dict) and "formula" in value:
                ws.cell(row=row_idx, column=col_idx, value=value["formula"])
            else:
                ws.cell(row=row_idx, column=col_idx, value=value)


def export_workbook(manifest_path: Path, output_path: Path):
    manifest = load_json(manifest_path)
    formula_library = load_json(ROOT / manifest["formulaLibrary"])

    wb = Workbook()
    first = True

    for sheet_info in manifest["sheets"]:
        sheet_file = ROOT / sheet_info["file"]
        sheet = load_json(sheet_file)

        if first:
            ws = wb.active
            ws.title = sheet_info["name"]
            first = False
        else:
            ws = wb.create_sheet(title=sheet_info["name"])

        for table in sheet["tables"]:
            apply_table(ws, table)

    wb.save(output_path)


if __name__ == "__main__":
    output_file = ROOT / "ServiceRequestWorkbook.xlsx"
    export_workbook(ROOT / "workbook_manifest.json", output_file)
    print(f"Exported workbook to {output_file}")
