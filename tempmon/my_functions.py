import sys
import ctypes
from twiggy import log
import elevate
import click


def elevater():
    # Check if already running as Windows Administrator
    if ctypes.windll.shell32.IsUserAnAdmin():
        log.info("Already elevated. Continuing.")
    # If not, use the 'elevate' module to try to gain permission
    else:
        log.warning("Not elevated. Attempting UAC elevation.")
        try:
            elevate.elevate()
        except OSError:
            log.critical("UAC elevation failed.")
            sys.exit(1)
