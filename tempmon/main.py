from time import sleep
from threading import Thread
import click
from twiggy import log
import twiggy_setup
import config
import gui
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
    gui_logger = log.name("gui")
    gui_config_logger = log.name("gui_config")
    sg_logger = log.name("sensor_grabber")

    # Call elevater for UAC rights and pass its logger
    my.elevater(elevater_logger)

    # Create a settings instance, and pass the logger and config file to it.
    my_config = config.Config(settings_logger, config_file)

    # Create a new OHM instance, and pass the logger to it
    ohm = Ohm(ohm_logger)

    # Create Sensor_grabber
    sg = my.Sensor_grabber(sg_logger, ohm)
    # Define the monitor_temps() function as a thread
    monitor_thread = Thread(target=sg.monitor_temps)
    # Set it to be a daemon, so that it will terminate when __main__ does.
    monitor_thread.daemon = True
    # And start it.
    monitor_thread.start()

    # Create a GUI instance, and pass the logger to it
    g = gui.Gui(gui_logger, gui_config_logger, my_config, sg)

    g.make_gui()

    g.start_gui()


if __name__ == "__main__":
    main()
