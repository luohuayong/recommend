# -*- coding: utf-8 -*-
import psycopg2
class PostgreSqlUtil:
    def __init__(self, host, user, pwd, db, port):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = port

    def __GetConnect(self):
        if not self.db:
            raise(NameError, '没有设置数据库信息')
        self.conn = psycopg2.connect(database=self.db, user=self.user,password=self.pwd,host=self.host, port=self.port)
        cur = self.conn.cursor()
        if not cur:
            raise(NameError, '连接数据库失败')
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        self.conn.close()
        return resList

    def ExecNoQuery(self, sql,parameters):
        cur = self.__GetConnect()
        cur.execute(sql, parameters)
        self.conn.commit()
        self.conn.close()