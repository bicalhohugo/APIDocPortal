from flask import (
        Blueprint, render_template
)
from markupsafe import Markup

from apidocs.helpers.pagination import Pagination
from apidocs.helpers.utils import get_logged_username, get_datetime_now
from apidocs.modules.access_control.manager import login_required, editor_required
from apidocs.db.mongodb import MongoDb

bp = Blueprint('service_controller', __name__)

db_services = MongoDb('services')
db_services_data = MongoDb('services_data')
db_services_history = MongoDb('services_history')

### METHODS ###

def get_published_services():
    filter = {'published': True, 'is_queue' : False}
    sort = [('name', 1), ('version', 1)]

    return db_services.get_all_by_filter(filter, sort)

def get_published_rmq_services():
    filter = {'published': True, 'is_queue' : True}
    sort = [('name', 1), ('version', 1)]

    return db_services.get_all_by_filter(filter, sort)

def get_non_published_services():
    filter = {'published': False}
    sort = [('name', 1), ('version', 1)]

    return db_services.get_all_by_filter(filter, sort)

def get_published_services_distinct(page_num):
    distinct = 'name'
    filter = {'published': True, 'is_queue' : False}
    sort = {'name': 1}

    db_services.set_page_num(page_num)
    return db_services.get_all_distinct(distinct, filter, sort), db_services.count_total(filter, distinct)

def get_published_rmq_services_distinct(page_num):
    distinct = 'name'
    filter = {'published': True, 'is_queue' : True}
    sort = {'name': 1}

    db_services.set_page_num(page_num)
    return db_services.get_all_distinct(distinct, filter, sort), db_services.count_total(filter, distinct)

def get_service_by_id(id):
    return db_services.get_by_id(id)

def get_published_services_by_name(name, page_num):
    filter = { 'name' : name, 'published' : True, 'is_queue' : False }
    sort = [('name', 1), ('version', 1)]

    db_services.set_page_num(page_num)
    return db_services.get_all_by_filter(filter, sort), db_services.count_total(filter)

def get_published_rmq_services_by_name(name, page_num):
    filter = { 'name' : name, 'published' : True, 'is_queue' : True }
    sort = [('name', 1), ('version', 1)]

    db_services.set_page_num(page_num)
    return db_services.get_all_by_filter(filter, sort), db_services.count_total(filter)

def get_service_by_name_and_version(name, version):
    filter = { 'name' : name, 'version': version }

    return db_services.get_one_by_filter(filter)

def get_published_services_by_keywords(keyword):
    filtered_services = None

    if keyword or keyword.strip():
        filter = { "published" : True, 'is_queue' : False, "$or": [ { 'name' : { '$regex' : keyword, "$options" : "i" } },  { 'description' : { '$regex' : keyword, "$options" : "i" } } ] }
        filtered_services = db_services.get_all_by_filter(filter)

    return filtered_services

def get_published_rmq_services_by_keywords(keyword):
    filtered_services = None

    if keyword or keyword.strip():
        filter = { "published" : True, 'is_queue' : True, "$or": [ { 'name' : { '$regex' : keyword, "$options" : "i" } },  { 'description' : { '$regex' : keyword, "$options" : "i" } } ] }
        filtered_services = db_services.get_all_by_filter(filter)

    return filtered_services

def service_insert(service):
    return db_services.insert(service)

def service_update(updated_service):
    updated_service['last_handler_user'] = get_logged_username()
    updated_service['last_handler_date'] = get_datetime_now()

    return db_services.update(updated_service)

#-- services data --#

def get_service_data_by_id(id):
    return db_services_data.get_by_id(id)

def get_service_data_by_service_id(service_id):
    filter = { 'service_id' : service_id }

    return db_services_data.get_one_by_filter(filter)

def service_data_insert(service_data):
    return db_services_data.insert(service_data)

def service_data_update(updated_service_data):
    return db_services_data.update(updated_service_data)

#-- services history --#

def get_service_history_by_id(id):
    return db_services_history.get_by_id(id)

def get_service_history_by_service_id(service_id):
    filter = { 'service_id' : service_id }

    return db_services_history.get_one_by_filter(filter)

def get_all_service_history_by_service_name(service_name, service_version):
    filter = { 'service_name' : service_name, 'service_version' : { '$lte' : service_version } }
    sort = [('service_version', 1)]

    db_services_history.set_no_pagination(True)
    return db_services_history.get_all_by_filter(filter, sort)

def service_history_insert(service_history):
    return db_services_history.insert(service_history)

def service_history_update(updated_service_history):
    return db_services_history.update(updated_service_history)


### ROUTES ###

@bp.route("/service/list", defaults={'page_num' : 1})
@bp.route("/service/list/<int:page_num>")
@login_required
@editor_required
def service_list(page_num):
    services, total_services = get_published_services_distinct(page_num)
    services_count = len(services)

    pagination = Pagination(total_services, page_num)

    return render_template('service/list.html', rmq=False, pagination=pagination, services=services, services_count=services_count)


@bp.route("/service/<string:service_name>/versions", defaults={'page_num' : 1})
@bp.route("/service/<string:service_name>/versions/<int:page_num>")
@login_required
@editor_required
def service_version_list(service_name, page_num):
    services, total_services = get_published_services_by_name(service_name, page_num)

    pagination = Pagination(total_services, page_num)

    return render_template('service/version.html', pagination=pagination, rmq=False, service_name=service_name, services=services)


@bp.route("/service/detail/<string:id>")
@login_required
@editor_required
def service_detail(id):
    service = get_service_by_id(id)
    service_data = get_service_data_by_service_id(id)
    service_histories = None

    if service:
        service_histories = get_all_service_history_by_service_name(service['name'], service['version'])

    return render_template('service/detail.html', rmq=False, service=service, service_data=service_data, service_histories=service_histories, Markup=Markup)


@bp.route("/queue/list", defaults={'page_num' : 1})
@bp.route("/queue/list/<int:page_num>")
@login_required
@editor_required
def rmq_service_list(page_num):
    services, total_services = get_published_rmq_services_distinct(page_num)
    services_count = len(services)
    pagination = Pagination(total_services, page_num)

    return render_template('service/list.html', pagination=pagination, rmq=True, services=services, services_count=services_count)


@bp.route("/queue/<string:service_name>/versions", defaults={'page_num' : 1})
@bp.route("/queue/<string:service_name>/versions/<int:page_num>")
@login_required
@editor_required
def rmq_service_version_list(service_name, page_num):
    services, total_services = get_published_rmq_services_by_name(service_name, page_num)

    pagination = Pagination(total_services, page_num)

    return render_template('service/version.html', pagination=pagination, rmq=True, service_name=service_name, services=services)


@bp.route("/queue/detail/<string:id>")
@login_required
@editor_required
def rmq_service_detail(id):
    service = get_service_by_id(id)
    service_data = get_service_data_by_service_id(id)
    service_histories = None

    if service:
        service_histories = get_all_service_history_by_service_name(service['name'], service['version'])

    return render_template('service/detail.html', rmq=True, service=service, service_data=service_data, service_histories=service_histories, Markup=Markup)
