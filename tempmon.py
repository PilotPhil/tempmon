'''A simple GUI to monitor CPU and GPU core temperatures

NOTE: Must be run as admin

TODO:
- [DONE] implement button to reset plot
- [DONE] implement button to reset max values
- implement popup to warn of high temps
- add current temp to plot, at plot point
- add historical temp when mousing over plot
- convert x-axis value from total_running_time to the actual time
- [DONE] add to Github
- add view for fan speed
- add other system sensors
- show time and time since highest recorded temperature
- send notifications to phone to warn of high temps (notify.run)
    - add checkbox to show whether warning has cleared or not
    - add value picker to change threshold
    - add config reader for persistent threshold setting
        - convert config_reader() from plaintext to JSON
'''

from dearpygui.dearpygui import *
from ohm_handler import *
from time import sleep, time
from notify_run import Notify


# initialize OpenHardwareMonitor
handle = init_ohm()

# initialize Notify.run
notif = Notify()

# Some window formality
set_main_window_title("TempMon")
set_main_window_size(800, 400)

# Show logger
show_logger()

# Define config file location
config_file = r'assets/config.txt'

# define plot and table names
myplot = "CPU and GPU Temperatures"
mytable = "Current Temps"

# define DPG data
add_data("CPU Temp", [])
add_data("GPU Temp", [])
add_data("frameCount", 0)
add_data("timeCounter", get_total_time())
add_data("maxCPU", 0)
add_data("maxGPU", 0)
add_data("threshold", config_reader(config_file))

# begin left panel
add_group("Left Panel", width=200)

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
add_button("Reset Plot", callback="reset_plot")

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

# assign render callback to the plot window
set_render_callback("plot_callback")

# theme changer combo box and necessary callback
set_theme("Gold")
themes = ["Dark", "Light", "Classic", "Dark 2", "Grey", "Dark Grey", "Cherry", "Purple", "Gold", "Red"]
add_combo(" ##Themes", themes, default_value="Gold", callback="applyTheme", parent="Left Panel", before="Table Window")

def applyTheme(sender, data):
    theme = get_value(" ##Themes")
    set_theme(theme)

def reset_max(sender, data):
    """Reset max CPU and GPU temperature records and update table"""
    add_data("maxCPU", 0)
    add_data("maxGPU", 0)
    set_table_item(mytable, 1, 1, "0")
    set_table_item(mytable, 1, 2, "0")

def reset_plot(sender, data):
    """Clear plot and reset associated variables"""
    clear_plot(myplot)
    add_data("CPU Temp", [])
    add_data("GPU Temp", [])
    add_data("frameCount", 0)

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
        current_cpu, current_gpu = cpu_temp(handle), gpu_temp(handle)

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
        thresh_check(threshold, temps)

        # update DPG register with all updated data
        add_data("frameCount", frame_count)
        add_data("CPU Temp", cpu_data) 
        add_data("GPU Temp", gpu_data) 
        add_data("timeCounter", get_total_time())

def thresh_check(threshold: float, temps: dict) -> None:
    """Check temperature against threshold. Send notification if out of range.
    
    Args:
        threshold (float):
            The value to be checked against. If temp is higher, a notification will be sent.
        temps (dict): 
            requires a dictionary of format {sensor(str), temperature(float)}
    """
    for sensor, value in temps:
        if value > threshold:
            # check if temperature has gone below threshold since last notification
            warning_cleared = get_data("is_warning_cleared")
            if warning_cleared:
                notif_string = f"Temp Warning: {sensor} at {value}\u00B0C"
                notif.send(notif_string, " ")
                log_warning(notif_string)
                add_data("is_warning_cleared", False)
        else:
            log("Threshold check cleared.")
            add_data("is_warning_cleared", True)

def config_reader(file) -> float:
    with open(file, 'r') as f:
        threshold = f.read()
    return threshold


# and kick it off.
start_dearpygui()
