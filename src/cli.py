import argparse
import pathlib
import commands
import logging
logger = logging.getLogger(__name__)

def init_parser():

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    parser.add_argument('-v', '--verbose', action="store_true")

    parser_add = subparser.add_parser("add")
    parser_add.set_defaults(func=commands.add)

    parser_add.add_argument("caldav_config", type=pathlib.Path)
    parser_add.add_argument('-d', '--dry-run', action="store_true")
    parser_add.add_argument('-i', '--init-type', default="keep-remote",
                            choices=["keep-remote", "two-way", "keep-local"])

    return parser

def start_cli():

    logger.info("initializing parser.")
    parser = init_parser()
    logger.info("parser initialized.")

    logger.info("parsing args and launching command.")
    parser.parse_args()
    logger.info("command complete.")
