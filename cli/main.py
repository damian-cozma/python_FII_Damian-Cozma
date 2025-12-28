import sys

from core.storage_init import storage_init
from db.db_init import db_init

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
    if not all(r in args for r in required):
        print_missing_args(command, required)
        sys.exit(1)

elif command == 'delete':
    required = ['--id']
    if not all(r in args for r in required):
        print_missing_args(command, required)
        sys.exit(1)

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