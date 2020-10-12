__version__ = "0.1.0"

from dearpygui.core import *
from dearpygui.simple import *
import modules.ohm as ohm

# initialize OpenHardwareMonitor
ohm = ohm.helper()

# define plot and table names, just for convenience.
myplot = "CPU and GPU Temperatures"
mytable = "Current Temps"

class gui():
    class settings():
        
        _observers = []
        
        def attach(self, observer):
            self._observers.append(observer)
            log(f"Attached observer.")
        
        def detach(self, observer):
            self._observers.remove(observer)
            log(f"Detached observer.")
        
        def write_settings(self, settings):
            for observer in self._observers:
                observer.update(settings)

    def __init__(self, _settings_handler):
        """Define DearPyGui data sources"""

        # Get settings from file, using handler that was passed to __init__
        settings_dict = _settings_handler.import_config()

        # Define theme names and log levels, for later use.
        log("Initializing gui.gui class.")
        self.themes = ["Dark", "Light", "Classic", "Dark 2", "Grey",
                       "Dark Grey", "Cherry", "Purple", "Gold", "Red"]
        self.log_levels = ["Trace", "Debug", "Info", "Warning", "Error", "Off"]

        # Set theme, based on settings passed via argument
        set_theme(settings_dict["theme"])

        # define DPG data
        add_data("CPU Temp", [])
        add_data("GPU Temp", [])
        add_data("frameCount", 0)
        add_data("timeCounter", get_total_time())
        add_value("maxCPU", 0)
        add_value("maxGPU", 0)
        add_value("cpu_threshold", settings_dict["cpu_threshold"])
        add_value("gpu_threshold", settings_dict["gpu_threshold"])
        add_value("is_cpu_warning_cleared", True)
        add_value("is_gpu_warning_cleared", True)

        # And attach the passed observer to class's settings subject
        self.settings().attach(_settings_handler)

    @staticmethod
    def apply_theme(sender, data):
        theme = get_value(" ##Themes")
        set_theme(theme)

    @staticmethod
    def set_logger_level(sender, data):
        level = get_value("Log Level##logging")
        set_log_level(level)

    @staticmethod
    def reset_max(sender, data):
        """Reset max CPU and GPU temperature records and update table"""
        add_value("maxCPU", 0)
        add_value("maxGPU", 0)
        set_table_item(mytable, 1, 1, "0")
        set_table_item(mytable, 1, 2, "0")

    @staticmethod
    def reset_plot(sender, data):
        """Clear plot and reset associated variables"""
        clear_plot(myplot)
        add_data("CPU Temp", [])
        add_data("GPU Temp", [])
        add_data("frameCount", 0)

    @staticmethod
    def show_logger_callback(sender, data):
        show_logger()
        log("Logger opened")

    @staticmethod
    def plot_callback(sender, data):
        """Update plot and table data every 1 second"""
        # get the last time the callback updated the data
        lastTime = get_data("timeCounter")
        
        # if it has been >= 1 second since last update, do another update.
        # otherwise, exit.
        if get_total_time() - lastTime >= 1:
            log("Entering main logic loop")
            # get the number of frames that have been rendered and increment it
            frame_count = get_data("frameCount")
            log(f"{frame_count = }")
            frame_count += 1
            # grab current CPU and GPU temp
            current_cpu, current_gpu = ohm.get_cpu(), ohm.get_gpu()

            # Pull DearPyGui register data into local list variable
            cpu_data = get_data("CPU Temp")

            # Adds current temp to list, paired with frame count
            cpu_data.append([frame_count, current_cpu])

            # Pull DearPyGui register data into local list variable
            gpu_data = get_data("GPU Temp")

            # Adds current temp to list, paired with frame count
            gpu_data.append([frame_count, current_gpu])

            # Get current threshold values
            curr_cpu_thresh = get_value("cpu_threshold")
            curr_gpu_thresh = get_value("gpu_threshold")

            if len(cpu_data) > 100:
                del cpu_data[0]  # Keep list size under 50
            if len(gpu_data) > 100:
                del gpu_data[0]  # Keep list size under 50

            # update plot
            add_line_series(myplot, "Intel", cpu_data, color=[0, 0, 255, 255])
            add_line_series(myplot, "NVIDIA", gpu_data, color=[0, 255, 0, 255])

            # update table with current temps and thresholds
            set_table_item(mytable, 0, 1, str(int(current_cpu)))
            set_table_item(mytable, 0, 2, str(int(current_gpu)))
            set_table_item(mytable, 2, 1, str(int(curr_cpu_thresh)))
            set_table_item(mytable, 2, 2, str(int(curr_gpu_thresh)))

            # update plot limits, based on lowest
            # available frame_count in cpu_data.
            # data is trimmed to 100 records, so
            # keep the most recent 100 plot points in view.
            set_plot_xlimits(myplot, cpu_data[0][0], cpu_data[0][0]+100)

            # if current temp is higher than recorded maximum,
            # overwrite DPG register and update table.
            if current_cpu > get_value("maxCPU"):
                add_value("maxCPU", current_cpu)
                set_table_item(mytable, 1, 1, (str(int(current_cpu))))
            if current_gpu > get_value("maxGPU"):
                add_value("maxGPU", current_gpu)
                set_table_item(mytable, 1, 2, (str(int(current_gpu))))

            # check if temp is above threshold.
            # Get thresholds for each sensor, pack them into a dictionary
            # Pack current temps into a dictionary.
            # Send both to my_gui.thresh_check()
            cpu_threshold = get_value("cpu_threshold")
            gpu_threshold = get_value("gpu_threshold")
            temps = {'CPU': current_cpu, 'GPU': current_gpu}
            thresholds = {'CPU': cpu_threshold, 'GPU': gpu_threshold}
            gui.thresh_check(thresholds, temps)

            # update DPG register with all updated data
            add_data("frameCount", frame_count)
            add_data("CPU Temp", cpu_data)
            add_data("GPU Temp", gpu_data)
            add_data("timeCounter", get_total_time())
        else:
            pass

    @staticmethod
    def warning_manually_toggled(sender, data):
        log_info("Warning manually toggled.")

    @staticmethod
    def thresh_check(thresholds: dict, temps: dict) -> None:
        """Check temperatures against thresholds. Send notification if out of range.

        Args:
            thresholds (dict):
                dictionary with thresholds for CPU and GPU in float format.
            temps (dict):
                takes a dictionary of format {sensor(str), temperature(float)}
        """

        log("Beginning thresh_check")

        cpu_warning_cleared = get_value("is_cpu_warning_cleared")
        gpu_warning_cleared = get_value("is_gpu_warning_cleared")

        warnings_cleared = {'CPU': cpu_warning_cleared, 'GPU': gpu_warning_cleared}
        cpu_clear_thresh = thresholds['CPU'] - 5
        gpu_clear_thresh = thresholds['GPU'] - 5

        for sensor, value in temps.items():
            log(f"{sensor} at {value}, {warnings_cleared[sensor] = }")
            if value >= thresholds[sensor]:
                # check if temp has gone below threshold
                # since last notification
                if warnings_cleared[sensor]:
                    notif_string = f"Temp Warning: {sensor} at {value}\u00B0C"
                    # notif.send(notif_string, " ")
                    log_warning(notif_string)
                    if sensor == 'CPU':
                        set_value("is_cpu_warning_cleared", False)
                    elif sensor == 'GPU':
                        add_value("is_gpu_warning_cleared", False)
                elif not warnings_cleared[sensor]:
                    log_info(f"{sensor} temp still above threshold. Warning not cleared.")
            elif value > (thresholds[sensor] - 5.0) and not warnings_cleared[sensor]:
                log_debug(f"{sensor} has not dropped 5\u00B0C below threshold. Warning not cleared.")
            else:
                log_info(f"{sensor} threshold check cleared. {sensor} is at {value}\u00B0C")
                if warnings_cleared[sensor] == False:
                    # log_info("Warning cleared by system.")
                    if sensor == 'CPU':
                        log_info("CPU warning cleared by system.")
                        set_value("is_cpu_warning_cleared", True)
                        log_debug(f"{get_value('is_cpu_warning_cleared') = }")
                    elif sensor == 'GPU':
                        log_info("GPU warning cleared by system")
                        add_value("is_gpu_warning_cleared", True)

    def update_threshold(self, sender, data):
        settings_dict = {"cpu_threshold": 70, "gpu_threshold": 70, "theme": "Gold"}
        self.settings().write_settings(settings_dict)

    def save_threshold(self, sender, data):
        # cpu_threshold = get_value("cpu_threshold")

        settings_dict = {"cpu_threshold": get_value("cpu_threshold"), "gpu_threshold": get_value("gpu_threshold")}
        self.settings().write_settings(settings_dict)
    
    def save_theme(self, sender, data):
        settings_dict = {"theme": get_theme()}
        self.settings().write_settings(settings_dict)

    def make_gui(self):
        """Define the GUI layout and its data sources."""

        # some window formality
        set_main_window_title("TempMon")
        set_main_window_size(800, 400)
        set_item_height("logger##standard", 300)
        set_window_pos("logger##standard", 250, 30)

        # Set logger level to "Info"
        set_log_level(0)

        # define plot and table names, just for convenience.
        myplot = "CPU and GPU Temperatures"
        mytable = "Current Temps"

        with menu_bar("Menu Bar"):

            with menu("Theme"):
                add_combo(" ##Themes",
                          items = self.themes,
                          default_value=get_theme(),
                          callback=self.apply_theme)  # theme selector
                add_button("Save Theme", callback=self.save_theme)

            with menu("Actions"):
                add_button("Reset Max", callback=self.reset_max)
                add_button("Reset Plot", callback=self.reset_plot)

            with menu("Log Level"):
                # logger level selector
                add_radio_button("Log Level##logging",
                                 items = self.log_levels,
                                 callback=self.set_logger_level,
                                 default_value=2)

                add_button("Show Logger", callback=show_logger)  # shows logger
            
            with menu("Threshold"):
                # Sliders to change threshold values. Updates DPG register automatically.
                add_slider_float("CPU Threshold", default_value=get_value("cpu_threshold"), source="cpu_threshold")
                add_slider_float("GPU Threshold", default_value=get_value("gpu_threshold"), source="gpu_threshold")
                add_button("Save", callback=self.save_threshold)

        # begin left panel for table and buttons
        with group("Left Panel", width=200):
            with child("Table Window", height=75, border=False):
                add_table(mytable, ["", "Intel", "NVIDIA"])
                add_row(mytable, ["Current:", 0, 0])
                add_row(mytable, ["Max:", 0, 0])
                add_row(mytable, ["Thresh:", 0, 0])

            # indicates if temperature warning has cleared
            add_checkbox("CPU Warning Cleared?",
                         source="is_cpu_warning_cleared",
                         callback=self.warning_manually_toggled)

            add_checkbox("GPU Warning Cleared?",
                         source="is_gpu_warning_cleared",
                         callback=self.warning_manually_toggled)

        # to align plot
        add_same_line()

        # add plot
        add_plot(myplot, x_axis_name="Time (seconds)", y_axis_name="Temp")

        # set plot limits
        set_plot_xlimits(myplot, 0, 100)
        set_plot_ylimits(myplot, 0, 100)

        set_render_callback(self.plot_callback)

    def start_gui(self):
        """Method to expose start_dearpygui()"""
        start_dearpygui()
