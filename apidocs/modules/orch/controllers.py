from flask import (
        Blueprint, render_template
)

from apidocs.helpers.pagination import Pagination
from apidocs.helpers.utils import get_logged_username, get_datetime_now
from apidocs.modules.access_control.manager import login_required, editor_required
from apidocs.db.mongodb import MongoDb

bp = Blueprint('orch_controller', __name__)

db_orchs = MongoDb('orchs')
db_orchs_data = MongoDb('orchs_data')
db_orchs_history = MongoDb('orchs_history')

### METHODS ###

def get_published_orchs():
    filter = {'published': True}
    sort = [('name', 1), ('version', 1)]

    return db_orchs.get_all_by_filter(filter, sort)

def get_non_published_orchs():
    filter = {'published': False}
    sort = [('name', 1), ('version', 1)]

    return db_orchs.get_all_by_filter(filter, sort)

def get_published_orchs_distinct(page_num):
    distinct = 'name'
    filter = {'published': True}
    sort = {'name': 1}

    db_orchs.set_page_num(page_num)
    return db_orchs.get_all_distinct(distinct, filter, sort), db_orchs.count_total(filter, distinct)

def get_orch_by_id(id):
    return db_orchs.get_by_id(id)

def get_published_orchs_by_name(name, page_num):
    filter = { 'name' : name, 'published' : True }
    sort = [('name', 1), ('version', 1)]

    db_orchs.set_page_num(page_num)
    return db_orchs.get_all_by_filter(filter, sort), db_orchs.count_total(filter)

def get_orch_by_name_and_version(name, version):
    filter = { 'name' : name, 'version': version }

    return db_orchs.get_one_by_filter(filter)

def get_published_orchs_by_keywords(keyword):
    filtered_orchs = None

    if keyword or keyword.strip():
        filter = { "published" : True, "$or": [ { 'name' : { '$regex' : keyword, "$options" : "i" } },  { 'description' : { '$regex' : keyword, "$options" : "i" } } ] }
        filtered_orchs = db_orchs.get_all_by_filter(filter)

    return filtered_orchs

def orch_insert(orch):
    return db_orchs.insert(orch)

def orch_update(updated_orch):
    updated_orch['last_handler_user'] = get_logged_username()
    updated_orch['last_handler_date'] = get_datetime_now()

    return db_orchs.update(updated_orch)

#-- orchs data --#

def get_orch_data_by_id(id):
    return db_orchs_data.get_by_id(id)

def get_orch_data_by_orch_id(orch_id):
    filter = { 'orch_id' : orch_id }

    return db_orchs_data.get_one_by_filter(filter)

def orch_data_insert(orch_data):
    return db_orchs_data.insert(orch_data)

def orch_data_update(updated_orch_data):
    return db_orchs_data.update(updated_orch_data)

#-- orchs history --#

def get_orch_history_by_id(id):
    return db_orchs_history.get_by_id(id)

def get_orch_history_by_orch_id(orch_id):
    filter = { 'orch_id' : orch_id }

    return db_orchs_history.get_one_by_filter(filter)

def get_all_orch_history_by_orch_name(orch_name, orch_version):
    filter = { 'orch_name' : orch_name, 'orch_version' : { '$lte' : orch_version } }
    sort = [('orch_version', 1)]

    return db_orchs_history.get_all_by_filter(filter, sort)

def orch_history_insert(orch_history):
    return db_orchs_history.insert(orch_history)

def orch_history_update(updated_orch_history):
    return db_orchs_history.update(updated_orch_history)

### ROUTES ###


@bp.route("/orch/list", defaults={'page_num' : 1})
@bp.route("/orch/list/<int:page_num>")
@login_required
@editor_required
def orch_list(page_num):
    orchs, total_orchs = get_published_orchs_distinct(page_num)
    orchs_count = len(orchs)
    pagination = Pagination(total_orchs, page_num)

    return render_template('orch/list.html', pagination=pagination, orchs=orchs, orchs_count=orchs_count)


@bp.route("/orch/<string:orch_name>/versions", defaults={'page_num' : 1})
@bp.route("/orch/<string:orch_name>/versions/<int:page_num>")
@login_required
@editor_required
def orch_version_list(orch_name, page_num):
    orchs, total_orchs = get_published_orchs_by_name(orch_name, page_num)
    pagination = Pagination(total_orchs, page_num)

    return render_template('orch/version.html', pagination=pagination, orch_name=orch_name, orchs=orchs)


@bp.route("/orch/detail/<string:id>")
@login_required
@editor_required
def orch_detail(id):
    orch = get_orch_by_id(id)
    orch_data = get_orch_data_by_orch_id(id)
    orch_histories = None

    if orch:
        orch_histories = get_all_orch_history_by_orch_name(orch['name'], orch['version'])

    return render_template('orch/detail.html', orch=orch, orch_data=orch_data, orch_histories=orch_histories)
