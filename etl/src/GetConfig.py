import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read("conf/recommend.ini")
#sqlserver  info
sqlserverhost=cf.get("Sqlserverdb", "sqlserverhost")
sqlserverport=cf.getint("Sqlserverdb", "sqlserverport")
sqlserveruser=cf.get("Sqlserverdb", "sqlserveruser")
sqlserverpwd=cf.get("Sqlserverdb", "sqlserverpwd")
sqlserverdbname=cf.get("Sqlserverdb", "sqlserverdbname")

# postgresql info
pghost=cf.get("Posrgresqldb", "pghost")
pgport=cf.getint("Posrgresqldb", "pgport")
pguser=cf.get("Posrgresqldb", "pguser")
pgpwd=cf.get("Posrgresqldb", "pgpwd")
pgdbname=cf.get("Posrgresqldb", "pgdbname")


# mysql info
mysqlhost=cf.get("Mysqldb", "mysqlhost")
mysqlport=cf.getint("Mysqldb", "mysqlport")
mysqluser=cf.get("Mysqldb", "mysqluser")
mysqlpwd=cf.get("Mysqldb", "mysqlpwd")
mysqldbname=cf.get("Mysqldb", "mysqldbname")


#apscheduler info
isTimer=cf.getboolean("Timesetting", "isTimer")
minute=cf.get("Timesetting", "minute")
hour=cf.get("Timesetting", "hour")
day=cf.get("Timesetting", "day")


# kafka
hosts=cf.get("kafka", "hosts")
topics=cf.get("kafka", "topics")