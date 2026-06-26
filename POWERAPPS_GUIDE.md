# PowerApps Integration Guide

This guide explains how to connect your Service Request Workbook with PowerApps to create a request portal.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     PowerApps Canvas App                         │
│                   (Request Portal UI)                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                ┌──────────┴──────────┐
                │                     │
         ┌──────▼──────┐      ┌──────▼──────────────────┐
         │  Excel Data │      │  REST API Server       │
         │  (SharePoint)       │  (api_server.py)       │
         │              │      │  - GET requests        │
         │              │      │  - POST new request    │
         │  Requests    │      │  - PUT update request  │
         │  Dashboard   │      │  - GET metrics         │
         └──────────────┘      └────────────────────────┘
                │                     │
                └──────────────┬──────┘
                               │
                    ┌──────────▼──────────┐
                    │ Power Automate Flow │
                    │ (Optional sync)     │
                    └─────────────────────┘
```

## Setup Steps

### 1. Prepare Your Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Generate the Excel workbook
python export_workbook.py
```

This creates `ServiceRequestWorkbook.xlsx` with:
- **Requests sheet**: Database of all service requests
- **Dashboard sheet**: Summary metrics and KPIs

### 2. Option A: Excel Online in SharePoint

**Best for**: Direct Excel data binding, easiest setup

1. **Upload workbook to SharePoint:**
   ```bash
   # Configure your SharePoint location
   python setup_powerapps.py
   
   # Upload the generated ServiceRequestWorkbook.xlsx to SharePoint
   # Path: https://yourorg.sharepoint.com/sites/servicerequests/Shared Documents/workbooks/
   ```

2. **Create PowerApps Canvas App:**
   - Create new Canvas App
   - Add data source: `Excel Online (Business)`
   - Connect to your SharePoint site
   - Select `ServiceRequestWorkbook.xlsx`
   - Add table: `ServiceRequests`

3. **Add UI Controls:**
   - `Gallery` control: Display all requests from `ServiceRequests` table
   - `Form` control: Create/edit requests
   - `Label` controls: Show dashboard metrics

**Advantages:**
- ✓ Direct Excel binding
- ✓ No server required
- ✓ Data stays in SharePoint
- ✓ Easy to maintain

**Limitations:**
- Limited to Excel's capabilities
- Real-time sync may have delays
- File locking issues with multiple users

### 3. Option B: REST API (Recommended)

**Best for**: Custom logic, real-time updates, advanced features

1. **Start the API Server:**
   ```bash
   python api_server.py
   ```
   Server runs on `http://localhost:5000`

2. **API Endpoints:**

   **List all requests:**
   ```
   GET /api/requests
   Response: [
     {
       "requestId": "REQ-1001",
       "customer": "Acme Corp",
       "status": "Open",
       ...
     }
   ]
   ```

   **Get specific request:**
   ```
   GET /api/requests/REQ-1001
   ```

   **Create new request:**
   ```
   POST /api/requests
   Body: {
     "customer": "Company Name",
     "serviceType": "Network Support",
     "priority": "High",
     "assignedTo": "Alice"
   }
   Response: {"requestId": "REQ-1003", "message": "Request created"}
   ```

   **Update request:**
   ```
   PUT /api/requests/REQ-1001
   Body: {
     "status": "In Progress",
     "assignedTo": "Bob"
   }
   ```

   **Get dashboard metrics:**
   ```
   GET /api/dashboard
   Response: {
     "totalRequests": 2,
     "openRequests": 1,
     "highPriorityRequests": 1,
     "assignedToAlice": 1
   }
   ```

3. **Create PowerApps Connector:**
   - Go to Power Apps → Data → Custom connectors
   - Create new HTTP connector pointing to `http://localhost:5000`
   - Add actions for each endpoint
   - Use in your canvas app

4. **Example PowerApps Formula:**
   ```powerapps
   // Load requests
   OnVisible = Set(
     RequestsList,
     ForAll(
       MyCustomConnector.GetRequests().value,
       {
         ID: requestId,
         Customer: customer,
         Status: status
       }
     )
   );

   // Submit new request
   Button.OnSelect = MyCustomConnector.CreateRequest({
     customer: CustomerInput.Value,
     serviceType: ServiceTypeDropdown.Value,
     priority: PriorityDropdown.Value
   });
   ```

### 4. Option C: Power Automate Sync (Optional)

Use Power Automate to sync between Excel and Dataverse or other systems.

**Flow:** Excel workbook → Power Automate → Dataverse

```
Trigger: "When a file is created or modified" (SharePoint)
  ↓
Action: "Read Excel workbook" (ServiceRequestWorkbook.xlsx)
  ↓
Action: "Create row" or "Update row" (Dataverse)
  ↓
Action: "Send notification" (Teams/Email)
```

Configure in `powerapps_config.py`:
```python
config = PowerAppsConfig(
    sharepoint_site_url="your_url",
    dataverse_enabled=True,
    dataverse_environment="your_environment",
    dataverse_table="cr_servicerequests"
)
```

## Development Workflow

### 1. Add New Feature (e.g., "Resolution Time")

**Step 1: Update formula library**
```python
# In workbook_definition.py
formulas.register("resolutionTime", "=DATEDIF([@[Request Date]], TODAY(), 'D')")
```

**Step 2: Add column to table**
```python
# In ServiceRequests table
Column(key="resolutionTime", header="Resolution Time", type="number", formula="resolutionTime")
```

**Step 3: Update row data**
```python
Row(
    id="row_1",
    values={
        ...
        "resolutionTime": "resolutionTime",  # Formula key reference
    }
)
```

**Step 4: Export and test**
```bash
python export_workbook.py
python api_server.py
```

**Step 5: Verify in PowerApps**
- Refresh data sources
- Check that new column appears
- Test filters/formulas with new data

### 2. Update PowerApps App

- Edit your PowerApps canvas app
- Add new controls or galleries for new columns
- Use formulas to filter/sort by new metrics
- Publish to users

## Testing

### Test API Endpoints
```bash
# Run API tests
python -c "
from api_server import app, find_requests_table

with app.app_context():
    with app.test_client() as client:
        # Test endpoints
        print(client.get('/api/requests').get_json())
        print(client.get('/api/dashboard').get_json())
"
```

### Test Workbook Export
```bash
python export_workbook.py
# Check ServiceRequestWorkbook.xlsx is created
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| PowerApps can't connect to API | Check firewall, ensure port 5000 is open |
| Excel locked in SharePoint | Use Excel Online instead of desktop app |
| Formulas not calculating | Verify Excel is in "Automatic" calculation mode |
| Data not syncing | Restart API server, refresh PowerApps data source |
| Permission errors in SharePoint | Ensure you have Editor access to document library |

## Migration to Production

1. **Set up Azure App Service** to host API server
   - Deploy `api_server.py` to Azure
   - Update connection strings in PowerApps

2. **Move workbook to production SharePoint**
   - Upload to production site
   - Update data source connections in PowerApps

3. **Configure backups**
   - Enable SharePoint versioning
   - Set up automated backups

4. **Security**
   - Enable MFA for SharePoint
   - Use Azure AD authentication for API
   - Restrict API access by role

## Summary

- **Local testing**: Use REST API + Python workbook
- **Team collaboration**: Use Excel in SharePoint
- **Advanced features**: Combine both approaches
- **Production**: Deploy API to Azure, use Dataverse for data storage
