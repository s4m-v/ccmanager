import sys

from libs.args import process_args
from libs.config import init_config, check_config, read_config, vprint
from commands.add import *

def verbose_arg_print(command, cmd_opts, cmd_args, config):
    vprint(config, "command: " + command)
    vprint(config, "command options: " + ", ".join(cmd_opts))
    vprint(config, "command arguments: " + ", ".join(cmd_args))
    vprint(config, "Config:")
    for key, value in config.items():
        vprint(config, f"{key} : {value}")

def main():

# ccmanager

    command = ""
    cmd_opts = []
    cmd_args = []

    # returns (def_config_dict, alias_dict)
    config, alias = init_config()

    read_config(config)

    (command, cmd_opts, cmd_args) = process_args(config, alias)

    verbose_arg_print(command, cmd_opts, cmd_args, config)

    check_config(config)

    match command:

        case "add":
            add(cmd_opts, cmd_args, config)

        case _:
            print("Unknown Command")
            sys.exit(1)


if __name__ == "__main__":
    main()
