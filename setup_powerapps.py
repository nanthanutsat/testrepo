"""
Setup script for PowerApps integration.
Configure and deploy the request portal integration.
"""
import sys
from pathlib import Path


def setup_powerapps_integration():
    """
    Interactive setup for PowerApps integration.
    """
    print("=" * 60)
    print("PowerApps Request Portal Integration Setup")
    print("=" * 60)
    
    print("\n1. REST API Setup")
    print("-" * 40)
    print("The REST API server allows PowerApps to:")
    print("  - GET /api/requests - List all requests")
    print("  - GET /api/requests/<id> - Get specific request")
    print("  - POST /api/requests - Create new request")
    print("  - PUT /api/requests/<id> - Update request")
    print("  - GET /api/dashboard - Get dashboard metrics")
    print("\nTo start the API server:")
    print("  python api_server.py")
    print("\nThen configure PowerApps connector to http://localhost:5000")
    
    print("\n2. SharePoint Configuration")
    print("-" * 40)
    sharepoint_url = input("Enter your SharePoint site URL: ").strip()
    if not sharepoint_url:
        sharepoint_url = "https://yourorganization.sharepoint.com/sites/servicerequests"
        print(f"Using default: {sharepoint_url}")
    
    document_library = input("Enter document library name (default: Shared Documents): ").strip()
    if not document_library:
        document_library = "Shared Documents"
    
    folder_path = input("Enter folder path (default: /workbooks): ").strip()
    if not folder_path:
        folder_path = "/workbooks"
    
    # Save configuration
    from powerapps_integration import update_powerapps_config
    config = update_powerapps_config(sharepoint_url, document_library, folder_path)
    
    print(f"\n✓ Configuration saved to powerapps_config.json")
    print(f"  SharePoint URL: {config.sharepoint_site_url}")
    print(f"  Document Library: {config.document_library}")
    print(f"  Folder Path: {config.folder_path}")
    
    print("\n3. Next Steps")
    print("-" * 40)
    print("1. Upload ServiceRequestWorkbook.xlsx to SharePoint:")
    print(f"   {config.sharepoint_site_url}/{config.document_library}/{config.folder_path}/")
    print("\n2. Create PowerApps canvas app:")
    print("   - Add data source: Excel Online (Business)")
    print("   - Connect to ServiceRequestWorkbook.xlsx")
    print("   - Select ServiceRequests table")
    print("\n3. Add REST API connector (optional):")
    print("   - Use Custom Connector or HTTP action")
    print("   - Point to REST API endpoints listed above")
    print("\n4. Set up Power Automate flow (optional):")
    print("   - Sync Excel data to Dataverse")
    print("   - Trigger on file changes")
    print("\n4. Test the integration:")
    print("   - Open PowerApps app")
    print("   - Verify data loads from workbook")
    print("   - Test create/update operations")


def install_dependencies():
    """Install Python dependencies."""
    print("Installing dependencies...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


if __name__ == "__main__":
    try:
        setup_powerapps_integration()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
