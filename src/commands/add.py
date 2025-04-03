import sys
import shutil
import subprocess
import time
from pathlib import Path
import os
import logging

logger = logging.getLogger(__name__)

def gen_calcurse(path):

    path.mkdir()

    process = subprocess.Popen(["calcurse", "-D", path],
                               stdout=subprocess.DEVNULL)
    time.sleep(1)

    process.terminate()
    process.wait()

def create_caldav(config, path):

    path.mkdir()
    Path(path, "syncdb").touch()
    Path(path, "hook").mkdir()
    shutil.copyfile(config, Path(path, "config"))

def init_caldav(init_type, path):

    print(init_type)

    result = subprocess.run([
        "calcurse-caldav",
        "--init", f"{init_type}",
        "--config", f"{Path(path, "config")}",
        "--datadir", f"{Path(path, "data")}",
        "--syncdb", f"{Path(path, "syncdb")}",
        "--lockfile", f"{Path(path, "lockfile")}",
        "--hookdir", f"{Path(path, "hook")}",
        ], stderr=subprocess.PIPE)

    if result.returncode:

        logger.error("calcurse-caldav failed:")
        logger.error(result.stderr.decode('utf-8'))

        logger.info("Removing calendar...")
        shutil.rmtree(Path(path, "..").resolve())

def add(name, caldav_config='', dry_run=False, init_type="keep-remote",
        data_dir=Path("$HOME/.ccmanager/")):

    # Add
    # This command will break into 3 parts
    # 1. create file structure
    # 2. generate calcurse data
    # 3. run calcurse caldav init

    logger.info("Starting add subcommand!")

    cal_path = Path(os.path.expandvars(data_dir), name)

    if cal_path.exists():
        logger.error("cal directory already exists")
        sys.exit(1)

    cal_path.mkdir()

    calcurse_path = Path(cal_path, "calcurse")

    logger.info("creating calcurse directoy and files...")
    if not dry_run:
        gen_calcurse(calcurse_path)
    logger.info("done.")
    
    if caldav_config:

        caldav_config = os.path.expandvars(caldav_config)
        caldav_path = Path(cal_path, "caldav")

        logger.info("creating caldav directoy and files...")
        if not dry_run:
            create_caldav(caldav_config, Path(cal_path, "caldav"))
        logger.info("done.")

        logger.info("Initializing caldav...")
        if not dry_run:
            init_caldav(init_type, caldav_path)
        logger.info("done.")

    logger.info("Add Subcommand Complete!")
