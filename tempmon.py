import modules.gui as gui  # private module for GUI control
import modules.tmsettings as tmsettings  # TempMon settings module
from modules.elevater import elevater  # private UAC elevation control

# Elevate UAC
elevater()

# Reading my config here and passing values to my gui as a dictionary
# ...but how do I pass it back to the settings writer?
# hm...
# loaded_settings = tmsettings.settings().import_config()
tm_sett_handle = tmsettings.settings()

# Instatiate a settings observer and attach it to GUI subject
# sett_observer = tmsettings.Observer()
# g.settings().attach(sett_observer)

# # Send settings to GUI
# g.settings().set_vars(loaded_settings)

# Initialize gui, make handle, pass settings for init
g = gui.gui(tm_sett_handle.import_config(), tm_sett_handle)

# Define layout
g.make_gui()

# Kick it off.
g.start_gui()
