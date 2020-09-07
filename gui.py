from dearpygui.dearpygui import *
from time import sleep, time
import ohm_helper
from notify_run import Notify
import config_helper

# initialize OpenHardwareMonitor
ohm = ohm_helper.ohm_helper()

# initialize Notify.run
notif = Notify()

class my_gui():
    def __init__(self):
        """Define the GUI layout and its data sources.
        """
        #some window formality
        set_main_window_title("TempMon")
        set_main_window_size(800, 400)

        # define plot and table names, just for convenience.
        myplot = "CPU and GPU Temperatures"
        mytable = "Current Temps"

        # Define theme names, for later use.
        themes = ["Dark", "Light", "Classic", "Dark 2", "Grey", "Dark Grey", "Cherry", "Purple", "Gold", "Red"]

        # And set it.
        set_theme("Gold")

        # Make config_helper instance to read config.
        configer = config_helper.config_reader()

        # define DPG data
        add_data("CPU Temp", [])
        add_data("GPU Temp", [])
        add_data("frameCount", 0)
        add_data("timeCounter", get_total_time())
        add_data("maxCPU", 0)
        add_data("maxGPU", 0)
        add_data("threshold", configer.conread())
        add_data("is_warning_cleared", True)

        # begin left panel
        add_group("Left Panel", width=200)

        # theme changer combo box and necessary callback
        add_combo(" ##Themes", themes, default_value="Gold", callback="my_gui.applyTheme", parent="Left Panel", before="Table Window")

        # add table to display current and max temp
        # and confine to a child group to restrict height
        add_child("Table Window", height=75, border=False)
        add_table(mytable, ["","Intel", "NVIDIA"])
        add_row(mytable, ["Current:", 0, 0])
        add_row(mytable, ["Max:", 0, 0])
        end_child()

        # add a button to reset max temp records to 0
        add_button("Reset Max", callback="reset_max")

        # add a button to rest plot
        add_button("Reset Plot", callback="my_gui.reset_plot")

        # add a button to show logger
        add_button("Show Logger", callback="my_gui.show_logger_callback")

        # add checkbox to indicate if temp warning has cleared
        add_checkbox("Warning Cleared?", data_source="is_warning_cleared", callback="my_gui.warning_manually_toggled")

        # add logger level combo box
        log_levels = ["Trace", "Debug", "Info", "Warning", "Error", "Off"]
        add_radio_button("Log Level##logging", log_levels, callback="my_gui.set_logger_level", default_value=2)

        # end left panel
        end_group()


        # add plot within a window
        add_same_line()
        add_group("Right Panel")
        add_plot(myplot, "Time", "Temp")
        end_group()

        # set plot limits
        set_plot_xlimits(myplot, 0, 100)
        set_plot_ylimits(myplot, 0, 100)

    @staticmethod
    def applyTheme(sender, data):
        theme = get_value(" ##Themes")
        set_theme(theme)

    @staticmethod
    def set_logger_level(sender, data):
        level = get_value("Log Level##logging")
        set_log_level(level)

    @staticmethod
    def reset_max(sender, data):
        """Reset max CPU and GPU temperature records and update table"""
        add_data("maxCPU", 0)
        add_data("maxGPU", 0)
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
            clear_plot(myplot)
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
        self.thresh_check(threshold, temps)

        # update DPG register with all updated data
        add_data("frameCount", frame_count)
        add_data("CPU Temp", cpu_data) 
        add_data("GPU Temp", gpu_data) 
        add_data("timeCounter", get_total_time())   

    @staticmethod
    def warning_manually_toggled(sender, data):
        log_info("Warning manually toggled.")

    @staticmethod
    def thresh_check(threshold: float, temps: dict) -> None:
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
                    notif.send(notif_string, " ")
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

    def start_gui(self):
        start_dearpygui()