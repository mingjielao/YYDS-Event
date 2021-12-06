from framework.base_application_resource import BaseApplicationResource
from address_services.base_address_service import AddressDataTransferObject
from address_services.smarty_address_service import SmartyAddressService

class EventVenueResource(BaseApplicationResource):

    def __init__(self, config_info):
        super().__init__(config_info)

    def get_links(self, resource_data):
        for r in resource_data:
            venue_id = r.get('id')

            links = []
            self_link = {"rel": "self", "href": "/api/eventvenue/" + str(venue_id)}
            links.append(self_link)

            r["links"] = links

        return resource_data

    def create(self, new_resource_info):
        db_svc = self._get_db_resource()
        if "street" not in new_resource_info or "city" not in new_resource_info or "state" not in new_resource_info:
            return -1

        # Validate address
        lookup = AddressDataTransferObject(new_resource_info["street"], new_resource_info["city"], new_resource_info["state"], new_resource_info["postal_code"])

        sm_adaptor = SmartyAddressService()
        sm_adaptor.do_lookup(lookup)

        if len(sm_adaptor.candidates) == 0:
            return -2

        next_id = db_svc.get_next_id()
        new_resource_info["id"] = next_id
        res = super().create(new_resource_info)

        if res == 1:
            res = {}
            res["location"] = "/api/eventvenue/" + str(next_id)

        return res
