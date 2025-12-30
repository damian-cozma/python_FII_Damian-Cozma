import sys

from lxml.html.defs import tags

from core.file_ops import add_file, delete_file
from core.storage_init import storage_init
from db.db_init import db_init
from db.song_repo import insert_song, search_by_id, delete_song

db_init()
storage_init()
VALID_COMMANDS = ['add', 'delete', 'edit', 'search', 'savelist', 'play', 'help']

def print_no_command():
    print("""
    No command provided.
    Use 'songstorage help' to see available commands.
    """)

def print_unknown_command(given_command):
    print(f'''
    Unknown command: {given_command}
    Use 'songstorage help' to see available commands.
    ''')

def print_missing_args(command, required):
    print(f"""
    Missing required arguments for '{command}'.
    Required: {', '.join(required)}
    Use 'songstorage help {command}' for details.
    """)

def get_flag_value(args, flag):
    if flag not in args:
        return None

    idx = args.index(flag)

    if idx + 1 >= len(args):
        return None

    return args[idx + 1]

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

    if not file or not artist or not title:
        print_missing_args(command, required)
        sys.exit(1)

    filename = add_file(file)
    try:
        insert_song(filename, artist, title, release_date, tags)
    except Exception:
        delete_file(filename)
        raise

elif command == 'delete':
    required = ['--id']

    song_id = get_flag_value(args, '--id')

    if not song_id:
        print_missing_args(command, required)
        sys.exit(1)

    row = search_by_id(song_id)
    if not row:
        print(f"No song found with id {song_id}")
        sys.exit(1)

    filename = row[0]
    delete_file(filename)
    delete_song(song_id)

    print(f"Deleted song {song_id}")

elif command == 'edit':
    required = ['--id']

    if not all(r in args for r in required):
        print_missing_args(command, required)
        sys.exit(1)

elif command == 'play':
    required = ['--id']

    if not all(r in args for r in required):
        print_missing_args(command, required)
        sys.exit(1)

elif command == 'savelist':
    required = ['--output']

    if not all(r in args for r in required):
        print_missing_args(command, required)
        sys.exit(1)

elif command == 'search':
    pass

elif command == 'help':
    if len(args) == 0:
        print('''
            Available commands:
        add        Add a new song
        delete     Delete a song by ID
        edit       Edit song metadata
        search     Search songs
        savelist   Create a playlist archive
        play       Play a song
        help       Show help
        
        Use 'songstorage help <command>' for details.
        ''')
    else:
        help_cmd = args[0]

        if help_cmd == 'add':
            print("""
        Usage:
        songstorage add --file PATH --artist TEXT --title TEXT
                       [--release-date DATE]
                       [--tags TAGS]
            """)

        elif help_cmd == 'delete':
            print("""
        Usage:
        songstorage delete --id ID
            """)

        elif help_cmd == 'edit':
            print("""
        Usage:
        songstorage edit --id ID
                        [--artist TEXT]
                        [--title TEXT]
                        [--release-date DATE]
                        [--tags TAGS]

        Note:
        At least one field must be provided for update.
            """)

        elif help_cmd == 'search':
            print("""
        Usage:
        songstorage search [--artist TEXT]
                           [--title TEXT]
                           [--format FORMAT]
                           [--tags TAG]
            """)

        elif help_cmd == 'savelist':
            print("""
        Usage:
        songstorage savelist --output NAME
                             [search filters...]
            """)

        elif help_cmd == 'play':
            print("""
        Usage:
        songstorage play --id ID
            """)

        elif help_cmd == 'help':
            print("""
        Usage:
        songstorage help
        songstorage help <command>
            """)