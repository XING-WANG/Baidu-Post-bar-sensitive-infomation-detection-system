import pymysql

conn = pymysql.connect(
    host = "localhost",
    user = "root",
    passwd ="xxx",
    database = "ISresult"
    )
cur = conn.cursor()

sql = '''CREATE TABLE IF NOT EXISTS `Conditions`(
    `cid` varchar(10),
    `url` varchar(100),
    `words` varchar(100) NOT NULL,
    `date` date NOT NULL,
    `time` time NOT NULL,
    PRIMARY KEY(`cid`)
)charset=utf8mb4;
'''

cur.execute(sql)

sql = '''CREATE TABLE IF NOT EXISTS `Results`(
    `rid` varchar(10),
    `cid` varchar(10) NOT NULL,
    `postid` varchar(15),
    `level` varchar(5) NOT NULL,
    `username` varchar(20) NOT NULL,
    `content` varchar(100),
    PRIMARY KEY(`rid`),
    FOREIGN KEY(`cid`) REFERENCES `Conditions`(`cid`)
    )charset=utf8mb4;
'''

cur.execute(sql)


"""
#查询并显示所有数据
cur.execute("select * from SaleList")
for item in cur:
    print(item)
#print(cur.fetchall())
"""

conn.commit()

#关闭游标
cur.close()
#关闭数据库
conn.close()

