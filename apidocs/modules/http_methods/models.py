from flask import (
        Blueprint
)

bp = Blueprint('http_methods_model', __name__)

class HttpMethodsModel:
    def __init__(self, method, button_class, div_class):
        self.method = method
        self.button_class = button_class
        self.div_class = div_class
    
    def get_model(self):
        model = {
            "method": self.method,
            "button_class": self.button_class,
            "div_class": self.div_class
        }

        return model