# -*- coding: utf-8 -*-
import pymssql
class MSSQL:
    """
    对pymssql的简单封装
    pymssql库，该库到这里下载：http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql
    使用该库时，需要在Sql Server Configuration Manager里面将TCP/IP协议开启
    """

    def __init__(self, host, user, pwd, db, port):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = port

    def __GetConnect(self):
        if not self.db:
            raise(NameError, '没有设置数据库信息')
        self.conn = pymssql.connect(host=self.host, port=self.port, user=self.user, password=self.pwd, database=self.db,
                                    charset='UTF-8')
        cur = self.conn.cursor()
        if not cur:
            raise(NameError, '连接数据库失败')
        else:
            return cur

    # def ExecQuery(self, sql):
    #     cur = self.__GetConnect()
    #     cur.execute(sql)
    #     resList = cur.fetchall()
    #
    #     self.conn.close()
    #     return resList

    def ExecQuery(self, sql,*arg):
        cur = self.__GetConnect()
        cur.execute(sql,*arg)
        resList = cur.fetchall()
        self.conn.close()
        return resList

    # def ExecQueryMany(self, sql,parameters):
    #     cur = self.__GetConnect()
    #     cur.execute(sql, parameters)
    #     resList = cur.fetchall()
    #     self.conn.close()
    #     return resList

    def ExecNoQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()