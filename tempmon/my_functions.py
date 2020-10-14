import sys
import ctypes
from twiggy import log
import elevate
import click


def elevater():
    # Make internal logger
    logger = log.name("elevater")

    # Check if already running as Windows Administrator
    if ctypes.windll.shell32.IsUserAnAdmin():
        logger.info("Already elevated. Continuing.")
    # If not, use the 'elevate' module to try to gain permission
    else:
        log.warning("Not elevated. Attempting UAC elevation.")
        try:
            elevate.elevate()
            logger.info("UAC elevation successful. Continuing.")
        except OSError:
            logger.critical("UAC elevation failed.")
            sys.exit(1)
