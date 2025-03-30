import sys

def check_opts(opts, CMD_OPTIONS):

    for opt in opts:

        if opt in CMD_OPTIONS:
            continue
        else:
            print("Error: invalid options")
            sys.exit(1)

    return
