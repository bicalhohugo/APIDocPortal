from flask import (
        Blueprint, render_template, url_for, flash, redirect
)
from apidocs.modules.access_control.manager import login_required, admin_required
from apidocs.db.mongodb import MongoDb

bp = Blueprint('provider_controller', __name__)
db_providers = MongoDb('providers')

### METHODS ###

def get_provider_by_id(provider_id):
    return db_providers.get_by_id(provider_id)

def provider_insert(provider):
    return db_providers.insert(provider)

def provider_update(updated_provider):
    return db_providers.update(updated_provider)

def provider_delete(provider_id):
    try:
        result = db_providers.delete(provider_id)
        flash("Provedor foi excluído com sucesso!", 'success')
        return True
    except Exception as ex:
        flash("Ocorreu um erro ao excluir o provedor: {}".format(ex), 'error')
        return False

### ROUTES ###