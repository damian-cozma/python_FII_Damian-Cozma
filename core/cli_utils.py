from db.song_repo import search_by_fields


def get_flag_value(args, flag):
    if flag not in args:
        return None

    idx = args.index(flag)

    if idx + 1 >= len(args):
        return None

    return args[idx + 1]

def run_search_from_args(args):
    artist = get_flag_value(args, '--artist')
    title = get_flag_value(args, '--title')
    release_date = get_flag_value(args, '--release-date')
    tags = get_flag_value(args, '--tags')

    if artist is None and title is None and release_date is None and tags is None:
        raise ValueError("You must provide at least one search field.")

    return search_by_fields(artist, title, release_date, tags)