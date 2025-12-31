import logging
from pathlib import Path

LOG_FILE = Path("songstorage.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ]
)

logger = logging.getLogger("songstorage")
