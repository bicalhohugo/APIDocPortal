from flask import (
        Blueprint
)

from apidocs.helpers.utils import get_logged_username, get_datetime_now

bp = Blueprint('orch_model', __name__)

class OrchModel:
    def __init__(self, name, version, published=False):
        self.name = name
        self.version = version
        self.published = published
        self.last_handler_user = get_logged_username()
        self.last_handler_date = get_datetime_now()

    def get_model(self):
        model = {
                    "name": self.name,
                    "version": self.version,
                    "published" : self.published,
                    "last_handler_user" : self.last_handler_user,
                    "last_handler_date": self.last_handler_date
        }

        return model

class OrchDataModel:
    def __init__(self, orch_id, description, paradigm, mechanism, services, retry_policy, mapping_services, mapping_success_output, mapping_error_output, return_code_success, return_code_error, apis=None, orchestrators=None, important_notes=None):
        self.orch_id = orch_id
        self.description = description
        self.apis = apis
        self.orchestrators = orchestrators
        self.paradigm = paradigm
        self.mechanism = mechanism
        self.services = services
        self.retry_policy = retry_policy
        self.mapping_services = mapping_services
        self.mapping_success_output = mapping_success_output
        self.mapping_error_output = mapping_error_output
        self.important_notes = important_notes
        self.return_code_success = return_code_success
        self.return_code_error = return_code_error

    def get_model(self):
        model = {
                    "orch_id": self.orch_id,
                    "description": self.description,
                    "apis": self.apis, #list de serviceApisModel
                    "orchestrators": self.orchestrators, #list de serviceOrchestratorsModel
                    "paradigm": self.paradigm, #serviceProviderModel
                    "mechanism": self.mechanism, #serviceAdapterModel
                    "services" : self.services, #list de OrchServicesModel
                    "retry_policy" : self.retry_policy,
                    "mapping": {
                        "services": self.mapping_services, #list de serviceMappingInputModel
                        "success_output": self.mapping_success_output, #list de serviceMappingSuccessOutputModel
                        "error_output": self.mapping_error_output #list de serviceMappingErrorOutputModel
                    },
                    "important_notes": self.important_notes,
                    "return_code": {
                        "success": self.return_code_success, #list de serviceReturnCodeSuccessModel
                        "error":  self.return_code_error #list de serviceReturnCodeErrorModel
                    }
                }

        return model

class OrchHistoryModel:
    def __init__(self, orch_id, orch_name, orch_version, date, author, project, description):
        self.orch_id = orch_id
        self.orch_name = orch_name
        self.orch_version = orch_version
        self.date = date
        self.author = author
        self.project = project
        self.description = description

    def get_model(self):
        model = {
                    "orch_id": self.orch_id,
                    "orch_name": self.orch_name,
                    "orch_version" : self.orch_version,
                    "date" : self.date,
                    "author" : self.author,
                    "project" : self.project,
                    "description" : self.description
                }

        return model

class OrchApisModel:
    def __init__(self, id, path):
        self.id = id
        self.path = path

    def get_model(self):
        model = {
                    "id" : self.id,
                    "path" : self.path
                }

        return model

class OrchOrchestratorsModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_model(self):
        model = {
                    "id" : self.id,
                    "name" : self.name
                }

        return model

class OrchParadigmModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_model(self):
        model = {
                    "id" : self.id,
                    "name" : self.name
                }

        return model

class OrchMechanismModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_model(self):
        model = {
                    "id" : self.id,
                    "name" : self.name
                }

        return model

class OrchServicesModel:
    def __init__(self, order, ms, rules, paradigm, retry, provider):
        self.order = order
        self.ms = ms
        self.rules = rules
        self.paradigm = paradigm
        self.retry = retry
        self.provider = provider

    def get_model(self):
        model = {
                    "order": self.order,
                    "ms": self.ms,
                    "rules": self.rules,
                    "paradigm": self.paradigm,
                    "retry": self.retry,
                    "provider": self.provider
                }

        return model

class OrchRetryPolicyModel:
    def __init__(self, ms, retry, interval):
        self.ms = ms
        self.retry = retry
        self.interval = interval

    def get_model(self):
        model = {
                    "ms": self.ms,
                    "retry": self.retry,
                    "interval": self.interval
                }

        return model

class OrchMappingServicesModel:
    def __init__(self, service_id, service_name, mapping_input):
        self.service_id = service_id
        self.service_name = service_name
        self.mapping_input = mapping_input

    def get_model(self):
        model = {
                    "service_id": self.service_id,
                    "service_name": self.service_name,
                    "mapping_input": self.mapping_input
                }

        return model

class OrchMappingInputModel:
    def __init__(self, canonical, description, required, data_type, domain=None, provider_tag=None, ms_rules=None):
        self.canonical = canonical
        self.description = description
        self.required = required
        self.data_type = data_type
        self.domain = domain
        self.provider_tag = provider_tag
        self.ms_rules = ms_rules

    def get_model(self):
        model = {
                    "canonical": self.canonical,
                    "description": self.description,
                    "required": self.required,
                    "data_type": self.data_type,
                    "domain": self.domain,
                    "provider_tag": self.provider_tag,
                    "ms_rules": self.ms_rules
                }

        return model

class OrchMappingSuccessOutputModel:
    def __init__(self, canonical, description, required, data_type, domain=None, provider_tag=None, ms_rules=None):
        self.canonical = canonical
        self.description = description
        self.required = required
        self.data_type = data_type
        self.domain = domain
        self.provider_tag = provider_tag
        self.ms_rules = ms_rules

    def get_model(self):
        model = {
                    "canonical": self.canonical,
                    "description": self.description,
                    "required": self.required,
                    "data_type": self.data_type,
                    "domain": self.domain,
                    "provider_tag": self.provider_tag,
                    "ms_rules": self.ms_rules
                }

        return model

class OrchMappingErrorOutputModel:
    def __init__(self, canonical, description, required, data_type, provider_tag=None, ms_rules=None):
        self.canonical = canonical
        self.description = description
        self.required = required
        self.data_type = data_type
        self.provider_tag = provider_tag
        self.ms_rules = ms_rules

    def get_model(self):
        model = {
                    "canonical": self.canonical,
                    "description": self.description,
                    "required": self.required,
                    "data_type": self.data_type,
                    "provider_tag": self.provider_tag,
                    "ms_rules": self.ms_rules
                }

        return model

class OrchReturnCodeSuccessModel:
    def __init__(self, http_status, message, provider_condition):
        self.http_status = http_status
        self.message = message
        self.provider_condition = provider_condition

    def get_model(self):
        model = {
                    "http_status" : self.http_status,
                    "message" : self.message,
                    "provider_condition" : self.provider_condition
                }

        return model

class OrchReturnCodeErrorModel:
    def __init__(self, http_status, message, detail, provider_condition):
        self.http_status = http_status
        self.message = message
        self.detail = detail
        self.provider_condition = provider_condition

    def get_model(self):
        model = {
                    "http_status" : self.http_status,
                    "message" : self.message,
                    "detail" : self.detail,
                    "provider_condition" : self.provider_condition
                }

        return model
