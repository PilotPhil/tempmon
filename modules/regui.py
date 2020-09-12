from dearpygui.dearpygui import *
from dearpygui.wrappers import *
from time import sleep, time
import ohm

# initialize OpenHardwareMonitor
ohm = ohm.helper()

class my_gui():
    def set_vars(self, settings_dict: dict):
        """Define DearPyGui data sources"""
        # Define theme names, for later use.
        self.themes = ["Dark", "Light", "Classic", "Dark 2", "Grey", "Dark Grey", "Cherry", "Purple", "Gold", "Red"]
        self.log_levels = ["Trace", "Debug", "Info", "Warning", "Error", "Off"]
        
        # Set theme, based on settings passed via argument
        set_theme(settings_dict["theme"])

        # TODO: set imported settings from here. 
        # Make config_helper instance to read config.

        # define DPG data
        add_data("CPU Temp", [])
        add_data("GPU Temp", [])
        add_data("frameCount", 0)
        add_data("timeCounter", get_total_time())
        add_data("maxCPU", 0)
        add_data("maxGPU", 0)
        add_data("threshold", settings_dict["threshold"])
        add_data("is_warning_cleared", True)

    def applyTheme(self, sender, data):
        theme = get_value(" ##Themes")
        set_theme(theme)

    def set_logger_level(self, sender, data):
        level = get_value("Log Level##logging")
        set_log_level(level)

    def reset_max(self, sender, data):
        """Reset max CPU and GPU temperature records and update table"""
        add_data("maxCPU", 0)
        add_data("maxGPU", 0)
        set_table_item(mytable, 1, 1, "0")
        set_table_item(mytable, 1, 2, "0")

    def reset_plot(self, sender, data):
        """Clear plot and reset associated variables"""
        clear_plot(myplot)
        add_data("CPU Temp", [])
        add_data("GPU Temp", [])
        add_data("frameCount", 0)

    def show_logger_callback(self, sender, data):
        show_logger()
        log("Logger opened")

    def plot_callback(self, sender, data):
        """Update plot and table data every 1 second"""
        
        # get the last time the callback updated the data
        lastTime = get_data("timeCounter")

        # if it has been >= 1 second since last update, do another update.
        # otherwise, exit.
        if get_total_time() - lastTime >= 1:
            # get the number of frames that have been rendered and increment it
            frame_count = get_data("frameCount")
            frame_count+=1
            
            #grab current CPU and GPU temp
            current_cpu, current_gpu = ohm.get_cpu(), ohm.get_gpu()

            cpu_data = get_data("CPU Temp") # Pull DearPyGui register data into local list variable
            cpu_data.append([frame_count, current_cpu]) # Adds current temp to list, paired with frame count
            
            gpu_data = get_data("GPU Temp") # Pull DearPyGui register data into local list variable
            gpu_data.append([frame_count, current_gpu]) # Adds current temp to list, paired with frame count

            if len(cpu_data) > 100: del cpu_data[0] # Keep list size under 50
            if len(gpu_data) > 100: del gpu_data[0] # Keep list size under 50

            # update plot
            add_line_series(myplot, "Intel", cpu_data, color=[0,0,255,255])
            add_line_series(myplot, "NVIDIA", gpu_data, color=[0,255,0,255])

            # update table with current temps
            set_table_item(mytable, 0, 1, str(int(current_cpu)))
            set_table_item(mytable, 0, 2, str(int(current_gpu)))

            # update plot limits, based on lowest available frame_count in cpu_data.
            # data is trimmed to 100 records, so keep the most recent 100 plot points in view.
            set_plot_xlimits(myplot, cpu_data[0][0], cpu_data[0][0]+100)

            # if current temp is higher than recorded maximum, 
            # overwrite DPG register and update table.
            if current_cpu > get_data("maxCPU"):
                add_data("maxCPU", current_cpu)
                set_table_item(mytable,1,1,(str(int(current_cpu))))
            if current_gpu > get_data("maxGPU"):
                add_data("maxGPU", current_gpu)
                set_table_item(mytable,1,2,(str(int(current_gpu))))
            
            # check if temp is above threshold and send a notification if so
            threshold = get_data("threshold")
            temps = {'CPU' : current_cpu, 'GPU' : current_gpu}
            thresh_check(threshold, temps)

            # update DPG register with all updated data
            add_data("frameCount", frame_count)
            add_data("CPU Temp", cpu_data) 
            add_data("GPU Temp", gpu_data) 
            add_data("timeCounter", get_total_time())

    def warning_manually_toggled(self, sender, data):
        log_info("Warning manually toggled.")

    def thresh_check(self, threshold: float, temps: dict) -> None:
        """Check temperature against threshold. Send notification if out of range.
        
        Args:
            threshold (float):
                The value to be checked against. If temp is higher, a notification will be sent.
            temps (dict): 
                requires a dictionary of format {sensor(str), temperature(float)}
        """
        warning_cleared = get_data("is_warning_cleared")
        for sensor, value in temps.items():
            if value > threshold:
                # check if temperature has gone below threshold since last notification
                
                if warning_cleared:
                    notif_string = f"Temp Warning: {sensor} at {value}\u00B0C"
                    # notif.send(notif_string, " ")
                    log_warning(notif_string)
                    add_data("is_warning_cleared", False)
                    warning_cleared = True
                elif not warning_cleared:
                    log_info("Temp still above threshold. Warning not cleared. Notification cancelled.")
            else:
                log("Threshold check cleared.")
                if not warning_cleared:
                    log_info("Warning cleared by system.")
                add_data("is_warning_cleared", True)
                warning_cleared = True
    
    def make_gui(self):
        """Define the GUI layout and its data sources."""

        #some window formality
        set_main_window_title("TempMon")
        set_main_window_size(800, 400)
        set_item_height("logger##standard", 300)
        set_window_pos("logger##standard", 250, 30)

        # Set logger level to "Info"
        set_log_level(2)

        # define plot and table names, just for convenience.
        myplot = "CPU and GPU Temperatures"
        mytable = "Current Temps"

        # Define theme names, for later use.
        themes = ["Dark", "Light", "Classic", "Dark 2", "Grey", "Dark Grey", "Cherry", "Purple", "Gold", "Red"]
        log_levels = ["Trace", "Debug", "Info", "Warning", "Error", "Off"]


        with menu_bar("Menu Bar"):
            
            with menu("Theme"):
                add_combo(" ##Themes", themes, default_value="Gold", callback=self.applyTheme) # theme selector

            with menu("Actions"):
                add_button("Reset Max", callback=self.reset_max) # resets max temp records to 0
                add_button("Reset Plot", callback=self.reset_plot) # resets plot

            with menu("Log Level"):
                add_radio_button("Log Level##logging", log_levels, callback=self.set_logger_level, default_value=2) # logger level selector
                add_button("Show Logger", callback=show_logger) # shows logger



        # begin left panel for table and buttons
        with group("Left Panel", width=200):
            with child("Table Window", height=75, border=False):
                add_table(mytable, ["","Intel", "NVIDIA"])
                add_row(mytable, ["Current:", 0, 0])
                add_row(mytable, ["Max:", 0, 0])
            
            add_checkbox("Warning Cleared?", data_source="is_warning_cleared", callback=self.warning_manually_toggled) # indicates if temperature warning has cleared

        # to align plot
        add_same_line()

        # add plot
        add_plot(myplot, "Time", "Temp")

        # set plot limits
        set_plot_xlimits(myplot, 0, 100)
        set_plot_ylimits(myplot, 0, 100)

        set_render_callback(self.plot_callback)

    def start_gui(self):
        """Method to expose start_dearpygui()"""
        start_dearpygui()