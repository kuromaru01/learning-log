import csv
import sqlite3
from pathlib import Path

DB_PATH = Path("app.db")
CSV_PATH = Path("users.csv")

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            birth_date TEXT
        )
    """)

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f, conn:
        reader = csv.DictReader(f)

        rows = []
        for row in reader:
            user_id = (row.get("user_id") or "").strip()
            name = (row.get("name") or "").strip()
            birth_date = (row.get("birth_date") or "").strip() or None

            if not user_id or not name:
                # 勉強用なので雑にスキップ（実務はエラー収集）
                continue

            rows.append((user_id, name, birth_date))

        conn.executemany(
            "INSERT OR REPLACE INTO users (user_id, name, birth_date) VALUES (?, ?, ?)",
            rows
        )

    conn.close()

if __name__ == "__main__":
    main()
