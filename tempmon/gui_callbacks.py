import dearpygui.core as dc
import dearpygui.simple as ds


class Callbacks:
    def __init__(self, logger):
        self.__log = logger

    def register_sg(self, sg):
        self.__sg = sg

    def update_plot(self, *args):
        """
        docstring
        """
        pass

    # Alright, this guy is all fucked up.
    def render_callback(self, *args):
        # update plot
        cpu, gpu = self.__sg.get_temps()
        self.__log.debug("render_callback started")
        try:
            self.__log.debug(f"render_callback got temps: {cpu[-1] = }, {gpu[-1] = }")
        except IndexError:
            self.__log.debug("cpu or gpu variable is empty.")
        dc.add_line_series(
            "CPU and GPU Temperatures", "Intel", cpu, color=[0, 0, 255, 255]
        )
        dc.add_line_series(
            "CPU and GPU Temperatures", "NVIDIA", gpu, color=[0, 255, 0, 255]
        )
        try:
            dc.set_plot_xlimits("CPU and GPU Temperatures", cpu[0][0], cpu[-1][0])
        except IndexError:
            self.__log.debug("cpu or gpu variable is empty.")


def call(instance_method):
    def cb(*args):
        return instance_method(instance_method.__self__, *args)

    return cb


# ent = Entity()

# add_button("See me", callback=oop_callback(ent.do_something))
# add_button("Watch me", callback=oop_callback(ent.do_another))
# start_dearpygui()