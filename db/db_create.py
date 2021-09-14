import pymysql

conn = pymysql.connect(
    host = "localhost",
    user = "root",
    passwd ="xxx",
    database = "ISresult"
    )
cur = conn.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS ISresult")
#cur.execute("DROP DATABASE ISresult")



conn.commit()

#关闭游标
cur.close()
#关闭数据库
conn.close()


