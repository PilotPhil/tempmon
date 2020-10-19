import sys
import ctypes
import inspect
import arrow
import elevate


def elevater(logger):
    """Function to check for UAC permissions, and request them if not present."""

    # Check if already running as Windows Administrator
    if ctypes.windll.shell32.IsUserAnAdmin():
        logger.info("Already elevated. Continuing...")
    # If not, use the 'elevate' module to try to gain permission
    else:
        logger.warning("Not elevated. Attempting UAC elevation...")
        try:
            elevate.elevate()
            logger.info("UAC elevation successful. Continuing...")
        except OSError:
            logger.critical("UAC elevation failed. Exiting with status code 1.")
            sys.exit(1)


def caller_name(skip=2):
    """Get a name of a caller in the format module.class.method

    `skip` specifies how many levels of stack to skip while getting caller
    name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

    An empty string is returned if skipped levels exceed stack height

    Source: Stack Overflow — https://bit.ly/3o31hqi
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return ""
    parentframe = stack[start][0]

    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if "self" in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals["self"].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != "<module>":  # top level usually
        name.append(codename)  # function or a method

    # Avoid circular refs and frame leaks
    #  https://docs.python.org/2.7/library/inspect.html#the-interpreter-stack
    del parentframe, stack

    return ".".join(name)


class Sensor_grabber:
    def __init__(self, logger, ohm):
        self.__log = logger
        self.__ohm = ohm
        self.__cpu_temp = []
        self.__gpu_temp = []

    def __get_cpu_temp(self):
        """Private function to get CPU temperature"""
        pass

    def __get_gpu_temp(self):
        """Private function to get GPU temperature"""
        pass

    def update(self):
        """Update internal variables with current sensor temps"""
        pass

    def monitor_temps(self):
        """Function to update private temp variables every 1 second"""
        pass

    def get_temps(self):
        """Retrieve current variable data"""
        pass