from flask import (
        Blueprint, render_template, url_for, send_file, flash, redirect
)
import os
import yaml

from apidocs.helpers.pagination import Pagination
from apidocs.modules.access_control.manager import login_required
from apidocs.db.mongodb import MongoDb
from apidocs.helpers.utils import yml_path
from apidocs.modules.http_methods.controllers import get_http_methods, get_http_method_by_key

bp = Blueprint('api_controller', __name__)
db_apis = MongoDb('apis')

### API METHODS ###

def get_apis(page_num=1):
    sort = [( 'method', 1),( 'path', 1)]

    db_apis.set_page_num(page_num)
    return db_apis.get_all(sort), db_apis.count_total()

def write_api(api):
    result = db_apis.insert(api)
    
    return result

def update_api(api):
    result = db_apis.update(api)
    
    return result

def get_api_by_id(id):
    return db_apis.get_by_id(id)

def get_apis_by_method(method, page_num):
    filter = { 'method' : method }

    db_apis.set_page_num(page_num)
    return db_apis.get_all_by_filter(filter), db_apis.count_total(filter)

def get_apis_by_keywords(keyword):
    filtered_apis = None

    if keyword or keyword.strip():
        filter = { "$or": [ { 'path' : { '$regex' : keyword, "$options" : "i" } },  { 'summary' : { '$regex' : keyword, "$options" : "i" } } ] }        
        filtered_apis = db_apis.get_all_by_filter(filter)

    return filtered_apis    

def get_api_by_path_and_method(api):
    filter = { 'path': api['path'], 'method' : api['method'] }
    return db_apis.get_all_by_filter(filter)

def api_already_exists(api):
    filtered_apis = get_api_by_path_and_method(api)

    if filtered_apis.count() > 0:
        return True
    else:
        return False

def get_static_yaml_file(api_id):
    return url_for('static', filename='yml/{}.yaml'.format(api_id))

def get_yaml_file(api_id):
    file = os.path.join(yml_path(), "{}.yaml".format(api_id))
    
    if os.path.exists(file):
        return file
    else: #TODO: Ainda com erro quando o arquivo YAML não existe mais na pasta, rever bloco abaixo
        try:
            api = get_api_by_id(api_id)
            yamlstream = api["yamlstream"]
            return save_yml_to_directory(api_id, yamlstream)
        except:
            return None

def save_yml_to_directory(api_id, yamlstream):
    try:
        file = os.path.join(yml_path(), "{}.yaml".format(api_id))

        with open(file, 'w') as outfile:
            yaml.safe_dump(yamlstream, outfile, default_flow_style=True)
        
        return outfile
    except:
        return None

def download_yaml_file(api_id):
    file = get_yaml_file(api_id)

    if file: 
        return file
    
    flash("Não foi possível recuperar o YAML dessa API, tente novamente!", "error")
    return None

### CSS METHODS ####

def css_button_class(method):
    method = get_http_method_by_key(method)
    css = ''

    if method:
        css = method['button_class']

    return css

def css_div_class(method):
    method = get_http_method_by_key(method)
    css = ''

    if method:
        css = method['div_class']

    return css

#### VIEW ROUTES ###

@bp.route("/api/list", defaults={'page_num' : 1})
@bp.route("/api/list/<int:page_num>")
@login_required
def api_list(page_num):
    apis, total_apis = get_apis(page_num)
    http_methods = get_http_methods()
    pagination = Pagination(total_apis, page_num)
  
    return render_template('api/list.html', pagination=pagination, apis=apis, method=None, http_methods=http_methods, css_button_class=css_button_class, css_div_class=css_div_class)

@bp.route("/api/list/<string:method>", defaults={'page_num' : 1})
@bp.route("/api/list/<string:method>/<int:page_num>")
@login_required
def api_list_by_method(method, page_num):
    apis, total_apis = get_apis_by_method(method, page_num)
    http_methods = get_http_methods()
    pagination = Pagination(total_apis, page_num)

    return render_template('api/list.html', pagination=pagination, apis=apis, method=method, http_methods=http_methods, css_button_class=css_button_class, css_div_class=css_div_class)

@bp.route("/api/detail/<string:id>")
@login_required
def api_detail(id):
    try:
        api = get_api_by_id(id)
        yaml_file = get_static_yaml_file(api['_id'])
    except:
        api = None
        yaml_file = None
    
    return render_template('api/detail-swagger.html', api=api, yaml_file=yaml_file)

@bp.route("/api/download/<string:id>")
@login_required
def download_api_yaml(id):
    file = download_yaml_file(id)

    if file:
        return send_file(file, as_attachment=True)
    
    return redirect(url_for('api_controller.api_detail', id=id))