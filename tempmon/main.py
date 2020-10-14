__version__ = "0.5.0-alpha.0"

import click
from twiggy import log
from twiggy_setup import twiggy_setup
import my_functions as my


@click.command()
@click.option(
    "-l",
    "--logfile",
    help="File to log output to. Uses STDERR if not specified.",
    type=click.Path(dir_okay=False, writable=True),
)
@click.option(
    "-v",
    "--verbose",
    "verbosity",
    count=True,
    help="Output verbose logs. Use -vv for DEBUG level logs.",
)
@click.version_option()
def main(logfile, verbosity):
    # Configure logger
    twiggy_setup(logfile, verbosity)

    # Get UAC rights
    my.elevater()


if __name__ == "__main__":
    main()
