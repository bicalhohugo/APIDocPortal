from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from apidocs.modules.access_control.manager import login_required, admin_required
from apidocs.config.configuration import Configuration
from apidocs.modules.configuration.models import ConfigurationModel
from apidocs.modules.user.controllers import register_new_admin

bp = Blueprint('configuration_controller', __name__)

### METHODS ###

def save_configurations():
    database_host = request.form['database_host']
    database_port = request.form['database_port']
    database_db = request.form['database_db']
    pagination_max_per_page = request.form['pagination_max_per_page']

    error = None

    if database_host is None or not database_host:
        error = 'Host da Database não informado.'
    elif database_port is None or not database_port:
        error = 'Porta da Database não informado.'
    elif database_db is None or not database_db:
        error = 'Database não informado.'
    elif pagination_max_per_page is None or not pagination_max_per_page:
        error = 'Qtd. por Página com valor inválido e/ou não informado.'
    else:
        try:
            if int(pagination_max_per_page) < 3 or int(pagination_max_per_page) > 100:
                error = 'Qtd. por Página informado deve estar entre 3 e 100.'
        except Exception as e:
            error = 'Qtd. por Página com valor inválido e/ou não informado.'

    if error is None:
        model = ConfigurationModel(database_host, database_port, database_db, pagination_max_per_page)
        config = model.get_configuration_model()
        result = Configuration().save_configurations(config)

        flash('Configurações alteradas com sucesso!', 'success')
        return True
    else:
        flash(error, 'error')
        return False

def seed():
    try:
        #Cria usuário admin
        register_new_admin('Admin', 'API Docs', 'admin@apidocs.com.br', 'admin')

        #Cria os métodos http

        return True, ""
    except Exception as e:
        return False, e

### ROUTES ###

@bp.route("/configuration/seed")
def configuration_seed():
    seed_result, seed_error = seed()
    if seed_result:
        return "Todos os dados foram adicionados no DB"
    else:
        return f"Ocorreu um erro ao adicionar as informações ao DB: {seed_error}"

@bp.route("/configuration/properties")
@login_required
@admin_required
def configuration_properties():
    config = Configuration().get_configurations()
    return render_template('configuration/properties.html', config=config)

@bp.route("/configuration/save_properties", methods=('POST',))
@login_required
@admin_required
def save_configuration_changes():
    save_configurations()
    return redirect(url_for('configuration_controller.configuration_properties'))