__version__ = "0.5.0-alpha.0"

import json


class settings:
    def __init__(self, config_file=r"assets/config.json"):
        self.values = {}
        self.config_file = config_file

    def import_config(self):
        with open(self.config_file, "r") as f:
            config = json.load(f)
            self.values.update(config)
            return self.values

    def export_config(self, settings_dict):
        with open(self.config_file, "w") as f:
            self.values.update(settings_dict)
            json.dump(self.values, f)
            print("Settings written:")
            print(json.dumps(settings_dict))

    def update(self, settings_dict):
        # need to convert subject's settings values to a
        # validated settings dictionary so I can pass it
        # safely to export_config
        print("Observer updated. Running export_config...")
        self.export_config(settings_dict)
