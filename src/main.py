from cli import start_cli
from tui import start_tui
import sys

def main():

    if len(sys.argv) == 1:
        start_tui()
    else:
        start_cli()

if __name__ == "__main__":
    main()
