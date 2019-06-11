from flask import (
        Blueprint, session, render_template
)
from apidocs.modules.audit_log.models import AuditLogModel
from apidocs.db.mongodb import MongoDb

bp = Blueprint('audit_log_controller', __name__)
db_logs = MongoDb('audit_logs')
db_events = MongoDb('audit_events')

### METHODS ###

def audit_log(event_type):
    user_id = session.get('user_id')
    audit_event = get_audit_event(event_type)

    log = AuditLogModel(user_id, audit_event).get_model()

    db_logs.insert(log)

def get_audit_log(user_id):
    filter = { "user_id" : user_id}
    logs = db_logs.get_all_by_filter(filter).sort("event_date", -1)

    return logs

def get_audit_event(event_type):
    filter = { "type" : event_type }
    events = db_events.get_one_by_filter(filter)
    
    return events

### ROUTES ###

@bp.route("/audit/logs")
def user_audit_logs():
    user_id = session.get('user_id')
    logs = get_audit_log(user_id)

    return render_template('audit_log/details.html', logs=logs)