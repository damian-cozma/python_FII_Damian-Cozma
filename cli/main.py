import sys

from cli.cli import SongCLI
from db.db_init import db_init
from core.storage_init import storage_init
from core.savelists_init import savelists_init


def main():
    db_init()
    storage_init()
    savelists_init()

    cli = SongCLI()
    cli.run(sys.argv)


if __name__ == "__main__":
    main()
