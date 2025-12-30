import sys

from core.cli_messages import print_no_command, print_unknown_command, print_missing_args, format_song_row
from core.cli_utils import get_flag_value, run_search_from_args
from core.file_ops import add_file, delete_file, create_savelist
from core.help_texts import HELP_TEXTS
from core.savelists_init import savelists_init
from core.storage_init import storage_init
from core.validators import validate_release_date, validate_tags
from db.db_init import db_init
from db.song_repo import insert_song, search_by_id, delete_song, edit_song, search_by_fields

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

    if file is None or artist is None or title is None:
        print_missing_args(command, required)
        sys.exit(1)

    try:
        if release_date is not None:
            validate_release_date(release_date)
        if tags is not None:
            validate_tags(tags)
    except ValueError as e:
        print(e)
        sys.exit(1)

    filename = None
    try:
        filename = add_file(file)
        insert_song(filename, artist, title, release_date, tags)
    except Exception as e:
        if filename:
            delete_file(filename)
        print(e)
        sys.exit(1)

    print(f'Song {artist} - {title} added.')

elif command == 'delete':
    required = ['--id']

    song_id = get_flag_value(args, '--id')

    if song_id is None:
        print_missing_args(command, required)
        sys.exit(1)

    row = search_by_id(song_id)
    if row is None:
        print(f"No song found with id {song_id}")
        sys.exit(1)

    filename = row[0]
    delete_file(filename)
    delete_song(song_id)

    print(f"Deleted song {song_id}")

elif command == 'edit':
    required = ['--id']

    song_id = get_flag_value(args, '--id')

    artist = get_flag_value(args, '--artist')
    title = get_flag_value(args, '--title')
    release_date = get_flag_value(args, '--release-date')
    tags = get_flag_value(args, '--tags')

    if song_id is None:
        print_missing_args(command, required)
        sys.exit(1)

    if artist is None and title is None and release_date is None and tags is None:
        print('You must provide at least one field.')
        sys.exit(1)

    try:
        if release_date is not None:
            validate_release_date(release_date)
        if tags is not None:
            validate_tags(tags)
    except ValueError as e:
        print(e)
        sys.exit(1)

    edit_song(song_id, artist, title, release_date, tags)

elif command == 'search':
    try:
        rows = run_search_from_args(args)
    except ValueError as e:
        print(e)
        sys.exit(1)

    if not rows:
        print('No results found.')
        sys.exit(0)

    for row in rows:
        print(format_song_row(row))

elif command == 'savelist':
    required = ['--output']

    output = get_flag_value(args, '--output')
    if output is None:
        print_missing_args(command, required)
        sys.exit(1)

    try:
        rows = run_search_from_args(args)
    except ValueError as e:
        print(e)
        sys.exit(1)

    if not rows:
        print('No results found.')
        sys.exit(0)

    try:
        create_savelist(output, rows)
    except FileExistsError as e:
        print(e)
        sys.exit(1)

    print(f'Created savelist \'{output}\' with {len(rows)} songs.')

elif command == 'play':
    required = ['--id']

    if not all(r in args for r in required):
        print_missing_args(command, required)
        sys.exit(1)

elif command == 'help':
    if len(args) == 0:
        print(HELP_TEXTS["main"])
    else:
        help_cmd = args[0]
        print(HELP_TEXTS.get(help_cmd, HELP_TEXTS["main"]))