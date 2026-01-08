from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "songs.db"
STORAGE_PATH = BASE_DIR / "storage"
SAVELISTS_PATH = BASE_DIR / "savelists"

def storage_init():
    STORAGE_PATH.mkdir(parents=True, exist_ok=True)

def savelists_init():
    SAVELISTS_PATH.mkdir(parents=True, exist_ok=True)