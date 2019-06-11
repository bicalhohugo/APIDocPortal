from flask import (
    session, current_app, flash, g
)
import os
import datetime
import base64
import re
from apidocs.config.configuration import Configuration

### STATUS ###

def status_list():
    return  { "A" : "Ativo", "D" : "Desativado", "P" : "Aguardando Aprovação" }

def show_status_text(status):
    lst = status_list()

    return lst[status]

### PROFILE ###

def profile_list():
    return  { "A" : "Administrador", "E" : "Editor", "U" : "Usuário" }

def show_profile_text(profile):
    lst = profile_list()

    return lst[profile]

### UPLOAD E YAML PATHS ###

def upload_path():
    return os.path.join(current_app.config['UPLOAD_PATH'], 'uploads')

def yml_path():
    return os.path.join(current_app.config['UPLOAD_PATH'], 'yml')

def diagrams_path():
    return os.path.join(current_app.config['UPLOAD_PATH'], 'diagrams')

### SESSION CONTROL ###

def session_clear(session_name):
    if session.get(session_name):
        session.pop(session_name)

def get_session_object(session_name):
    obj = None

    if session.get(session_name):
        obj = session.get(session_name)
    
    return obj

def write_session_object(session_name, obj):
    session[session_name] = obj

def remove_all_session_info():
    session.clear()

### Logged User Info ###

def get_logged_username():
    username = g.user['name']

    return username

### DateTime Now Info ###

def get_datetime_now():
    now = datetime.datetime.now()

    return now.strftime("%d/%m/%Y %H:%M:%S")

### Version Validator ###

def version_validator(version):
    return re.match('^[0-9]{1,2}.{1}[0-9]{1,2}.{1}[0-9]{1,2}$', version)

### Configuration Reader ###

def get_configurations():
    config = Configuration().get_configurations()
    return config