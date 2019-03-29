import logging

import mysql.connector
from src.settings import MESSAGES
from src.settings.creds import MYSQL


class MysqlWrapper(object):
    def __init__(self):
        self.host = MYSQL['HOST']
        self.user = MYSQL['USER']
        self.pswd = MYSQL['PSWD']
        self.db_n = MYSQL['DB_N']
        self.tb_n = MYSQL['TB_N']

        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.host,
                                                      user=self.user,
                                                      password=self.pswd,
                                                      database=self.db_n,
                                                      auth_plugin='mysql_native_password')
            logging.info(MESSAGES['MYSQL_CONN_SUCC'])
        except Exception as exc:
            logging.ERROR(MESSAGES['MYSQL_CONN_ERR'].format(exc))
            raise exc

    def select_all(self):
        select_stmt = "SELECT location, sum(total) FROM " + self.db_n + "." + self.tb_n + " GROUP BY location"
        try:
            cursor = self.connection.cursor()
            logging.info(MESSAGES['MYSQL_OBT_SUCC'].format('global'))
        except Exception as exc:
            logging.info(MESSAGES['MYSQL_OBT_ERR'].format('global', 'exc'))
            raise exc

        cursor.execute(select_stmt)
        return cursor.fetchall()

    def select_by_kw(self, kw):
        select_stmt = "SELECT location, sum(total) FROM " + self.db_n + "." + self.tb_n + " WHERE keyword = \'" + kw + "\' GROUP BY location"

        try:
            cursor = self.connection.cursor()
            logging.info(MESSAGES['MYSQL_OBT_SUCC'].format('keyword'))
        except Exception as exc:
            logging.info(MESSAGES['MYSQL_OBT_ERR'].format('keyword', exc))
            raise exc

        cursor.execute(select_stmt)
        return cursor.fetchall()

    def select_by_parser(self, parser_id):
        select_stmt = "SELECT location, sum(total) FROM " + self.db_n + "." + self.tb_n + " WHERE parserID = " + str(parser_id) + " GROUP BY location"

        try:
            cursor = self.connection.cursor()
            logging.info(MESSAGES['MYSQL_OBT_SUCC'].format('parser'))
        except Exception as exc:
            logging.info(MESSAGES['MYSQL_OBT_ERR'].format('parser', exc))
            raise exc

        cursor.execute(select_stmt)
        return cursor.fetchall()

    def select_and_kw_by_parser(self, kw, parser_id):
        select_stmt = "SELECT location, sum(total) FROM " + self.db_n + "." + self.tb_n + " WHERE parserID = " + str(parser_id) + " AND keyword = \'" + kw + "\' GROUP BY location"

        try:
            cursor = self.connection.cursor()
            logging.info(MESSAGES['MYSQL_OBT_SUCC'].format('parser'))
        except Exception as exc:
            logging.info(MESSAGES['MYSQL_OBT_ERR'].format('parser', exc))
            raise exc

        cursor.execute(select_stmt)
        return cursor.fetchall()

    def update(self, info):

        operation = "BEGIN; " + \
                    "SELECT total FROM " + self.db_n + "." + self.tb_n + " WHERE parserID = " + str(info[0]) + " AND location = \'" + info[1] + "\' AND keyword = \'" + info[2] + "\' FOR UPDATE;" + \
                    "UPDATE " + self.db_n + "." + self.tb_n + " SET total = total+1 WHERE parserID = " + str(info[0]) + " AND location = \'" + info[1] + "\' AND keyword = \'" + info[2] + "\';" + \
                    "COMMIT;"

        cursor = self.connection.cursor()

        insert_one = False
        for result in cursor.execute(operation, multi=True):
            if result.with_rows:
                rows_affected = result.fetchall()
                if not rows_affected:
                    insert_one = True

        if insert_one:
            self.insert(info)

    def insert(self, info):
        operation = "INSERT INTO " + self.db_n + "." + self.tb_n + " (parserID, location, keyword, total) " \
                    "VALUES (" + str(info[0]) + ", \'" + info[1] + "\', \'" + info[2] + "\', 1);"

        cursor = self.connection.cursor()
        cursor.execute(operation)
        self.connection.commit()

    def close(self):
        self.connection.close()
