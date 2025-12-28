from datetime import datetime
import sqlite3

from core.config import DB_PATH

def insert_song(filename, artist, title, release_date=None, tags=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO songs (filename, artist, title, release_date, tags, format, added_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        filename,
        artist,
        title,
        release_date,
        tags,
        filename.split('.')[-1],
        datetime.now().isoformat()
    ))

    song_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return song_id

def search_by_id(song_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT filename FROM songs WHERE id = ?", (song_id,))

    row = cursor.fetchone()
    conn.close()

    return row

def delete_song(song_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM songs WHERE id  = ?", (song_id,))

    conn.commit()
    conn.close()