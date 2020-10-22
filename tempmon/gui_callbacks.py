from time import sleep
import pendulum
import dearpygui.core as dc
import dearpygui.simple as ds
from my_func import Logger

last_run_time = pendulum.now()
Logger.info(f"{last_run_time = }")


class Callbacks:
    def __init__(self):
        pass

    def register_sg(self, sg):
        self.__sg = sg

    def update_plot(self, *args):
        """
        docstring
        """
        pass

    # Alright, this guy is all fucked up.
    def render_callback(self, *args):
        # # Wait for one second before continuing
        # sleep(1)
        # # Okay, well THAT didn't work so good.

        global last_run_time
        # now = pendulum.now()
        # print(last_run_time)

        # if last_run_time.add(seconds=1) > pendulum.now():
        if last_run_time.diff(pendulum.now()).in_seconds() > 1:
            # Update latest run time for the next loop
            last_run_time = pendulum.now()
            Logger.debug(f"{last_run_time = }, {pendulum.now() = }")
            Logger.info("1 second since last temperature update. Running...")

            # update plot
            cpu, gpu = self.__sg.get_temps()
            Logger.debug("Entering...")
            try:
                Logger.debug(f"Got temps: {cpu[-1] = }, {gpu[-1] = }")
                Logger.debug(f"{len(cpu) = }, {len(gpu) = }")
            except IndexError:
                Logger.debug("'cpu' or 'gpu' variable is empty.")
            dc.add_line_series(
                "CPU and GPU Temperatures", "Intel", cpu, color=[0, 0, 255, 255]
            )
            dc.add_line_series(
                "CPU and GPU Temperatures", "NVIDIA", gpu, color=[0, 255, 0, 255]
            )
            try:
                dc.set_plot_xlimits("CPU and GPU Temperatures", cpu[0][0], cpu[-1][0])
            except IndexError:
                Logger.debug("'cpu' or 'gpu' variable is empty.")
            Logger.debug("Exiting...")
        else:
            Logger.debug("Less than 1 second since last temperature update. Passing...")


def call(instance_method):
    def cb(*args):
        return instance_method(instance_method.__self__, *args)

    return cb


# ent = Entity()

# add_button("See me", callback=oop_callback(ent.do_something))
# add_button("Watch me", callback=oop_callback(ent.do_another))
# start_dearpygui()