#TODO deal with duplicate options

import sys
import os.path

from config import init_config, read_config, vprint
from commands.add import add

#TODO move these two functions to generic command function
#     in commands folder

def process_full_opt(opt, config):
    
        full_opt = opt[2:]

        if full_opt in config:

            if full_opt in config["requires_arg"]: 
                return True, full_opt
            
            config[full_opt] = True
            return False, ""
        else:
            print("Error: --" + full_opt + " is invalid.")
            sys.exit(1)

def process_alias_opt(opt, config, alias):

    alias_opt = opt[1:]

    if len(alias_opt) == 1 and alias[alias_opt] in config["requires_arg"]:
        return True, alias[alias_opt]

    for char in alias_opt:

        if char in alias:
            if alias[char] in config:

                config[alias[char]] = True
                continue
        else:
            print("Error: -" + char + " is invalid.")
            sys.exit(1)

    return False, ""

def init_cli():

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
                        process_full_opt(arg, config)
            else:
                is_config_arg, config_entry = \
                        process_alias_opt(arg, config, alias)
            continue

        if not command:
            command = arg
            continue

        cmd_args.append(arg)

    if is_config_arg or not command:
        print("Error: Missing Input")
        sys.exit(1)

    return (command, cmd_args, config)

def verbose_arg_print(command, cmd_args, config):
    vprint(config, "command: " + command)
    vprint(config, "command arguments: " + ", ".join(cmd_args))
    vprint(config, "Config:")
    for key, value in config.items():
        if key in "requires_arg": continue
        vprint(config, f"\t{key} : {value}")

def main_cli():

    command = ""
    cmd_args = []
    config = {}

    (command, cmd_args, config) = init_cli()

    verbose_arg_print(command, cmd_args, config)

    match command:

        case "add":
            add(cmd_args, config)

        case _:
            print("Unknown Command")
            sys.exit(1)
