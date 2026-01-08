import sys

from core.cli_messages import (
    print_no_command,
    print_unknown_command,
    print_missing_args,
    format_song_row
)
from core.cli_utils import get_flag_value, run_search_from_args
from core.help_texts import HELP_TEXTS
from core.validators import validate_release_date, validate_tags
from core.logger import logger
from core.service import SongService


class SongCLI:
    def __init__(self):
        self.service = SongService()
        self.VALID_COMMANDS = ['add', 'delete', 'edit', 'search', 'savelist', 'play', 'help']

    def run(self, argv):
        if len(argv) == 1:
            print_no_command()
            sys.exit(1)

        command = argv[1]
        args = argv[2:]

        if command not in self.VALID_COMMANDS:
            print_unknown_command(command)
            sys.exit(1)

        handler = getattr(self, f"handle_{command}", None)
        if handler is None:
            print_unknown_command(command)
            sys.exit(1)

        handler(args)

    def handle_add(self, args):
        required = ['--file', '--artist', '--title']

        file = get_flag_value(args, '--file')
        artist = get_flag_value(args, '--artist')
        title = get_flag_value(args, '--title')
        release_date = get_flag_value(args, '--release-date')
        tags = get_flag_value(args, '--tags')

        logger.info(f"ADD command started | file={file} | artist={artist} | title={title}")

        if file is None or artist is None or title is None:
            print_missing_args('add', required)
            logger.error("ADD failed | missing required arguments")
            sys.exit(1)

        try:
            if release_date:
                validate_release_date(release_date)
            if tags:
                validate_tags(tags)

            self.service.add_song(file, artist, title, release_date, tags)

        except Exception as e:
            print(e)
            logger.error(f"ADD failed | error={e}")
            sys.exit(1)

        print(f"Song {artist} - {title} added.")
        logger.info(f"ADD success | artist={artist} | title={title}")

    def handle_delete(self, args):
        required = ['--id']

        song_id = get_flag_value(args, '--id')
        logger.info(f"DELETE command started | id={song_id}")

        if song_id is None:
            print_missing_args('delete', required)
            logger.error("DELETE failed | missing --id")
            sys.exit(1)

        try:
            self.service.delete_song(song_id)

        except ValueError:
            print(f"No song found with id {song_id}")
            logger.error(f"DELETE failed | id={song_id} | song not found")
            sys.exit(1)

        except Exception as e:
            print(e)
            logger.error(f"DELETE failed | id={song_id} | error={e}")
            sys.exit(1)

        print(f"Deleted song {song_id}")
        logger.info(f"DELETE success | id={song_id}")

    def handle_edit(self, args):
        required = ['--id']

        song_id = get_flag_value(args, '--id')
        artist = get_flag_value(args, '--artist')
        title = get_flag_value(args, '--title')
        release_date = get_flag_value(args, '--release-date')
        tags = get_flag_value(args, '--tags')

        logger.info(
            f"EDIT command started | id={song_id} | "
            f"artist={artist} | title={title} | "
            f"release_date={release_date} | tags={tags}"
        )

        if song_id is None:
            print_missing_args('edit', required)
            logger.error("EDIT failed | missing --id")
            sys.exit(1)

        if artist is None and title is None and release_date is None and tags is None:
            print("You must provide at least one field.")
            logger.error(f"EDIT failed | id={song_id} | no fields provided")
            sys.exit(1)

        try:
            if release_date is not None:
                validate_release_date(release_date)
            if tags is not None:
                validate_tags(tags)
        except ValueError as e:
            print(e)
            logger.error(f"EDIT failed | validation error | {e}")
            sys.exit(1)

        try:
            self.service.edit_song(song_id, artist, title, release_date, tags)
        except ValueError:
            print(f"No song found with id {song_id}")
            logger.error(f"EDIT failed | id={song_id} | song not found")
            sys.exit(1)
        except Exception as e:
            print(e)
            logger.error(f"EDIT failed | id={song_id} | error={e}")
            sys.exit(1)

        updated_fields = [
            name for name, value in {
                "artist": artist,
                "title": title,
                "release_date": release_date,
                "tags": tags
            }.items() if value is not None
        ]

        print(
            "Song updated successfully on the following field(s):",
            " ".join(updated_fields)
        )
        logger.info(f"EDIT success | id={song_id} | fields={updated_fields}")

    def handle_search(self, args):
        logger.info(f"SEARCH command started | args={args}")

        artist = get_flag_value(args, '--artist')
        title = get_flag_value(args, '--title')
        release_date = get_flag_value(args, '--release-date')
        tags = get_flag_value(args, '--tags')

        try:
            rows = self.service.search(
                artist=artist,
                title=title,
                release_date=release_date,
                tags=tags
            )

        except Exception as e:
            print(e)
            logger.error(f"SEARCH failed | error={e}")
            sys.exit(1)

        if not rows:
            print("No results found.")
            logger.info("SEARCH success | results=0")
            sys.exit(0)

        for row in rows:
            print(format_song_row(row))

        logger.info(f"SEARCH success | results={len(rows)}")

    def handle_savelist(self, args):
        required = ['--output']

        output = get_flag_value(args, '--output')
        logger.info(f"SAVELIST command started | output={output} | args={args}")

        if output is None:
            print_missing_args('savelist', required)
            logger.error("SAVELIST failed | missing --output")
            sys.exit(1)

        artist = get_flag_value(args, '--artist')
        title = get_flag_value(args, '--title')
        release_date = get_flag_value(args, '--release-date')
        tags = get_flag_value(args, '--tags')

        if artist is None and title is None and release_date is None and tags is None:
            print("You must provide at least one search field.")
            logger.error("SAVELIST failed | no search fields provided")
            sys.exit(1)

        try:
            rows = self.service.create_savelist(
                output=output,
                artist=artist,
                title=title,
                release_date=release_date,
                tags=tags
            )

        except FileExistsError:
            print(f"Savelist '{output}' already exists.")
            logger.error(f"SAVELIST failed | output={output} | already exists")
            sys.exit(1)

        except Exception as e:
            print(e)
            logger.error(f"SAVELIST failed | error={e}")
            sys.exit(1)

        if not rows:
            print("No results found.")
            logger.info(f"SAVELIST success | output={output} | songs=0")
            sys.exit(0)

        print(f"Created savelist '{output}' with {len(rows)} song(s).")
        logger.info(f"SAVELIST success | output={output} | songs={len(rows)}")

    def handle_play(self, args):
        required = ['--id']

        song_id = get_flag_value(args, '--id')
        if song_id is None:
            print_missing_args('play', required)
            sys.exit(1)

        logger.info(f"PLAY command started | id={song_id}")

        try:
            self.service.play_song(song_id)

        except ValueError:
            print(f"No song found with id {song_id}")
            logger.error(f"PLAY failed | id={song_id} | song not found")
            sys.exit(1)

        except Exception as e:
            print(e)
            logger.error(f"PLAY failed | id={song_id} | error={e}")
            sys.exit(1)

        print(f"Playing song with id {song_id}")
        logger.info(f"PLAY success | id={song_id}")

    def handle_help(self, args):
        logger.info(f"HELP command started | args={args}")

        if len(args) == 0:
            print(HELP_TEXTS["main"])
            return

        help_cmd = args[0]
        print(HELP_TEXTS.get(help_cmd, HELP_TEXTS["main"]))