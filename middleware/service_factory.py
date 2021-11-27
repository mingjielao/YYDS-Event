import middleware.context as context

from application_services.EventsResource.event_application_service import EventResource
from database_services.event_rdb_service import EventRDBService


class ServiceFactory:

    def __init__(self):
        self.db_connect_info = context.get_db_info()
        r_svc = EventRDBService(self.db_connect_info)

        self.services = {}

        event_svc_config_info = {
            "db_resource": r_svc,
            "db_table_name": "events",
            "key_columns": ["event_id"]
        }
        event_svc = EventResource(event_svc_config_info)

        self.services["events"] = event_svc

    def get_service(self, service_name):
        result = self.services.get(service_name, None)
        return result
