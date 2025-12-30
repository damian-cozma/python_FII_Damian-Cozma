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