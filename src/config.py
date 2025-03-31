import os
import sys

def vprint(config, msg):
    if config["verbose"]:
        print("verbose: " + msg)

def check_config(config):

    if not os.path.exists(config["data-dir"]):
        os.makedirs(config["data-dir"], exist_ok=True)

    if not config["init-type"] in ["keep-local", "keep-remote", "twoway"]:
        print("Error: Config: invalid init-type")
        sys.exit(1)

def process_file(config, file):

    for line in file:
    
        if line.isspace():
            continue
    
        try:
    
            entry = line[0:line.index(':')].strip(" \n\t")
            value = line[line.index(':') + 1:].strip(" \n\t")

            if not entry in config:
                raise ValueError

            if value == "yes":
                value = True
            if value == "no":
                value = False

            if not type(value) is type(config[entry]):
                raise ValueError
    
            config[entry] = value
    
        except (ValueError, IndexError):
            print("Invalid config entry: " + line)
            continue

def read_config(config, path):

    config_file = os.path.join(path, "config")

    try:

        with open(config_file, 'r') as file:
            process_file(config, file)

    except FileNotFoundError:
        return
    except PermissionError:
        return

    check_config(config)

def init_config():

    config = {}
    alias = {}
    requires_arg = []
    
    config["verbose"] = False
    alias["v"] = "verbose"

    config["dry-run"] = False
    alias["d"] = "dry-run"

    config["data-dir"] = os.path.expandvars("$HOME/.ccmanager")
    alias["D"] = "data-dir"
    requires_arg.append("data-dir")

    config["init-type"] = "keep-remote"
    alias["i"] = "init-type"
    requires_arg.append("init-type")

    config["requires_arg"] = requires_arg

    return (config, alias)
