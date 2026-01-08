"""
Validation utilities for SongStorage input data.

This module provides helper functions for validating user-provided
metadata fields such as release dates and tags.
"""

from datetime import datetime

def validate_release_date(release_date):
    """
    Validate the format of a release date string.

    The expected format is YYYY-MM-DD.
    """
    try:
        datetime.strptime(release_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Release date must be in YYYY-MM-DD format")

def validate_tags(tags):
    """
    Validate a comma-separated list of tags.

    Tags must not contain empty values.
    """
    parts = tags.split(',')

    cleaned = [tag.strip() for tag in parts]
    if any(tag == '' for tag in cleaned):
        raise ValueError("Tags must be comma-separated values without empty entries.")
