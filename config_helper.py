class Iconfig_interface():
    # Define config file location
    config_file = r'assets/config.txt'

class config_reader(Iconfig_interface):    
    # define config readers and writers
    def read(self) -> float:
        """Read file, return a float"""
        with open(self.config_file, 'r') as f:
            threshold = f.read()
        return float(threshold)

class config_writer(Iconfig_interface):
    def write(self, value: float) -> None:
        '''Write config value to file'''
        with open(self.config_file, "w") as f:
            f.write(str(value))
            print(str(value))

