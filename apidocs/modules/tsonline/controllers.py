from flask import (
    Blueprint, render_template, redirect, request, url_for, flash,
    send_from_directory)
import os
import shutil
import yaml
from apidocs.modules.access_control.manager import login_required, editor_required
from apidocs.modules.adapters.controllers import get_all_adapter_type
from apidocs.modules.api.controllers import update_api, write_api, get_api_by_path_and_method, api_already_exists, css_button_class, css_div_class
from apidocs.modules.api.models import ApiModel
from apidocs.modules.orch.controllers import get_non_published_orchs, get_orch_by_id, get_orch_data_by_orch_id, \
    get_orch_history_by_orch_id, get_all_orch_history_by_orch_name, orch_insert, get_orch_by_name_and_version, \
    orch_data_update, orch_data_insert, orch_update, orch_history_insert, orch_history_update
from apidocs.modules.orch.models import OrchModel, OrchHistoryModel, OrchMappingSuccessOutputModel, \
    OrchMappingErrorOutputModel, OrchReturnCodeSuccessModel, OrchReturnCodeErrorModel, OrchDataModel, \
    OrchMappingServicesModel, OrchServicesModel, OrchRetryPolicyModel, OrchMappingInputModel
from apidocs.modules.service.controllers import service_insert, get_service_by_name_and_version, get_service_by_id, \
    service_data_insert, get_service_data_by_service_id, service_data_update, \
    service_history_insert, service_history_update, get_all_service_history_by_service_name, \
    get_service_history_by_service_id, service_update, get_non_published_services
from apidocs.modules.service.models import ServiceModel, ServiceDataModel, ServiceProviderModel, ServiceAdapterModel, \
    ServiceApisModel, ServiceOrchestratorsModel, ServiceMappingInputModel, ServiceMappingSuccessOutputModel, \
    ServiceMappingErrorOutputModel, ServiceReturnCodeSuccessModel, ServiceReturnCodeErrorModel, \
    ServiceDbAdapterConfiguration, ServiceWsAdapterConfiguration, ServiceHistoryModel, get_id_key, ServiceRmq, \
    ServiceRmqRetryPolicy, ServiceRmqConfiguration
from apidocs.helpers.utils import session_clear, get_session_object, write_session_object, upload_path, yml_path, \
    version_validator, diagrams_path

bp = Blueprint('tsonline_controller', __name__)

### METHODS ###

def session_api_preview_clear():
    session_clear('apis-preview')

def get_api_preview_from_session():
    return get_session_object('apis-preview')

def write_api_preview_in_session(obj):
    write_session_object('apis-preview', obj)

def move_yaml_file(yaml_file, api_id):
    original_path = os.path.join(upload_path(), yaml_file)
    new_path = os.path.join(yml_path(), "{}.yaml".format(api_id))
    
    if os.path.isfile(original_path):
        shutil.copy2(original_path, new_path)
        remove_uploaded_file(yaml_file)

def remove_uploaded_file(uploaded_filename):
    file = os.path.join(upload_path(), uploaded_filename)
    if os.path.exists(file):    
        os.remove(file)

def api_upload_to_preview():
    session_api_preview_clear()

    try:
        yaml_file = request.files['yaml_file']
        yaml_filename = yaml_file.filename

        file = os.path.join(upload_path(), yaml_filename)
        yaml_file.save(file)

        yaml_stream = None

        with open(file, 'r') as stream:
            yaml_stream = yaml.safe_load(stream)

        paths = None
        
        try:
            paths = yaml_stream['paths']
        except:
            raise Exception("O arquivo informado não possui o atributo 'PATHS' obrigatório para as APIs")
        
        if paths:
            apis_already_exists = []
            apis = []

            for path in paths:
                methods = paths[path]
                for method in methods:
                    try:
                        summary = methods[method]['summary']
                    except:
                        summary = "(Sem descrição)"

                    api = ApiModel(str(method).upper(), str(path), summary, yaml_filename, str(yaml_stream)).get_model()

                    #print("API inserida no preview: {}".format(api))

                    if api_already_exists(api):
                        apis_already_exists.append(api)
                    else:
                        apis.append(api)

            if len(apis_already_exists) + len(apis) > 1:
                raise Exception("O arquivo contém mais de 1 API, por favor, separe as APIs em arquivos distintos e tente novamente.")

            #flash("{} API(s) lida com sucesso do arquivo YAML '{}'.".format(len(apis) + len(apis_already_exists), yaml_filename), 'success')
            write_api_preview_in_session({ 'apis_to_insert': apis, 'apis_to_update': apis_already_exists })

            return True

    except FileNotFoundError:
        flash("Arquivo YAML não foi informado!", 'error')
        session_api_preview_clear()

    except Exception as ex:
        flash("Erro ao processar o arquivo YAML '{}'. ERRO: {}.".format(yaml_filename, ex), 'error')
        session_api_preview_clear()

        remove_uploaded_file(yaml_filename)

    return False

def api_save():
    files_to_move = []

    try:
        apis = get_api_preview_from_session()

        for api in apis['apis_to_insert']:
            #print("API inserida no db: {}".format(api))
            result = write_api(api)

            files_to_move.append({ 'yaml_file': api['yamlfile'], 'api_id' : result })
       
        for api in apis['apis_to_update']:
            #print("API atualizada no db: {}".format(api))
            api_to_update = get_api_by_path_and_method(api)[0]
            api_to_update['summary'] = api['summary']
            api_to_update['yamlfile'] = api['yamlfile']
            api_to_update['yamlstream'] = api['yamlstream']
            result = update_api(api_to_update)
            
            files_to_move.append({ 'yaml_file': api['yamlfile'], 'api_id' : result })

        for file in files_to_move:
            move_yaml_file(file['yaml_file'], file['api_id'])
    
        flash('API(s) gravada(s) no banco de dados com sucesso!', 'info')
        session_api_preview_clear()
        
        return True
    except Exception as ex:
        for file in files_to_move:
            remove_uploaded_file(file['yaml_file'])
        
        flash('Ocorreu um erro ao gravar os dados da API na base. ERRO: {}'.format(ex), 'error')

        return False

### ROUTES ###

### APIS ###

@bp.route("/tsonline/apis")
@login_required
@editor_required
def tsonline_apis():
    return render_template('tsonline/apis.html')

@bp.route("/tsonline/apis/upload", methods=('POST',))
@login_required
@editor_required
def tsonline_apis_upload():
    if api_upload_to_preview() == True:
        return redirect(url_for('tsonline_controller.tsonline_apis_preview'))
    else:
        return redirect(url_for('tsonline_controller.tsonline_apis'))

@bp.route("/tsonline/apis/preview")
@login_required
@editor_required
def tsonline_apis_preview():
    apis = get_api_preview_from_session()
    
    return render_template('tsonline/apis-preview.html', apis=apis, css_button_class=css_button_class, css_div_class=css_div_class)

@bp.route("/tsonline/apis/save", methods=('POST',))
@login_required
@editor_required
def tsonline_apis_save():
    if api_save() == True:
        return redirect(url_for('tsonline_controller.tsonline_apis'))
    else:
        return redirect(url_for('tsonline_controller.tsonline_apis_preview'))

### ORCHS ###

def save_new_orch():
    try:
        orch_name = request.form['orch_name']
        orch_version = request.form['orch_version']

        error = None
        if orch_name is None or orch_name == "":
            error = "Nome do orquestrador não está preenchido"
        elif orch_version is None or orch_version == "":
            error = "Versão do orquestrador não está preenchida"
        elif not version_validator(orch_version):
            error = "Versão está diferente do formato esperado. Exemplo: X.X.X ou 1.0.0"

        if error:
            flash(error, 'error')
            return False, None

        orch_in_db = get_orch_by_name_and_version(orch_name, orch_version)

        if orch_in_db:
            return False, orch_in_db['_id']

        orch_obj = OrchModel(orch_name, orch_version).get_model()

        return True, orch_insert(orch_obj)
    except Exception as ex:
        flash(f"Ocorreu um erro ao criar o orquestrador e a versão. ERRO: {ex}", 'error')
        return False, None

def orch_data_save(type, orch_id):
    try:
        description = request.form['description']

        txt_paradigm = request.form['paradigm']
        paradigm = ServiceProviderModel(1, txt_paradigm).get_model()

        txt_mechanism = request.form['mechanism']
        mechanism = ServiceAdapterModel(2, txt_mechanism).get_model()

        history_ids = request.form.getlist('history_id')
        history_orch_ids = request.form.getlist('history_orch_id')
        history_orch_names = request.form.getlist('history_orch_name')
        history_orch_versions = request.form.getlist('history_orch_version')
        history_dates = request.form.getlist('history_date')
        history_authors = request.form.getlist('history_author')
        history_projects = request.form.getlist('history_project')
        history_descriptions = request.form.getlist('history_description')

        for i in range(len(history_ids)):
            history_id = history_ids[i]
            history_orch_id = history_orch_ids[i]

            if history_id == "0" or history_orch_id == orch_id:

                history_orch_name = history_orch_names[i]
                history_orch_version = history_orch_versions[i]
                history_date = history_dates[i]
                history_author = history_authors[i]
                history_project = history_projects[i]
                history_description = history_descriptions[i]

                obj_history = OrchHistoryModel(history_orch_id, history_orch_name, history_orch_version, history_date, history_author, history_project, history_description).get_model()

                if history_id == "0":
                    orch_history_insert(obj_history)
                else:
                    obj_history["_id"] = get_id_key(history_id)
                    orch_history_update(obj_history)

        services = []
        services_orchestrated_orders = request.form.getlist('services_orchestrated_order')
        services_orchestrated_mss = request.form.getlist('services_orchestrated_ms')
        services_orchestrated_ruless = request.form.getlist('services_orchestrated_rules')
        services_orchestrated_paradigms = request.form.getlist('services_orchestrated_paradigm')
        services_orchestrated_retrys = request.form.getlist('services_orchestrated_retry')
        services_orchestrated_providers = request.form.getlist('services_orchestrated_provider')

        for i in range(len(services_orchestrated_orders)):
            services_orchestrated_order = services_orchestrated_orders[i]
            services_orchestrated_ms = services_orchestrated_mss[i]
            services_orchestrated_rules = services_orchestrated_ruless[i]
            services_orchestrated_paradigm = services_orchestrated_paradigms[i]
            services_orchestrated_retry = services_orchestrated_retrys[i]
            services_orchestrated_provider = services_orchestrated_providers[i]

            services.append(OrchServicesModel(services_orchestrated_order, services_orchestrated_ms, services_orchestrated_rules, services_orchestrated_paradigm, services_orchestrated_retry, services_orchestrated_provider).get_model())

        retry_policy = []
        retry_policy_mss = request.form.getlist('retry_policy_ms')
        retry_policy_retrys = request.form.getlist('retry_policy_retry')
        retry_policy_intervals = request.form.getlist('retry_policy_interval')

        for i in range(len(retry_policy_mss)):
            retry_policy_ms = retry_policy_mss[i]
            retry_policy_retry = retry_policy_retrys[i]
            retry_policy_interval = retry_policy_intervals[i]

            retry_policy.append(OrchRetryPolicyModel(retry_policy_ms, retry_policy_retry, retry_policy_interval).get_model())

        mapping_services = []
        request_ms_names = request.form.getlist('request_ms_name')

        for i in range(len(request_ms_names)):
            request_ms_name = request_ms_names[i]

            mapping_input = []
            mapping_input_canonicals = request.form.getlist(f'mapping_input_canonical_{i + 1}')
            mapping_input_descriptions = request.form.getlist(f'mapping_input_description_{i + 1}')
            mapping_input_requireds = request.form.getlist(f'mapping_input_required_{i + 1}')
            mapping_input_data_types = request.form.getlist(f'mapping_input_data_type_{i + 1}')
            mapping_input_domains = request.form.getlist(f'mapping_input_domain_{i + 1}')
            mapping_input_provider_tags = request.form.getlist(f'mapping_input_provider_tag_{i + 1}')
            mapping_input_ms_ruless = request.form.getlist(f'mapping_input_ms_rules_{i + 1}')

            for j in range(len(mapping_input_canonicals)):
                mapping_input_canonical = mapping_input_canonicals[j]
                mapping_input_description = mapping_input_descriptions[j]
                mapping_input_required = mapping_input_requireds[j]
                mapping_input_data_type = mapping_input_data_types[j]
                mapping_input_domain = mapping_input_domains[j]
                mapping_input_provider_tag = mapping_input_provider_tags[j]
                mapping_input_ms_rules = mapping_input_ms_ruless[j]

                mapping_input.append(OrchMappingInputModel(mapping_input_canonical, mapping_input_description, mapping_input_required, mapping_input_data_type, mapping_input_domain, mapping_input_provider_tag, mapping_input_ms_rules).get_model())

            mapping_services.append(OrchMappingServicesModel(1, request_ms_name, mapping_input).get_model())

        mapping_success_output = []
        mapping_success_canonical = request.form.getlist('mapping_success_canonical')
        mapping_success_description = request.form.getlist('mapping_success_description')
        mapping_success_required = request.form.getlist('mapping_success_required')
        mapping_success_data_type = request.form.getlist('mapping_success_data_type')
        mapping_success_domain = request.form.getlist('mapping_success_domain')
        mapping_success_provider_tag = request.form.getlist('mapping_success_provider_tag')
        mapping_success_ms_rules = request.form.getlist('mapping_success_ms_rules')

        for i in range(len(mapping_success_canonical)):
            success_canonical = mapping_success_canonical[i]
            success_description = mapping_success_description[i]
            success_required = mapping_success_required[i]
            success_data_type = mapping_success_data_type[i]
            success_domain = mapping_success_domain[i]
            success_provider_tag = mapping_success_provider_tag[i]
            success_ms_rules = mapping_success_ms_rules[i]
            mapping_success_output.append(OrchMappingSuccessOutputModel(success_canonical, success_description, success_required, success_data_type, success_domain, success_provider_tag, success_ms_rules).get_model())

        mapping_error_output = []
        mapping_error_canonical = request.form.getlist('mapping_error_canonical')
        mapping_error_description = request.form.getlist('mapping_error_description')
        mapping_error_required = request.form.getlist('mapping_error_required')
        mapping_error_data_type = request.form.getlist('mapping_error_data_type')
        mapping_error_provider_tag = request.form.getlist('mapping_error_provider_tag')
        mapping_error_ms_rules = request.form.getlist('mapping_error_ms_rules')

        for i in range(len(mapping_error_canonical)):
            error_canonical = mapping_error_canonical[i]
            error_description = mapping_error_description[i]
            error_required = mapping_error_required[i]
            error_data_type = mapping_error_data_type[i]
            error_provider_tag = mapping_error_provider_tag[i]
            error_ms_rules = mapping_error_ms_rules[i]
            mapping_error_output.append(OrchMappingErrorOutputModel(error_canonical, error_description, error_required, error_data_type, error_provider_tag, error_ms_rules).get_model())

        return_code_success = []
        success_http_status = request.form.getlist('success_http_status')
        success_message = request.form.getlist('success_message')
        success_provider_condition = request.form.getlist('success_provider_condition')

        for i in range(len(success_http_status)):
            http_status = success_http_status[i]
            message = success_message[i]
            provider_condition = success_provider_condition[i]

            return_code_success.append(OrchReturnCodeSuccessModel(http_status, message, provider_condition).get_model())

        return_code_error = []
        error_http_status = request.form.getlist('error_http_status')
        error_message = request.form.getlist('error_message')
        error_detail = request.form.getlist('error_detail')
        error_provider_condition = request.form.getlist('error_provider_condition')

        for i in range(len(error_http_status)):
            http_status = error_http_status[i]
            message = error_message[i]
            detail = error_detail[i]
            provider_condition = error_provider_condition[i]

            return_code_error.append(OrchReturnCodeErrorModel(http_status, message, detail, provider_condition).get_model())

        apis = []
        for api in request.form.getlist('apis'):
            if api:
                apis.append(ServiceApisModel(2, api).get_model())

        orchestrators = []
        for orchestrator in request.form.getlist('orchestrators'):
            if orchestrator:
                orchestrators.append(ServiceOrchestratorsModel(1, orchestrator).get_model())

        important_notes = request.form['important_notes']

        save_orch_data(orch_id, description, paradigm, mechanism, services, retry_policy, mapping_services, mapping_success_output,
                          mapping_error_output, return_code_success, return_code_error, apis, orchestrators,
                          important_notes)

        update_orch_publish_status(orch_id)

        flash(f'Orquestrador gravado no banco de dados com sucesso!', 'info')

        return True
    except Exception as ex:
        flash('Ocorreu um erro ao gravar os dados do Orquestrador na base. ERRO: {}'.format(ex), 'error')

        return False

def save_orch_data(orch_id, description, paradigm, mechanism, services, retry_policy, mapping_services, mapping_success_output, mapping_error_output, return_code_success, return_code_error, apis, orchestrators, important_notes):
    obj_orch_data = OrchDataModel(orch_id, description, paradigm, mechanism, services, retry_policy, mapping_services, mapping_success_output, mapping_error_output, return_code_success,
                                        return_code_error, apis, orchestrators, important_notes).get_model()

    data_id = None
    original_orch_data = get_orch_data_by_orch_id(orch_id)

    if original_orch_data:
        obj_orch_data['_id'] = original_orch_data['_id']
        data_id = orch_data_update(obj_orch_data)
    else:
        data_id = orch_data_insert(obj_orch_data)

    return data_id


def update_orch_publish_status(orch_id):
    published = None

    try:
        if request.form['chk_published']:
            published = True
        else:
            published = False
    except:
        published = False

    if published is not None:
        obj_orch = get_orch_by_id(orch_id)
        obj_orch['published'] = published
        orch_update(obj_orch)

    return published

@bp.route("/tsonline/orchs")
@login_required
@editor_required
def tsonline_orchs():
    orchs = get_non_published_orchs()
    orchs_count = orchs.count()

    return render_template('tsonline/orchs.html', orchs=orchs, orchs_count=orchs_count)

@bp.route("/tsonline/orch/new", methods=("POST",))
@login_required
@editor_required
def orch_new():
    new_orch_status, orch_id = save_new_orch()

    if orch_id is None:
        return redirect(url_for('tsonline_controller.tsonline_orchs'))

    if new_orch_status:
        return redirect(url_for('tsonline_controller.edit_orch', type="new", id=orch_id))

    flash("Orquestrador e versão já existentes em nossa base, entrando em modo de edição!", 'info')
    return redirect(url_for('tsonline_controller.edit_orch', type="edit", id=orch_id))

@bp.route('/uploads/diagrams/<filename>')
def send_diagram_file(filename):
    folder = diagrams_path()

    return send_from_directory(folder, filename)

@bp.route("/tsonline/orchs/<string:type>/<string:id>")
@login_required
@editor_required
def edit_orch(type, id):
    orch = get_orch_by_id(id)
    orch_data = get_orch_data_by_orch_id(id)
    orch_history = get_orch_history_by_orch_id(id)
    orch_histories = get_all_orch_history_by_orch_name(orch['name'], orch['version'])
    adapter_types = get_all_adapter_type()

    return render_template('tsonline/orchs-edit.html', type=type, orch=orch, orch_data=orch_data, adapter_types=adapter_types, orch_history=orch_history, orch_histories=orch_histories)

@bp.route("/tsonline/orchs/save", methods=('POST',))
@login_required
@editor_required
def tsonline_orch_save():
    orch_id = request.form['orch_id']
    type = request.form['type']

    if orch_data_save(type, orch_id):
        return redirect(url_for('tsonline_controller.tsonline_orchs'))
    else:
        return redirect(url_for('tsonline_controller.edit_orch', type=type, id=orch_id))

### SERVICES ###

def save_new_service():
    try:
        service_name = request.form['service_name']
        service_version = request.form['service_version']

        error = None
        if service_name is None or service_name == "":
            error = "Nome do serviço não está preenchido"
        elif service_version is None or service_version == "":
            error = "Versão do serviço não está preenchida"
        elif not version_validator(service_version):
            error = "Versão está diferente do formato esperado. Exemplo: X.X.X ou 1.0.0"

        if error:
            flash(error, 'error')
            return False, None

        service_in_db = get_service_by_name_and_version(service_name, service_version)

        if service_in_db:
            return False, service_in_db['_id']

        service_obj = ServiceModel(service_name, service_version).get_model()

        return True, service_insert(service_obj)
    except Exception as ex:
        flash(f"Ocorreu um erro ao criar o serviço e a versão. ERRO: {ex}", 'error')
        return False, None


def service_data_save(type, service_id):
    try:
        description = request.form['description']

        txt_provider = request.form['provider']
        provider = ServiceProviderModel(1, txt_provider).get_model()

        txt_adapter = request.form['adapter']
        adapter = ServiceAdapterModel(2, txt_adapter).get_model()

        history_ids = request.form.getlist('history_id')
        history_service_ids = request.form.getlist('history_service_id')
        history_service_names = request.form.getlist('history_service_name')
        history_service_versions = request.form.getlist('history_service_version')
        history_dates = request.form.getlist('history_date')
        history_authors = request.form.getlist('history_author')
        history_projects = request.form.getlist('history_project')
        history_descriptions = request.form.getlist('history_description')

        for i in range(len(history_ids)):
            history_id = history_ids[i]
            history_service_id = history_service_ids[i]

            if history_id == "0" or history_service_id == service_id:

                history_service_name = history_service_names[i]
                history_service_version = history_service_versions[i]
                history_date = history_dates[i]
                history_author = history_authors[i]
                history_project = history_projects[i]
                history_description = history_descriptions[i]

                obj_history = ServiceHistoryModel(history_service_id, history_service_name, history_service_version, history_date, history_author, history_project, history_description).get_model()

                if history_id == "0":
                    service_history_insert(obj_history)
                else:
                    obj_history["_id"] = get_id_key(history_id)
                    service_history_update(obj_history)

        mapping_input = []
        mapping_input_canonical = request.form.getlist('mapping_input_canonical')
        mapping_input_description = request.form.getlist('mapping_input_description')
        mapping_input_required = request.form.getlist('mapping_input_required')
        mapping_input_data_type = request.form.getlist('mapping_input_data_type')
        mapping_input_domain = request.form.getlist('mapping_input_domain')
        mapping_input_provider_tag = request.form.getlist('mapping_input_provider_tag')
        mapping_input_ms_rules = request.form.getlist('mapping_input_ms_rules')

        for i in range(len(mapping_input_canonical)):
            input_canonical = mapping_input_canonical[i]
            input_description = mapping_input_description[i]
            input_required = mapping_input_required[i]
            input_data_type = mapping_input_data_type[i]
            input_domain = mapping_input_domain[i]
            input_provider_tag = mapping_input_provider_tag[i]
            input_ms_rules = mapping_input_ms_rules[i]
            mapping_input.append(ServiceMappingInputModel(input_canonical, input_description, input_required, input_data_type, input_domain, input_provider_tag, input_ms_rules).get_model())

        mapping_success_output = []
        mapping_success_canonical = request.form.getlist('mapping_success_canonical')
        mapping_success_description = request.form.getlist('mapping_success_description')
        mapping_success_required = request.form.getlist('mapping_success_required')
        mapping_success_data_type = request.form.getlist('mapping_success_data_type')
        mapping_success_domain = request.form.getlist('mapping_success_domain')
        mapping_success_provider_tag = request.form.getlist('mapping_success_provider_tag')
        mapping_success_ms_rules = request.form.getlist('mapping_success_ms_rules')

        for i in range(len(mapping_success_canonical)):
            success_canonical = mapping_success_canonical[i]
            success_description = mapping_success_description[i]
            success_required = mapping_success_required[i]
            success_data_type = mapping_success_data_type[i]
            success_domain = mapping_success_domain[i]
            success_provider_tag = mapping_success_provider_tag[i]
            success_ms_rules = mapping_success_ms_rules[i]
            mapping_success_output.append(ServiceMappingSuccessOutputModel(success_canonical, success_description, success_required, success_data_type, success_domain, success_provider_tag, success_ms_rules).get_model())

        mapping_error_output = []
        mapping_error_canonical = request.form.getlist('mapping_error_canonical')
        mapping_error_description = request.form.getlist('mapping_error_description')
        mapping_error_required = request.form.getlist('mapping_error_required')
        mapping_error_data_type = request.form.getlist('mapping_error_data_type')
        mapping_error_provider_tag = request.form.getlist('mapping_error_provider_tag')
        mapping_error_ms_rules = request.form.getlist('mapping_error_ms_rules')

        for i in range(len(mapping_error_canonical)):
            error_canonical = mapping_error_canonical[i]
            error_description = mapping_error_description[i]
            error_required = mapping_error_required[i]
            error_data_type = mapping_error_data_type[i]
            error_provider_tag = mapping_error_provider_tag[i]
            error_ms_rules = mapping_error_ms_rules[i]
            mapping_error_output.append(ServiceMappingErrorOutputModel(error_canonical, error_description, error_required, error_data_type, error_provider_tag, error_ms_rules).get_model())

        return_code_success = []
        success_http_status = request.form.getlist('success_http_status')
        success_message = request.form.getlist('success_message')
        success_provider_condition = request.form.getlist('success_provider_condition')

        for i in range(len(success_http_status)):
            http_status = success_http_status[i]
            message = success_message[i]
            provider_condition = success_provider_condition[i]

            return_code_success.append(ServiceReturnCodeSuccessModel(http_status, message, provider_condition).get_model())

        return_code_error = []
        error_http_status = request.form.getlist('error_http_status')
        error_message = request.form.getlist('error_message')
        error_detail = request.form.getlist('error_detail')
        error_provider_condition = request.form.getlist('error_provider_condition')

        for i in range(len(error_http_status)):
            http_status = error_http_status[i]
            message = error_message[i]
            detail = error_detail[i]
            provider_condition = error_provider_condition[i]

            return_code_error.append(ServiceReturnCodeErrorModel(http_status, message, detail, provider_condition).get_model())

        apis = []
        for api in request.form.getlist('apis'):
            if api:
                apis.append(ServiceApisModel(2, api).get_model())

        orchestrators = []
        for orchestrator in request.form.getlist('orchestrators'):
            if orchestrator:
                orchestrators.append(ServiceOrchestratorsModel(1, orchestrator).get_model())

        request_example = request.form['request_example']
        reply_success = request.form['reply_success']
        reply_error = request.form['reply_error']
        important_notes = request.form['important_notes']

        selected_adapter_type = request.form['selected_adapter_type']

        db_adapter_configuration = None

        if selected_adapter_type == "db":
            db_datasource = request.form['db_datasource']
            db_sql_type = request.form['db_sql_type']
            db_statement = request.form['db_statement']
            db_adapter_configuration = ServiceDbAdapterConfiguration(db_datasource, db_sql_type, db_statement).get_model()

        ws_adapter_configuration = None

        if selected_adapter_type == "ws":
            ws_uri = request.form['ws_uri']
            ws_http_method = request.form['ws_http_method']
            ws_authentication_type = request.form['ws_authentication_type']
            ws_timeout = request.form['ws_timeout']
            ws_encoding = request.form['ws_encoding']
            ws_content_type = request.form['ws_content_type']
            ws_adapter_configuration = ServiceWsAdapterConfiguration(ws_uri, ws_http_method, ws_authentication_type, ws_timeout, ws_encoding, ws_content_type).get_model()

        rmq = None
        rmq_retry_policy = None
        rmq_configuration = None

        is_rmq_queue_service = False

        selected_rmq = request.form['selected_rmq']

        if selected_rmq == "Sim":
            rmq_retry = request.form['rmq_retry']
            rmq_loop = request.form['rmq_loop']
            rmq_interval = request.form['rmq_interval']
            rmq_exchange = request.form['rmq_exchange']
            rmq_principal_queue = request.form['rmq_principal_queue']
            rmq_retry_queue = request.form['rmq_retry_queue']
            rmq_dlx_queue = request.form['rmq_dlx_queue']

            is_rmq_queue_service = True

            rmq_retry_policy = ServiceRmqRetryPolicy(rmq_retry, rmq_loop, rmq_interval).get_model()
            rmq_configuration = ServiceRmqConfiguration(rmq_exchange, rmq_principal_queue, rmq_retry_queue, rmq_dlx_queue).get_model()

        rmq = ServiceRmq(is_rmq_queue_service, rmq_retry_policy, rmq_configuration).get_model()

        save_service_data(service_id, description, provider, adapter, mapping_input, mapping_success_output, mapping_error_output, return_code_success, return_code_error, apis, orchestrators, request_example, reply_success, reply_error, important_notes, db_adapter_configuration, ws_adapter_configuration, rmq)

        update_service_publish_status(service_id, is_rmq_queue_service)

        flash(f'Serviço gravado no banco de dados com sucesso!', 'info')

        return True
    except Exception as ex:
        flash('Ocorreu um erro ao gravar os dados do Serviço na base. ERRO: {}'.format(ex), 'error')

        return False

def save_service_data(service_id, description, provider, adapter, mapping_input, mapping_success_output, mapping_error_output, return_code_success, return_code_error, apis, orchestrators, request_example, reply_success, reply_error, important_notes, db_adapter_configuration, ws_adapter_configuration, rmq):
    obj_service_data = ServiceDataModel(service_id, description, provider, adapter, mapping_input,
                                        mapping_success_output, mapping_error_output, return_code_success,
                                        return_code_error, apis, orchestrators, request_example, reply_success,
                                        reply_error, important_notes, db_adapter_configuration,
                                        ws_adapter_configuration, rmq).get_model()

    data_id = None
    original_service_data = get_service_data_by_service_id(service_id)

    if original_service_data:
        obj_service_data['_id'] = original_service_data['_id']
        data_id = service_data_update(obj_service_data)
    else:
        data_id = service_data_insert(obj_service_data)

    return data_id


def update_service_publish_status(service_id, is_queue):
    published = None

    try:
        if request.form['chk_published']:
            published = True
        else:
            published = False
    except:
        published = False

    if published is not None:
        obj_service = get_service_by_id(service_id)
        obj_service['published'] = published
        obj_service['is_queue'] = is_queue
        service_update(obj_service)

    return published


@bp.route("/tsonline/services")
@login_required
@editor_required
def tsonline_services():
    services = get_non_published_services()
    services_count = services.count()

    return render_template('tsonline/services.html', services=services, services_count=services_count)

@bp.route("/tsonline/service/new", methods=("POST",))
@login_required
@editor_required
def service_new():
    new_service_status, service_id = save_new_service()

    if service_id is None:
        return redirect(url_for('tsonline_controller.tsonline_services'))

    if new_service_status:
        return redirect(url_for('tsonline_controller.edit_service', type="new", id=service_id))

    flash("Serviço e versão já existentes em nossa base, entrando em modo de edição!", 'info')
    return redirect(url_for('tsonline_controller.edit_service', type="edit", id=service_id))

@bp.route("/tsonline/services/<string:type>/<string:id>")
@login_required
@editor_required
def edit_service(type, id):
    service = get_service_by_id(id)
    service_data = get_service_data_by_service_id(id)
    service_history = get_service_history_by_service_id(id)
    service_histories = get_all_service_history_by_service_name(service['name'], service['version'])
    adapter_types = get_all_adapter_type()

    return render_template('tsonline/services-edit.html', type=type, service=service, service_data=service_data, adapter_types=adapter_types, service_history=service_history, service_histories=service_histories)

@bp.route("/tsonline/services/save", methods=('POST',))
@login_required
@editor_required
def tsonline_service_save():
    service_id = request.form['service_id']
    type = request.form['type']

    if service_data_save(type, service_id):
        return redirect(url_for('tsonline_controller.tsonline_services'))
    else:
        return redirect(url_for('tsonline_controller.edit_service', type=type, id=service_id))
