# PowerApps Setup Guide - Service Request Portal

This guide will walk you through creating and deploying a complete PowerApps canvas application connected to your Excel workbook via Microsoft connections.

## Prerequisites

✓ Microsoft 365 account (or Office 365)
✓ Power Apps license (included with Microsoft 365)
✓ SharePoint site set up
✓ ServiceRequestWorkbook.xlsx uploaded to SharePoint
✓ Excel data source configured

## Step 1: Upload Workbook to SharePoint

1. Go to your **SharePoint site**
2. Navigate to **Shared Documents** (or create a folder named "workbooks")
3. **Upload** `ServiceRequestWorkbook.xlsx`
4. Copy the full file path (you'll need this later)

Example: `https://yourorg.sharepoint.com/sites/servicerequests/Shared Documents/workbooks/ServiceRequestWorkbook.xlsx`

## Step 2: Create PowerApps Canvas App

### Option A: Start from Blank

1. Go to **https://make.powerapps.com**
2. Click **+ Create** → **Canvas app**
3. Name it: `Service Request Portal`
4. Choose **Tablet** or **Phone + Tablet** layout
5. Click **Create**

### Option B: Start from Excel (Recommended)

1. Go to **SharePoint** → Navigate to your workbook
2. Click **ServiceRequestWorkbook.xlsx**
3. Click **Integrate** → **Power Apps** → **Create an app**
4. Select the **ServiceRequests** table
5. Power Apps automatically creates a basic 3-screen app
6. Click **Create**

## Step 3: Add Data Connection

If using Option A:

1. In Power Apps Designer, go to **Data**
2. Click **+ Add data**
3. Select **Excel Online (Business)**
4. Sign in with your Microsoft account
5. Select your **SharePoint site**
6. Select **Shared Documents** (or your folder)
7. Select **ServiceRequestWorkbook.xlsx**
8. Check both tables: **ServiceRequests** and **DashboardMetrics**
9. Click **Connect**

## Step 4: Build the App - Quick Start

### Home Screen (Dashboard)

Replace the default screen with this layout:

**Add Components:**

1. **Add a Label** (Header)
   - Text: `"Service Request Portal"`
   - Font Size: 32
   - Font Weight: Bold
   - Color: RGB(0, 120, 212) - Microsoft Blue

2. **Add 4 Cards** (Metrics)
   ```
   Card 1 - Total Requests:
   Items: [{Metric: "Total Requests", Value: CountRows(ServiceRequests)}]
   
   Card 2 - Open Requests:
   Items: [{Metric: "Open Requests", Value: CountIf(ServiceRequests, Status="Open")}]
   
   Card 3 - High Priority:
   Items: [{Metric: "High Priority", Value: CountIf(ServiceRequests, Priority="High")}]
   
   Card 4 - My Requests:
   Items: [{Metric: "Assigned to Me", Value: CountIf(ServiceRequests, 'Assigned To'=User().Email)}]
   ```

3. **Add Navigation Buttons**
   ```
   Button 1 - View All Requests
   OnSelect: Navigate(Screen2_RequestsList, ScreenTransition.Fade)
   
   Button 2 - Create Request
   OnSelect: Navigate(Screen3_CreateRequest, ScreenTransition.Fade)
   
   Button 3 - Refresh
   OnSelect: ClearCollect(colServiceRequests, ServiceRequests); Notify("Data refreshed", NotificationType.Success)
   ```

### Requests List Screen

1. **Add Search Box**
   ```
   TextInput: SearchBox
   Placeholder: "Search by ID or customer..."
   OnChange: Set(gblSearchTerm, SearchBox.Value)
   ```

2. **Add Status Filter Dropdown**
   ```
   Items: ["All", "Open", "In Progress", "Closed"]
   OnChange: Set(gblStatusFilter, Dropdown.Value)
   ```

3. **Add Gallery**
   ```
   Name: RequestsGallery
   Data source: ServiceRequests
   Items formula:
   Filter(
       ServiceRequests,
       (If(IsBlank(gblStatusFilter) Or gblStatusFilter="All", true, Status=gblStatusFilter)) And
       (If(IsBlank(gblSearchTerm), true, Or(Search(gblSearchTerm, 'Request ID'), Search(gblSearchTerm, customer))))
   )
   
   Layout: List
   Display fields:
   - Request ID
   - Customer
   - Service Type
   - Status
   - Priority
   ```

4. **Add Buttons in Gallery**
   ```
   Edit Button:
   OnSelect: Set(gblSelectedRequest, ThisItem); Navigate(Screen4_RequestDetail, ScreenTransition.Fade)
   ```

### Create Request Screen

1. **Add Form Controls**
   ```
   Customer Input (TextInput):
   Label: "Customer Name *"
   Required: true
   
   Service Type Dropdown:
   Items: ["Network Support", "Software Update", "Hardware Repair", "Account Management"]
   Label: "Service Type *"
   
   Priority Dropdown:
   Items: ["Low", "Medium", "High", "Critical"]
   Label: "Priority"
   DefaultValue: "Medium"
   
   Assigned To Dropdown:
   Items: ["Alice", "Bob", "Charlie", "Unassigned"]
   Label: "Assign To"
   
   Description TextArea:
   Label: "Description"
   ```

2. **Add Submit Button**
   ```
   Text: "Create Request"
   OnSelect:
   If(
       And(Not(IsBlank(CustomerInput.Value)), Not(IsBlank(ServiceTypeDropdown.Value))),
       Patch(
           ServiceRequests,
           Defaults(ServiceRequests),
           {
               customer: CustomerInput.Value,
               serviceType: ServiceTypeDropdown.Value,
               status: "Open",
               priority: PriorityDropdown.Value,
               requestDate: Today(),
               assignedTo: AssignedToDropdown.Value,
               requestId: Concatenate("REQ-", Int(Rand()*100000))
           }
       );
       Notify("Request created successfully", NotificationType.Success);
       Navigate(Screen2_RequestsList, ScreenTransition.Fade),
       Notify("Please fill in required fields", NotificationType.Error)
   )
   ```

### Request Detail Screen

1. **Add Details Display**
   ```
   Label - Request ID:
   Text: Concatenate("Request: ", gblSelectedRequest.requestId)
   
   Label - Customer:
   Text: Concatenate("Customer: ", gblSelectedRequest.customer)
   
   Label - Service Type:
   Text: Concatenate("Service: ", gblSelectedRequest.serviceType)
   ```

2. **Add Editable Dropdowns**
   ```
   Status Dropdown:
   Items: ["Open", "In Progress", "Closed"]
   DefaultValue: gblSelectedRequest.status
   
   Assigned To Dropdown:
   Items: ["Alice", "Bob", "Charlie", "Unassigned"]
   DefaultValue: gblSelectedRequest.'Assigned To'
   ```

3. **Add Action Buttons**
   ```
   Update Button:
   OnSelect:
   Patch(ServiceRequests, gblSelectedRequest, {status: StatusDropdown.Value, 'Assigned To': AssignedToDropdown.Value});
   Notify("Updated successfully", NotificationType.Success);
   Navigate(Screen2_RequestsList, ScreenTransition.Fade)
   
   Delete Button:
   OnSelect:
   If(Confirm("Delete this request?"), Remove(ServiceRequests, gblSelectedRequest); Navigate(Screen2_RequestsList, ScreenTransition.Fade))
   ```

## Step 5: Add Global Variables

Add to App.OnStart:

```powerapps
Set(gblNavigationMode, "Home");
Set(gblSelectedRequest, Blank());
Set(gblRefreshing, false);
ClearCollect(colServiceRequests, ServiceRequests)
```

## Step 6: Configure Connections

1. Go to **Settings** → **Connections**
2. Ensure **Excel Online (Business)** is connected
3. Verify **SharePoint** connection is active
4. (Optional) Add **Office 365 Users** for user lookups

## Step 7: Style & Theme

1. Go to **Settings** → **Display**
2. Choose a **Theme** (light/dark mode)
3. Set **Accent color** to your brand color
4. Apply **Font** consistency

## Step 8: Test the App

### Functional Tests

✓ **Home Screen**
  - Metrics display correct counts
  - Navigation buttons work
  - Refresh button updates data

✓ **Requests List**
  - Gallery shows all requests
  - Search filters by ID and customer
  - Status dropdown filters correctly
  - Click to view detail works

✓ **Create Request**
  - Form validates required fields
  - Submitting creates new row in Excel
  - Redirects to list after creation

✓ **Request Detail**
  - Shows correct request info
  - Can update status and assignee
  - Delete confirmation works

### Data Flow Tests

1. Create a request in PowerApps
2. Check Excel workbook - new row should appear
3. Refresh app - new request should be visible
4. Update request status in PowerApps
5. Check Excel - status should be updated

## Step 9: Publish & Share

### Publish

1. Click **File** → **Save**
2. Click **Publish** → **Publish this version**
3. Select **Specific people** (if controlling access)

### Share with Users

1. In Power Apps home, find your app
2. Click **...** → **Share**
3. Enter email addresses
4. Choose permission level: **Edit** or **Play**
5. Click **Share**

### Make App Mobile

1. In app designer, click **Settings**
2. Enable **Phone layout**
3. Adjust controls for mobile screens
4. Test on mobile device/emulator

## Step 10: Add Advanced Features (Optional)

### Approval Workflow

Add a **Approval Status** column to track:

```powerapps
ApprovalDropdown.Items: ["Pending", "Approved", "Rejected"]

ApproveButton.OnSelect:
Patch(ServiceRequests, gblSelectedRequest, {
    approvalStatus: "Approved",
    approvedBy: User().Email,
    approvalDate: Now()
})
```

### Email Notifications

Connect to **Office 365 Outlook**:

```powerapps
Office365Outlook.SendEmail(
    User().Email,
    "Request Created: " & gblSelectedRequest.requestId,
    Concatenate("Customer: ", gblSelectedRequest.customer)
)
```

### File Attachments

Add **Power Apps attachments** (Premium feature):

```powerapps
Attachments_1.Data Source: ServiceRequests
Attachments_1.Record ID: gblSelectedRequest.requestId
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Can't see ServiceRequests table | Reload page, re-add data connection |
| Formula errors (red squiggles) | Check field names match Excel exactly |
| App runs slow | Reduce gallery items, use Filter instead of full collection |
| Excel won't update | Refresh connection, ensure SharePoint access |
| Users can't see data | Check SharePoint permissions, Excel share settings |

## Monitoring & Maintenance

### Check Analytics

1. Published app → **Analytics**
2. View usage metrics
3. Identify slow screens
4. Monitor error rates

### Update Data Source

When you add new columns to Excel:

1. Go to Power Apps Designer
2. Click **Data** → Find Excel connection
3. Click **Refresh** icon
4. New columns should appear

### Backup App

1. Published app → **...** → **Details**
2. Click **Export**
3. Save `.msapp` file

## Production Checklist

- [ ] Workbook uploaded and accessible
- [ ] All data connections working
- [ ] App tested with actual data
- [ ] Navigation working on all screens
- [ ] Form validation working
- [ ] Mobile layout tested
- [ ] Offline mode handled
- [ ] Error messages clear
- [ ] Performance acceptable
- [ ] Users can access app
- [ ] Training documentation ready
- [ ] Support plan in place

## Next Steps

1. **Extend with Power Automate**: Add automated email notifications
2. **Add Power BI Dashboard**: Embed report in PowerApps
3. **Use Dataverse**: Move to enterprise-grade data storage
4. **Mobile App**: Publish to iOS/Android
5. **Multi-tenant**: Share across organization

## Support

- Power Apps docs: https://docs.microsoft.com/en-us/powerapps/
- Community: https://powerusers.microsoft.com/
- Microsoft Support: https://support.microsoft.com/
