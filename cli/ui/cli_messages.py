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

def format_song_row(row):
    song_id = row[0]
    artist = row[2]
    title = row[3]
    release_date = row[4]
    tags = row[5]

    line = f"[{song_id}] {artist} - {title}"
    if release_date is not None:
        line += f" ({release_date})"

    if tags:
        line += f" [{tags}]"

    return line