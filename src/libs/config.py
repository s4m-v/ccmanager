def init_config():

    config = {}
    alias = {}
    
    config["verbose"] = False
    alias["v"] = "verbose"

    config["dry-run"] = False
    alias["d"] = "dry-run"

    config["data-dir"] = "/home/sam/.ccmanager"
    alias["D"] = "data-dir"

    config["config-dir"] = "/home/sam/.ccmanager"
    alias["C"] = "config-dir"

    return (config, alias)
