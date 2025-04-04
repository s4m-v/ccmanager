import os
import time
import sys
from pathlib import Path
import logging
import subprocess

logger = logging.getLogger(__name__)

def gen_backup_path(backup_path):

    backup_name = time.strftime("backup_%Y-%m-%d_%H-%M-%S")

    backup_file = Path(backup_path, backup_name + ".ics")
    if backup_file.exists():

        i = 1
        while True:

            backup_name = backup_name + "_" + str(i)
            backup_file = Path(backup_path, backup_name + ".ics")
            if not backup_file.exists():
                break
            i += 1

    return backup_file

def backup(name, data_dir="$HOME/.ccmanager/"):

    logger.info("starting backup.")

    cal_path = Path(os.path.expandvars(data_dir), name).resolve()
    backup_path = Path(cal_path, "backups")
    calcurse_path = Path(cal_path, "calcurse")

    logger.info("checking directories...")

    if not cal_path.exists():

        logger.error("calendar does not exist.")
        sys.exit(1)

    elif not backup_path.exists():

        logger.info("No backups folder found, making new one.")
        backup_path.mkdir()

    else:

        logger.info("everything exists.")

    logger.info("running calcurse export command...")
    result = subprocess.run(["calcurse", "-D", calcurse_path, "-x"], 
                            capture_output=True,
                            text=True)

    if result.returncode:

        logger.error("calcurse export failed:")
        logger.error(result.stderr)

        return False


    logger.info("done.")

    logger.info("Writing backup...")

    with open(gen_backup_path(backup_path), 'w') as file:
        file.write(result.stdout)

    logger.info("done.")

    logger.info("backup complete.")
    return True

