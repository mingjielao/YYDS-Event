from framework.base_application_resource import BaseApplicationResource

class EventResource(BaseApplicationResource):

    def __init__(self, config_info):
        super().__init__(config_info)

    def get_links(self, resource_data):
        for r in resource_data:
            event_id = r.get('event_id')

            links = []
            self_link = {"rel": "self", "href": "/api/event/" + str(event_id)}
            links.append(self_link)

            users_link = {"rel": "event_members", "href": "/api/users?event_id=" + str(event_id)}
            links.append(users_link)

            r["links"] = links

        return resource_data

    def create(self, new_resource_info):
        db_svc = self._get_db_resource()
        if 'event_start_time' not in new_resource_info or 'event_end_time' not in new_resource_info or 'event_organizer' not in new_resource_info:
            return -1
        next_id = db_svc.get_next_id()
        new_resource_info["event_id"] = next_id
        res = super().create(new_resource_info)

        return res
