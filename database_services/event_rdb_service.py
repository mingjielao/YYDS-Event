from Framework.RDBService import RDBService


class EventRDBService(RDBService):

    def __init__(self, connect_info):
        super().__init__(connect_info)

    @staticmethod
    def get_next_id():
        sql = "select max(event_id) as event_id from YYDS.events;"
        res = RDBService.run_sql(sql, fetch=True)
        res = res[0]["event_id"] + 1
        return res


