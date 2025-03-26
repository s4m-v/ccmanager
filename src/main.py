import sys

from libs.args import process_args
from libs.config import init_config
from commands.add import add

GLOBAL_OPTIONS = [
        ["v", "verbose"],
        ["d", "dry-run"],
        ["D", "data-dir"],
        ["C", "config-dir"],
        ]

def main():


    command = ""
    cmd_opts = []
    cmd_args = []

    config_pack = init_config()

    (command, cmd_opts, cmd_args) = process_args(config_pack)

    config, _ = config_pack

    print(config)
    print(command)
    print(cmd_opts)
    print(cmd_args)

    match command:

        case "add":
            add(cmd_opts, cmd_args, config)

        case _:
            print("Unknown Command")
            sys.exit(1)


if __name__ == "__main__":
    main()
