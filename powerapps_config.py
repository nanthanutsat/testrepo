"""
PowerApps integration configuration and utilities.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class PowerAppsConfig:
    """PowerApps integration configuration."""
    
    # SharePoint/OneDrive settings
    sharepoint_site_url: str
    document_library: str = "Shared Documents"
    folder_path: str = "/workbooks"
    
    # Power Automate settings
    power_automate_enabled: bool = True
    
    # REST API settings
    rest_api_enabled: bool = True
    api_base_url: str = "http://localhost:5000"
    
    # Dataverse settings (optional)
    dataverse_enabled: bool = False
    dataverse_environment: Optional[str] = None
    dataverse_table: str = "cr_servicerequests"


class PowerAppsConnector:
    """Handle PowerApps connectivity and data sync."""
    
    def __init__(self, config: PowerAppsConfig):
        self.config = config
    
    def get_sharepoint_url(self) -> str:
        """Generate SharePoint URL for workbook access."""
        path = self.config.folder_path.lstrip("/")
        return (
            f"{self.config.sharepoint_site_url}/"
            f"{self.config.document_library}/"
            f"{path}/"
        )
    
    def generate_power_automate_flow(self) -> dict:
        """
        Generate Power Automate flow configuration for syncing data.
        This can be imported into Power Automate.
        """
        return {
            "displayName": "Sync Service Requests Workbook",
            "description": "Syncs Excel workbook with PowerApps request portal",
            "triggers": [
                {
                    "type": "recurrence",
                    "frequency": "hour",
                    "interval": 1,
                }
            ],
            "actions": [
                {
                    "name": "ReadExcelWorkbook",
                    "type": "ExcelOnline",
                    "inputs": {
                        "location": self.config.sharepoint_site_url,
                        "path": self.config.folder_path,
                        "file": "ServiceRequestWorkbook.xlsx",
                        "table": "ServiceRequests",
                    }
                },
                {
                    "name": "SyncToDataverse",
                    "type": "Dataverse",
                    "condition": "if(equals(variables('dataverse_enabled'), true))",
                    "inputs": {
                        "environment": self.config.dataverse_environment,
                        "table": self.config.dataverse_table,
                    }
                }
            ]
        }
    
    def get_powerapps_connection_string(self) -> str:
        """
        Get connection string for PowerApps to use Excel as data source.
        """
        return (
            f"Provider=Excel;Data Source={self.config.sharepoint_site_url}/"
            f"{self.config.document_library}/{self.config.folder_path}/"
            f"ServiceRequestWorkbook.xlsx"
        )


def create_default_config() -> PowerAppsConfig:
    """Create a default PowerApps configuration."""
    return PowerAppsConfig(
        sharepoint_site_url="https://yourorganization.sharepoint.com/sites/yoursite",
        document_library="Shared Documents",
        folder_path="/workbooks",
        power_automate_enabled=True,
        rest_api_enabled=True,
    )
