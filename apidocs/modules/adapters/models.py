from flask import (
        Blueprint
)

bp = Blueprint('adapter_type_model', __name__)

class AdapterTypeModel:
    def __init__(self, type):
        self.type = type
    
    def get_model(self):
        model = {
            "type": self.type
        }

        return model