import shutil
import sys
from pathlib import Path

from core.config import STORAGE_PATH

def add_file(file):
    ALLOWED_FORMATS = ['.mp3', '.wav', '.flac']
    file_path = Path(file)

    if not file_path.exists():
        print('''
        Incorrect path.
        Use 'songstorage help add' for details.
        ''')
        sys.exit(1)
    elif not file_path.is_file():
        print('''
        Careful! You have provided a directory.
        Use 'songstorage help add' for details.
        ''')
        sys.exit(1)
    elif file_path.suffix not in ALLOWED_FORMATS:
        print(f'''
        Incompatible format.
        Available formats: {ALLOWED_FORMATS}
        ''')
        sys.exit(1)
    else:
        dest = STORAGE_PATH / file_path.name
        shutil.copy2(file_path, dest)

    return file_path.name

def delete_file(filename):
    file_path = STORAGE_PATH / filename
    if file_path.exists():
        file_path.unlink()