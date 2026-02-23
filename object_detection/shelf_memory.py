from config_loader import load_config, save_config


class ShelfMemory:
    def __init__(self):
        self.config = load_config()
        self.inventory = self.config["inventory"]

    def register_pickup(self, label):
        if label in self.inventory and self.inventory[label] > 0:
            self.inventory[label] -= 1
            self.config["inventory"] = self.inventory
            save_config(self.config)