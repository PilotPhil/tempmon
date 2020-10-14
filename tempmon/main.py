__version__ = "0.5.0-alpha.0"

import click
from twiggy import quick_setup, log
import my_functions as my


@click.command()
@click.option(
    "-l",
    "--logfile",
    help="File to log output to. Uses STDOUT and STDERR if not specified.",
)
@click.option(
    "-v",
    "--verbose",
    "verbosity",
    count=True,
    help="Output verbose logs. Use -vv for DEBUG level logs.",
)
def main(logfile, verbosity):
    # Get UAC rights
    # my.elevater()
    # set_verbose(1)
    print(verbosity)
    print(logfile)
    pass


# def duh():
#     print("duh")


# main.add_command(mc.version)
# main.add_option(mc.set_log_file)
# main.add_option(mc.set_verbose)

if __name__ == "__main__":
    main()
