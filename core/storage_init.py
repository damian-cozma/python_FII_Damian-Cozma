from core.config import STORAGE_PATH

def storage_init():
    STORAGE_PATH.mkdir(parents=True, exist_ok=True)