from bson import ObjectId
from flask import (
    Blueprint
)

from apidocs.helpers.utils import get_logged_username, get_datetime_now

bp = Blueprint('service_model', __name__)

def get_id_key(id):
    return ObjectId(id)

class ServiceModel:
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

class ServiceDataModel:
    def __init__(self, service_id, description, provider, adapter, mapping_input, mapping_success_output,
                 mapping_error_output, return_code_success, return_code_error, apis=None, orchestrators=None,
                 request=None, reply_success=None, reply_error=None, important_notes=None,
                 db_adapter_configuration=None, ws_adapter_configuration=None, rmq=None):
        self.service_id = service_id
        self.description = description
        self.apis = apis
        self.orchestrators = orchestrators
        self.provider = provider
        self.adapter = adapter
        self.request = request
        self.reply_success = reply_success
        self.reply_error = reply_error
        self.mapping_input = mapping_input
        self.mapping_success_output = mapping_success_output
        self.mapping_error_output = mapping_error_output
        self.important_notes = important_notes
        self.return_code_success = return_code_success
        self.return_code_error = return_code_error
        self.db_adapter_configuration = db_adapter_configuration
        self.ws_adapter_configuration = ws_adapter_configuration
        self.rmq = rmq

    def get_model(self):
        model = {
                    "service_id": self.service_id,
                    "description": self.description,
                    "apis": self.apis, #list de serviceApisModel
                    "orchestrators": self.orchestrators, #list de serviceOrchestratorsModel
                    "provider": self.provider, #serviceProviderModel
                    "adapter": self.adapter, #serviceAdapterModel
                    "provider_example_message": {
                        "request": self.request,
                        "reply_success": self.reply_success,
                        "reply_error": self.reply_error
                    },
                    "mapping": {
                        "input": self.mapping_input, #list de serviceMappingInputModel
                        "success_output": self.mapping_success_output, #list de serviceMappingSuccessOutputModel
                        "error_output": self.mapping_error_output #list de serviceMappingErrorOutputModel
                    },
                    "important_notes": self.important_notes,
                    "return_code": {
                        "success": self.return_code_success, #list de serviceReturnCodeSuccessModel
                        "error":  self.return_code_error #list de serviceReturnCodeErrorModel
                    },
                    "adapter_configuration": {
                        "db": self.db_adapter_configuration, #serviceDbAdapterConfiguration
                        "ws": self.ws_adapter_configuration #serviceWsAdapterConfiguration
                    },
                    "rmq" : self.rmq #ServiceRmq
                }

        return model

class ServiceHistoryModel:
    def __init__(self, service_id, service_name, service_version, date, author, project, description):
        self.service_id = service_id
        self.service_name = service_name
        self.service_version = service_version
        self.date = date
        self.author = author
        self.project = project
        self.description = description

    def get_model(self):
        model = {
                    "service_id": self.service_id,
                    "service_name": self.service_name,
                    "service_version" : self.service_version,
                    "date" : self.date,
                    "author" : self.author,
                    "project" : self.project,
                    "description" : self.description
                }

        return model

class ServiceApisModel:
    def __init__(self, id, path):
        self.id = id
        self.path = path

    def get_model(self):
        model = {
                    "id" : self.id,
                    "path" : self.path
                }

        return model

class ServiceOrchestratorsModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_model(self):
        model = {
                    "id" : self.id,
                    "name" : self.name
                }

        return model

class ServiceProviderModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_model(self):
        model = {
                    "id" : self.id,
                    "name" : self.name
                }

        return model

class ServiceAdapterModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_model(self):
        model = {
                    "id" : self.id,
                    "name" : self.name
                }

        return model

class ServiceMappingInputModel:
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

class ServiceMappingSuccessOutputModel:
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

class ServiceMappingErrorOutputModel:
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

class ServiceReturnCodeSuccessModel:
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

class ServiceReturnCodeErrorModel:
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

class ServiceDbAdapterConfiguration:
    def __init__(self, datasource, sql_type, statement):
        self.datasource = datasource
        self.sql_type = sql_type
        self.statement = statement

    def get_model(self):
        model = {
                    "datasource" : self.datasource,
                    "sql_type" : self.sql_type,
                    "statement" : self.statement
                }

        return model

class ServiceWsAdapterConfiguration:
    def __init__(self, uri, http_method, authentication_type, timeout, encoding, content_type):
        self.uri = uri
        self.http_method = http_method
        self.authentication_type = authentication_type
        self.timeout = timeout
        self.encoding = encoding
        self.content_type = content_type

    def get_model(self):
        model = {
                    "uri" : self.uri,
                    "http_method" : self.http_method,
                    "authentication_type" : self.authentication_type,
                    "timeout" : self.timeout,
                    "encoding" : self.encoding,
                    "content_type" : self.content_type
                }

        return model

class ServiceRmq:
    def __init__(self, is_queue, retry_policy, configuration):
        self.is_queue = is_queue
        self.retry_policy = retry_policy
        self.configuration = configuration

    def get_model(self):
        model = {
                    "is_queue" : self.is_queue,
                    "retry_policy" : self.retry_policy,
                    "configuration" : self.configuration
                }

        return model

class ServiceRmqRetryPolicy:
    def __init__(self, retry, loop, interval):
        self.retry = retry
        self.loop = loop
        self.interval = interval

    def get_model(self):
        model = {
                    "retry" : self.retry,
                    "loop" : self.loop,
                    "interval" : self.interval
                }

        return model

class ServiceRmqConfiguration:
    def __init__(self, exchange, principal_queue, retry_queue, dlx_queue):
        self.exchange = exchange
        self.principal_queue = principal_queue
        self.retry_queue = retry_queue
        self.dlx_queue = dlx_queue

    def get_model(self):
        model = {
                    "exchange" : self.exchange,
                    "principal_queue" : self.principal_queue,
                    "retry_queue" : self.retry_queue,
                    "dlx_queue" : self.dlx_queue
                }

        return model
