from flask import (
    Blueprint
)
import json

bp = Blueprint('config', __name__)

class Configuration(object):
    def __init__(self):
        self.config = []
        with open("config/properties.config", "r") as prop:
            self.config = json.load(prop)

    def get_configurations(self):
        return self.config
    
    def save_configurations(self, configurations):
        self.config = configurations
        with open('config/properties.config', 'w') as f:
            json.dump(self.config, f, indent=4)

        return "Ok"
