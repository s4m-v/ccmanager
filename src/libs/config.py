import os.path

def vprint(config, msg):

    if config["verbose"]:
        print("verbose: " + msg)

def check_config(config):

    if not os.path.exists(config["data-dir"]):
        os.makedirs(config["data-dir"], exist_ok=True)

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
    
    config["verbose"] = False
    alias["v"] = "verbose"

    config["dry-run"] = False
    alias["d"] = "dry-run"

    config["data-dir"] = os.path.expandvars("$HOME/.ccmanager")
    alias["D"] = "data-dir"

    return (config, alias)
