import os
from pathlib import Path
import logging
import shutil

logger = logging.getLogger(__name__)

def remove(name, dry_run=False, data_dir="$HOME/.ccmanager/"):

    logger.info("removing calendar.")

    cal_path = Path(os.path.expandvars(data_dir), name).resolve()

    if not cal_path.exists():
        logger.error("cal does not exist")
        return False

    logger.info("deleting calendar...")

    if not dry_run:
        shutil.rmtree(cal_path)

    logger.info("done.")

    return True
