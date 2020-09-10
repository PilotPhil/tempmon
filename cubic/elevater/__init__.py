import sys
import ctypes

def elevater():
    if ctypes.windll.shell32.IsUserAnAdmin():
        pass
    else:
        elevate()
        # make sure it was successful.
        if ctypes.windll.shell32.IsUserAnAdmin():
            print("Elevation successful.")
        else:
            print("Elevation failed.")
            print("Exiting with sys code: 1")
            sys.exit(1)