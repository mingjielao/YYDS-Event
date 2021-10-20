from Framework.RDBService import RDBService


class EventRDBService(RDBService):

    def __init__(self, connect_info):
        super().__init__(connect_info)

    def get_next_id(self):
        sql = "select max(id) as id from events;"
        res = self.run_sql(sql, fetch=True)
        res = res[0]["id"] + 1
        return res
