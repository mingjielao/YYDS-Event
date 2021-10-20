from Framework.BaseApplicationResource import BaseApplicationResource
from database_services import event_rdb_service


class EventResource(BaseApplicationResource):

    def __init__(self, config_info):
        super().__init__(config_info)

    def get_links(self, resource_data):
        pass

    def create(self, new_resource_info):

        next_id = event_rdb_service.get_next_id()
        new_resource_info["id"] = next_id
        res = super().create(new_resource_info)

        return res
