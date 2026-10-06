import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'farmer_queries.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farmer_name TEXT NOT NULL,
        contact TEXT NOT NULL,
        region TEXT NOT NULL,
        category TEXT NOT NULL,
        facility_affected TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        severity TEXT NOT NULL DEFAULT 'Medium',
        status TEXT NOT NULL DEFAULT 'Submitted',
        authority_remarks TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    ''')
    
    # Check if empty, then seed sample queries
    cursor.execute('SELECT COUNT(*) as count FROM queries')
    count = cursor.fetchone()['count']
    
    if count == 0:
        sample_queries = [
            (
                "Ramesh Patel",
                "+91 98765 43210",
                "Nagpur, Maharashtra",
                "Irrigation & Canal Water",
                "Wardha Sub-Canal Outlet #12",
                "Severe water blockage in canal outlet for paddy fields",
                "The primary sluice gate is silted up completely after recent silt deposition. Water is not reaching over 40 acres of standing crop. Immediate de-silting is required.",
                "High",
                "In Progress",
                "Executive Engineer visited site on 20th. Desilting excavator assigned for completion by weekend.",
                "2026-09-18 10:30:00",
                "2026-09-20 14:15:00"
            ),
            (
                "Balwant Singh",
                "+91 94123 78901",
                "Ludhiana, Punjab",
                "Seeds & Fertilizers",
                "District Agricultural Cooperative Center",
                "Shortage of subsidized DAP fertilizer for upcoming wheat sowing",
                "Local cooperative societies have exhausted DAP fertilizer buffer stock. Farmers are being forced to purchase from unregulated private dealers at 30% higher rates.",
                "Urgent",
                "Under Review",
                "Forwarded to District Agriculture Officer for emergency allocation from state buffer.",
                "2026-09-22 09:15:00",
                "2026-09-22 16:40:00"
            ),
            (
                "Lakshmi Devi",
                "+91 91234 56789",
                "Guntur, Andhra Pradesh",
                "Crop Subsidies & Loans",
                "AP Agricultural Credit Service Cell",
                "Delay in PM-Kisan installment and crop loss compensation",
                "Survey was completed in August regarding flood damage, but subsidy compensation has not yet been credited to the registered bank account.",
                "Medium",
                "Resolved",
                "Bank IFSC code discrepancy was rectified. Subsidy payment of Rs. 15,000 dispatched on 23rd Sept.",
                "2026-09-15 11:20:00",
                "2026-09-23 11:00:00"
            ),
            (
                "Manoj Kumar",
                "+91 98220 11223",
                "Indore, Madhya Pradesh",
                "Machinery & Equipment",
                "Custom Hiring Center (CHC) Sanwer",
                "Faulty combine harvester at subsidized Custom Hiring Center",
                "Rented harvester broke down within 2 hours of field operation. CHC staff refuses replacement or rent adjustment.",
                "Medium",
                "Submitted",
                "",
                "2026-09-24 08:45:00",
                "2026-09-24 08:45:00"
            ),
            (
                "Gurpreet Singh",
                "+91 98711 22334",
                "Amritsar, Punjab",
                "Pest & Disease Control",
                "Block Agronomy Extension Unit",
                "Unusual yellowing and viral infection in Cotton crop",
                "Multiple fields are showing rapid leaf curling and yellow mosaic symptoms. Need urgent visit from agricultural extension officer for diagnostic pest control advisory.",
                "High",
                "Submitted",
                "",
                "2026-09-24 18:20:00",
                "2026-09-24 18:20:00"
            )
        ]
        
        cursor.executemany('''
        INSERT INTO queries (
            farmer_name, contact, region, category, facility_affected,
            title, description, severity, status, authority_remarks,
            created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_queries)
    
    conn.commit()
    conn.close()

def row_to_dict(row):
    return dict(row) if row else None

def get_all_queries(status=None, category=None, severity=None, search=None, region=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sql = "SELECT * FROM queries WHERE 1=1"
    params = []
    
    if status and status != 'All':
        sql += " AND status = ?"
        params.append(status)
    if category and category != 'All':
        sql += " AND category = ?"
        params.append(category)
    if severity and severity != 'All':
        sql += " AND severity = ?"
        params.append(severity)
    if region and region != 'All':
        sql += " AND region LIKE ?"
        params.append(f"%{region}%")
    if search:
        sql += " AND (title LIKE ? OR description LIKE ? OR farmer_name LIKE ? OR facility_affected LIKE ?)"
        search_pattern = f"%{search}%"
        params.extend([search_pattern, search_pattern, search_pattern, search_pattern])
        
    sql += " ORDER BY id DESC"
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]

def get_query_by_id(query_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM queries WHERE id = ?", (query_id,))
    row = cursor.fetchone()
    conn.close()
    return row_to_dict(row)

def create_query(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
    INSERT INTO queries (
        farmer_name, contact, region, category, facility_affected,
        title, description, severity, status, authority_remarks,
        created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Submitted', '', ?, ?)
    ''', (
        data.get('farmer_name', '').strip(),
        data.get('contact', '').strip(),
        data.get('region', '').strip(),
        data.get('category', '').strip(),
        data.get('facility_affected', '').strip(),
        data.get('title', '').strip(),
        data.get('description', '').strip(),
        data.get('severity', 'Medium'),
        now,
        now
    ))
    
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return get_query_by_id(new_id)

def update_query(query_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
    UPDATE queries SET
        farmer_name = ?,
        contact = ?,
        region = ?,
        category = ?,
        facility_affected = ?,
        title = ?,
        description = ?,
        severity = ?,
        updated_at = ?
    WHERE id = ?
    ''', (
        data.get('farmer_name', '').strip(),
        data.get('contact', '').strip(),
        data.get('region', '').strip(),
        data.get('category', '').strip(),
        data.get('facility_affected', '').strip(),
        data.get('title', '').strip(),
        data.get('description', '').strip(),
        data.get('severity', 'Medium'),
        now,
        query_id
    ))
    
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return get_query_by_id(query_id) if updated else None

def update_query_status(query_id, status, authority_remarks):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
    UPDATE queries SET
        status = ?,
        authority_remarks = ?,
        updated_at = ?
    WHERE id = ?
    ''', (status, authority_remarks.strip(), now, query_id))
    
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return get_query_by_id(query_id) if updated else None

def delete_query(query_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM queries WHERE id = ?", (query_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def get_statistics():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM queries")
    total = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as submitted FROM queries WHERE status = 'Submitted'")
    submitted = cursor.fetchone()['submitted']
    
    cursor.execute("SELECT COUNT(*) as in_review FROM queries WHERE status IN ('Under Review', 'In Progress')")
    in_review = cursor.fetchone()['in_review']
    
    cursor.execute("SELECT COUNT(*) as resolved FROM queries WHERE status = 'Resolved'")
    resolved = cursor.fetchone()['resolved']
    
    cursor.execute("SELECT COUNT(*) as high_urgency FROM queries WHERE severity IN ('High', 'Urgent')")
    high_urgency = cursor.fetchone()['high_urgency']
    
    cursor.execute("SELECT category, COUNT(*) as count FROM queries GROUP BY category")
    by_category = {row['category']: row['count'] for row in cursor.fetchall()}
    
    conn.close()
    return {
        "total": total,
        "submitted": submitted,
        "in_review": in_review,
        "resolved": resolved,
        "high_urgency": high_urgency,
        "by_category": by_category
    }