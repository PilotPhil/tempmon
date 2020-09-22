import ctypes
import sys
from elevate import elevate


def elevater():
    if ctypes.windll.shell32.IsUserAnAdmin():
        pass
    else:
        print("Not elevated. Attempting UAC elevation.")
        try:
            elevate()
        except OSError:
            print("Elevation failed.")
            print("Exiting with sys code: 1")
            sys.exit(1)