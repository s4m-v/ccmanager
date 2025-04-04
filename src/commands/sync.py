import logging
import subprocess
import os
from pathlib import Path

logger = logging.getLogger(__name__)

def sync(name, data_dir="$HOME/.ccmanager/", init_type=''):

    logger.info("starting sync.")

    cal_path = Path(os.path.expandvars(data_dir), name).resolve()
    caldav_path = Path(cal_path, "caldav")
    calcurse_path = Path(cal_path, "calcurse")

    command = [
            "calcurse-caldav",
            "--datadir", calcurse_path,
            "--config", Path(caldav_path, "config"),
            "--syncdb", Path(caldav_path, "syncdb"),
            "--lockfile", Path(caldav_path, "lockfile"),
            "--hookdir", Path(caldav_path, "hook"),
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







