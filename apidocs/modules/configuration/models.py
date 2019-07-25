from flask import (
        Blueprint
)

bp = Blueprint('configuration_model', __name__)

class ConfigurationModel:
    def __init__(self, database_prefix, database_host, database_port, database_db, database_profile, pagination_max_per_page):
        self.database_prefix = database_prefix
        self.database_host = database_host
        self.database_port = database_port
        self.database_db = database_db
        self.database_profile = database_profile
        self.pagination_max_per_page = pagination_max_per_page
    
    def get_configuration_model(self):
        model = {
                    "database": {
                        "db": self.database_db,
                        "profile": self.database_profile,
                        "local": {
                            "mongo_prefix": "mongodb",
                            "host": "localhost",
                            "port": "27017"
                        },
                        "docker": {
                            "mongo_prefix": "mongodb",
                            "host": "mongo",
                            "port": "27017"
                        },
                        "cloud": {
                            "mongo_prefix": "mongodb+srv",
                            "host": "nexteldocs:nexteldocs@nexteldocs-duwlp.mongodb.net/test?retryWrites=true&w=majority",
                            "port": ""
                        }
                        
                    },
                    "pagination": {
                        "max_per_page": int(self.pagination_max_per_page)
                    }
                }

        return model