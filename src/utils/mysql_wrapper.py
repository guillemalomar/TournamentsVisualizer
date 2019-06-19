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
        select_stmt = "SELECT location, sum(players), rules FROM " + self.db_n + "." + self.tb_n + " GROUP BY location, rules"
        try:
            cursor = self.connection.cursor()
            logging.info(MESSAGES['MYSQL_OBT_SUCC'].format('global'))
        except Exception as exc:
            logging.info(MESSAGES['MYSQL_OBT_ERR'].format('global', 'exc'))
            raise exc

        cursor.execute(select_stmt)
        return cursor.fetchall()

    def select_filter_by_time(self, month):

        select_stmt = "SELECT location, players, rules FROM " + self.db_n + "." + self.tb_n + " WHERE MONTH(date) = " + str(month) + ""
        try:
            cursor = self.connection.cursor()
            logging.info(MESSAGES['MYSQL_OBT_SUCC'].format('global'))
        except Exception as exc:
            logging.info(MESSAGES['MYSQL_OBT_ERR'].format('global', 'exc'))
            raise exc

        cursor.execute(select_stmt)
        return cursor.fetchall()

    def close(self):
        self.connection.close()
