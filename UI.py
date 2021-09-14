from tkinter import *
from part2 import *
from part3 import *
from part4 import *
import sys
sys.path.append(sys.path[0]+'\\db')  #加入路径
from db_insert import *

#匹配结果输出模块
def getResults(fw):
    fp = open('./relative_files/Results','r', encoding='utf-8')
    txt_result.delete(1.0,END)
    while True:
        result = fp.readline()
        if not result:
            break
        fw.writelines(result)
        txt_result.insert(END,result)
    fw.flush()
    fp.close()
#将敏感词汇存入文件中
def inWords(fw):
    seq = entry_words.get()
    words = seq.split(';;')
    fp = open('./relative_files/Sensitive_words','w',encoding='utf-8')
    fw.writelines('敏感词汇：')
    for index in range(len(words)):
        fp.writelines(words[index]+'\n')
        fw.writelines(words[index]+'\t')
    fw.writelines('\n')
    fw.flush()
    fp.close()

#匹配模块
def analyze():
    fw = open('./relative_files/log','a',encoding='utf-8')
    fw.writelines('*************************************************************\n')
    fw.writelines('网址：'+entry_url.get()+'\n')
    inWords(fw)
    part2_main(entry_url.get())

    part3_main()
    getResults(fw)
    insert_result(entry_url.get(),entry_words.get())

    fw.writelines('\n\n')
    fw.close()

#举报模块
def information_manage():
    root_manage = Tk()
    root_manage.title("信息控管")

    root_manage.geometry('840x480')

    lb_postID = Label(root_manage,text='帖子ID：')
    lb_postID.place(relx=0.005, rely=0.08, relwidth=0.1, relheight=0.05)

    entry_postID = Entry(root_manage)
    entry_postID.place(relx=0.1, rely=0.07, relwidth=0.6, relheight=0.07)

    lb_level = Label(root_manage,text='xx楼：')
    lb_level.place(relx=0.005, rely=0.18, relwidth=0.1, relheight=0.05)

    entry_level = Entry(root_manage)
    entry_level.place(relx=0.1, rely=0.17, relwidth=0.6, relheight=0.07)

    lb_level = Label(root_manage,text='举报原因：')
    lb_level.place(relx=0.005, rely=0.3, relwidth=0.1, relheight=0.05)

    var = StringVar(root_manage)

    rd_01 = Radiobutton(root_manage,text="色情低俗",variable=var,value='10001')
    rd_01.place(relx=0.1, rely=0.29, relwidth=0.2, relheight=0.07)

    rd_02 = Radiobutton(root_manage,text="垃圾广告",variable=var,value='10002')
    rd_02.place(relx=0.4, rely=0.29, relwidth=0.2, relheight=0.07)

    rd_04 = Radiobutton(root_manage,text="辱骂攻击",variable=var,value='10004')
    rd_04.place(relx=0.7, rely=0.29, relwidth=0.2, relheight=0.07)

    rd_05 = Radiobutton(root_manage,text="违法内容",variable=var,value='10005')
    rd_05.place(relx=0.1, rely=0.37, relwidth=0.2, relheight=0.07)

    rd_09 = Radiobutton(root_manage,text="涉及未成年人不良信息",variable=var,value='10009')
    rd_09.place(relx=0.4, rely=0.37, relwidth=0.2, relheight=0.07)

    rd_10 = Radiobutton(root_manage,text="时政信息不实",variable=var,value='10010')
    rd_10.place(relx=0.7, rely=0.37, relwidth=0.2, relheight=0.07)

    rd_11 = Radiobutton(root_manage,text="其他违规信息",variable=var,value='10011')
    rd_11.place(relx=0.1, rely=0.45, relwidth=0.2, relheight=0.07)

    lb_reason = Label(root_manage,text='具体原因：')
    lb_reason.place(relx=0.005, rely=0.55, relwidth=0.1, relheight=0.05)

    entry_reason = Entry(root_manage)
    entry_reason.place(relx=0.1, rely=0.54, relwidth=0.6, relheight=0.3)

    btn_start= Button(root_manage,text='一键举报',command=lambda: part4_main(entry_postID.get(), entry_level.get(), var.get(), entry_reason.get()))
    btn_start.place(relx=0.8, rely=0.77, relwidth=0.15, relheight=0.07)


root = Tk()
root.title('信息管理系统')

root.geometry('960x560')

lb_url = Label(root,text='网址')
lb_url.place(relx=0.005, rely=0.08, relwidth=0.1, relheight=0.05)

entry_url = Entry(root)
entry_url.place(relx=0.1, rely=0.07, relwidth=0.6, relheight=0.07)

lb_words = Label(root,text='敏感词')
lb_words.place(relx=0.005, rely=0.2, relwidth=0.1, relheight=0.05)

entry_words = Entry(root)
entry_words.place(relx=0.1, rely=0.19, relwidth=0.6, relheight=0.07)


btn_match= Button(root,text='搜索',command=lambda: analyze())
btn_match.place(relx=0.75, rely=0.19, relwidth=0.15, relheight=0.07)

txt_result = Text(root)
txt_result.place(relx=0.05, rely=0.3, relwidth=0.7, relheight=0.65)

btn_manage= Button(root,text='信息控管',command=lambda: information_manage())
btn_manage.place(relx=0.8, rely=0.77, relwidth=0.15, relheight=0.07)

root.mainloop()
