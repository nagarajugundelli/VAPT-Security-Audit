from db import initialize_database, save_scan, get_scans
app = Flask(__name__)
initialize_database()
analysis = analyze_scan(scan_result)
import sqlite3

DATABASE = "vapt.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            port_count INTEGER NOT NULL,
            scan_result TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_scan(target, risk_level, port_count, scan_result):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scans
        (target, risk_level, port_count, scan_result)
        VALUES (?, ?, ?, ?)
    """, (
        target,
        risk_level,
        port_count,
        scan_result
    ))

    conn.commit()
    conn.close()


def get_scans():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM scans
        ORDER BY id DESC
    """)

    scans = cursor.fetchall()
    conn.close()

 
   return scans
scans = get_scans()
save_scan(
    target,
    analysis["risk_level"],
    analysis["port_count"],
    scan_result
)
return render_template(
    "index.html",
    scan_result=scan_result,
    target=target,
    analysis=analysis,
    scans=scans
)
