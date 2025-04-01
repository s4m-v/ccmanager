import logging
from cli import start_cli

logger = logging.getLogger(__name__)

def main():

    logging.basicConfig(level=logging.INFO)

    logger.info("starting cli.")
    start_cli()
    logger.info("cli finished.")

if __name__ == "__main__":
    main()
