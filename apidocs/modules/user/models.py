from flask import (
        Blueprint
)

bp = Blueprint('user_model', __name__)

class UserModel:
    def __init__(self, name, email, password, status, profile):
        self.name = name
        self.email = email
        self.password = password
        self.status = status
        self.profile = profile
    
    def get_model(self):
        model = {
            'name' : self.name, 
            'email' : self.email, 
            'password' : self.password, 
            'status' : self.status, 
            'profile' : self.profile
            }
        
        return model
    
    def save_model(self):
        pass
