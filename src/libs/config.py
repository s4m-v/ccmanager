import os.path

def vprint(config, msg):

    if config["verbose"]:
        print("verbose: " + msg)

def process_file(config, file):

    for line in file:
    
        if line.strip():
            continue
    
        try:
    
            entry = line[0:line.index(':')].rstrip(" \n\t")
            value = line[line.index(':') + 1:].rstrip(" \n\t")
    
            config[entry] = value
    
        except (ValueError, IndexError):
    
            vprint(config, "Invalid config entry, skipping...")
            continue

def read_config(config, path):

    config_file = os.path.join(path, "config")

    try:

        with open(config_file, 'r') as file:
            process_file(config, file)

    except FileNotFoundError:
        vprint(config, "File not Found!")
        return
    except PermissionError:
        vprint(config, "Insufficent Permissions!")
        return

def check_config(config):

    if not os.path.exists(config["data-dir"]):
        os.makedirs(config["data-dir"], exist_ok=True)

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
