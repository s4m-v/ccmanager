import argparse
from pathlib import Path
import sys
import commands
import logging
logger = logging.getLogger(__name__)

def run_remove(args):

    commands.remove(
            args.name,
            dry_run=args.dry_run,
            data_dir=args.data_dir
            )

def run_add(args):

    commands.add(
            args.name,
            caldav_config=args.caldav_conf,
            init_type=args.init_type,
            dry_run=args.dry_run,
            data_dir=args.data_dir
            )

def init_parser():

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    parser.add_argument('-v', '--verbose', action="store_true")

    ### ADD

    parser_add = subparser.add_parser("add")
    parser_add.set_defaults(func=run_add)

    parser_add.add_argument("name", type=str)
    parser_add.add_argument("-C", "--caldav-conf", type=Path,
                            default=None)
    parser_add.add_argument("-D", "--data-dir", type=Path, 
                            default=Path("$HOME/.ccmanager"))
    parser_add.add_argument('-d', '--dry-run', action="store_true")
    parser_add.add_argument('-i', '--init-type', default="keep-remote",
                            choices=["keep-remote", "two-way", "keep-local"])
    ### REMOVE

    parser_remove = subparser.add_parser("remove")
    parser_remove.set_defaults(func=run_remove)

    parser_remove.add_argument("name", type=str)
    parser_remove.add_argument("-d", "--dry-run", action="store_true")
    parser_remove.add_argument("-D", "--data-dir", type=Path, 
                            default=Path("$HOME/.ccmanager"))

    return parser

def start_cli():

    parser = init_parser()

    if len(sys.argv) == 1:
        parser.print_usage()
        sys.exit(0)

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig()

    logger.info("running command.")
    args.func(args)
    logger.info("running command complete.")

    logger.info("command complete.")
