from datetime import datetime

def validate_release_date(release_date):
    try:
        datetime.strptime(release_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Release date must be in YYYY-MM-DD format")

def validate_tags(tags):
    parts = tags.split(',')

    cleaned = [tag.strip() for tag in parts]
    if any(tag == '' for tag in cleaned):
        raise ValueError("Tags must be comma-separated values without empty entries.")
