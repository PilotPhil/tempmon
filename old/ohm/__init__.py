import os
import clr  # package pythonnet, not clr


class helper:

    # Define hardware and sensor types for use in later functions. Order matters.
    ohm_hwtypes = [
        "Mainboard",
        "SuperIO",
        "CPU",
        "RAM",
        "GpuNvidia",
        "GpuAti",
        "TBalancer",
        "Heatmaster",
        "HDD",
    ]
    ohm_sensortypes = [
        "Voltage",
        "Clock",
        "Temperature",
        "Load",
        "Fan",
        "Flow",
        "Control",
        "Level",
        "Factor",
        "Power",
        "Data",
        "SmallData",
    ]
    handle = None

    def __init__(
        self,
        file=os.path.join(os.path.dirname(__file__), r"OpenHardwareMonitorLib.dll"),
        MainboardEnabled=False,
        CPUEnabled=True,
        RAMEnabled=False,
        GPUEnabled=True,
        HDDEnabled=False,
    ):
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

        self.handle = Hardware.Computer()
        self.handle.MainboardEnabled = MainboardEnabled
        self.handle.CPUEnabled = CPUEnabled
        self.handle.RAMEnabled = RAMEnabled
        self.handle.GPUEnabled = GPUEnabled
        self.handle.HDDEnabled = HDDEnabled
        self.handle.Open()

    def get_cpu(self) -> float:
        """Return current combined CPU Package temperature in Celsius."""
        for i in self.handle.Hardware:
            i.Update()
            for sensor in i.Sensors:
                if sensor.Name == "CPU Package":
                    if sensor.Value != None:
                        return float(sensor.Value)
                    else:
                        return 0.0

    def get_gpu(self) -> float:
        """Return current GPU Core temperate in Celsius"""
        for i in self.handle.Hardware:
            i.Update()
            for sensor in i.Sensors:
                if sensor.Hardware.HardwareType == self.ohm_hwtypes.index(
                    "GpuNvidia"
                ) and sensor.SensorType == self.ohm_sensortypes.index("Temperature"):
                    if sensor.Value != None:
                        return float(sensor.Value)
                    else:
                        return 0.0