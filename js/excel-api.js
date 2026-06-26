// Excel Online / Microsoft Graph API Integration
class ExcelAPI {
    constructor() {
        this.accessToken = null;
        this.requests = [];
    }

    // Get access token
    async getAccessToken() {
        try {
            const account = msalApp.getActiveAccount();
            if (!account) {
                throw new Error('No active account');
            }

            const response = await msalApp.acquireTokenSilent(tokenRequest);
            this.accessToken = response.accessToken;
            return response.accessToken;
        } catch (error) {
            console.error('Error getting token:', error);
            throw error;
        }
    }

    // Fetch data from Excel table
    async getTableData(workbookPath, tableName) {
        try {
            const token = await this.getAccessToken();

            // Get workbook session
            const sessionResponse = await fetch(
                `https://graph.microsoft.com/v1.0/me/drive/root:${workbookPath}:/workbook/createSession`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ persistChanges: true })
                }
            );

            if (!sessionResponse.ok) {
                throw new Error(`Failed to create session: ${sessionResponse.statusText}`);
            }

            const session = await sessionResponse.json();
            const sessionId = session.id;

            // Get table data
            const tableResponse = await fetch(
                `https://graph.microsoft.com/v1.0/me/drive/root:${workbookPath}:/workbook/tables/${tableName}/rows`,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'workbook-session-id': sessionId
                    }
                }
            );

            if (!tableResponse.ok) {
                throw new Error(`Failed to fetch table data: ${tableResponse.statusText}`);
            }

            const data = await tableResponse.json();

            // Close session
            await fetch(
                `https://graph.microsoft.com/v1.0/me/drive/root:${workbookPath}:/workbook/closeSession`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'workbook-session-id': sessionId
                    }
                }
            );

            return data.value || [];
        } catch (error) {
            console.error('Error fetching table data:', error);
            throw error;
        }
    }

    // Add row to Excel table
    async addRow(workbookPath, tableName, rowData) {
        try {
            const token = await this.getAccessToken();

            // Get workbook session
            const sessionResponse = await fetch(
                `https://graph.microsoft.com/v1.0/me/drive/root:${workbookPath}:/workbook/createSession`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ persistChanges: true })
                }
            );

            const session = await sessionResponse.json();
            const sessionId = session.id;

            // Add row to table
            const addResponse = await fetch(
                `https://graph.microsoft.com/v1.0/me/drive/root:${workbookPath}:/workbook/tables/${tableName}/rows/add`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'workbook-session-id': sessionId,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ values: [rowData] })
                }
            );

            if (!addResponse.ok) {
                throw new Error(`Failed to add row: ${addResponse.statusText}`);
            }

            // Close session
            await fetch(
                `https://graph.microsoft.com/v1.0/me/drive/root:${workbookPath}:/workbook/closeSession`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'workbook-session-id': sessionId
                    }
                }
            );

            return await addResponse.json();
        } catch (error) {
            console.error('Error adding row:', error);
            throw error;
        }
    }

    // Update row in Excel table
    async updateRow(workbookPath, tableName, rowIndex, rowData) {
        try {
            const token = await this.getAccessToken();

            // Get workbook session
            const sessionResponse = await fetch(
                `https://graph.microsoft.com/v1.0/me/drive/root:${workbookPath}:/workbook/createSession`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ persistChanges: true })
                }
            );

            const session = await sessionResponse.json();
            const sessionId = session.id;

            // Update row
            const updateResponse = await fetch(
                `https://graph.microsoft.com/v1.0/me/drive/root:${workbookPath}:/workbook/tables/${tableName}/rows/${rowIndex}`,
                {
                    method: 'PATCH',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'workbook-session-id': sessionId,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ values: [rowData] })
                }
            );

            if (!updateResponse.ok) {
                throw new Error(`Failed to update row: ${updateResponse.statusText}`);
            }

            // Close session
            await fetch(
                `https://graph.microsoft.com/v1.0/me/drive/root:${workbookPath}:/workbook/closeSession`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'workbook-session-id': sessionId
                    }
                }
            );

            return await updateResponse.json();
        } catch (error) {
            console.error('Error updating row:', error);
            throw error;
        }
    }

    // Delete row from Excel table
    async deleteRow(workbookPath, tableName, rowIndex) {
        try {
            const token = await this.getAccessToken();

            // Get workbook session
            const sessionResponse = await fetch(
                `https://graph.microsoft.com/v1.0/me/drive/root:${workbookPath}:/workbook/createSession`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ persistChanges: true })
                }
            );

            const session = await sessionResponse.json();
            const sessionId = session.id;

            // Delete row
            const deleteResponse = await fetch(
                `https://graph.microsoft.com/v1.0/me/drive/root:${workbookPath}:/workbook/tables/${tableName}/rows/${rowIndex}`,
                {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'workbook-session-id': sessionId
                    }
                }
            );

            // Close session
            await fetch(
                `https://graph.microsoft.com/v1.0/me/drive/root:${workbookPath}:/workbook/closeSession`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'workbook-session-id': sessionId
                    }
                }
            );

            if (!deleteResponse.ok) {
                throw new Error(`Failed to delete row: ${deleteResponse.statusText}`);
            }

            return true;
        } catch (error) {
            console.error('Error deleting row:', error);
            throw error;
        }
    }

    // Parse Excel row into object
    parseRow(headers, values) {
        const obj = {};
        headers.forEach((header, index) => {
            obj[header] = values[index];
        });
        return obj;
    }
}

// Initialize Excel API
const excelAPI = new ExcelAPI();
