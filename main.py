import modules.regui as regui # private module for GUI control
import modules.tmsettings as tmsettings # TempMon settings module
from cubic.elevater import elevater # private UAC elevation control

# Elevate UAC
elevater()

# Reading my config here and passing values to my gui as a dictionary
# ...but how do I pass it back to the settings writer?
# hm...
set_handler = tmsettings.settings()
settings = set_handler.import_config()

# Initialize gui and make handler
g = regui.my_gui()

# Send settings to GUI
g.set_vars(settings)

# Define layout
g.make_gui()

# Kick it off.
g.start_gui()