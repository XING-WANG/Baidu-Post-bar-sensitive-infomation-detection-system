import pymysql
import datetime

MAX_NUM = 9999999999

#流水序号+1
def SeqNum(snum,MAX_NUM):
    num = int(snum) + 1
    if(num>MAX_NUM):
        return 'OverflowNum'
    rest = len('%d'%MAX_NUM) - len('%d'%num)
    if rest==0:
        return '%d'%num
    rnum = ''
    for i in range(0,rest):
        rnum = rnum + '0'
    return rnum + '%d'%num

#构造插入sql语句的数据描述
def StructSQL(s,data):
    #过滤SQL语句中的数据,转义 SQL 语句中使用的字符串中的特殊字符。
    data = data.replace('\\','')
    data = pymysql.escape_string(data)
    if s=='':
        if isinstance(data,str):
            return s + '\'' + data + '\''
        else:
            return s + str(data)
    else:
        if isinstance(data,str):
            return s + ',' + '\'' + data + '\''
        else:
            return s + ',' + str(data)

def insert_result(url,words):
    conn = pymysql.connect(
        host = "localhost",
        user = "root",
        passwd ="xxx",
        database = "ISresult"
    )
    cur = conn.cursor()
    
    date = str(datetime.date.today())
    time = str(datetime.datetime.now())[11:19]
    
    cur.execute("SELECT MAX(`cid`) FROM `Conditions`")
    oldcid = cur.fetchone()[0]

    if not oldcid:
        cid = '0000000001'
    else:
        cid = SeqNum(oldcid,MAX_NUM)

    data = StructSQL('',cid)
    data = StructSQL(data,url)
    data = StructSQL(data,words)
    data = StructSQL(data,date)
    data = StructSQL(data,time)

    cur.execute('INSERT INTO `Conditions` VALUES (%s)'%data)

    fp = open('./relative_files/Results','r',encoding='utf-8')

    while True:
        seq = fp.readline()
        if not seq:
            break
        if seq[0]=='*' and seq[1]!='*':
            seq = fp.readline()
            postid = seq.split('\t',1)[0]
        elif seq[0]=='*' and seq[1]=='*':
            seq = fp.readline()
            floor = seq.split('\t',2)
            level = floor[0].strip('第').strip('楼')
            username = floor[1]
            content = floor[2].strip('\n')

            cur.execute("SELECT MAX(`rid`) FROM `Results`")
            oldrid = cur.fetchone()[0]

            if not oldrid:
                rid = '0000000001'
            else:
                rid = SeqNum(oldrid,MAX_NUM)

            result = StructSQL('',rid)
            result = StructSQL(result,cid)
            result = StructSQL(result,postid)
            result = StructSQL(result,level)
            result = StructSQL(result,username)
            if len(content)>100:
                result = StructSQL(result,content[:90])
            else:
                result = StructSQL(result,content)
            cur.execute('INSERT INTO `Results` VALUES (%s)'%result)
            conn.commit()
            #print(postid,level,username,content)
        else:
            continue
        
    fp.close()
    conn.commit()

    #关闭游标
    cur.close()
    #关闭数据库
    conn.close()
