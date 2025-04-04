import os
from pathlib import Path
import logging
import shutil
import sys

logger = logging.getLogger(__name__)

def remove(name, dry_run=False, data_dir="$HOME/.ccmanager/"):

    logger.info("Starting remove command!")

    cal_path = Path(os.path.expandvars(data_dir), name).resolve()

    if not cal_path.exists():
        logger.error("cal does not exist")
        sys.exit(1)

    logger.info("removing calendar...")

    if not dry_run:
        shutil.rmtree(cal_path)

    logger.info("done.")
