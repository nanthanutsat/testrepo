"""
Service Request Workbook definition in Python.
"""
from workbook_models import (
    Workbook, Worksheet, Table, Column, Row, FormulaLibrary
)


# Initialize formula library
formulas = FormulaLibrary()
formulas.register("daysOpen", "=TODAY()-[@[Request Date]]")
formulas.register("totalRequests", "=ROWS(ServiceRequests)")
formulas.register("openRequests", '=COUNTIF(ServiceRequests[Status], "Open")')
formulas.register("highPriorityRequests", '=COUNTIFS(ServiceRequests[Priority], "High")')
formulas.register("assignedToAlice", '=COUNTIFS(ServiceRequests[Assigned To], "Alice")')


# Build the Requests worksheet
requests_table = Table(
    id="tbl_requests",
    name="ServiceRequests",
    worksheet_id="sheet_requests",
    columns=[
        Column(key="requestId", header="Request ID", type="string"),
        Column(key="customer", header="Customer", type="string"),
        Column(key="serviceType", header="Service Type", type="string"),
        Column(key="status", header="Status", type="string"),
        Column(key="priority", header="Priority", type="string"),
        Column(key="requestDate", header="Request Date", type="date"),
        Column(key="assignedTo", header="Assigned To", type="string"),
        Column(key="daysOpen", header="Days Open", type="number", formula="daysOpen"),
    ],
    rows=[
        Row(
            id="row_1",
            values={
                "requestId": "REQ-1001",
                "customer": "Acme Corp",
                "serviceType": "Network Support",
                "status": "Open",
                "priority": "High",
                "requestDate": "2026-06-01",
                "assignedTo": "Alice",
                "daysOpen": "daysOpen",  # Formula key reference
            },
        ),
        Row(
            id="row_2",
            values={
                "requestId": "REQ-1002",
                "customer": "Beta LLC",
                "serviceType": "Software Update",
                "status": "Closed",
                "priority": "Medium",
                "requestDate": "2026-06-02",
                "assignedTo": "Bob",
                "daysOpen": "daysOpen",  # Formula key reference
            },
        ),
    ],
)

requests_worksheet = Worksheet(
    id="sheet_requests",
    name="Requests",
    tables=[requests_table],
)


# Build the Dashboard worksheet
dashboard_table = Table(
    id="tbl_dashboard",
    name="DashboardMetrics",
    worksheet_id="sheet_dashboard",
    columns=[
        Column(key="metric", header="Metric", type="string"),
        Column(key="formulaKey", header="Formula Key", type="string"),
        Column(key="value", header="Value", type="number"),
    ],
    rows=[
        Row(
            id="row_1",
            values={
                "metric": "Total Requests",
                "formulaKey": "totalRequests",
                "value": "totalRequests",  # Will be replaced with formula
            },
        ),
        Row(
            id="row_2",
            values={
                "metric": "Open Requests",
                "formulaKey": "openRequests",
                "value": "openRequests",  # Will be replaced with formula
            },
        ),
        Row(
            id="row_3",
            values={
                "metric": "High Priority",
                "formulaKey": "highPriorityRequests",
                "value": "highPriorityRequests",  # Will be replaced with formula
            },
        ),
        Row(
            id="row_4",
            values={
                "metric": "Assigned to Alice",
                "formulaKey": "assignedToAlice",
                "value": "assignedToAlice",  # Will be replaced with formula
            },
        ),
    ],
)

dashboard_worksheet = Worksheet(
    id="sheet_dashboard",
    name="Dashboard",
    tables=[dashboard_table],
)


# Build the complete workbook
service_request_workbook = Workbook(
    name="ServiceRequestWorkbook",
    worksheets=[requests_worksheet, dashboard_worksheet],
)
