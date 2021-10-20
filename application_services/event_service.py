from Framework.BaseApplicationResource import BaseApplicationResource
from database_services.event_rdb_service import EventRDBService


class EventResource(BaseApplicationResource):

    def __init__(self, config_info):
        super().__init__(config_info)

    def get_links(self, resource_data):
        pass

    def create(self, new_resource_info):
        next_id = EventRDBService.get_next_id()
        new_resource_info["event_id"] = next_id
        res = super().create(new_resource_info)

        return res
