import sys

from libs.args import process_args
from libs.config import vprint
from commands.add import add

def verbose_arg_print(command, cmd_opts, cmd_args, config):
    vprint(config, "command: " + command)
    vprint(config, "command options: " + ", ".join(cmd_opts))
    vprint(config, "command arguments: " + ", ".join(cmd_args))
    vprint(config, "Config:")
    for key, value in config.items():
        vprint(config, f"\t{key} : {value}")

def main():

# ccmanager

    command = ""
    cmd_opts = []
    cmd_args = []
    config = {}

    (command, cmd_opts, cmd_args, config) = process_args()

    verbose_arg_print(command, cmd_opts, cmd_args, config)

    match command:

        case "add":
            add(cmd_opts, cmd_args, config)

        case _:
            print("Unknown Command")
            sys.exit(1)


if __name__ == "__main__":
    main()
