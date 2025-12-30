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
