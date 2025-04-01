import sys
import os
import shutil
import subprocess
import time
import logging
logger = logging.getLogger(__name__)

# Add new calendar

#Usage:

# add "calendar name" "config file"

# Needs to generate:

# ccmanager directory
# calcurse data directory
# syncdb
# calcurse-caldav config

def create_caldav_files(path):
    pass

def gen_calcurse_data(path):

    process = subprocess.Popen(["calcurse", "-D", path])

    time.sleep(3)

    process.terminate()
    process.wait()

def init_caldav(init_type):
    pass

def add(args):

    logger.info("Startig Add Subcommand!")

    # Add

    # This command will break into 3 parts
    # 1. create file structure
    # 2. generate calcurse data
    # 3. run calcurse caldav init

    caldav_path = ""
    calcurse_path = ""

    logger.info("creating caldav directoy and files...")
    create_caldav_files(caldav_path)
    logger.info("done.")

    logger.info("creating calcurse directoy and files...")
    gen_calcurse_data(calcurse_path)
    logger.info("done.")

    logger.info("Initializing caldav...")
    init_caldav("twoway")
    logger.info("done.")

    logger.info("Add Subcommand Complete!")
