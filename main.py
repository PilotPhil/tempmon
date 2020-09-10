import regui # private module for GUI control
import tmsettings # TempMon settings module
from cubic.elevater import elevater # private UAC elevater

# Elevate UAC
elevater()

# Reading my config here and passing values to my gui as a dictionary
# ...but how do I pass it back to the settings writer?
# hm...
settings = tmsettings.settings()

# Initialize gui and make handler
g = gui.my_gui()

g.set_vars(settings)

g.make_gui()

g.start_gui()