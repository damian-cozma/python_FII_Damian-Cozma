import shutil
import sys
from pathlib import Path

from core.config import STORAGE_PATH

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