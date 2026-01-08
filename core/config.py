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
    """
    STORAGE_PATH.mkdir(parents=True, exist_ok=True)

def savelists_init():
    """
    Initialize the directory used for storing savelist archives.
    """
    SAVELISTS_PATH.mkdir(parents=True, exist_ok=True)