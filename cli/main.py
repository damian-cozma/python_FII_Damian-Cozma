"""
Application entry point for the SongStorage CLI.

This module bootstraps the application by initializing required
infrastructure components and starting the command-line interface.
"""

import sys

from cli.cli import SongCLI
from core.config import storage_init, savelists_init
from db.db_init import db_init

def main():
    """
    Initialize application resources and start the CLI execution.
    """
    db_init()
    storage_init()
    savelists_init()

    cli = SongCLI()
    cli.run(sys.argv)


if __name__ == "__main__":
    main()
