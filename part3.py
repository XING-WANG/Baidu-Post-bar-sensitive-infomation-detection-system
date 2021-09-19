import os
import re

#帖子标题
class Post:
    def __init__(self,postID,postName,barName):
        self.postID = postID
        self.postName = postName
        self.barName = barName
#帖子的发言楼层
class Floor:
    def __init__(self,level,userName,content):
        self.level = level
        self.userName = userName
        self.content = content

#字符块大小
B = 2

shifts = dict()
prefixs = set()

shift_prefixs_map = dict()
prefix_patterns_map = dict()

#模式串
patterns = set()
#最短模式串
min_p = 0


def readpatterns():
    global min_p
    patterns.clear()
    fp = open('./relative_files/Sensitive_words','r', encoding='utf-8')
    while True:
        pattern = fp.readline().strip('\n')
        if not pattern:
            break
        patterns.add(pattern)
    fp.close()
    min_p = min([len(pattern) for pattern in patterns])

#构建shift表，prefix表，pattern表
def preWM():
    #清空映射表，否则多次运行会用之前的映射表
    shifts.clear()
    prefixs.clear()
    shift_prefixs_map.clear()
    prefix_patterns_map.clear()

    for pid in range(len(patterns)):
        pattern = list(patterns)[pid][:min_p]
        #prefix表
        prefix = pattern[:B]
        prefixs.add(prefix)
        #prefix和pattern的对应
        if prefix not in prefix_patterns_map:
            prefix_patterns_map[prefix] = [pid]
        else:
            prefix_patterns_map[prefix].append(pid)
        #shift表
        for cur in range(min_p-1):
            block = pattern[cur:cur+B]
            shift = min_p-1 - (cur+B-1)
            if block in shifts:
                shifts[block] = shift if shift<shifts[block] else shifts[block]
            else:
                shifts[block] = shift
            #shift和prefix的对应
            if shifts[block]==0:
                if block not in shift_prefixs_map:
                    shift_prefixs_map[block] = [prefix]
                else:
                    shift_prefixs_map[block].append(prefix)
#输出shift表，prefix表，pattern表
def out_prelists():
    print("shifts = ", shifts)
    print("shift_prefix_map = ", shift_prefixs_map)
    print("prefixs = ", prefixs)
    print("prefix_patterns_map = ", prefix_patterns_map)
    print("patterns = ", patterns)
#WM算法
def WM(floor,fp,post,post_flag):
    #标识第一次出现匹配词汇
    floor_flag = 0
    #seq中开始匹配的下标
    index = min_p - B

    while index<len(floor.content):

        cur = floor.content[index:index+B]
        if cur not in shifts:
            index += min_p-B+1
        else:
            if shifts[cur]!=0:
                index += shifts[cur]
            else:
                prefix_list = shift_prefixs_map[cur]
                for prefix in prefix_list:
                    if prefix == floor.content[index+B-min_p:index+2*B-min_p]:
                        for pid in prefix_patterns_map[prefix]:
                            pattern = list(patterns)[pid]
                            if floor.content[index+B-min_p:index+B+len(pattern)-min_p] == pattern:
                                if post_flag==0:
                                    post_flag=1
                                    #fp.writelines('\n***********************************************************************************************\n')
                                    fp.writelines('\n*————————————————————————————————————————————————————————————————*\n')
                                    fp.writelines(post.postID+'\t'+post.postName+'\t\t\t'+post.barName+'\n')
                                    

                                if floor_flag==0:
                                    floor_flag = 1
                                    #fp.writelines('第'+floor.level+'楼'+'\t'+floor.userName+'\t') 
                                    fp.writelines('\n** ** **\n')
                                    fp.writelines('第'+floor.level+'楼'+'\t'+floor.userName+'\t'+floor.content+'\n') 

                                fp.writelines('index:'+str(index)+','+pattern+'\t')
                                """
                                    print('*————————————————————————————————————————————————————————————————*')
                                    print('line:'+str(line))
                                print('index:'+str(index)+','+pattern)
                                """
                                break
                index +=1
    if floor_flag==1:
        fp.writelines('\n')
    return post_flag
#标题预处理
def predeal_post(target):
    target = target.strip('\n')
    target = target.replace('【图片】','')
    target = target.replace('】_百度贴吧','')
    ID_Name = target.split(' ',1)
    postID = ID_Name[0]


    post_bar = ID_Name[1].split('【')
    postName = post_bar[0]
    if len(post_bar)>1:
        barName = post_bar[1]
    else:
        barName = '**吧'

    post = Post(postID,postName,barName)
    return post

#楼层预处理
def predeal_floor(target):
    target = target.replace('来自Android客户端','').strip()
    target = target.replace('来自iPhone客户端','').strip()

    level_name_content = target.split(' ',4)
    level = level_name_content[0].replace('楼','')
    userName = level_name_content[3]
    if len(level_name_content)>4:
        content = level_name_content[4]
    else:
        content = ''
    floor = Floor(level,userName,content)

    return floor

#对logs下每一个文件进行多模式匹配
def match():
    fp = open('./relative_files/Results','w',encoding='utf-8')
    #fr = open('./relative_files/test','r', encoding='utf-8')

    for file in os.listdir('logs'):
        post_flag = 0
        if re.match(r'blog-([0-9]*).log', file) is not None:
            # print(file)
            fr = open('./logs/'+file,'r', encoding='utf-8')
        
        #标题信息
        target = fr.readline()
        post = predeal_post(target)
        while True:
            #某一层的信息
            target = fr.readline()
            fr.flush()
            if not target:
                break
            floor = predeal_floor(target)
            #fp.writelines(floor.level+'\t'+floor.userName+'\t'+floor.content)
            #out_prelists()
            post_flag = WM(floor,fp,post,post_flag)

        fr.close()
    fp.close()

#part3主函数
def part3_main():

    readpatterns()

    preWM()

    match()


