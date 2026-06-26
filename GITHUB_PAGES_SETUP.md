# GitHub Pages Service Request Portal

A web-based service request management application hosted on GitHub Pages that connects to Excel Online for data storage.

## Architecture

```
GitHub Pages (Static HTML/CSS/JS)
    ↓
    ├─ Microsoft Authentication (Azure AD)
    │
    └─ Excel Online API
        ↓
    SharePoint / OneDrive
        ↓
    ServiceRequestWorkbook.xlsx
```

## Features

✓ **Dashboard** - View request metrics at a glance
✓ **Request List** - Browse, search, and filter all requests
✓ **Create Request** - Submit new service requests
✓ **Edit Request** - Update status and details
✓ **Delete Request** - Remove outdated requests
✓ **Real-time Sync** - Changes sync instantly to Excel
✓ **Microsoft Login** - Secure authentication via Azure AD
✓ **Mobile Responsive** - Works on desktop, tablet, and mobile
✓ **No Backend Needed** - Fully client-side application

## Files Structure

```
/
├── index.html                    (Main application)
├── assets/
│   └── css/
│       └── style.css            (Styling)
├── config/
│   └── auth-config.js           (Azure AD & Excel config)
├── js/
│   ├── excel-api.js             (Excel Online API)
│   └── app.js                   (Application logic)
├── _config.yml                  (GitHub Pages config)
└── README.md                     (This file)
```

## Prerequisites

1. **Microsoft 365 Account** (Business or higher)
2. **GitHub Account** with a repository
3. **Azure AD Application** registered (for authentication)
4. **Excel Workbook** with service request table
5. **SharePoint Site** or OneDrive for workbook storage

## Setup Instructions

### Step 1: Register Azure AD Application

1. Go to **Azure Portal** (https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **+ New registration**
4. **Name**: `Service Request Portal`
5. **Supported account types**: `Accounts in any organizational directory`
6. **Redirect URI**: `https://yourusername.github.io/testrepo/` (Single-page application)
7. Click **Register**

8. Copy the **Application (client) ID** - you'll need this

9. Go to **API permissions**
   - Click **+ Add a permission**
   - Select **Microsoft Graph**
   - Select **Delegated permissions**
   - Search for and add: `files.readwrite.all`, `sites.readwrite.all`, `user.read`
   - Click **Grant admin consent**

### Step 2: Update Configuration

Edit `config/auth-config.js`:

```javascript
const msalConfig = {
    auth: {
        clientId: "YOUR_CLIENT_ID_HERE",  // Paste your Application ID
        authority: "https://login.microsoftonline.com/common",
        redirectUri: "https://yourusername.github.io/testrepo/"  // Your GitHub Pages URL
    },
    // ... rest of config
};
```

### Step 3: Prepare Excel Workbook

1. Create `ServiceRequestWorkbook.xlsx` with two tables:

**Table 1: ServiceRequests**
```
| Request ID | Customer | Service Type | Status | Priority | Request Date | Assigned To |
|------------|----------|--------------|--------|----------|--------------|-------------|
| REQ-1001   | Acme     | Network      | Open   | High     | 2026-06-01   | Alice       |
```

**Table 2: DashboardMetrics** (Optional)
```
| Metric | Value |
|--------|-------|
| Total  | 1     |
```

2. Upload to **SharePoint** or **OneDrive**
3. Get the file path: right-click → **Share** → **Copy link**

### Step 4: Get SharePoint Information

1. Open your workbook in Excel Online
2. Go to **File** → **Info**
3. Note the **Location** URL
4. Use Microsoft Graph Explorer to find:
   - SharePoint Site ID
   - Drive ID

Example GraphAPI calls:
```
GET https://graph.microsoft.com/v1.0/me/drive
GET https://graph.microsoft.com/v1.0/sites/root
```

### Step 5: Update Excel Configuration

Edit `config/auth-config.js`:

```javascript
const excelConfig = {
    sharePointSiteId: "site-id-from-graph",
    driveId: "drive-id-from-graph",
    workbookPath: "/workbooks/ServiceRequestWorkbook.xlsx",
    requestsTableName: "ServiceRequests",
    dashboardTableName: "DashboardMetrics"
};
```

### Step 6: Deploy to GitHub Pages

1. **Create/Fork Repository**
   ```bash
   git clone https://github.com/yourusername/testrepo
   cd testrepo
   ```

2. **Create `_config.yml`** for GitHub Pages
   ```yaml
   theme: jekyll-theme-slate
   plugins:
     - jekyll-sitemap
   ```

3. **Commit and Push**
   ```bash
   git add -A
   git commit -m "Add Service Request Portal GitHub Pages app"
   git push origin main
   ```

4. **Enable GitHub Pages**
   - Go to repository **Settings** → **Pages**
   - **Source**: `main` branch
   - **Folder**: root (`/`)
   - Click **Save**

5. **Access Your App**
   ```
   https://yourusername.github.io/testrepo/
   ```

## Usage

### Login
1. Click **Login** button
2. Sign in with your Microsoft account
3. Grant permissions for Excel access

### Dashboard
- View metrics: Total, Open, High Priority, Assigned to Me
- Metrics update in real-time
- Click buttons to navigate to other sections

### View Requests
1. Click **Requests** tab
2. **Search** by Request ID or Customer name
3. **Filter** by Status (Open, In Progress, Closed)
4. Click request to view details

### Create Request
1. Click **Create** tab
2. Fill in form:
   - Customer Name (required)
   - Service Type (required)
   - Priority (optional, defaults to Medium)
   - Assigned To (optional)
3. Click **Create Request**
4. Request appears in Excel automatically

### Update Request
1. Click request in list
2. Change **Status** dropdown
3. Click **Update**
4. Changes sync to Excel

### Delete Request
1. Click request in list
2. Click **Delete** button
3. Confirm deletion
4. Request removed from Excel

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Login button doesn't work | Check `clientId` in auth-config.js |
| Can't connect to Excel | Verify SharePoint URL and file path |
| Permission denied errors | Grant admin consent in Azure AD |
| Data not loading | Check Excel table names and structure |
| Changes not appearing in Excel | Verify permissions, try logging out/in |

## API Details

### Excel Online API Endpoints

**Get Table Data:**
```
GET /me/drive/root:{workbookPath}:/workbook/tables/{tableName}/rows
```

**Add Row:**
```
POST /me/drive/root:{workbookPath}:/workbook/tables/{tableName}/rows/add
Body: { values: [[col1, col2, ...]] }
```

**Update Row:**
```
PATCH /me/drive/root:{workbookPath}:/workbook/tables/{tableName}/rows/{index}
Body: { values: [[col1, col2, ...]] }
```

**Delete Row:**
```
DELETE /me/drive/root:{workbookPath}:/workbook/tables/{tableName}/rows/{index}
```

## Security Considerations

✓ **No Backend Needed** - All data stored in your Excel/SharePoint
✓ **Microsoft Authentication** - Uses Azure AD for secure login
✓ **Token Management** - MSAL handles token refresh automatically
✓ **Session Storage** - Tokens cached in browser session only
✓ **HTTPS Only** - GitHub Pages uses HTTPS by default
✓ **Permissions** - Users can only access their own files

**Best Practices:**
- Limit app registration permissions to minimum required
- Use conditional access policies in Azure AD
- Enable MFA for users
- Regularly audit access logs
- Keep ServiceRequestWorkbook.xlsx organized

## Performance Tips

1. **Limit table size** - Archive old requests to another sheet
2. **Use filters** - Reduces data fetched from Excel
3. **Batch operations** - Group creates/updates when possible
4. **Cache data** - App caches requests in memory

## Customization

### Change Styling
Edit `assets/css/style.css` to customize colors and layout:
```css
:root {
    --primary-color: #0078d4;    /* Change this */
    --secondary-color: #107c10;  /* And this */
}
```

### Add More Fields
1. Add columns to Excel table
2. Update parsing in `excel-api.js`
3. Update form in `index.html`

### Add User Permissions
```javascript
// In app.js, modify updateRequest():
if (request.assignedTo !== currentUser.name && !isAdmin(currentUser)) {
    showNotification('You can only edit your own requests', 'error');
    return;
}
```

## Deployment Checklist

- [ ] Azure AD app registered
- [ ] Client ID added to config
- [ ] Excel workbook created and uploaded
- [ ] SharePoint Site ID and Drive ID configured
- [ ] GitHub repository created
- [ ] Files committed and pushed
- [ ] GitHub Pages enabled
- [ ] Tested login flow
- [ ] Tested create request
- [ ] Tested read/update/delete
- [ ] Verified Excel sync works
- [ ] Mobile tested

## Support

- **GitHub Issues**: Use repository issues for bugs/features
- **Microsoft Docs**: https://docs.microsoft.com/graph/
- **Excel API**: https://docs.microsoft.com/excel/api/
- **MSAL.js**: https://github.com/AzureAD/microsoft-authentication-library-for-js

## License

This project is provided as-is. Ensure you have proper Microsoft 365 licenses for Excel Online and SharePoint.

---

**Ready to deploy?** Follow the Setup Instructions above to get started!
