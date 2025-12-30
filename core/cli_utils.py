def get_flag_value(args, flag):
    if flag not in args:
        return None

    idx = args.index(flag)

    if idx + 1 >= len(args):
        return None

    return args[idx + 1]