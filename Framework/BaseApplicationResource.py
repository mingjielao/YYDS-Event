from abc import ABC, abstractmethod


class BaseApplicationException(Exception):

    def __init__(self):
        pass


class BaseApplicationResource(ABC):

    def __init__(self, config_info):
        self._db_resource = config_info.get("db_resource", None)
        self._db_table_name = config_info.get("db_table_name", None)
        self._key_columns = config_info.get("key_column", None)

    def get_by_template(self, template=None, field_list=None, limit=None, offset=None):
        db_resource = self._get_db_resource()

        res = db_resource.find_by_template(
            template=template,
            field_list=field_list,
            limit=limit,
            offset=offset
        )
        return res

    def create(self, new_resource_data):

        db_resource = self._get_db_resource()
        res = db_resource.create(new_resource_data)
        return res

    def get_by_resource_id(self, resource_id):
        db_resource = self._get_db_resource()
        res = db_resource.get_by_attribute("event_id", resource_id)
        res = self.get_links(res)
        return res

    def delete_by_resource_id(self, resource_id):
        db_resource = self._get_db_resource()
        res = db_resource.delete_by_attribute("event_id", resource_id)
        return res

    def put_by_resource_id(self, resource_id, update_data):
        db_resource = self._get_db_resource()
        res = db_resource.put_by_attribute("event_id", resource_id, update_data)
        return res

    def get_data_resource_info(self):
        pass

    @abstractmethod
    def get_links(self, resource_data):
        pass

    def _get_db_resource(self):
        result = self._db_resource
        return result

    def _get_db_table_name(self):
        result = self._db_table_name
        return result

    def _get_key_columns(self):
        result = self._key_columns
        return result
