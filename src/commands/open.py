import logging
import os
from pathlib import Path
import subprocess
import sys
from .backup import backup
from .sync import sync

logger = logging.getLogger(__name__)

def open(name, data_dir="$HOME/.ccmanager/"):

    cal_path = Path(os.path.expandvars(data_dir), name)

    calcurse_path = Path(cal_path, "calcurse")
    caldav_path = Path(cal_path, "caldav")

    if not cal_path.exists():
        sys.exit(1)

    if caldav_path.exists():
        backup(name, data_dir=data_dir)
        sync(name, data_dir=data_dir)

    subprocess.run([ "calcurse", "-D", calcurse_path])

    if caldav_path.exists():
        backup(name, data_dir=data_dir)
        sync(name, data_dir=data_dir)
