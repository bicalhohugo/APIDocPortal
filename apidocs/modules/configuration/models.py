from flask import (
        Blueprint
)

bp = Blueprint('configuration_model', __name__)

class ConfigurationModel:
    def __init__(self, database_host, database_port, database_db, pagination_max_per_page):
        self.database_host = database_host
        self.database_port = database_port
        self.database_db = database_db
        self.pagination_max_per_page = pagination_max_per_page
    
    def get_configuration_model(self):
        model = {
                    "database": {
                        "host": self.database_host,
                        "port": int(self.database_port),
                        "db": self.database_db
                    },
                    "pagination": {
                        "max_per_page": int(self.pagination_max_per_page)
                    }
                }

        return model