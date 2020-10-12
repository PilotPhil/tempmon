import sys
import ctypes   # Used to check for administrator permissions on Windows
import elevate  # PyPi module for requesting administrator permissions
import modules.gui as gui  # private module for GUI control
import modules.tmsettings as tmsettings  # TempMon settings module

def main():
    # Elevate UAC
    if ctypes.windll.shell32.IsUserAnAdmin():
        pass
    else:
        print("Not elevated. Attempting UAC elevation.")
        try:
            elevate.elevate()
        except OSError:
            print("Elevation failed.")
            print("Exiting with sys code: 1")
            sys.exit(1)


    # Reading my config here and passing values to my gui as a dictionary
    # ...but how do I pass it back to the settings writer?
    # hm...
    # loaded_settings = tmsettings.settings().import_config()
    tm_settings_handle = tmsettings.settings()

    # Instatiate a settings observer and attach it to GUI subject
    # sett_observer = tmsettings.Observer()
    # g.settings().attach(sett_observer)

    # # Send settings to GUI
    # g.settings().set_vars(loaded_settings)

    # Initialize gui, make handle, pass settings for init
    g = gui.gui(tm_settings_handle.import_config(), tm_settings_handle)

    # Define layout
    g.make_gui()

    # Kick it off.
    g.start_gui()


if __name__ == "__main__":
    main()