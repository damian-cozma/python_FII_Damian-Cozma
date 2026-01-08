"""
Service layer for the SongStorage application.

This module contains the SongService class, which orchestrates business
logic for managing songs, delegating persistence and filesystem operations
to lower-level modules.
"""

from core.file_ops import add_file, delete_file, create_savelist, play_audio
from db.song_repo import insert_song, delete_song, search_by_id, edit_song, search_by_fields, search_all
from core.config import STORAGE_PATH

class SongService:
    """
    Business logic service for song management operations.

    This class coordinates actions such as adding, deleting, editing,
    searching, playing songs, and creating savelists.
    """

    def add_song(self, file, artist, title, release_date=None, tags=None):
        """
        Add a new song to storage and persist its metadata.
        """
        filename = add_file(file)
        return insert_song(filename, artist, title, release_date, tags)

    def delete_song(self, song_id):
        """
        Delete a song and its associated file by ID.
        """
        row = search_by_id(song_id)
        if row is None:
            raise ValueError("Song not found")

        filename = row[0]
        delete_file(filename)
        delete_song(song_id)

    def edit_song(self, song_id, artist=None, title=None, release_date=None, tags=None):
        """
        Update metadata fields for an existing song.
        """
        row = search_by_id(song_id)
        if row is None:
            raise ValueError("Song not found")

        edit_song(song_id, artist, title, release_date, tags)

    def search(self, artist=None, title=None, release_date=None, tags=None, format=None):
        """
        Search for songs using optional metadata filters.

        If no filters are provided, all songs are returned.
        """
        if artist is None and title is None and release_date is None and tags is None:
            return search_all()

        return search_by_fields(
            artist=artist,
            title=title,
            release_date=release_date,
            tags=tags,
            format=format
        )

    def play_song(self, song_id):
        """
        Play an audio file associated with a song by ID.
        """
        row = search_by_id(song_id)
        if row is None:
            raise ValueError("Song not found")

        filename = row[0]
        file_path = STORAGE_PATH / filename
        play_audio(file_path)

    def create_savelist(self, output, artist=None, title=None, release_date=None, tags=None):
        """
        Create a savelist archive based on search criteria.
        """
        rows = search_by_fields(
            artist=artist,
            title=title,
            release_date=release_date,
            tags=tags
        )

        if not rows:
            return []

        create_savelist(output, rows)
        return rows

