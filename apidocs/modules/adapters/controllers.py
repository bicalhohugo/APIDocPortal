from flask import (
        Blueprint, render_template, url_for, flash, redirect
)
from apidocs.modules.access_control.manager import login_required, admin_required
from apidocs.db.mongodb import MongoDb

bp = Blueprint('adapter_controller', __name__)
db_adapters = MongoDb('adapters')
db_adapters_type = MongoDb('adapters_type')

### METHODS ###

def get_all_adapter_type():
    return db_adapters_type.get_all();

def get_adapter_type_by_id(adapter_type_id):
    return db_adapters_type.get_by_id(adapter_type_id)

def adapter_type_insert(adapter_type):
    return db_adapters_type.insert(adapter_type)

def adapter_type_update(updated_adapter_type):
    return db_adapters_type.update(updated_adapter_type)

def adapter_type_delete(adapter_type_id):
    try:
        result = db_adapters_type.delete(adapter_type_id)
        flash("Tipo de Adaptador foi excluído com sucesso!", 'success')
        return True
    except Exception as ex:
        flash("Ocorreu um erro ao excluir o tipo de adaptador: {}".format(ex), 'error')
        return False

def get_adapter_by_id(adapter_id):
    return db_adapters.get_by_id(adapter_id)

def adapter_insert(adapter):
    return db_adapters.insert(adapter)

def adapter_update(updated_adapter):
    return db_adapters.update(updated_adapter)

def adapter_delete(adapter_id):
    try:
        result = db_adapters.delete(adapter_id)
        flash("Adaptador foi excluído com sucesso!", 'success')
        return True
    except Exception as ex:
        flash("Ocorreu um erro ao excluir o adaptador: {}".format(ex), 'error')
        return False

### ROUTES ###