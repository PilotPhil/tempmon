import ctypes
from elevate import elevate


def elevater():
    if ctypes.windll.shell32.IsUserAnAdmin():
        pass
    else:
        print("Not elevated.")
        elevate()
        # make sure it was successful.
        if ctypes.windll.shell32.IsUserAnAdmin():
            print("Elevation successful.")
        else:
            print("Elevation failed.")
            print("Exiting with sys code: 1")
            print("But not actually, because I'm debugging")
            # sys.exit(1)
