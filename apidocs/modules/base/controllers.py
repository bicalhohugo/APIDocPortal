from flask import (
        Blueprint, render_template, g
)
from apidocs.modules.api.controllers import get_apis
from apidocs.modules.orch.controllers import get_published_orchs
from apidocs.modules.service.controllers import get_published_services, get_published_rmq_services
from apidocs.modules.access_control.manager import login_required, is_logged_user_an_editor
from apidocs.modules.user.controllers import get_active_users

bp = Blueprint('base_controller', __name__)

@bp.route("/")
@login_required
def index():
    apis, apis_count = get_apis()

    if is_logged_user_an_editor():
        orchsCount = get_published_orchs().count()
        servicesCount = get_published_services().count()
        queues_count = get_published_rmq_services().count()
        users_count = 0
    else:
        orchsCount = 0
        servicesCount = 0
        queues_count = 0
        users, users_count = get_active_users()

    return render_template('base/index.html', apisCount=apis_count, users_count=users_count, orchsCount=orchsCount, servicesCount=servicesCount, queues_count=queues_count)