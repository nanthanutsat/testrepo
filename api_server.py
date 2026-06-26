"""
REST API for PowerApps to consume service request data.
Flask-based API for CRUD operations on service requests.
"""
from flask import Flask, jsonify, request
from workbook_definition import service_request_workbook, formulas
from typing import Dict, List, Any


app = Flask(__name__)


def find_requests_table():
    """Find the ServiceRequests table in the workbook."""
    for worksheet in service_request_workbook.worksheets:
        if worksheet.name == "Requests":
            for table in worksheet.tables:
                if table.name == "ServiceRequests":
                    return table
    return None


@app.route("/api/requests", methods=["GET"])
def get_requests():
    """
    GET /api/requests
    Returns all service requests from the workbook.
    """
    table = find_requests_table()
    if not table:
        return jsonify({"error": "ServiceRequests table not found"}), 404
    
    requests_data = []
    for row in table.rows:
        row_dict = {"id": row.id}
        for col in table.columns:
            value = row.values.get(col.key)
            # Resolve formula keys to actual formulas if needed
            if isinstance(value, str) and value in formulas.formulas:
                row_dict[col.key] = formulas.get(value)
            else:
                row_dict[col.key] = value
        requests_data.append(row_dict)
    
    return jsonify(requests_data)


@app.route("/api/requests/<request_id>", methods=["GET"])
def get_request(request_id):
    """
    GET /api/requests/<request_id>
    Returns a specific service request by ID.
    """
    table = find_requests_table()
    if not table:
        return jsonify({"error": "ServiceRequests table not found"}), 404
    
    for row in table.rows:
        if row.values.get("requestId") == request_id:
            row_dict = {"id": row.id}
            for col in table.columns:
                value = row.values.get(col.key)
                if isinstance(value, str) and value in formulas.formulas:
                    row_dict[col.key] = formulas.get(value)
                else:
                    row_dict[col.key] = value
            return jsonify(row_dict)
    
    return jsonify({"error": "Request not found"}), 404


@app.route("/api/requests", methods=["POST"])
def create_request():
    """
    POST /api/requests
    Create a new service request.
    """
    from workbook_models import Row
    
    data = request.get_json()
    table = find_requests_table()
    if not table:
        return jsonify({"error": "ServiceRequests table not found"}), 404
    
    # Generate new request ID
    max_id = 1000
    for row in table.rows:
        try:
            current_id = int(row.values.get("requestId", "REQ-1000").split("-")[1])
            max_id = max(max_id, current_id)
        except (ValueError, IndexError):
            pass
    
    new_id = f"REQ-{max_id + 1}"
    new_row = Row(
        id=f"row_{len(table.rows) + 1}",
        values={
            "requestId": new_id,
            "customer": data.get("customer", ""),
            "serviceType": data.get("serviceType", ""),
            "status": data.get("status", "Open"),
            "priority": data.get("priority", "Medium"),
            "requestDate": data.get("requestDate", ""),
            "assignedTo": data.get("assignedTo", ""),
            "daysOpen": "daysOpen",
        }
    )
    table.rows.append(new_row)
    
    return jsonify({
        "id": new_row.id,
        "requestId": new_id,
        "message": "Request created successfully"
    }), 201


@app.route("/api/requests/<request_id>", methods=["PUT"])
def update_request(request_id):
    """
    PUT /api/requests/<request_id>
    Update an existing service request.
    """
    data = request.get_json()
    table = find_requests_table()
    if not table:
        return jsonify({"error": "ServiceRequests table not found"}), 404
    
    for row in table.rows:
        if row.values.get("requestId") == request_id:
            # Update allowed fields
            allowed_fields = ["status", "priority", "assignedTo", "serviceType"]
            for field in allowed_fields:
                if field in data:
                    row.values[field] = data[field]
            
            return jsonify({"message": "Request updated successfully"}), 200
    
    return jsonify({"error": "Request not found"}), 404


@app.route("/api/dashboard", methods=["GET"])
def get_dashboard():
    """
    GET /api/dashboard
    Returns dashboard metrics from the Dashboard worksheet.
    """
    table = find_requests_table()
    if not table:
        return jsonify({"error": "ServiceRequests table not found"}), 404
    
    # Calculate metrics
    metrics = {
        "totalRequests": len(table.rows),
        "openRequests": sum(1 for row in table.rows if row.values.get("status") == "Open"),
        "highPriorityRequests": sum(1 for row in table.rows if row.values.get("priority") == "High"),
        "assignedToAlice": sum(1 for row in table.rows if row.values.get("assignedTo") == "Alice"),
    }
    
    return jsonify(metrics)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
