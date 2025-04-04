import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

def list(data_dir="$HOME/.ccmanager/"):

    ccm_path = Path(os.path.expandvars(data_dir))

    dir_list = os.listdir(ccm_path)

    valid_dir_list = []

    for dir in dir_list:
        if Path(ccm_path, dir, "calcurse").exists():
            valid_dir_list.append(dir)

    print(*valid_dir_list, sep=", ")

    return valid_dir_list


    


