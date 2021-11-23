from framework.rdb_data_resource import RDBDataResource

class EventRDBService(RDBDataResource):

    def __init__(self, connect_info):
        super().__init__(connect_info)

    def get_next_id(self):
        sql = "select max(event_id) as event_id from YYDS.events;"
        res = self._run_q(sql, fetch=True)
        res = res[0]["event_id"] + 1
        return res


