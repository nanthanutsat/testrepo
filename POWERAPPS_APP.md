# Service Request Portal - PowerApps Canvas App

Complete PowerApps canvas application for your service request management system.

## What's Included

### PowerApps Files

| File | Purpose |
|------|---------|
| `powerapps_app_generator.py` | Python script to generate PowerApps app configuration |
| `powerapps_app_config.json` | PowerApps app structure (screens, controls, formulas) |
| `powerapps_app.fx` | PowerFx code - Copy/paste formulas for all screens |
| `POWERAPPS_SETUP.md` | **START HERE** - Step-by-step setup guide |
| `POWERAPPS_FORMULAS.md` | Reference guide for copy/paste formulas |

### Supporting Files

| File | Purpose |
|------|---------|
| `powerapps_config.py` | Configuration for SharePoint/Azure connections |
| `powerapps_integration.py` | Integration utilities for setup |
| `POWERAPPS_GUIDE.md` | Advanced integration patterns |

## Quick Start (5 minutes)

### 1. Upload Workbook to SharePoint

```bash
# Make sure you have ServiceRequestWorkbook.xlsx
ls -lh ServiceRequestWorkbook.xlsx

# Upload to SharePoint:
# https://yourorg.sharepoint.com/sites/servicerequests/Shared Documents/
```

### 2. Create PowerApps App

1. Go to **https://make.powerapps.com**
2. Click **Create** → **Canvas app**
3. Name it: **Service Request Portal**
4. Layout: **Tablet**
5. Click **Create**

### 3. Add Excel Data Source

1. In designer, click **Data** → **+ Add data**
2. Search for **Excel Online (Business)**
3. Select your SharePoint site
4. Select **ServiceRequestWorkbook.xlsx**
5. Add tables: **ServiceRequests** and **DashboardMetrics**

### 4. Build Screens

Follow the step-by-step guide in `POWERAPPS_SETUP.md`:
- Home Screen (Dashboard)
- Requests List Screen
- Create Request Screen
- Request Detail Screen

### 5. Copy PowerFx Formulas

For each screen and control, copy corresponding formulas from `POWERAPPS_FORMULAS.md` or `powerapps_app.fx`

### 6. Test & Publish

1. Click **Play** (►) to test
2. Verify all screens work
3. Click **File** → **Save** → **Publish**
4. Share with your team

## App Screens

### Screen 1: Home (Dashboard)
```
┌─────────────────────────────────────────┐
│  Service Request Portal                 │
├─────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐               │
│  │ Total   │  │ Open    │               │
│  │ 2       │  │ 1       │               │
│  └─────────┘  └─────────┘               │
│  ┌─────────┐  ┌─────────┐               │
│  │ High    │  │ My      │               │
│  │ Priority│  │ Requests│               │
│  │ 1       │  │ 1       │               │
│  └─────────┘  └─────────┘               │
├─────────────────────────────────────────┤
│ [View All] [Create] [Refresh]           │
└─────────────────────────────────────────┘
```

### Screen 2: Requests List
```
┌─────────────────────────────────────────┐
│  All Service Requests                   │
├─────────────────────────────────────────┤
│ [Search...] [Status ▼]                  │
├─────────────────────────────────────────┤
│ REQ-1001 | Acme Corp | Network | Open  │
│ REQ-1002 | Beta LLC  | Software| Closed│
├─────────────────────────────────────────┤
│ [Back] [+ Create New]                   │
└─────────────────────────────────────────┘
```

### Screen 3: Create Request
```
┌─────────────────────────────────────────┐
│  New Service Request                    │
├─────────────────────────────────────────┤
│ Customer: [________________]             │
│ Service:  [Network Support ▼]            │
│ Priority: [Medium ▼]                     │
│ Assign:   [Unassigned ▼]                 │
│ Notes:    [________________]             │
│           [________________]             │
├─────────────────────────────────────────┤
│ [Create]  [Cancel]                      │
└─────────────────────────────────────────┘
```

### Screen 4: Request Details
```
┌─────────────────────────────────────────┐
│  Request: REQ-1001                      │
├─────────────────────────────────────────┤
│ Customer: Acme Corp                     │
│ Service: Network Support                │
│ Priority: High                          │
│ Status:   [In Progress ▼]                │
│ Assigned: [Alice ▼]                      │
├─────────────────────────────────────────┤
│ [Update] [Delete] [Back]                │
└─────────────────────────────────────────┘
```

## Data Flow

```
PowerApps UI
    ↓
(Create/Edit/Delete)
    ↓
Excel Online
(ServiceRequestWorkbook.xlsx)
    ↓
SharePoint
(Shared Documents)
```

## Key Features Implemented

✓ **Dashboard view** - See all metrics at a glance
✓ **List view** - Browse all requests with search/filter
✓ **Create form** - Submit new service requests
✓ **Detail view** - View and edit request details
✓ **Real-time sync** - Changes sync to Excel instantly
✓ **Validation** - Required field checks
✓ **Notifications** - User feedback on actions
✓ **Navigation** - Smooth screen transitions
✓ **Offline support** - Works without internet (limited)
✓ **Mobile ready** - Responsive design

## Common Tasks

### Add a New Status Option

1. Edit **StatusDropdown** on Create/Detail screens
2. Items property: `["Open", "In Progress", "Closed", "On Hold"]`
3. Update filters in gallery formulas

### Change Request ID Format

Current: `REQ-1001`

To change:
```powerapps
// In Create form Submit button, change:
requestId: Concatenate("SR-", Int(Rand()*100000))
```

### Add Email Notifications

1. Add connection: **Office 365 Outlook**
2. Use formula:
```powerapps
Office365Outlook.SendEmail(
    User().Email,
    "Request Created",
    Concatenate("Request: ", newRequest.requestId)
)
```

### Restrict by User Role

```powerapps
If(
    CountIf(
        Office365Users.GetMyManagerV2().value,
        mail = User().Email
    ) > 0,
    // Show admin controls
    Show_AdminPanel(),
    // Hide admin controls
    Hide_AdminPanel()
)
```

## Troubleshooting

### Data not showing in gallery
- Check Excel table is properly formatted
- Refresh data connection in Power Apps
- Verify SharePoint permissions

### Formulas show red error squiggles
- Check field names match Excel exactly (case-sensitive for some)
- Verify data types (text vs number)
- Use brackets around fields with spaces: `'Request ID'`

### Create button doesn't work
- Verify required fields are not empty
- Check Patch formula syntax
- Look for validation errors

### App is slow
- Reduce gallery items with Filter
- Use collections instead of full data sources
- Optimize filter logic

See `POWERAPPS_SETUP.md` for complete troubleshooting guide.

## Deployment Checklist

- [ ] Workbook uploaded to SharePoint
- [ ] PowerApps app created
- [ ] Excel data source connected
- [ ] All 4 screens built
- [ ] Formulas copied and tested
- [ ] App tested on desktop
- [ ] App tested on mobile
- [ ] Navigation working
- [ ] Form validation working
- [ ] Create/Update/Delete working
- [ ] Notifications displaying
- [ ] App published
- [ ] Users granted access
- [ ] User training completed

## Next Steps

### Immediate
1. Follow `POWERAPPS_SETUP.md` to build the app
2. Test with sample data
3. Share with your team

### Short-term
1. Add email notifications via Power Automate
2. Create mobile-optimized layout
3. Add approval workflow
4. Set up scheduled exports

### Long-term
1. Migrate to Dataverse for better performance
2. Add Power BI dashboard
3. Implement role-based access
4. Create companion mobile app

## Support Resources

- **Power Apps Docs**: https://docs.microsoft.com/en-us/powerapps/
- **Power Apps Community**: https://powerusers.microsoft.com/
- **Formula Reference**: https://docs.microsoft.com/en-us/powerapps/maker/canvas-apps/formula-reference
- **Video Tutorials**: https://www.youtube.com/PowerAppsOfficial

## Files Summary

```
/workspaces/testrepo/
├── ServiceRequestWorkbook.xlsx      (Excel workbook)
├── api_server.py                    (REST API for advanced scenarios)
├── export_workbook.py               (Export Python model to Excel)
├── workbook_definition.py           (Python workbook definition)
│
├── POWERAPPS_SETUP.md               ✓ START HERE
├── POWERAPPS_FORMULAS.md            (Copy/paste formulas)
├── POWERAPPS_GUIDE.md               (Advanced patterns)
├── powerapps_app.fx                 (PowerFx code)
├── powerapps_app_config.json        (App configuration)
├── powerapps_app_generator.py       (Config generator)
├── powerapps_config.py              (Connection config)
└── powerapps_integration.py         (Setup utilities)
```

## License

This PowerApps setup is provided as-is for use with Microsoft 365. Ensure you have appropriate licenses for Power Apps, SharePoint, and Excel Online.

---

**Ready to build?** Start with `POWERAPPS_SETUP.md`
