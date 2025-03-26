#TODO deal with duplicate options

import sys

def check_options(options, CMD_OPTIONS, GLOBALS_OPTIONS):

    for option in options:

        if option in CMD_OPTIONS or option in GLOBALS_OPTIONS:
            continue
        else:
            return False

    return True

def process_full_opt(opt, cmd_opts, config):
    
        full_opt = opt[2:]

        if full_opt in config:

            if "dir" in full_opt: 
                return True, full_opt
            
            config[full_opt] = True
            return False, ""

        cmd_opts.append(full_opt)
        return False, ""


def process_alias_opt(opt, cmd_opts, config, alias):

    alias_opt = opt[1:]

    if len(alias_opt) == 1 and alias_opt.isupper():
        return True, alias[alias_opt]

    for char in alias_opt:

        if char in alias:
            if alias[char] in config:
                config[alias[char]] = True
                continue

        cmd_opts.append(char)

    return False, ""


def process_option(opt, cmd_opts, config_pack):

    config, alias = config_pack

    if opt[0:2] == "--":
        return process_full_opt(opt, cmd_opts, config)

    return process_alias_opt(opt, cmd_opts, config, alias)


def process_args(config_pack):

# Argument Structure
# ccmanager [options] command [rest of args]

# will return tuple in this format:
# ("command", [options, ...], ["rest of args", ...])

    args_len = len(sys.argv)

    if args_len <= 1:
        print("usage: " + sys.argv[0] + " [OPTIONS] command [ARGUMENTS]")
        sys.exit(1)

    args = sys.argv[1:]

    command = ""
    cmd_opts = []
    cmd_args = []

    config_read = False
    config_entry = ""
    config, _ = config_pack

    for arg in args:

        if config_read:
            config[config_entry] = arg
            config_read = False
            continue

        if arg[0] == '-':
            config_read, config_entry = process_option(arg, cmd_opts, config_pack)
            continue

        if not command:
            command = arg
            continue

        cmd_args.append(arg)

    if config_read:
        print(config_entry + ": missing input")
        sys.exit(1)

    return (command, cmd_opts, cmd_args)
