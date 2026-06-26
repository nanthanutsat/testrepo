"""
Integration module to sync workbook with PowerApps.
Handles export to SharePoint and API startup.
"""
import json
from pathlib import Path
from powerapps_config import PowerAppsConfig, PowerAppsConnector


def update_powerapps_config(
    sharepoint_url: str,
    document_library: str = "Shared Documents",
    folder_path: str = "/workbooks",
) -> PowerAppsConfig:
    """
    Update PowerApps configuration with your SharePoint details.
    
    Args:
        sharepoint_url: Your SharePoint site URL
        document_library: Document library name (default: Shared Documents)
        folder_path: Folder path in the library (default: /workbooks)
    
    Returns:
        Updated PowerAppsConfig instance
    """
    config = PowerAppsConfig(
        sharepoint_site_url=sharepoint_url,
        document_library=document_library,
        folder_path=folder_path,
    )
    
    # Save config to file for reference
    config_file = Path(__file__).parent / "powerapps_config.json"
    with open(config_file, "w") as f:
        json.dump({
            "sharepoint_site_url": config.sharepoint_site_url,
            "document_library": config.document_library,
            "folder_path": config.folder_path,
            "power_automate_enabled": config.power_automate_enabled,
            "rest_api_enabled": config.rest_api_enabled,
        }, f, indent=2)
    
    return config


def load_powerapps_config() -> PowerAppsConfig:
    """Load PowerApps configuration from file."""
    config_file = Path(__file__).parent / "powerapps_config.json"
    
    if not config_file.exists():
        raise FileNotFoundError(
            f"PowerApps config not found at {config_file}. "
            "Run update_powerapps_config() first."
        )
    
    with open(config_file) as f:
        data = json.load(f)
    
    return PowerAppsConfig(
        sharepoint_site_url=data["sharepoint_site_url"],
        document_library=data["document_library"],
        folder_path=data["folder_path"],
        power_automate_enabled=data.get("power_automate_enabled", True),
        rest_api_enabled=data.get("rest_api_enabled", True),
    )


if __name__ == "__main__":
    # Example: Update your SharePoint configuration
    # Replace with your actual SharePoint details
    config = update_powerapps_config(
        sharepoint_url="https://yourorganization.sharepoint.com/sites/servicerequests",
        document_library="Shared Documents",
        folder_path="/workbooks",
    )
    
    connector = PowerAppsConnector(config)
    print(f"SharePoint URL: {connector.get_sharepoint_url()}")
    print(f"Connection String: {connector.get_powerapps_connection_string()}")
