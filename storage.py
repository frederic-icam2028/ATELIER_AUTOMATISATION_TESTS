import sqlite3
import json
from datetime import datetime

DB_NAME = "runs.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            api TEXT NOT NULL,
            summary TEXT NOT NULL,
            tests TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_run(result):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO runs (timestamp, api, summary, tests)
        VALUES (?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        result["api"],
        json.dumps(result["summary"]),
        json.dumps(result["tests"])
    ))
    conn.commit()
    conn.close()


def list_runs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, api, summary, tests
        FROM runs
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "timestamp": row[1],
            "api": row[2],
            "summary": json.loads(row[3]),
            "tests": json.loads(row[4]),
        })
    return results
