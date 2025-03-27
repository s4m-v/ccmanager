from libs.args import check_cmd_options

COMMAND_OPTIONS = ["h"]

def add(opts, args, config):
    print(check_cmd_options(opts, COMMAND_OPTIONS))
