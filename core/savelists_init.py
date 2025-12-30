from core.config import SAVELISTS_PATH

def savelists_init():
    SAVELISTS_PATH.mkdir(parents=True, exist_ok=True)