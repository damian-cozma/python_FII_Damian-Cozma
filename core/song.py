"""
Domain model definitions for the SongStorage application.

This module defines the Song data structure used to represent
song metadata across the application.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Song:
    """
    Data model representing a song and its associated metadata.
    """
    id: Optional[int]
    filename: str
    artist: str
    title: str
    release_date: Optional[str]
    tags: Optional[str]
    format: str
