from flask import (
        Blueprint
)

bp = Blueprint('api_model', __name__)

class ApiModel:
    def __init__(self, method, path, summary, yamlfile, yamlstream):
        self.method = method
        self.path = path
        self.summary = summary
        self.yamlfile = yamlfile
        self.yamlstream = yamlstream
        #self.description = description
        #self.path_params = path_params
        #self.body_params = body_params
        #self.responses = responses
    
    def get_model(self):
        model = {
            "method": self.method,
            "path": self.path,
            "summary": self.summary,
            "yamlfile": self.yamlfile,
            "yamlstream": self.yamlstream
        }

        return model