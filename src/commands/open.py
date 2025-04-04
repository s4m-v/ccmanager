import logging
import os
from pathlib import Path
import subprocess
from .backup import backup
from .sync import sync

logger = logging.getLogger(__name__)

def prep_caldav(name, data_dir):

    logger.info("Backing up calendar...")
    backup(name, data_dir)
    logger.info("done.")

    logger.info("Syncing calendar...")
    sync(name, data_dir)
    logger.info("done.")

def open(name, data_dir="$HOME/.ccmanager/"):

    logger.info("opening calendar.")

    cal_path = Path(os.path.expandvars(data_dir), name)

    calcurse_path = Path(cal_path, "calcurse")
    caldav_path = Path(cal_path, "caldav")

    if not cal_path.exists():
        logger.error("calendar " + name + " not found.")
        return False

    if caldav_path.exists():
        prep_caldav(name, data_dir)
    else:
        return False

    logger.info("running calcurse...")
    subprocess.run([ "calcurse", "-D", calcurse_path])
    logger.info("done.")

    if caldav_path.exists():
        prep_caldav(name, data_dir)
    else:
        return False

    logger.info("calendar closed.")
    return True
