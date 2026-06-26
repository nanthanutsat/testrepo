"""
PowerApps Canvas App Generator
Generates app definition and setup code for importing into Microsoft Power Apps
"""
import json
from pathlib import Path


class PowerAppsAppGenerator:
    """Generate PowerApps canvas app configuration."""
    
    def __init__(self, app_name: str, sharepoint_site: str):
        self.app_name = app_name
        self.sharepoint_site = sharepoint_site
        self.screens = {}
        self.datasources = []
        self.connections = []
    
    def add_excel_datasource(self, library: str, file_name: str, table_name: str) -> None:
        """Add Excel Online datasource."""
        self.datasources.append({
            "name": table_name,
            "type": "ExcelOnline",
            "library": library,
            "file": file_name,
            "table": table_name,
        })
        self.connections.append({
            "type": "ExcelOnline",
            "name": f"Excel_{table_name}",
        })
    
    def generate_app_structure(self) -> dict:
        """Generate PowerApps app structure."""
        return {
            "appName": self.app_name,
            "appId": "00000000-0000-0000-0000-000000000000",
            "version": "1.0",
            "screens": self.screens,
            "datasources": self.datasources,
            "connections": self.connections,
            "variables": {
                "global": {
                    "selectedRequest": None,
                    "refreshing": False,
                }
            }
        }


class PowerAppsScreenBuilder:
    """Build individual screens for PowerApps app."""
    
    @staticmethod
    def build_home_screen() -> dict:
        """Build home/dashboard screen."""
        return {
            "name": "HomeScreen",
            "title": "Service Request Dashboard",
            "controls": [
                {
                    "name": "HeaderLabel",
                    "type": "Label",
                    "properties": {
                        "text": "Service Request Portal",
                        "fontSize": 32,
                        "fontWeight": "bold",
                        "color": "#0078D4",
                    }
                },
                {
                    "name": "TotalRequestsCard",
                    "type": "Card",
                    "properties": {
                        "title": "Total Requests",
                        "value": "=CountRows(ServiceRequests)",
                    }
                },
                {
                    "name": "OpenRequestsCard",
                    "type": "Card",
                    "properties": {
                        "title": "Open Requests",
                        "value": "=CountIf(ServiceRequests, Status=\"Open\")",
                    }
                },
                {
                    "name": "HighPriorityCard",
                    "type": "Card",
                    "properties": {
                        "title": "High Priority",
                        "value": "=CountIf(ServiceRequests, Priority=\"High\")",
                    }
                },
                {
                    "name": "MyRequestsCard",
                    "type": "Card",
                    "properties": {
                        "title": "Assigned to Me",
                        "value": "=CountIf(ServiceRequests, 'Assigned To'=User().Email)",
                    }
                },
            ]
        }
    
    @staticmethod
    def build_requests_list_screen() -> dict:
        """Build requests list/gallery screen."""
        return {
            "name": "RequestsListScreen",
            "title": "Service Requests",
            "controls": [
                {
                    "name": "HeaderLabel",
                    "type": "Label",
                    "properties": {
                        "text": "All Service Requests",
                        "fontSize": 28,
                        "fontWeight": "bold",
                    }
                },
                {
                    "name": "SearchBox",
                    "type": "TextInput",
                    "properties": {
                        "placeholder": "Search by ID or customer...",
                        "width": "100%",
                    }
                },
                {
                    "name": "StatusFilter",
                    "type": "Dropdown",
                    "properties": {
                        "items": ["All", "Open", "In Progress", "Closed"],
                        "defaultValue": "All",
                    }
                },
                {
                    "name": "RequestsGallery",
                    "type": "Gallery",
                    "properties": {
                        "items": "=Filter(ServiceRequests, If(StatusFilter.Value=\"All\", true, Status=StatusFilter.Value))",
                        "layout": "List",
                        "fields": [
                            {"name": "requestId", "header": "Request ID"},
                            {"name": "customer", "header": "Customer"},
                            {"name": "serviceType", "header": "Service Type"},
                            {"name": "status", "header": "Status"},
                            {"name": "priority", "header": "Priority"},
                        ]
                    }
                },
            ]
        }
    
    @staticmethod
    def build_create_request_screen() -> dict:
        """Build create/edit request form screen."""
        return {
            "name": "CreateRequestScreen",
            "title": "Create Service Request",
            "controls": [
                {
                    "name": "FormTitle",
                    "type": "Label",
                    "properties": {
                        "text": "New Service Request",
                        "fontSize": 28,
                        "fontWeight": "bold",
                    }
                },
                {
                    "name": "CustomerInput",
                    "type": "TextInput",
                    "properties": {
                        "label": "Customer Name",
                        "required": True,
                    }
                },
                {
                    "name": "ServiceTypeDropdown",
                    "type": "Dropdown",
                    "properties": {
                        "label": "Service Type",
                        "items": [
                            "Network Support",
                            "Software Update",
                            "Hardware Repair",
                            "Account Management",
                        ],
                        "required": True,
                    }
                },
                {
                    "name": "PriorityDropdown",
                    "type": "Dropdown",
                    "properties": {
                        "label": "Priority",
                        "items": ["Low", "Medium", "High", "Critical"],
                        "defaultValue": "Medium",
                    }
                },
                {
                    "name": "AssignedToDropdown",
                    "type": "Dropdown",
                    "properties": {
                        "label": "Assign To",
                        "items": [
                            "Alice",
                            "Bob",
                            "Charlie",
                            "Unassigned",
                        ],
                        "defaultValue": "Unassigned",
                    }
                },
                {
                    "name": "DescriptionInput",
                    "type": "TextArea",
                    "properties": {
                        "label": "Description",
                        "height": 150,
                    }
                },
                {
                    "name": "SubmitButton",
                    "type": "Button",
                    "properties": {
                        "text": "Create Request",
                        "onSelect": "=Patch(ServiceRequests, Defaults(ServiceRequests), {customer: CustomerInput.Value, serviceType: ServiceTypeDropdown.Value, priority: PriorityDropdown.Value, 'Assigned To': AssignedToDropdown.Value}); Navigate(RequestsListScreen, ScreenTransition.Fade)",
                    }
                },
            ]
        }
    
    @staticmethod
    def build_request_detail_screen() -> dict:
        """Build request detail/edit screen."""
        return {
            "name": "RequestDetailScreen",
            "title": "Request Details",
            "controls": [
                {
                    "name": "BackButton",
                    "type": "Button",
                    "properties": {
                        "text": "← Back",
                        "onSelect": "Navigate(RequestsListScreen, ScreenTransition.Fade)",
                    }
                },
                {
                    "name": "HeaderLabel",
                    "type": "Label",
                    "properties": {
                        "text": "=Concatenate('Request ID: ', selectedRequest.'Request ID')",
                        "fontSize": 24,
                        "fontWeight": "bold",
                    }
                },
                {
                    "name": "CustomerLabel",
                    "type": "Label",
                    "properties": {
                        "text": "=Concatenate('Customer: ', selectedRequest.customer)",
                    }
                },
                {
                    "name": "ServiceTypeLabel",
                    "type": "Label",
                    "properties": {
                        "text": "=Concatenate('Service Type: ', selectedRequest.'Service Type')",
                    }
                },
                {
                    "name": "StatusDropdown",
                    "type": "Dropdown",
                    "properties": {
                        "label": "Status",
                        "items": ["Open", "In Progress", "Closed"],
                        "defaultValue": "=selectedRequest.Status",
                    }
                },
                {
                    "name": "UpdateButton",
                    "type": "Button",
                    "properties": {
                        "text": "Update Request",
                        "onSelect": "=Patch(ServiceRequests, selectedRequest, {Status: StatusDropdown.Value}); Navigate(RequestsListScreen, ScreenTransition.Fade)",
                    }
                },
            ]
        }


def generate_powerapps_app_config(output_path: Path) -> None:
    """Generate complete PowerApps app configuration."""
    
    app_gen = PowerAppsAppGenerator(
        app_name="ServiceRequestPortal",
        sharepoint_site="https://yourorganization.sharepoint.com/sites/servicerequests"
    )
    
    # Add Excel datasource
    app_gen.add_excel_datasource(
        library="Shared Documents",
        file_name="ServiceRequestWorkbook.xlsx",
        table_name="ServiceRequests"
    )
    
    # Build screens
    screen_builder = PowerAppsScreenBuilder()
    screens = {
        "HomeScreen": screen_builder.build_home_screen(),
        "RequestsListScreen": screen_builder.build_requests_list_screen(),
        "CreateRequestScreen": screen_builder.build_create_request_screen(),
        "RequestDetailScreen": screen_builder.build_request_detail_screen(),
    }
    
    app_gen.screens = screens
    
    # Generate config
    config = app_gen.generate_app_structure()
    
    # Write to file
    with open(output_path, "w") as f:
        json.dump(config, f, indent=2)


if __name__ == "__main__":
    output_file = Path(__file__).parent / "powerapps_app_config.json"
    generate_powerapps_app_config(output_file)
    print(f"Generated PowerApps app config: {output_file}")
