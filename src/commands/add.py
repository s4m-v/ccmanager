import sys
import os
import shutil
import subprocess
import time

from config import vprint

# Add new calendar

#Usage:

# add "calendar name" "config file"

# Needs to generate:

# ccmanager directory
# calcurse data directory
# syncdb
# calcurse-caldav config

def gen_calcurse_data(path):

    process = subprocess.Popen(["calcurse", "-D", path])

    time.sleep(3)

    process.terminate()
    process.wait()

def check_args(args):

    args_len = len(args)

    match args_len:
        case 0:
            print("ccmanager add CAL_NAME CALDAV_CONF")
            sys.exit(1)
        case 1:
            print("Error: missing conf file arg")
            sys.exit(1)
        case 2:
            pass
        case _:
            print("Error: Too many args")
            sys.exit(1)

def add(args, config):

    check_args(args)

    cal_name = args[0]
    conf_file = args[1]

    ccm_path = os.path.join(config["data-dir"], cal_name)
    cc_path = os.path.join(ccm_path, "data")

    os.makedirs(cc_path, exist_ok=True)
    os.makedirs(os.path.join(ccm_path, "hook"), exist_ok=True)
    with open(os.path.join(ccm_path, "syncdb"), 'w') : pass
    shutil.copy(conf_file, os.path.join(ccm_path, "config"))

    gen_calcurse_data(cc_path)

    #TODO init calcurse-dav sync
