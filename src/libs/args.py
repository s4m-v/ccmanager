import sys

def check_options(options, CMD_OPTIONS, GLOBALS_OPTIONS):

    for option in options:

        if option in CMD_OPTIONS or option in GLOBALS_OPTIONS:
            continue
        else:
            return False

    return True

def process_option(options, arg):

    if arg[0:2] == "--":
        options.append(arg[2:])
        return

    for char in arg[1:]:
        options.append(char)
    

def process_args():

# Argument Structure
# ccmanager [options] command [rest of args]

# will return tuple in this format:
# ("command", [options, ...], ["rest of args", ...])

    if len(sys.argv) <= 1:
        print("usage: " + sys.argv[0] + " [OPTIONS] command [ARGUMENTS]")
        sys.exit(1)

    args = sys.argv[1:]

    command = ""
    options = []
    cmd_args = []

    for arg in args:

        if arg[0] == '-':
            process_option(options, arg)
            continue

        if not command:
            command = arg
            continue

        cmd_args.append(arg)

    return (command, options, cmd_args)
