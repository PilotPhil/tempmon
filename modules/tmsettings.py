import json

class settings():
    def __init__(self, config_file=r'assets/config.json'):
        self.values = {"cpu_threshold": 90, "gpu_threshold": 90, "theme": "Gold"}
        self.config_file = config_file


    def import_config(self):
        with open(self.config_file, "r") as f:
            config = json.load(f)
            for key, value in config.items():
                if key in self.values:
                    self.values[key] = value
                else:
                    pass
            return self.values

    def export_config(self, settings_dict):
        with open(self.config_file, "w") as f:
            json.dump(settings_dict, f)
            print("Settings written:")
            print(json.dumps(self.values))
    
    def update(self, settings_dict):
        # need to convert subject's settings values to a 
        # validated settings dictionary so I can pass it
        # safely to export_config
        print("Observer updated. Running export_config...")
        self.export_config(settings_dict)