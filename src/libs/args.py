#TODO deal with duplicate options

import sys
import os.path

from libs.config import init_config, read_config, vprint

#TODO move these two functions to generic command function
#     in commands folder

def check_cmd_options(opts, CMD_OPTIONS):

    for opt in opts:

        if opt in CMD_OPTIONS:
            continue
        else:
            return False

    return True

def check_cmd_arguments(args, CMD_ARGUMENTS):

    for arg in args:

        if arg in CMD_ARGUMENTS:
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

def process_args():

# Argument Structure
# ccmanager [options] command [rest of args]

# will return tuple in this format:
# ("command", [command options, ...], [command args, ...])

    args_len = len(sys.argv)

    if args_len <= 1:
        print("usage: " + sys.argv[0] + " [OPTIONS] command [ARGUMENTS]")
        sys.exit(1)

    args = sys.argv[1:]

    command = ""
    cmd_opts = []
    cmd_args = []

    config, alias = init_config()

    # Checking for config dir arg
    conf_arg_index = 0

    try:
        conf_arg_index = args.index("--config-dir")
        conf_arg_value = args[conf_arg_index + 1]
        read_config(config, conf_arg_value)

        args.remove("--config-dir")
        args.remove(conf_arg_value)

    except ValueError:
        pass
    except IndexError:
        print("Error: Missing config arg!")
        sys.exit(1)

    if not conf_arg_index:
        read_config(config, os.path.expandvars("$HOME/.config/ccmanager"))

    # The Arg Process Loop

    # This loop checks to see what
    # kind of arg it is in this order:

    # option arg
    # option
    # command
    # command arg

    # This loop uses a boolean to take next arg
    # if the previous option requires it's own arg


    is_config_arg = False
    config_entry = ""

    for arg in args:

        if is_config_arg:
            config[config_entry] = arg
            is_config_arg = False
            continue

        if arg[0] == '-':

            if arg[1] == "-":
                is_config_arg, config_entry = \
                        process_full_opt(arg, cmd_opts, config)
            else:
                is_config_arg, config_entry = \
                        process_alias_opt(arg, cmd_opts, config, alias)
            continue

        if not command:
            command = arg
            continue

        cmd_args.append(arg)

    if is_config_arg or not command:
        print("Error: Missing Input")
        sys.exit(1)

    return (command, cmd_opts, cmd_args, config)
