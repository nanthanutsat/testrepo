# PowerApps Quick Reference - Copy/Paste Formulas

Use these formulas directly in your PowerApps controls. Replace placeholder names with your actual control names.

## Navigation Formulas

### Go to Home Screen
```powerapps
Navigate(Screen1_HomeScreen, ScreenTransition.Fade)
```

### Go to Requests List
```powerapps
Navigate(Screen2_RequestsList, ScreenTransition.Fade)
```

### Go to Create Request
```powerapps
Navigate(Screen3_CreateRequest, ScreenTransition.Fade)
```

### Go to Request Detail
```powerapps
Set(gblSelectedRequest, ThisItem);
Navigate(Screen4_RequestDetail, ScreenTransition.Fade)
```

## Data Query Formulas

### Get All Requests
```powerapps
ServiceRequests
```

### Count All Requests
```powerapps
CountRows(ServiceRequests)
```

### Count Open Requests
```powerapps
CountIf(ServiceRequests, Status = "Open")
```

### Count High Priority
```powerapps
CountIf(ServiceRequests, Priority = "High")
```

### Count Requests Assigned to Current User
```powerapps
CountIf(ServiceRequests, 'Assigned To' = User().Email)
```

### Filter by Status
```powerapps
Filter(ServiceRequests, Status = "Open")
```

### Search in Multiple Fields
```powerapps
Filter(ServiceRequests, 
    Or(
        Search(SearchTerm, 'Request ID'),
        Search(SearchTerm, customer)
    )
)
```

### Complex Filter (Status + Search)
```powerapps
Filter(
    ServiceRequests,
    (If(IsBlank(gblStatusFilter) Or gblStatusFilter = "All", true, Status = gblStatusFilter)) And
    (If(IsBlank(gblSearchTerm), true, Or(Search(gblSearchTerm, 'Request ID'), Search(gblSearchTerm, customer))))
)
```

## Form & Data Manipulation

### Create New Request
```powerapps
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
Notify("Request created", NotificationType.Success);
Navigate(Screen2_RequestsList, ScreenTransition.Fade)
```

### Update Request Status
```powerapps
Patch(
    ServiceRequests,
    gblSelectedRequest,
    { status: StatusDropdown.Value }
);
Notify("Updated successfully", NotificationType.Success)
```

### Update Multiple Fields
```powerapps
Patch(
    ServiceRequests,
    gblSelectedRequest,
    {
        status: StatusDropdown.Value,
        'Assigned To': AssignedToDropdown.Value,
        priority: PriorityDropdown.Value
    }
);
Notify("Request updated", NotificationType.Success)
```

### Delete Request
```powerapps
If(
    Confirm("Are you sure you want to delete this request?"),
    Remove(ServiceRequests, gblSelectedRequest);
    Notify("Request deleted", NotificationType.Information);
    Navigate(Screen2_RequestsList, ScreenTransition.Fade),
    Notify("Delete cancelled", NotificationType.Information)
)
```

### Reset Form
```powerapps
Reset(CustomerInput);
Reset(ServiceTypeDropdown);
Reset(PriorityDropdown);
Reset(AssignedToDropdown)
```

## Conditional Logic

### Required Field Validation
```powerapps
If(
    And(
        Not(IsBlank(CustomerInput.Value)),
        Not(IsBlank(ServiceTypeDropdown.Value))
    ),
    // Do something
    Notify("Please fill in all required fields", NotificationType.Error)
)
```

### Check User Permission
```powerapps
If(
    User().Email = "admin@yourorg.com",
    // Show admin options
    Notify("Admin access granted", NotificationType.Information),
    // Hide admin options
    Notify("You don't have permission", NotificationType.Warning)
)
```

### Conditional Status Color
```powerapps
Switch(
    Status,
    "Open", Red,
    "In Progress", Orange,
    "Closed", Green,
    Gray
)
```

## Text & Display Formulas

### Concatenate Request Info
```powerapps
Concatenate("Request ", gblSelectedRequest.'Request ID', " - ", gblSelectedRequest.customer)
```

### Format Date
```powerapps
Text(gblSelectedRequest.requestDate, "mm/dd/yyyy")
```

### Display Days Since Created
```powerapps
Concatenate(
    DateDiff(gblSelectedRequest.requestDate, Today()),
    " days"
)
```

### Format Status with Badge
```powerapps
Concatenate("[", gblSelectedRequest.status, "]")
```

## Collection & Refresh Operations

### Create Collection
```powerapps
ClearCollect(colServiceRequests, ServiceRequests)
```

### Refresh Collection
```powerapps
Set(gblRefreshing, true);
ClearCollect(colServiceRequests, ServiceRequests);
Set(gblRefreshing, false)
```

### Sort Collection
```powerapps
ClearCollect(
    colServiceRequests,
    Sort(ServiceRequests, requestDate, Ascending)
)
```

## User & Context

### Get Current User Email
```powerapps
User().Email
```

### Get Current User Display Name
```powerapps
User().FullName
```

### Get Current Date/Time
```powerapps
Now()
```

### Get Current Date Only
```powerapps
Today()
```

## Notification & Feedback

### Success Notification
```powerapps
Notify("Operation successful", NotificationType.Success)
```

### Error Notification
```powerapps
Notify("An error occurred", NotificationType.Error)
```

### Warning Notification
```powerapps
Notify("Please verify your data", NotificationType.Warning)
```

### Confirmation Dialog
```powerapps
If(
    Confirm("Continue with this action?"),
    // User clicked Yes
    DoSomething(),
    // User clicked No
    Notify("Cancelled", NotificationType.Information)
)
```

## Gallery & List Operations

### Get Selected Item
```powerapps
RequestsGallery.Selected
```

### Get Count of Items in Gallery
```powerapps
CountRows(RequestsGallery.AllItems)
```

### Highlight Selected Row
```powerapps
If(
    ThisItem = RequestsGallery.Selected,
    LightGray,
    White
)
```

## Common Patterns

### Search + Filter Pattern
```powerapps
// In dropdown OnChange:
Set(gblStatusFilter, StatusDropdown.Value)

// In gallery Items:
Filter(
    ServiceRequests,
    (
        If(IsBlank(gblStatusFilter) Or gblStatusFilter = "All", 
           true, 
           Status = gblStatusFilter
        ) And
        If(IsBlank(gblSearchTerm), 
           true, 
           Search(gblSearchTerm, 'Request ID')
        )
    )
)
```

### Load More Pattern
```powerapps
// Gallery Items:
If(
    GalleryScroll.Visible && Abs(GalleryScroll.ScrollPosition - GalleryScroll.Max) < 100,
    Set(gblPageNum, gblPageNum + 1);
    ClearCollect(colAll, colAll, Filter(ServiceRequests, ID > Max(colAll, ID))),
    Filter(ServiceRequests, ...)
)
```

### Master-Detail Pattern
```powerapps
// List Screen - Gallery OnSelect:
Set(gblSelectedRequest, ThisItem);
Navigate(Screen_Detail, ScreenTransition.Fade)

// Detail Screen - OnVisible:
If(IsBlank(gblSelectedRequest), Navigate(Screen_List))
```

## Tips & Best Practices

1. **Use Global Variables** for data that needs to persist: `Set(gbl..., value)`
2. **Use Collections** for filtered/sorted data: `ClearCollect(col..., data)`
3. **Always validate** before submitting: `If(Not(IsBlank(input)), ...)`
4. **Use Notify** for user feedback: `Notify("Message", type)`
5. **Test formulas** in formula bar first: `f(x) =` then copy to control
6. **Reference tables correctly**: Use brackets for spaces: `'Request ID'`
7. **Use ThisItem** in galleries to reference current row
8. **Clear collections** before rebuilding: `ClearCollect(col, ...)`
9. **Set loading state**: Use boolean for spinner visibility
10. **Handle errors**: Wrap Patch with If(ErrorMessage="", success, error)
