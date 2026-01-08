from dataclasses import dataclass
from typing import Optional

@dataclass
class Song:
    id: Optional[int]
    filename: str
    artist: str
    title: str
    release_date: Optional[str]
    tags: Optional[str]
    format: str
