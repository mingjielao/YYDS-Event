from abc import ABC, abstractmethod
from Framework.RDBService import RDBService


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
        db_table_name = self._get_db_table_name()

        res = db_resource.find_by_template(
            db_schema=db_resource._db_schema,
            table_name=db_table_name,
            template=template,
            field_list=field_list,
            limit=limit,
            offset=offset
        )
        return res

    def create(self, new_resource_data):

        db_resource = self._get_db_resource()
        db_table_name = self._get_db_table_name()
        res = db_resource.create(db_resource._db_schema, db_table_name, new_resource_data)
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
