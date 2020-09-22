import json

class settings():
    def __init__(self, config_file=r'assets/config.json'):
        self.values = {"threshold":90, "theme":"Gold"}
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

    def export_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.values, f)
            print("Settings written:")
            print(json.dumps(self.values))