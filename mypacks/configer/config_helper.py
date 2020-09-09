import json

class Iconfig_interface():
    def __init__(self, config_file=r'assets/config.txt'):
        # Define config file location
        self.config_file = config_file

class reader(Iconfig_interface):    
    # define config readers and writers
    def read(self) -> float:
        """Read file, return a float"""
        with open(self.config_file, 'r') as f:
            threshold = f.read()
        return float(threshold)

class writer(Iconfig_interface):
    def write(self, value: float) -> None:
        """Write config value to file"""
        with open(self.config_file, 'w') as write_file:
            # f.write(str(value))
            json.dump(value, write_file)
            print(str(value))

