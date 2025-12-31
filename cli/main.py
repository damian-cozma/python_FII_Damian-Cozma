import sys

from core.cli_messages import print_no_command, print_unknown_command, print_missing_args, format_song_row
from core.cli_utils import get_flag_value, run_search_from_args
from core.config import STORAGE_PATH
from core.file_ops import add_file, delete_file, create_savelist, play_audio
from core.help_texts import HELP_TEXTS
from core.savelists_init import savelists_init
from core.storage_init import storage_init
from core.validators import validate_release_date, validate_tags
from db.db_init import db_init
from db.song_repo import insert_song, search_by_id, delete_song, edit_song
from core.logger import logger

db_init()
storage_init()
savelists_init()
VALID_COMMANDS = ['add', 'delete', 'edit', 'search', 'savelist', 'play', 'help']

arg_size = len(sys.argv)

if arg_size == 1:
    print_no_command()
    sys.exit(1)

command = sys.argv[1]
args = sys.argv[2:]

if command not in VALID_COMMANDS:
    print_unknown_command(command)
    sys.exit(1)

if command == 'add':
    required = ['--file', '--artist', '--title']

    file = get_flag_value(args, '--file')
    artist = get_flag_value(args, '--artist')
    title = get_flag_value(args, '--title')
    release_date = get_flag_value(args, '--release-date')
    tags = get_flag_value(args, '--tags')

    logger.info(f"ADD command started | file={file} | artist={artist} | title={title}")

    if file is None or artist is None or title is None:
        print_missing_args(command, required)
        logger.error("ADD failed | missing required arguments")
        sys.exit(1)

    try:
        if release_date is not None:
            validate_release_date(release_date)
        if tags is not None:
            validate_tags(tags)
    except ValueError as e:
        print(e)
        logger.error(f"ADD failed | validation error | {e}")
        sys.exit(1)

    filename = None
    try:
        filename = add_file(file)
        insert_song(filename, artist, title, release_date, tags)
    except Exception as e:
        if filename:
            delete_file(filename)
        print(e)
        logger.error(f"ADD failed | file={file} | error={e}")
        sys.exit(1)

    print(f'Song {artist} - {title} added.')
    logger.info(f"ADD success | file={filename} | artist={artist} | title={title}")

elif command == 'delete':
    required = ['--id']

    song_id = get_flag_value(args, '--id')
    logger.info(f"DELETE command started | id={song_id}")

    if song_id is None:
        print_missing_args(command, required)
        logger.error("DELETE failed | missing --id")
        sys.exit(1)

    row = search_by_id(song_id)
    if row is None:
        print(f"No song found with id {song_id}")
        logger.error(f"DELETE failed | id={song_id} | song not found")
        sys.exit(1)

    filename = row[0]

    try:
        delete_file(filename)
        delete_song(song_id)
    except Exception as e:
        print(e)
        logger.error(f"DELETE failed | id={song_id} | file={filename} | error={e}")
        sys.exit(1)

    print(f"Deleted song {song_id}")
    logger.info(f"DELETE success | id={song_id} | file={filename}")

elif command == 'edit':
    required = ['--id']

    song_id = get_flag_value(args, '--id')

    artist = get_flag_value(args, '--artist')
    title = get_flag_value(args, '--title')
    release_date = get_flag_value(args, '--release-date')
    tags = get_flag_value(args, '--tags')

    logger.info(
        f"EDIT command started | id={song_id} | "
        f"artist={artist} | title={title} | release_date={release_date} | tags={tags}"
    )

    if song_id is None:
        print_missing_args(command, required)
        logger.error("EDIT failed | missing --id")
        sys.exit(1)

    row = search_by_id(song_id)
    if row is None:
        print(f"No song found with id {song_id}")
        logger.error(f"EDIT failed | id={song_id} | song not found")
        sys.exit(1)

    if artist is None and title is None and release_date is None and tags is None:
        print('You must provide at least one field.')
        logger.error(f"EDIT failed | id={song_id} | no fields provided")
        sys.exit(1)

    try:
        if release_date is not None:
            validate_release_date(release_date)
        if tags is not None:
            validate_tags(tags)
    except ValueError as e:
        print(e)
        logger.error(f"EDIT failed | id={song_id} | validation error | {e}")
        sys.exit(1)

    edit_song(song_id, artist, title, release_date, tags)

    print(f"Updated song {song_id}")

    updated_fields = [k for k, v in {
        "artist": artist,
        "title": title,
        "release_date": release_date,
        "tags": tags
    }.items() if v is not None]

    logger.info(f"EDIT success | id={song_id} | fields={updated_fields}")

elif command == 'search':
    logger.info(f"SEARCH command started | args={args}")

    try:
        rows = run_search_from_args(args)
    except ValueError as e:
        print(e)
        logger.error(f"SEARCH failed | error={e}")
        sys.exit(1)

    if not rows:
        print('No results found.')
        logger.info("SEARCH success | results=0")
        sys.exit(0)

    for row in rows:
        print(format_song_row(row))

    logger.info(f"SEARCH success | results={len(rows)}")

elif command == 'savelist':
    required = ['--output']

    output = get_flag_value(args, '--output')
    logger.info(f"SAVELIST command started | output={output} | args={args}")

    if output is None:
        print_missing_args(command, required)
        logger.error("SAVELIST failed | missing --output")
        sys.exit(1)

    try:
        rows = run_search_from_args(args)
    except ValueError as e:
        print(e)
        logger.error(f"SAVELIST failed | search error | {e}")
        sys.exit(1)

    if not rows:
        print('No results found.')
        logger.info(f"SAVELIST success | output={output} | songs=0")
        sys.exit(0)

    try:
        create_savelist(output, rows)
    except FileExistsError as e:
        print(e)
        logger.error(f"SAVELIST failed | output={output} | already exists")
        sys.exit(1)

    print(f'Created savelist \'{output}\' with {len(rows)} songs.')
    logger.info(f"SAVELIST success | output={output} | songs={len(rows)}")

elif command == 'play':
    required = ['--id']

    song_id = get_flag_value(args, '--id')
    if song_id is None:
        print_missing_args(command, required)
        sys.exit(1)

    logger.info(f"PLAY command started | id={song_id}")

    row = search_by_id(song_id)
    if row is None:
        print(f"No song found with id {song_id}")
        logger.error(f"PLAY failed | id={song_id} | song not found")
        sys.exit(1)

    filename = row[0]
    file_path = STORAGE_PATH / filename

    print(f"Playing: {filename}")
    play_audio(file_path)
    logger.info(f"PLAY success | id={song_id} | file={filename}")

elif command == 'help':
    if len(args) == 0:
        print(HELP_TEXTS["main"])
    else:
        help_cmd = args[0]
        print(HELP_TEXTS.get(help_cmd, HELP_TEXTS["main"]))