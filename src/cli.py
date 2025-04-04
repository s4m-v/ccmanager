import argparse
from pathlib import Path
import sys
import commands
import logging

logger = logging.getLogger(__name__)

def run_add(args):

    return commands.add(
            args.name,
            caldav_config=args.caldav_conf,
            init_type=args.init_type,
            dry_run=args.dry_run,
            data_dir=args.data_dir
            )

def run_backup(args):

    return commands.backup(
            args.name,
            data_dir=args.data_dir
            )

def run_list(args):
    return commands.list(data_dir=args.data_dir)


def run_open(args):

    return commands.open(
            args.name,
            data_dir=args.data_dir
            )

def run_sync(args):

    return commands.sync(
            args.name,
            data_dir=args.data_dir
            )

def run_remove(args):

    return commands.remove(
            args.name,
            dry_run=args.dry_run,
            data_dir=args.data_dir
            )

def init_parser():

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    parser.add_argument('-v', '--verbose', action="store_true")
    parser.add_argument("-D", "--data-dir", type=Path, 
                            default=Path("$HOME/.ccmanager"))

    ### ADD

    parser_add = subparser.add_parser("add")
    parser_add.set_defaults(func=run_add)

    parser_add.add_argument("name", type=str)
    parser_add.add_argument("-C", "--caldav-conf", type=Path,
                            default=None)
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

    ### open

    parser_open = subparser.add_parser("open")
    parser_open.set_defaults(func=run_open)
    parser_open.add_argument("name", type=str)

    ### sync

    parser_sync = subparser.add_parser("sync")
    parser_sync.set_defaults(func=run_sync)
    parser_sync.add_argument("name", type=str)

    ### backup

    parser_backup = subparser.add_parser("backup")
    parser_backup.set_defaults(func=run_backup)
    parser_backup.add_argument("name", type=str)

    ### list

    parser_list = subparser.add_parser("list")
    parser_list.set_defaults(func=run_list)

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
    result = args.func(args)
    logger.info("running command complete.")

    if not result:
        sys.exit(1)

    sys.exit(0)
