
from libs.args import process_args
from commands.add import add

GLOBAL_OPTIONS = ["v"]

def main():

    command = ""
    options = []
    cmd_args = []

    (command, options, cmd_args) = process_args()

    print(command)
    print(options)
    print(cmd_args)

    match command:

        case "add":
            add(options, cmd_args, GLOBAL_OPTIONS)


if __name__ == "__main__":
    main()
