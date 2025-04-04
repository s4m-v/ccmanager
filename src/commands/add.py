import shutil
import subprocess
from pathlib import Path
import os
import logging
from .sync import sync

logger = logging.getLogger(__name__)

def gen_calcurse(path):

    path.mkdir()

    try:
        subprocess.run(["calcurse", "-D", path],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL,
                       timeout=1)
    except subprocess.TimeoutExpired:
        pass

def create_caldav(config, path):

    path.mkdir()
    Path(path, "syncdb").touch()
    Path(path, "hook").mkdir()
    shutil.copyfile(config, Path(path, "config"))

def add(name, caldav_config='', dry_run=False, init_type="keep-remote",
        data_dir="$HOME/.ccmanager/"):

    # Add
    # This command will break into 3 parts
    # 1. create file structure
    # 2. generate calcurse data
    # 3. run calcurse caldav init

    logger.info("adding calendar.")

    cal_path = Path(os.path.expandvars(data_dir), name).resolve()

    if cal_path.exists():
        logger.error("cal directory already exists.")
        return False

    cal_path.mkdir()

    calcurse_path = Path(cal_path, "calcurse")

    logger.info("creating calcurse directoy and files...")
    if not dry_run:
        gen_calcurse(calcurse_path)
    logger.info("done.")
    
    if caldav_config:

        logger.info("creating caldav directoy and files...")

        caldav_config = os.path.expandvars(caldav_config)

        if not dry_run:
            create_caldav(caldav_config, Path(cal_path, "caldav"))

        logger.info("done.")

        logger.info("Initializing caldav...")

        if not dry_run:

            if not sync(name, data_dir=data_dir, init_type=init_type):
                logger.info("removing tree...")
                shutil.rmtree(cal_path)

        logger.info("done.")

    logger.info("calendar added.")

    return True
