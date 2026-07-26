import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("hectron_memory.db")

class HectronDB:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS gnosis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT,
                omega REAL
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS decrees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                content TEXT NOT NULL,
                omega REAL,
                status TEXT DEFAULT 'COAGULADO'
            )
        """)
        self.conn.commit()

    def save_decree(self, content: str, omega: float):
        self.conn.execute(
            "INSERT INTO decrees (timestamp, content, omega) VALUES (?, ?, ?)",
            (datetime.now().isoformat(), content, omega)
        )
        self.conn.commit()

    def get_last_decrees(self, limit=20):
        cursor = self.conn.execute(
            "SELECT * FROM decrees ORDER BY id DESC LIMIT ?", (limit,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def coagula(self, key: str, value: str, omega: float = None):
        self.conn.execute(
            "INSERT INTO gnosis (timestamp, key, value, omega) VALUES (?, ?, ?, ?)",
            (datetime.now().isoformat(), key, value, omega)
        )
        self.conn.commit()
