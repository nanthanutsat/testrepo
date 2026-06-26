"""
Workbook data models for Excel workbook definition and export.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Column:
    """Column definition for a table."""
    key: str
    header: str
    type: str
    formula: Optional[str] = None


@dataclass
class Row:
    """Row definition with values and formulas."""
    id: str
    values: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Table:
    """Table definition with columns and rows."""
    id: str
    name: str
    worksheet_id: str
    columns: List[Column] = field(default_factory=list)
    rows: List[Row] = field(default_factory=list)
    header_row: bool = True
    address: Optional[str] = None


@dataclass
class Worksheet:
    """Worksheet definition."""
    id: str
    name: str
    tables: List[Table] = field(default_factory=list)
    tab_color: str = "#FFFFFF"


@dataclass
class Workbook:
    """Workbook definition."""
    name: str
    worksheets: List[Worksheet] = field(default_factory=list)

    def get_worksheet(self, ws_id: str) -> Optional[Worksheet]:
        for ws in self.worksheets:
            if ws.id == ws_id:
                return ws
        return None

    def get_table(self, table_name: str) -> Optional[Table]:
        for ws in self.worksheets:
            for table in ws.tables:
                if table.name == table_name:
                    return table
        return None


class FormulaLibrary:
    """Centralized formula management."""

    def __init__(self):
        self.formulas: Dict[str, str] = {}

    def register(self, key: str, formula: str) -> None:
        """Register a formula by key."""
        self.formulas[key] = formula

    def get(self, key: str) -> str:
        """Retrieve a formula by key."""
        return self.formulas.get(key, "")

    def resolve(self, key_or_formula: str) -> str:
        """
        Resolve a formula key to its template.
        If it's a key in the library, return the template.
        Otherwise, return as-is (assume it's an inline formula).
        """
        if key_or_formula in self.formulas:
            return self.formulas[key_or_formula]
        return key_or_formula
