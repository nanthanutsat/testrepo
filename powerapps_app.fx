// Service Request Portal - PowerApps Canvas App
// PowerFx Code for All Screens

// ==========================================
// GLOBAL VARIABLES & SETTINGS
// ==========================================

App.OnStart:
Set(
    gblNavigationMode,
    "Home"
);
Set(
    gblSelectedRequest,
    Blank()
);
Set(
    gblRefreshing,
    false
);
ClearCollect(
    colServiceRequests,
    ServiceRequests
);

// ==========================================
// HOME SCREEN - DASHBOARD
// ==========================================

Screen1_HomeScreen.OnVisible:
Set(
    gblRefreshing,
    true
);
ClearCollect(
    colServiceRequests,
    ServiceRequests
);
Set(
    gblRefreshing,
    false
)

// Dashboard Cards - Metrics
TotalRequestsCard.Items:
[
    {
        Metric: "Total Requests",
        Value: CountRows(colServiceRequests),
        Color: "#0078D4"
    }
]

OpenRequestsCard.Items:
[
    {
        Metric: "Open Requests",
        Value: CountIf(colServiceRequests, status = "Open"),
        Color: "#D83B01"
    }
]

HighPriorityCard.Items:
[
    {
        Metric: "High Priority",
        Value: CountIf(colServiceRequests, priority = "High"),
        Color: "#A4373A"
    }
]

AssignedToMeCard.Items:
[
    {
        Metric: "Assigned to Me",
        Value: CountIf(colServiceRequests, assignedTo = User().Email),
        Color: "#107C10"
    }
]

// Navigation Buttons
NavToRequests.OnSelect:
Navigate(
    Screen2_RequestsList,
    ScreenTransition.Fade
)

NavToCreateRequest.OnSelect:
Navigate(
    Screen3_CreateRequest,
    ScreenTransition.Fade
)

RefreshButton.OnSelect:
Set(gblRefreshing, true);
ClearCollect(colServiceRequests, ServiceRequests);
Set(gblRefreshing, false);
Notify("Data refreshed", NotificationType.Success)


// ==========================================
// REQUESTS LIST SCREEN
// ==========================================

Screen2_RequestsList.OnVisible:
ClearCollect(
    colServiceRequests,
    ServiceRequests
)

// Search & Filter
SearchBox.OnChange:
Set(
    gblSearchTerm,
    SearchBox.Value
)

StatusFilter.OnChange:
Set(
    gblStatusFilter,
    StatusFilter.Value
)

// Gallery Items - Filtered
RequestsGallery.Items:
Filter(
    colServiceRequests,
    (
        If(
            IsBlank(gblStatusFilter) Or gblStatusFilter = "All",
            true,
            status = gblStatusFilter
        ) And
        If(
            IsBlank(gblSearchTerm),
            true,
            Or(
                Search(gblSearchTerm, requestId),
                Search(gblSearchTerm, customer)
            )
        )
    )
)

// Gallery Item Selection
RequestsGallery.OnSelect:
Set(
    gblSelectedRequest,
    ThisItem
);
Navigate(
    Screen4_RequestDetail,
    ScreenTransition.Fade
)

// Action Buttons in Gallery
EditButton.OnSelect:
Set(gblSelectedRequest, ThisItem);
Navigate(Screen4_RequestDetail, ScreenTransition.Fade)

// Back Button
BackButton1.OnSelect:
Navigate(
    Screen1_HomeScreen,
    ScreenTransition.Fade
)

// Create New Button
CreateNewButton.OnSelect:
Navigate(
    Screen3_CreateRequest,
    ScreenTransition.Fade
)


// ==========================================
// CREATE REQUEST SCREEN
// ==========================================

Screen3_CreateRequest.OnVisible:
Reset(CustomerInput);
Reset(ServiceTypeDropdown);
Reset(PriorityDropdown);
Reset(AssignedToDropdown);
Reset(DescriptionInput)

// Form Submission
SubmitButton.OnSelect:
If(
    And(
        Not(IsBlank(CustomerInput.Value)),
        Not(IsBlank(ServiceTypeDropdown.Value))
    ),
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
    Notify("Please fill in all required fields", NotificationType.Error)
)

// Cancel Button
CancelButton.OnSelect:
Navigate(
    Screen2_RequestsList,
    ScreenTransition.Fade
)

// Back Button
BackButton2.OnSelect:
Navigate(
    Screen1_HomeScreen,
    ScreenTransition.Fade
)


// ==========================================
// REQUEST DETAIL SCREEN
// ==========================================

Screen4_RequestDetail.OnVisible:
If(
    IsBlank(gblSelectedRequest),
    Navigate(Screen2_RequestsList, ScreenTransition.Fade)
)

// Display Selected Request Info
RequestIDLabel.Text:
Concatenate("Request: ", gblSelectedRequest.requestId)

CustomerLabel.Text:
Concatenate("Customer: ", gblSelectedRequest.customer)

ServiceTypeLabel.Text:
Concatenate("Service: ", gblSelectedRequest.serviceType)

PriorityLabel.Text:
Concatenate("Priority: ", gblSelectedRequest.priority)

StatusLabel.Default:
gblSelectedRequest.status

AssignedToLabel.Default:
gblSelectedRequest.assignedTo

// Update Request
UpdateButton.OnSelect:
If(
    Not(IsBlank(StatusLabel.Value)),
    Patch(
        ServiceRequests,
        gblSelectedRequest,
        {
            status: StatusLabel.Value,
            assignedTo: AssignedToLabel.Value
        }
    );
    Notify("Request updated successfully", NotificationType.Success);
    ClearCollect(colServiceRequests, ServiceRequests);
    Navigate(Screen2_RequestsList, ScreenTransition.Fade),
    Notify("Cannot update with blank status", NotificationType.Error)
)

// Delete Request
DeleteButton.OnSelect:
If(
    Confirm("Are you sure you want to delete this request?"),
    Remove(ServiceRequests, gblSelectedRequest);
    Notify("Request deleted", NotificationType.Information);
    Navigate(Screen2_RequestsList, ScreenTransition.Fade)
)

// Back Button
BackButton4.OnSelect:
Navigate(
    Screen2_RequestsList,
    ScreenTransition.Fade
)


// ==========================================
// ERROR HANDLING & UTILITIES
// ==========================================

// Global Error Handler
ErrorHandler.Text:
If(
    gblLastError,
    Concatenate(
        "Error: ",
        gblLastError.Description
    ),
    ""
)

// Loading Indicator
LoadingSpinner.Visible:
gblRefreshing

// Offline Mode Check
OfflineIndicator.Visible:
Not(Connection.Connected)
