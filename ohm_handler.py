'''Custom handler for retrieving sensor data from OpenHardwareMonitorLib.dll
NOTE: Must be run as Admin to retrieve CPU temps. 

TODO:
- convert to class, to protect private variables
- install somewhere so that this can be used in other projects, and not just in the working directory.
- compile as distributable wheel
'''

import clr #package pythonnet, not clr

# Define hardware and sensor types for use in later functions. Order matters.
ohm_hwtypes = ['Mainboard','SuperIO','CPU','RAM','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']
ohm_sensortypes = ['Voltage','Clock','Temperature','Load','Fan','Flow','Control','Level','Factor','Power','Data','SmallData']

def init_ohm(file = r'C:\Users\caden\source\playground\tempmon\OpenHardwareMonitorLib.dll', 
             MainboardEnabled = False, 
             CPUEnabled = True, 
             RAMEnabled = False, 
             GPUEnabled = True, 
             HDDEnabled = False):
    """Initialize the OpenHardwareMonitor library and return a handle object.

    Specific hardware types can be enabled with arguments.
    By default, only the CPU and GPU are enabled.

    Args:
        file (str):
            Location of OpenHardwareMonitor.dll assembly
            Seems to require an absolute path.
        MainboardEnabled (bool)
        CPUEnabled (bool)
        RAMEnabled (bool)
        GPUEnabled (bool)
        HDDEnabled (bool)

    Returns:
        handle
            an object that allows access to hardware information.
    """
    clr.AddReference(file)

    from OpenHardwareMonitor import Hardware

    handle = Hardware.Computer()
    handle.MainboardEnabled = MainboardEnabled
    handle.CPUEnabled = CPUEnabled
    handle.RAMEnabled = RAMEnabled
    handle.GPUEnabled = GPUEnabled
    handle.HDDEnabled = HDDEnabled
    handle.Open()
    return handle

def cpu_temp(handle):
    """Return current combined CPU Package temperature in Celsius."""
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            if sensor.Name == 'CPU Package':
                return float(sensor.Value)
            
def gpu_temp(handle):
    """Return current GPU Core temperate in Celsius"""
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            if sensor.Hardware.HardwareType == ohm_hwtypes.index('GpuNvidia') and sensor.SensorType == ohm_sensortypes.index('Temperature'):
                return float(sensor.Value)

# ************** DEPRECRATED **************
'''
def print_all_sensors(handle):
    """Print all sensor data."""
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            print(f"""
{ohm_hwtypes[sensor.Hardware.HardwareType] = }
{ohm_sensortypes[sensor.SensorType] = }
{sensor.Name = }
{sensor.Value = }
{sensor.Index = }""")

# Original functions
# NOTE: all deprecated.

def fetch_stats(handle):
    """DEPRECATED - Fetch all stats."""
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            parse_sensor(sensor)
        for j in i.SubHardware:
            j.Update()
            for subsensor in j.Sensors:
                parse_sensor(subsensor)

def parse_sensor(sensor):
    """DEPECRECATED - Return temperature values"""
    if sensor.Value is not None:
        if sensor.SensorType == ohm_sensortypes.index('Temperature'):
            print(u"%s %s Temperature Sensor #%i %s - %s\u00B0C" % (ohm_hwtypes[sensor.Hardware.HardwareType], sensor.Hardware.Nam00
'''
# ************** END DEPRECRATED **************