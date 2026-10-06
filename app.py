import os
from flask import Flask, request, jsonify, send_from_directory
import database

app = Flask(__name__, static_folder='static', static_url_path='')

# Initialize database on startup
database.init_db()

CATEGORIES = [
    "Irrigation & Canal Water",
    "Seeds & Fertilizers",
    "Crop Subsidies & Loans",
    "Machinery & Equipment",
    "Pest & Disease Control",
    "Market & MSP Access",
    "Storage & Cold Chain",
    "Electricity & Power Supply",
    "Other Agricultural Facilities"
]

SEVERITIES = ["Low", "Medium", "High", "Urgent"]
STATUSES = ["Submitted", "Under Review", "In Progress", "Resolved", "Rejected"]

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    return jsonify({
        "categories": CATEGORIES,
        "severities": SEVERITIES,
        "statuses": STATUSES
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        stats = database.get_statistics()
        return jsonify({"success": True, "data": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/queries', methods=['GET'])
def get_queries():
    try:
        status = request.args.get('status')
        category = request.args.get('category')
        severity = request.args.get('severity')
        region = request.args.get('region')
        search = request.args.get('search')
        
        queries = database.get_all_queries(
            status=status,
            category=category,
            severity=severity,
            region=region,
            search=search
        )
        return jsonify({"success": True, "data": queries, "count": len(queries)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/queries/<int:query_id>', methods=['GET'])
def get_query(query_id):
    try:
        query = database.get_query_by_id(query_id)
        if not query:
            return jsonify({"success": False, "error": "Query not found"}), 404
        return jsonify({"success": True, "data": query})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/queries', methods=['POST'])
def create_query():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Missing JSON payload"}), 400
            
        required_fields = ['farmer_name', 'contact', 'region', 'category', 'facility_affected', 'title', 'description']
        missing = [f for f in required_fields if not data.get(f) or not str(data.get(f)).strip()]
        if missing:
            return jsonify({
                "success": False, 
                "error": f"Missing required fields: {', '.join(missing)}"
            }), 400
            
        if data.get('severity') and data['severity'] not in SEVERITIES:
            data['severity'] = 'Medium'
            
        created = database.create_query(data)
        return jsonify({"success": True, "data": created, "message": "Query registered successfully!"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/queries/<int:query_id>', methods=['PUT'])
def update_query(query_id):
    try:
        existing = database.get_query_by_id(query_id)
        if not existing:
            return jsonify({"success": False, "error": "Query not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Missing JSON payload"}), 400
            
        required_fields = ['farmer_name', 'contact', 'region', 'category', 'facility_affected', 'title', 'description']
        missing = [f for f in required_fields if not data.get(f) or not str(data.get(f)).strip()]
        if missing:
            return jsonify({
                "success": False, 
                "error": f"Missing required fields: {', '.join(missing)}"
            }), 400
            
        updated = database.update_query(query_id, data)
        return jsonify({"success": True, "data": updated, "message": "Query updated successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/queries/<int:query_id>/status', methods=['PATCH'])
def update_status(query_id):
    try:
        existing = database.get_query_by_id(query_id)
        if not existing:
            return jsonify({"success": False, "error": "Query not found"}), 404
            
        data = request.get_json() or {}
        new_status = data.get('status')
        remarks = data.get('authority_remarks', '')
        
        if not new_status or new_status not in STATUSES:
            return jsonify({
                "success": False, 
                "error": f"Invalid status. Must be one of: {', '.join(STATUSES)}"
            }), 400
            
        updated = database.update_query_status(query_id, new_status, remarks)
        return jsonify({
            "success": True, 
            "data": updated, 
            "message": f"Query status updated to '{new_status}' successfully!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/queries/<int:query_id>', methods=['DELETE'])
def delete_query(query_id):
    try:
        existing = database.get_query_by_id(query_id)
        if not existing:
            return jsonify({"success": False, "error": "Query not found"}), 404
            
        success = database.delete_query(query_id)
        if success:
            return jsonify({"success": True, "message": f"Query #{query_id} has been deleted."})
        else:
            return jsonify({"success": False, "error": "Could not delete query"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Farmer Query Portal Server running on http://127.0.0.1:{port} - app.py:165")
    app.run(host='0.0.0.0', port=port, debug=False)