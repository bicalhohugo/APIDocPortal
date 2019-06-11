from flask import (
        Blueprint, render_template, request
)
from apidocs.modules.access_control.manager import login_required
from apidocs.modules.api.controllers import get_apis_by_keywords
from apidocs.modules.orch.controllers import get_published_orchs_by_keywords
from apidocs.modules.service.controllers import get_published_services_by_keywords, \
    get_published_rmq_services_by_keywords

bp = Blueprint('search_controller', __name__)

### ROUTES ###

@bp.route("/search/list", methods=('GET', 'POST'))
@login_required
def search_list():
    search_word = ''
    
    apis = None
    api_count = 0
    
    orchs = None
    orch_count = 0

    services = None
    service_count = 0

    queues = None
    queue_count = 0

    search_count = 0

    if request.method == 'POST':
        search_word = str(request.form['search_words'])

        apis = get_apis_by_keywords(search_word)
        api_count = 0 if apis == None else apis.count()

        orchs = get_published_orchs_by_keywords(search_word)
        orch_count = 0 if orchs == None else orchs.count()

        services = get_published_services_by_keywords(search_word)
        service_count = 0 if services == None else services.count()

        queues = get_published_rmq_services_by_keywords(search_word)
        queue_count = 0 if queues == None else queues.count()

        search_count = api_count + orch_count + service_count + queue_count

    return render_template('search/list.html', apis=apis, api_count=api_count, orchs=orchs, orch_count=orch_count, services=services, service_count=service_count, queues=queues, queue_count=queue_count, search_word=search_word, search_count=search_count)