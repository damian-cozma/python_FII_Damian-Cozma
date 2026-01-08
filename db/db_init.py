"""
Database initialization utilities for the SongStorage application.

This module is responsible for creating the SQLite database file
and initializing the required schema if it does not already exist.
"""

import sqlite3
from core.config import DB_PATH

def db_init():
    """
    Initialize the application database and create required tables.

    This function ensures the database directory exists and creates
    the songs table if it is not already present.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL UNIQUE,
            artist TEXT NOT NULL,
            title TEXT NOT NULL,
            release_date TEXT,
            tags TEXT,
            format TEXT NOT NULL,
            added_at TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()