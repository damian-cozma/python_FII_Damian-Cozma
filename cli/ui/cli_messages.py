"""
CLI presentation utilities for user-facing messages and output formatting.

This module contains helper functions responsible for displaying
informational and error messages, as well as formatting song metadata
for console output.
"""

def print_no_command():
    """
    Display an error message when no CLI command is provided.
    """
    print("""
    No command provided.
    Use 'songstorage help' to see available commands.
    """)

def print_unknown_command(given_command):
    """
    Display an error message for an unknown CLI command.
    """
    print(f'''
    Unknown command: {given_command}
    Use 'songstorage help' to see available commands.
    ''')

def print_missing_args(command, required):
    """
    Display an error message when required arguments are missing.
    """
    print(f"""
    Missing required arguments for '{command}'.
    Required: {', '.join(required)}
    Use 'songstorage help {command}' for details.
    """)

def format_song_row(row):
    """
    Format a database song record into a human-readable CLI string.
    """
    song_id = row[0]
    artist = row[2]
    title = row[3]
    release_date = row[4]
    tags = row[5]
    format_ = row[6]

    line = f"[{song_id}] {artist} - {title}"
    if release_date:
        line += f" ({release_date})"

    if tags:
        line += f" [{tags}]"

    if format_:
        line += f" [{format_}]"

    return line