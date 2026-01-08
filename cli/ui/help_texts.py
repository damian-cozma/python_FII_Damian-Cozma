"""
Static help text definitions for the SongStorage CLI.

This module contains user-facing help messages for all supported
commands. The texts are displayed by the CLI layer and do not contain
any application logic.
"""

HELP_TEXTS = {
    "main": """
Available commands:
  add        Add a new song
  delete     Delete a song by ID
  edit       Edit song metadata
  search     Search songs
  savelist   Create a playlist archive
  play       Play a song
  help       Show help

Use 'songstorage help <command>' for details.

Note:
Values containing spaces must be quoted.
""",

    "add": """
Usage:
songstorage add --file PATH --artist TEXT --title TEXT
               [--release-date DATE]
               [--tags TAGS]
               
Note:
Release date must be in YYYY-MM-DD format.
Tags must be quoted and separated by commas.
""",

    "delete": """
Usage:
songstorage delete --id ID
""",

    "edit": """
Usage:
songstorage edit --id ID
                [--artist TEXT]
                [--title TEXT]
                [--release-date DATE]
                [--tags TAGS]
                
Note:
At least one field must be provided for update.
Release date must be in YYYY-MM-DD format.
Tags must be quoted and separated by commas.
""",

    "search": """
Usage:
songstorage search [--artist TEXT]
                   [--title TEXT]
                   [--format FORMAT]
                   [--tags TAG]
""",

    "savelist": """
Usage:
songstorage savelist --output NAME
                     [search filters...]
""",

    "play": """
Usage:
songstorage play --id ID
""",

    "help": """
Usage:
songstorage help
songstorage help <command>
"""
}
