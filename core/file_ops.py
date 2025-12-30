import shutil
import sys
from pathlib import Path

from core.config import STORAGE_PATH, SAVELISTS_PATH


def add_file(file):
    ALLOWED_FORMATS = ['.mp3', '.wav', '.flac']
    file_path = Path(file)

    if not file_path.exists():
        raise FileNotFoundError("File not found.")
    elif not file_path.is_file():
        raise IsADirectoryError("Provided path is not a file.")
    elif file_path.suffix not in ALLOWED_FORMATS:
        raise ValueError("Incompatible format.")
    else:
        dest = STORAGE_PATH / file_path.name

        if dest.exists():
            raise FileExistsError("File already exists.")

        shutil.copy2(file_path, dest)

    return file_path.name

def delete_file(filename):
    file_path = STORAGE_PATH / filename

    if file_path.exists():
        file_path.unlink()

def create_savelist(name, rows):
    file_path = SAVELISTS_PATH / name
    playlist_path = file_path / "playlist.txt"

    if file_path.exists():
        raise FileExistsError("Directory already exists.")

    file_path.mkdir(parents=True)

    for row in rows:
        shutil.copy2(STORAGE_PATH / row[1], file_path)

    with open(playlist_path, "w", encoding="utf-8") as f:
        for row in rows:
            song_id = row[0]
            artist = row[2]
            title = row[3]
            release_date = row[4]
            tags = row[5]

            release_date = release_date if release_date else ""
            tags = tags if tags else ""

            f.write(f"{song_id}|{artist}|{title}|{release_date}|{tags}\n")