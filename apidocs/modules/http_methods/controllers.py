from flask import (
        Blueprint, render_template, url_for, flash, redirect
)
from apidocs.modules.access_control.manager import login_required, admin_required
from apidocs.db.mongodb import MongoDb
from apidocs.modules.http_methods.models import HttpMethodsModel

bp = Blueprint('http_methods_controller', __name__)
db_http_methods = MongoDb('http_methods')

### METHODS ###

def get_http_methods():
    return db_http_methods.get_all()

def get_http_method_by_key(method):
    filter = { 'method' : method}

    return db_http_methods.get_one_by_filter(filter)

def save_http_methods(method, button_class, div_class):
    if get_http_method_by_key(method):
        return
        
    http_methods = HttpMethodsModel(method, button_class, div_class).get_model()

    http_methods_insert(http_methods)

def http_methods_insert(http_methods):
    return db_http_methods.insert(http_methods)