import click
from twiggy import log
import twiggy_setup
import config
from ohm import Ohm
import my_functions as my


@click.command()
@click.option(
    "-l",
    "--logfile",
    help="File to log output to. \n\rDefault = STDERR.",
    type=click.Path(dir_okay=False, writable=True),
)
@click.option(
    "-c",
    "--config",
    "config_file",
    help="File used to read and write settings. Default = 'config.json'.",
    type=click.Path(dir_okay=False, writable=True),
    default="config.json",
)
@click.option(
    "-v",
    "--verbose",
    "verbosity",
    count=True,
    help="Output verbose logs. Use -vv for DEBUG level logs.",
)
@click.version_option()
def main(logfile, verbosity, config_file):
    # Configure twiggy with logfile and verbosity level
    twiggy_setup.twiggy_setup(logfile, verbosity)

    # Create logger instances
    elevater_logger = log.name("elevate")
    settings_logger = log.name("settings")
    ohm_logger = log.name("ohm")

    # Call elevater for UAC rights and pass its logger
    my.elevater(elevater_logger)

    # Create a settings instance, and pass the logger and config file to it.
    settings = config.Config(settings_logger, config_file)

    ohm = Ohm(ohm_logger)

    print(settings.get_config())
    print(ohm.get_cpu_temp())


if __name__ == "__main__":
    main()
