"""
Application configuration and filesystem paths.

This module defines global configuration values such as base directories
and provides initialization helpers for required filesystem resources.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "songs.db"
STORAGE_PATH = BASE_DIR / "storage"
SAVELISTS_PATH = BASE_DIR / "savelists"

def storage_init():
    """
    Initialize the storage directory used for storing audio files.

    It ensures that all missing parent directories are created as needed,
    while preventing an error from being raised if the directory already exists.
    """
    STORAGE_PATH.mkdir(parents=True, exist_ok=True)

def savelists_init():
    """
    Initialize the directory used for storing savelist archives.

    It ensures that all missing parent directories are created as needed,
    while preventing an error from being raised if the directory already exists.
    """
    SAVELISTS_PATH.mkdir(parents=True, exist_ok=True)