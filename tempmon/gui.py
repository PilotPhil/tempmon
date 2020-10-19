import dearpygui.core as dc
import dearpygui.simple as ds


"""Planning:
Need this module to:
- [] Request current settings
- [] Request that new settings get written
- [] Create the GUI
- [] Allow changing settings and themes
- [] Request CPU and GPU temps
- []
"""


class Gui:
    def __init__(self, logger, config_logger, config_handler):
        self.__log = logger
        self.config = self.Config(config_logger, config_handler)
        self.__log.debug(f"Initializing main GUI class...")
        self.__log.debug(f"Requesting config...")
        self.config_dict = self.config.get_config()
        self.__log.info(f"Setting current theme...")
        dc.set_theme(self.config_dict["theme"])
        self.__log.debug("Initializing theme variable.")
        self.themes = [
            "Dark",
            "Light",
            "Classic",
            "Dark 2",
            "Grey",
            "Dark Grey",
            "Cherry",
            "Purple",
            "Gold",
            "Red",
        ]

    class Config:
        def __init__(self, logger, handler):
            self.__log = logger
            self.__cfg_handler = handler
            self.__config_dict = {}

        def get_config(self):
            self.__log.debug(f"Request to get config information received.")
            return self.__cfg_handler.get_config()

        def write_config(self, config_dict):
            self.__log.debug(f"Config write request received.")
            self.__cfg_handler.write_config(config_dict)

    def make_gui(self):
        # Window formality
        dc.set_main_window_title("TempMon")
        dc.set_main_window_size(800, 400)

        # define plot and table names, just for convenience.
        myplot = "CPU and GPU Temperatures"
        mytable = "Current Temps"

        with ds.window("Main"):

            with ds.menu_bar("Menu"):

                with ds.menu("Options"):

                    dc.add_combo("##Themes", items=self.themes)

            # add plot
            dc.add_plot(myplot, x_axis_name="Time (seconds)", y_axis_name="Temp")

            # set plot limits
            dc.set_plot_xlimits(myplot, 0, 100)
            dc.set_plot_ylimits(myplot, 0, 100)

    def start_gui(self):
        dc.start_dearpygui("Main")