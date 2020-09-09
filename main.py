import sys
import argparse
import ctypes # for UAC checking
import gui # private module for GUI control
import tmsettings

# ensure elevated status
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

# Reading my config here and passing values to my gui as a dictionary
# ...but how do I pass it back to the settings writer?
# hm...
settings = tmsettings.settings()

# Initialize gui and make handler
g = gui.my_gui()

g.start_gui()