import datetime
import socket
from flask import (
        Blueprint
)

bp = Blueprint('audit_log_model', __name__)

class AuditLogModel:
    def __init__(self, user_id, audit_event):
        self.ip = socket.gethostbyname(socket.getfqdn())
        self.event_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.user_id = user_id
        self.audit_event = audit_event

    def get_model(self):
        model = { "ip" : self.ip, "user_id" : self.user_id, "event_date" : self.event_date, "audit_event": self.audit_event }

        return model