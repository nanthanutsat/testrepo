// Microsoft Azure AD Authentication Configuration
const msalConfig = {
    auth: {
        clientId: "YOUR_CLIENT_ID_HERE",
        authority: "https://login.microsoftonline.com/common",
        redirectUri: window.location.origin
    },
    cache: {
        cacheLocation: "sessionStorage",
        storeAuthStateInCookie: false
    }
};

const loginRequest = {
    scopes: ["files.readwrite.all", "Sites.ReadWrite.All"]
};

const tokenRequest = {
    scopes: ["files.readwrite.all", "Sites.ReadWrite.All", "user.read"]
};

// Excel Online Configuration
const excelConfig = {
    sharePointSiteId: "YOUR_SHAREPOINT_SITE_ID_HERE",
    driveId: "YOUR_DRIVE_ID_HERE",
    workbookPath: "/workbooks/ServiceRequestWorkbook.xlsx",
    requestsTableName: "ServiceRequests",
    dashboardTableName: "DashboardMetrics"
};
