import logging
import subprocess
import os
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

def sync(name, data_dir="$HOME/.ccmanager/", init_type=''):

    logger.info("Starting sync.")

    cal_path = Path(os.path.expandvars(data_dir), name, "caldav").resolve()

    command = [
            "calcurse-caldav",
            "--config", Path(cal_path, "config"),
            "--datadir", Path(cal_path, "data"),
            "--syncdb", Path(cal_path, "syncdb"),
            "--lockfile", Path(cal_path, "lockfile"),
            "--hookdir", Path(cal_path, "hook"),
            ]

    if init_type:

        command.append("--init")
        command.append(init_type)

        logger.info("running init caldav script.")

    else:
        logger.info("running caldav script.")

    result = subprocess.run(
            command, 
            stderr=subprocess.PIPE,
            text=True)

    if result.returncode:

        logger.error("calcurse-caldav failed:")
        logger.error(result.stderr)

        return False

    logger.info("sync complete.")

    return True







