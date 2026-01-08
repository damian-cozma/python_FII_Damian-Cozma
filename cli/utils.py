"""
CLI utility helpers for argument parsing.

This module contains helper functions used by the command-line interface
to extract and process command-line flags.
"""

def get_flag_value(args, flag):
    """
    Retrieve the value associated with a CLI flag.
    """
    if flag not in args:
        return None

    idx = args.index(flag)

    if idx + 1 >= len(args):
        return None

    return args[idx + 1]