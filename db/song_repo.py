"""
Database access layer for the SongStorage application.

This module contains low-level functions responsible for interacting
with the SQLite database, including CRUD operations and search queries
for song records.
"""

from datetime import datetime
import sqlite3

from core.config import DB_PATH

def insert_song(filename, artist, title, release_date=None, tags=None):
    """
    Insert a new song record into the database.
    """
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
    """
    Retrieve the filename of a song by its ID.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT filename FROM songs WHERE id = ?", (song_id,))

    row = cursor.fetchone()
    conn.close()

    return row

def delete_song(song_id):
    """
    Delete a song record from the database by ID.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM songs WHERE id  = ?", (song_id,))

    conn.commit()
    conn.close()

def edit_song(song_id, artist=None, title=None, release_date=None, tags=None):
    """
    Update one or more metadata fields for an existing song.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    fields = []
    values = []

    if artist is not None:
        fields.append('artist = ?')
        values.append(artist)

    if title is not None:
        fields.append('title = ?')
        values.append(title)

    if release_date is not None:
        fields.append('release_date = ?')
        values.append(release_date)

    if tags is not None:
        fields.append('tags = ?')
        values.append(tags)

    values.append(song_id)

    if not fields:
        conn.close()
        return

    query = "UPDATE songs SET " + ', '.join(fields) + " WHERE id = ?"
    cursor.execute(query, values)

    conn.commit()
    conn.close()

def search_by_fields(artist=None, title=None, release_date=None, tags=None):
    """
    Search for songs matching the provided metadata filters.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    fields = []
    values = []

    if artist is not None:
        fields.append('artist = ?')
        values.append(artist)

    if title is not None:
        fields.append('title = ?')
        values.append(title)

    if release_date is not None:
        fields.append('release_date = ?')
        values.append(release_date)

    if tags is not None:
        fields.append('tags LIKE ?')
        values.append(f"%{tags}%")

    if not fields:
        conn.close()
        return []

    query = "SELECT * FROM songs WHERE " + ' AND '.join(fields)
    cursor.execute(query, values)

    rows = cursor.fetchall()
    conn.close()

    return rows

def search_all():
    """
    Retrieve all song records from the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM songs")
    rows = cursor.fetchall()

    conn.close()
    return rows