import pymysql
import json
import logging

import middleware.context as context

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class RDBService:
    @classmethod
    def __init__(cls, connect_info):

        cls._db_schema = connect_info["db_schema"]
        cls._table_name = connect_info["table_name"]
        cls._key_column = connect_info["key_column"]

    @staticmethod
    def _get_db_connection():

        db_connect_info = context.get_db_info()

        logger.info("RDBService._get_db_connection:")
        logger.info("\t HOST = " + db_connect_info['host'])

        db_info = context.get_db_info()

        db_connection = pymysql.connect(
            **db_info,
            autocommit=True
        )
        return db_connection

    @staticmethod
    def run_sql(sql_statement, args=None, fetch=False):

        conn = RDBService._get_db_connection()

        try:
            cur = conn.cursor()
            res = cur.execute(sql_statement, args=args)
            if fetch:
                res = cur.fetchall()
        except Exception as e:
            conn.close()
            raise e

        return res

    @classmethod
    def get_by_prefix(cls, column_name, value_prefix):

        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + cls.db_schema + "." + cls.table_name + " where " + \
              column_name + " like " + "'" + value_prefix + "%'"
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def get_by_attribute(cls, column_name, attribute):

        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + cls._db_schema + "." + cls._table_name + " where " + \
              column_name + " = " + attribute

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def delete_by_attribute(cls, column_name, attribute):

        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        sql = "delete from " + cls._db_schema + "." + cls._table_name + " where " + \
              column_name + " = " + attribute

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def put_by_attribute(cls, column_name, attribute, update_data):
        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        for col, content in update_data.items():
            sql = "UPDATE " + cls._db_schema + "." + cls._table_name + " SET " + col + " = '" \
                        + content + "' WHERE " + column_name + " = " + attribute
            print(sql)
            res = cur.execute(sql)
            conn.commit()

        conn.close()

        return res

    @classmethod
    def get_where_clause_args(cls, template):

        terms = []
        args = []
        clause = None

        if template is None or template == {}:
            clause = ""
            args = None
        else:
            for k, v in template.items():
                terms.append(k + "=%s")
                args.append(v)

            clause = " where " + " AND ".join(terms)

        return clause, args

    @classmethod
    def find_by_template(cls, template=None, field_list=None,
                         limit=None, offset=None):

        wc, args = cls.get_where_clause_args(template)
        # proj = self._get_project_terms(field_list)
        sql = "select * from " + cls._db_schema + "." + cls._table_name + " " + wc

        if limit is not None:
            sql += " limit " + str(limit)
        if offset is not None:
            sql += " offset " + str(offset)

        res = RDBService.run_sql(sql, args, fetch=True)

        return res

    @classmethod
    def create(cls, create_data):

        cols = []
        vals = []
        args = []

        for k, v in create_data.items():
            cols.append(k)
            vals.append('%s')
            args.append(v)

        cols_clause = "(" + ",".join(cols) + ")"
        vals_clause = "values (" + ",".join(vals) + ")"

        sql_stmt = "insert into " + cls._db_schema + "." + cls._table_name + " " + cols_clause + \
                   " " + vals_clause

        res = RDBService.run_sql(sql_stmt, args)
        return res
