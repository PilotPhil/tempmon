import sys
import argparse
import ctypes # for UAC checking
import gui # private module for GUI control
import tmsettings

# ensure elevated status
if ctypes.windll.shell32.IsUserAnAdmin() == True:
    pass
else:
    elevate()
    # make sure it was successful.
    if ctypes.windll.shell32.IsUserAnAdmin() == True:
        print("Elevation successful.")
    else:
        print("Elevation failed.")
        print("Exiting with sys code: 1")
        sys.exit(1)

# Need to read my config here and pass it to my gui
# ...but how do I pass it back?
# hm...

settings = tmsettings.settings()

# Initialize gui and make handler
g = gui.my_gui()

g.start_gui()