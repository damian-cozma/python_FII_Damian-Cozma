import sys

from cli.cli import SongCLI
from core.config import storage_init, savelists_init
from db.db_init import db_init

def main():
    db_init()
    storage_init()
    savelists_init()

    cli = SongCLI()
    cli.run(sys.argv)


if __name__ == "__main__":
    main()
