from libs.args import check_options

COMMAND_OPTIONS = ["h"]

def add(options, cmd_args, GLOBAL_OPTIONS):
    print(check_options(options, COMMAND_OPTIONS, GLOBAL_OPTIONS))
