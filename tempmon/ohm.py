"""Module to interface with OpenHardwareMonitor.dll

Source: Stack Overflow — https://bit.ly/3dCQePS"""

"""TODO:
- [] Add support for CPU and GPU load
- [] Add support for AMD
- [] Add support for other sensors
"""

__version__ = "0.2.0-alpha.0"

import os
import clr  # pip package 'pythonnet'
from my_functions import caller_name


class Ohm:
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
        logger,
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
                Directory of OpenHardwareMonitor.dll assembly.
                Requires an absolute path.
            MainboardEnabled (bool)
            CPUEnabled (bool)
            RAMEnabled (bool)
            GPUEnabled (bool)
            HDDEnabled (bool)

        Returns:
            handle
                an object that allows access to hardware information.
        """
        self.__log = logger

        clr.AddReference(file)

        from OpenHardwareMonitor import Hardware

        self.handle = Hardware.Computer()
        self.handle.MainboardEnabled = MainboardEnabled
        self.handle.CPUEnabled = CPUEnabled
        self.handle.RAMEnabled = RAMEnabled
        self.handle.GPUEnabled = GPUEnabled
        self.handle.HDDEnabled = HDDEnabled
        self.handle.Open()

        self.__log.info(f"OHM initialized.")

    def get_cpu_temp(self) -> float:
        """Return current combined CPU Package temperature in Celsius."""

        for i in self.handle.Hardware:
            i.Update()
            for sensor in i.Sensors:
                if sensor.Name == "CPU Package":
                    if sensor.Value != None:
                        self.__log.debug(
                            f"CPU temp requested by {caller_name()}. Current: {sensor.Value}"
                        )
                        return float(sensor.Value)
                    else:
                        self.__log.warning("CPU temp is 'None'")
                        return 0.0

    def get_gpu_temp(self) -> float:
        """Return current GPU Core temperate in Celsius"""

        for i in self.handle.Hardware:
            i.Update()
            for sensor in i.Sensors:
                if sensor.Hardware.HardwareType == self.ohm_hwtypes.index(
                    "GpuNvidia"
                ) and sensor.SensorType == self.ohm_sensortypes.index("Temperature"):
                    if sensor.Value != None:
                        self.__log.debug(
                            f"GPU temp requested by {caller_name()}. Current: {sensor.Value}"
                        )
                        return float(sensor.Value)
                    else:
                        self.__log.warning("GPU temp is 'None'")
                        return 0.0