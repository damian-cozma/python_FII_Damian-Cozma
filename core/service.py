from core.file_ops import add_file, delete_file, create_savelist, play_audio
from db.song_repo import insert_song, delete_song, search_by_id, edit_song, search_by_fields, search_all
from core.config import STORAGE_PATH

class SongService:

    def add_song(self, file, artist, title, release_date=None, tags=None):
        filename = add_file(file)
        return insert_song(filename, artist, title, release_date, tags)

    def delete_song(self, song_id):
        row = search_by_id(song_id)
        if row is None:
            raise ValueError("Song not found")

        filename = row[0]
        delete_file(filename)
        delete_song(song_id)

    def edit_song(self, song_id, artist=None, title=None, release_date=None, tags=None):
        row = search_by_id(song_id)
        if row is None:
            raise ValueError("Song not found")

        edit_song(song_id, artist, title, release_date, tags)

    def search(self, artist=None, title=None, release_date=None, tags=None):
        if artist is None and title is None and release_date is None and tags is None:
            return search_all()

        return search_by_fields(
            artist=artist,
            title=title,
            release_date=release_date,
            tags=tags
        )

    def play_song(self, song_id):
        row = search_by_id(song_id)
        if row is None:
            raise ValueError("Song not found")

        filename = row[0]
        file_path = STORAGE_PATH / filename
        play_audio(file_path)

    def create_savelist(self, output, artist=None, title=None, release_date=None, tags=None):
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

