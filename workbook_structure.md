# Workbook Test Environment Structure

This document describes a test-friendly data model for an Excel workbook with multiple worksheets and tables linked by formulas.

## 1. Core concepts

- `Workbook`: the whole file.
- `Worksheet`: individual sheet/tab.
- `Table`: structured blocks of rows and columns inside a worksheet.
- `Cell`: a single address with a value and/or formula.
- `Formula`: an expression that may reference cells, ranges, tables, or other worksheets.
- `Reference`: dependency from one formula to another worksheet/table/cell.

## 2. Data structure

### Workbook

```json
{
  "name": "SalesWorkbook",
  "worksheets": [ /* Worksheet[] */ ],
  "namedRanges": [ /* NamedRange[] */ ]
}
```

### Worksheet

```json
{
  "id": "sheet_sales",
  "name": "Sales",
  "tables": [ /* Table[] */ ],
  "cells": [ /* Cell[] */ ],
  "metadata": {
    "tabColor": "#FFFFFF"
  }
}
```

### Table

```json
{
  "id": "tbl_sales",
  "name": "SalesData",
  "worksheetId": "sheet_sales",
  "columns": [ /* Column[] */ ],
  "rows": [ /* Row[] */ ],
  "headerRow": true,
  "address": "A1:D5"
}
```

### Column

```json
{
  "key": "product",
  "header": "Product",
  "type": "string"
}
```

### Row

```json
{
  "id": "row_1",
  "values": {
    "product": "Widget",
    "quantity": 10,
    "unitPrice": 5.5,
    "total": {
      "formula": "=Quantity * UnitPrice"
    }
  }
}
```

### Cell

```json
{
  "address": "D2",
  "value": 55,
  "formula": "=B2 * C2",
  "references": ["B2", "C2"]
}
```

### Formula reference

```json
{
  "formula": "=SUM(SalesData[Total])",
  "references": [
    { "worksheet": "Sales", "table": "SalesData", "column": "Total" }
  ]
}
```

## 3. Example workbook structure

```json
{
  "name": "TestWorkbook",
  "worksheets": [
    {
      "id": "sheet_sales",
      "name": "Sales",
      "tables": [
        {
          "id": "tbl_sales",
          "name": "SalesData",
          "worksheetId": "sheet_sales",
          "columns": [
            { "key": "product", "header": "Product", "type": "string" },
            { "key": "quantity", "header": "Quantity", "type": "number" },
            { "key": "unitPrice", "header": "Unit Price", "type": "number" },
            { "key": "total", "header": "Total", "type": "number", "formula": "=Quantity * UnitPrice" }
          ],
          "rows": [
            {
              "id": "row_1",
              "values": {
                "product": "Widget",
                "quantity": 10,
                "unitPrice": 5.5,
                "total": { "formula": "=B2 * C2" }
              }
            },
            {
              "id": "row_2",
              "values": {
                "product": "Gadget",
                "quantity": 7,
                "unitPrice": 12,
                "total": { "formula": "=B3 * C3" }
              }
            }
          ]
        }
      ]
    },
    {
      "id": "sheet_inventory",
      "name": "Inventory",
      "tables": [
        {
          "id": "tbl_inventory",
          "name": "InventoryData",
          "worksheetId": "sheet_inventory",
          "columns": [
            { "key": "product", "header": "Product", "type": "string" },
            { "key": "stock", "header": "Stock", "type": "number" },
            { "key": "reorderLevel", "header": "Reorder Level", "type": "number" },
            {
              "key": "needed",
              "header": "Needed",
              "type": "number",
              "formula": "=MAX(0, ReorderLevel - Stock)"
            }
          ],
          "rows": [
            {
              "id": "row_1",
              "values": {
                "product": "Widget",
                "stock": 25,
                "reorderLevel": 50,
                "needed": { "formula": "=MAX(0, C2 - B2)" }
              }
            }
          ]
        }
      ]
    },
    {
      "id": "sheet_summary",
      "name": "Summary",
      "tables": [
        {
          "id": "tbl_summary",
          "name": "SummaryData",
          "worksheetId": "sheet_summary",
          "columns": [
            { "key": "metric", "header": "Metric", "type": "string" },
            { "key": "value", "header": "Value", "type": "number" }
          ],
          "rows": [
            {
              "id": "row_1",
              "values": {
                "metric": "Total Sales",
                "value": {
                  "formula": "=SUM(SalesData[Total])",
                  "references": [
                    { "worksheet": "Sales", "table": "SalesData", "column": "Total" }
                  ]
                }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

## 4. Service request workbook example

This example shows the two worksheets you described:
- `Requests`: a database table for every service request.
- `Dashboard`: a summary worksheet that reads results from the `Requests` table.

```json
{
  "name": "ServiceRequestWorkbook",
  "worksheets": [
    {
      "id": "sheet_requests",
      "name": "Requests",
      "tables": [
        {
          "id": "tbl_requests",
          "name": "ServiceRequests",
          "worksheetId": "sheet_requests",
          "columns": [
            { "key": "requestId", "header": "Request ID", "type": "string" },
            { "key": "customer", "header": "Customer", "type": "string" },
            { "key": "serviceType", "header": "Service Type", "type": "string" },
            { "key": "status", "header": "Status", "type": "string" },
            { "key": "priority", "header": "Priority", "type": "string" },
            { "key": "requestDate", "header": "Request Date", "type": "date" },
            { "key": "assignedTo", "header": "Assigned To", "type": "string" }
          ],
          "rows": [
            {
              "id": "row_1",
              "values": {
                "requestId": "REQ-1001",
                "customer": "Acme Corp",
                "serviceType": "Network Support",
                "status": "Open",
                "priority": "High",
                "requestDate": "2026-06-01",
                "assignedTo": "Alice"
              }
            },
            {
              "id": "row_2",
              "values": {
                "requestId": "REQ-1002",
                "customer": "Beta LLC",
                "serviceType": "Software Update",
                "status": "Closed",
                "priority": "Medium",
                "requestDate": "2026-06-02",
                "assignedTo": "Bob"
              }
            }
          ]
        }
      ]
    },
    {
      "id": "sheet_dashboard",
      "name": "Dashboard",
      "tables": [
        {
          "id": "tbl_dashboard",
          "name": "DashboardMetrics",
          "worksheetId": "sheet_dashboard",
          "columns": [
            { "key": "metric", "header": "Metric", "type": "string" },
            { "key": "value", "header": "Value", "type": "number" },
            { "key": "formula", "header": "Formula", "type": "string" }
          ],
          "rows": [
            {
              "id": "row_1",
              "values": {
                "metric": "Total Requests",
                "value": {
                  "formula": "=ROWS(ServiceRequests)"
                },
                "formula": "=ROWS(ServiceRequests)"
              }
            },
            {
              "id": "row_2",
              "values": {
                "metric": "Open Requests",
                "value": {
                  "formula": "=COUNTIF(ServiceRequests[Status], \"Open\")"
                },
                "formula": "=COUNTIF(ServiceRequests[Status], \"Open\")"
              }
            },
            {
              "id": "row_3",
              "values": {
                "metric": "High Priority",
                "value": {
                  "formula": "=COUNTIFS(ServiceRequests[Priority], \"High\")"
                },
                "formula": "=COUNTIFS(ServiceRequests[Priority], \"High\")"
              }
            },
            {
              "id": "row_4",
              "values": {
                "metric": "Assigned to Alice",
                "value": {
                  "formula": "=COUNTIFS(ServiceRequests[Assigned To], \"Alice\")"
                },
                "formula": "=COUNTIFS(ServiceRequests[Assigned To], \"Alice\")"
              }
            }
          ]
        }
      ],
      "cells": [
        {
          "address": "B2",
          "formula": "=ROWS(ServiceRequests)",
          "references": [
            { "worksheet": "Requests", "table": "ServiceRequests" }
          ]
        }
      ]
    }
  ]
}
```

## 5. Recommended test environment pattern

1. Model each worksheet and table separately.
2. Store formulas as expressions plus explicit references.
3. Track dependencies across worksheets for test validation.
4. Use the structure to generate sample workbook files or to unit-test formula propagation.

## 5. Notes

- Use `worksheetId` to map tables and formulas back to sheets.
- Use `references` to verify cross-sheet links without executing Excel.
- This structure is suitable for code-driven test harnesses, migration scripts, and workbook validation logic.
