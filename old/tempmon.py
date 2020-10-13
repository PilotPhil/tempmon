__version__ = "0.5.0-alpha.0"

import sys
import ctypes  # Used to check for administrator permissions on Windows
import elevate  # PyPi module for requesting administrator permissions
import modules.gui as gui  # private module for GUI control
import modules.tmsettings as tmsettings  # TempMon settings module


def elevater():
    # Check if already running as Windows Administrator
    if ctypes.windll.shell32.IsUserAnAdmin():
        pass
    # If not, use the 'elevate' module to try to gain permission
    else:
        print("Not elevated. Attempting UAC elevation.")
        try:
            elevate.elevate()
        except OSError:
            print("Elevation failed.")
            print("Exiting with sys code: 1")
            sys.exit(1)


def main():
    # Get UAC rights
    elevater()

    # Create a handler for settings module
    settings_handler = tmsettings.settings()

    # Initialize gui, pass the settings handler
    g = gui.gui(settings_handler)

    # Define layout
    g.make_gui()

    # Kick it off.
    g.start_gui()


if __name__ == "__main__":
    main()
