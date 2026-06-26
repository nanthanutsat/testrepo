// Main Application Logic
let msalApp = null;
let currentUser = null;
let allRequests = [];
let filteredRequests = [];

// Initialize MSAL
async function initMSAL() {
    try {
        msalApp = new msal.PublicClientApplication(msalConfig);
        await msalApp.initialize();

        // Check for existing session
        const account = msalApp.getActiveAccount();
        if (account) {
            currentUser = account;
            updateUserUI();
            await refreshData();
        }
    } catch (error) {
        console.error('Error initializing MSAL:', error);
    }
}

// Login with Microsoft
async function loginWithMicrosoft() {
    try {
        const response = await msalApp.loginPopup(loginRequest);
        currentUser = response.account;
        updateUserUI();
        await refreshData();
        showNotification('Logged in successfully', 'success');
    } catch (error) {
        console.error('Login error:', error);
        showNotification('Login failed', 'error');
    }
}

// Logout
function logout() {
    msalApp.logoutPopup({
        postLogoutRedirectUri: window.location.origin
    }).then(() => {
        currentUser = null;
        allRequests = [];
        updateUserUI();
        navigateTo('home');
        showNotification('Logged out', 'success');
    });
}

// Update user UI elements
function updateUserUI() {
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const userInfo = document.getElementById('userInfo');

    if (currentUser) {
        loginBtn.style.display = 'none';
        logoutBtn.style.display = 'block';
        userInfo.textContent = currentUser.name;
        userInfo.style.display = 'inline';
    } else {
        loginBtn.style.display = 'block';
        logoutBtn.style.display = 'none';
        userInfo.style.display = 'none';
    }
}

// Navigate between screens
function navigateTo(screenName) {
    // Hide all screens
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });

    // Show selected screen
    const screen = document.getElementById(screenName + 'Screen');
    if (screen) {
        screen.classList.add('active');
    }

    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    event.target.classList.add('active');
}

// Refresh data from Excel
async function refreshData() {
    if (!currentUser) {
        showNotification('Please login first', 'error');
        return;
    }

    try {
        // Show loading
        const requestsList = document.getElementById('requestsList');
        requestsList.innerHTML = '<div class="spinner"></div>';

        // Fetch requests from Excel
        const rows = await excelAPI.getTableData(
            excelConfig.workbookPath,
            excelConfig.requestsTableName
        );

        // Parse rows
        allRequests = rows.map(row => ({
            requestId: row.values[0],
            customer: row.values[1],
            serviceType: row.values[2],
            status: row.values[3],
            priority: row.values[4],
            requestDate: row.values[5],
            assignedTo: row.values[6]
        }));

        filteredRequests = [...allRequests];
        updateDashboard();
        renderRequestsList();

        showNotification('Data refreshed', 'success');
    } catch (error) {
        console.error('Error refreshing data:', error);
        showNotification('Failed to refresh data', 'error');
    }
}

// Update dashboard metrics
function updateDashboard() {
    const totalCount = allRequests.length;
    const openCount = allRequests.filter(r => r.status === 'Open').length;
    const highCount = allRequests.filter(r => r.priority === 'High').length;
    const myCount = allRequests.filter(r => r.assignedTo === currentUser?.name).length;

    document.getElementById('totalRequests').textContent = totalCount;
    document.getElementById('openRequests').textContent = openCount;
    document.getElementById('highPriority').textContent = highCount;
    document.getElementById('myRequests').textContent = myCount;
}

// Filter requests
function filterRequests() {
    const searchTerm = document.getElementById('searchBox').value.toLowerCase();
    const statusFilter = document.getElementById('statusFilter').value;

    filteredRequests = allRequests.filter(request => {
        const matchesSearch = !searchTerm ||
            request.requestId.toLowerCase().includes(searchTerm) ||
            request.customer.toLowerCase().includes(searchTerm);

        const matchesStatus = !statusFilter || request.status === statusFilter;

        return matchesSearch && matchesStatus;
    });

    renderRequestsList();
}

// Render requests list
function renderRequestsList() {
    const requestsList = document.getElementById('requestsList');

    if (filteredRequests.length === 0) {
        requestsList.innerHTML = '<p style="padding: 20px; text-align: center;">No requests found</p>';
        return;
    }

    requestsList.innerHTML = filteredRequests.map(request => `
        <div class="request-item" onclick="viewRequestDetail('${request.requestId}')">
            <div class="request-info">
                <div class="request-id">${request.requestId}</div>
                <div class="request-customer">${request.customer}</div>
                <div class="request-meta">
                    <span>${request.serviceType}</span>
                    <span class="status-badge ${request.status.toLowerCase().replace(' ', '-')}">${request.status}</span>
                    <span class="priority-badge ${request.priority.toLowerCase()}">${request.priority}</span>
                </div>
            </div>
            <div>
                <button class="btn-secondary" onclick="event.stopPropagation(); viewRequestDetail('${request.requestId}')">View</button>
            </div>
        </div>
    `).join('');
}

// View request detail
function viewRequestDetail(requestId) {
    const request = allRequests.find(r => r.requestId === requestId);
    if (!request) return;

    const detailTitle = document.getElementById('detailTitle');
    const detailContent = document.getElementById('detailContent');

    detailTitle.textContent = `Request: ${request.requestId}`;
    detailContent.innerHTML = `
        <div class="detail-field">
            <div class="detail-label">Customer</div>
            <div class="detail-value">${request.customer}</div>
        </div>
        <div class="detail-field">
            <div class="detail-label">Service Type</div>
            <div class="detail-value">${request.serviceType}</div>
        </div>
        <div class="detail-field">
            <div class="detail-label">Status</div>
            <select id="statusUpdate" class="form-control">
                <option value="Open" ${request.status === 'Open' ? 'selected' : ''}>Open</option>
                <option value="In Progress" ${request.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
                <option value="Closed" ${request.status === 'Closed' ? 'selected' : ''}>Closed</option>
            </select>
        </div>
        <div class="detail-field">
            <div class="detail-label">Priority</div>
            <div class="detail-value">${request.priority}</div>
        </div>
        <div class="detail-field">
            <div class="detail-label">Assigned To</div>
            <div class="detail-value">${request.assignedTo}</div>
        </div>
        <div class="detail-field">
            <div class="detail-label">Request Date</div>
            <div class="detail-value">${request.requestDate}</div>
        </div>
        <div class="detail-actions">
            <button class="btn-primary" onclick="updateRequest('${request.requestId}')">Update</button>
            <button class="btn-danger" onclick="deleteRequest('${request.requestId}')">Delete</button>
            <button class="btn-secondary" onclick="navigateTo('requests')">Back</button>
        </div>
    `;

    navigateTo('detail');
}

// Update request
async function updateRequest(requestId) {
    try {
        const newStatus = document.getElementById('statusUpdate').value;
        const requestIndex = allRequests.findIndex(r => r.requestId === requestId);

        if (requestIndex === -1) return;

        // Update in Excel
        const request = allRequests[requestIndex];
        const rowData = [
            request.requestId,
            request.customer,
            request.serviceType,
            newStatus,
            request.priority,
            request.requestDate,
            request.assignedTo
        ];

        await excelAPI.updateRow(
            excelConfig.workbookPath,
            excelConfig.requestsTableName,
            requestIndex,
            rowData
        );

        showNotification('Request updated successfully', 'success');
        await refreshData();
        navigateTo('requests');
    } catch (error) {
        console.error('Error updating request:', error);
        showNotification('Failed to update request', 'error');
    }
}

// Delete request
async function deleteRequest(requestId) {
    if (!confirm('Are you sure you want to delete this request?')) return;

    try {
        const requestIndex = allRequests.findIndex(r => r.requestId === requestId);
        if (requestIndex === -1) return;

        await excelAPI.deleteRow(
            excelConfig.workbookPath,
            excelConfig.requestsTableName,
            requestIndex
        );

        showNotification('Request deleted successfully', 'success');
        await refreshData();
        navigateTo('requests');
    } catch (error) {
        console.error('Error deleting request:', error);
        showNotification('Failed to delete request', 'error');
    }
}

// Submit new request
async function submitRequest(event) {
    event.preventDefault();

    if (!currentUser) {
        showNotification('Please login first', 'error');
        return;
    }

    try {
        const customer = document.getElementById('customerInput').value;
        const serviceType = document.getElementById('serviceTypeInput').value;
        const priority = document.getElementById('priorityInput').value;
        const assigned = document.getElementById('assignedInput').value;
        const requestId = 'REQ-' + Math.floor(Math.random() * 100000);

        const rowData = [
            requestId,
            customer,
            serviceType,
            'Open',
            priority,
            new Date().toISOString().split('T')[0],
            assigned
        ];

        await excelAPI.addRow(
            excelConfig.workbookPath,
            excelConfig.requestsTableName,
            rowData
        );

        showNotification('Request created successfully', 'success');
        document.getElementById('createForm').reset();
        await refreshData();
        navigateTo('requests');
    } catch (error) {
        console.error('Error creating request:', error);
        showNotification('Failed to create request', 'error');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification show ${type}`;

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Initialize app on page load
window.addEventListener('DOMContentLoaded', () => {
    initMSAL();
});
