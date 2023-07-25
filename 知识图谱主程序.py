from py2neo import *
import numpy as np
import matplotlib.pyplot as plt
from tkinter import scrolledtext
from tkinter import ttk
import ttkbootstrap as ttkb
from tkinter import END
import random
import tkinter
from PIL import Image,ImageTk
from PIL import ImageSequence
from ttkbootstrap.constants import *
import os,sys # 系统模块
import sqlite3
import json
import requests
#357884102


graph = Graph('http://localhost:7474/',auth=("neo4j", "20020531"))
nodes = NodeMatcher(graph)
Sql = nodes.match("Person").all()
for up in Sql:
    up['fans']=int(up['fans'])
n=len(graph.nodes)

STR_FRAME_FILENAME = "frame{}.png"  # 每帧图片的文件名格式


class playGif():
    def __init__(self, file, temporary=""):  # temporary 指临时目录路径，为空时则随机生成
        self.__strPath = file
        self.__index = 1  # 当前显示图片的帧数

        if len(temporary) == 0:
            self.strTemporaryFolder = self.crearteTemporaryFolder()  # 随机得到临时目录
        else:
            self.strTemporaryFolder = temporary  # 指定的临时目录

        self.__intCount = 0  # gif 文件的帧数

        self.decomposePics()  # 开始分解

        #

    def crearteTemporaryFolder(self):  # 生成临时目录名返回
        # 获取当前调用模块主程序的运行目录
        strSelfPath = str(os.path.dirname(os.path.realpath(sys.argv[0])))
        if len(strSelfPath) == 0:
            strSelfPath = os.path.join(os.getcwd())

        def createRandomFolder(strSelfPath):  # 内嵌方法，生成随机目录用
            length = random.randint(5, 10)  # 随机长度
            path = ""
            for i in range(length):
                path = path + chr(random.randint(97, 122))  # 随机生成a-z字母

            return os.path.join(strSelfPath, path)
            #

        # 获取当前软件目录

        folder = createRandomFolder(strSelfPath)
        while os.path.isdir(folder):  # 已存在
            folder = createRandomFolder(strSelfPath)

        return folder
        #

    def decomposePics(self):  # 分解 gif 文件的每一帧到独立的图片文件，存在临时目录中
        i = 0
        img = Image.open(self.__strPath)
        self.__width, self.__height = img.size  # 得到图片的尺寸

        os.mkdir(self.strTemporaryFolder)  # 创建临时目录
        for frame in ImageSequence.Iterator(img):  # 遍历每帧图片
            frame.save(os.path.join(self.strTemporaryFolder, STR_FRAME_FILENAME.format(i + 1)))  # 保存独立图片
            i += 1

        self.__intCount = i  # 得到 gif 的帧数
        #

    def getPicture(self, frame=0):  # 返回第 frame 帧的图片(width=0,height=0)
        if frame == 0:
            frame = self.__index
        elif frame >= self.__intCount:
            frame = self.__intCount  # 最后一张

        img = tkinter.PhotoImage(file=os.path.join(self.strTemporaryFolder, STR_FRAME_FILENAME.format(frame)))
        self.__index = self.getNextFrameIndex()

        return img  # 返回图片

        #

    def getNextFrameIndex(self, frame=0):  # 返回下一张的帧数序号
        if frame == 0:
            frame = self.__index  # 按当前插入帧数

        if frame == self.__intCount:
            return 1  # 返回第1张，即从新开始播放
        else:
            return frame + 1  # 下一张
        #

    def playGif(self, tk, widget, time=100):  # 开始调用自身实现播放，time 单位为毫秒
        img = self.getPicture()
        widget.config(image=img)
        widget.image = img
        tk.after(time, self.playGif, tk, widget, time)  # 在 time 时间后调用自身

        #

    def close(self):  # 关闭动画文件，删除临时文件及目录
        files = os.listdir(self.strTemporaryFolder)
        for file in files:
            os.remove(os.path.join(self.strTemporaryFolder, file))

        os.rmdir(self.strTemporaryFolder)


def INIT_PLT():
    '''
    用于plt初始化
    让plt可以正常显示中文
    '''
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['figure.figsize'] = (10.0, 8.0)  # set default size of plots
    plt.rcParams['image.interpolation'] = 'nearest'
    plt.rcParams['image.cmap'] = 'gray'


def Find_Percent(str):
    m=0
    for i in range(0,n):
        node = graph.nodes.get(i)
        if node!=None:
            if dict(node)['name'] == str:
                m=m+1
        else:
            continue
    p=round(m/n*100,2)
    print(str,"的占比为：",p,"%")
    '''print(dict(node))
    print(node.labels)
    print(dict(node)['name'])'''
#a=set(a) 列表自动去重


def Pie_Chart(str):
    '''
    :param str:给定的某一个属性值，如观看的视频类型
    :return:绘制一个饼图，各种类型的视频占比
    '''
    a={}
    for up in Sql:
        if up['tag'] not in a:
            a[up['tag']]=1
        else:
            a[up['tag']]=a[up['tag']]+1
    Keylist=[]
    Valuelist=[]
    for key in a:
        Keylist.append(key)
        Valuelist.append(a[key])
    tit="关于B站各类UP主分区的占比情况"
    plt.title(tit)
    plt.pie(Valuelist, labels=Keylist, autopct='%1.1f%%')  # 绘制饼图
    plt.show()
import requests
import math
import json
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 QIHU 360SE/13.1.5600.0'}

def TiHuan(key):
    if key=='电子竞技':
        return '臭打游戏的'
    elif key=='动画':
        return '纯纯的二刺螈'
    elif key=='暂无tag':
        return '成分太杂'
    else:
        return key


def Tk_DingZhen(key):
    Ding = tkinter.Toplevel()
    Ding.title('一眼丁真')
    Ding.geometry('422x519')
    im = Image.open("E:\\study\\知识图谱\\丁真.jpg")
    img = ImageTk.PhotoImage(im)
    imLabel = tkinter.Label(Ding, image=img).place(x=0, y=0, width=422, height=519)
    TXT='一眼丁真，鉴定为'+TiHuan(key)
    L1 = tkinter.Text(Ding)
    L1.insert('end', TXT)
    L1.place(x=100,y=450)
    Ding.mainloop()


def Tk_Guanren(key):
    Ding = tkinter.Toplevel()
    Ding.title('让嘉然小姐来分析你的成分吧')
    Ding.geometry('600x933')
    im = Image.open("E:\\study\\知识图谱\\嘉然.jpg")
    img = ImageTk.PhotoImage(im)
    imLabel = tkinter.Label(Ding, image=img).place(x=0, y=0, width=600, height=933)
    L1 = tkinter.Text(Ding)
    L2 = tkinter.Text(Ding)
    L1.insert('end', TiHuan(key))
    L1.place(x=180, y=720, width=120, height=30)
    L2.insert('end', TiHuan(key))
    L2.place(x=210, y=880, width=120, height=30)
    Ding.mainloop()


def insertUser(infos):
    conn = sqlite3.connect('../My_Python/BiliFollowDB.db')
    link = conn.cursor()

    InsertCmd = "insert into user (UID,NAME,vipType,verifyType,sign,verifyDesc) values (?,?,?,?,?,?);"

    ExistCmd = "select count(UID) from user where UID='%d';"  # % UID

    newID = []

    for info in infos:
        answer = link.execute(ExistCmd % info['uid'])
        for row in answer:
            exist_ID = row[0]

        if exist_ID == 0:
            newID.append(info['uid'])
            link.execute(InsertCmd, (
            info['uid'], info['name'], info['vipType'], info['verifyType'], info['sign'], info['verifyDesc']))

    conn.commit()
    conn.close()

    return newID


def insertFollowing(uid: int, subscribe):
    conn = sqlite3.connect('../My_Python/BiliFollowDB.db')
    link = conn.cursor()

    InsertCmd = "insert into relation (follower,following,followTime) values (?,?,?);"

    for follow in subscribe:
        try:
            link.execute(InsertCmd, (uid, follow[0], follow[1]))
        except:
            None
    conn.commit()
    conn.close()


def getFollowingList(uid: int):
    url = "https://api.bilibili.com/x/relation/followings?vmid=%d&pn=%d&ps=50&order=desc&order_type=attention&jsonp=jsonp"  # % (UID, Page Number)
    subscribe = []
    newID = []
    for i in range(1, 6):
        html = requests.get(url % (uid, i))
        if html.status_code != 200:
            print("GET ERROR!")

        text = html.text
        dic = json.loads(text)

        if dic['code'] == -400:
            break

        list = dic['data']['list']

        for usr in list:
            info = {}
            info['uid'] = usr['mid']
            info['name'] = usr['uname']
            info['vipType'] = usr['vip']['vipType']
            info['verifyType'] = usr['official_verify']['type']
            info['sign'] = usr['sign']
            if info['verifyType'] == -1:
                info['verifyDesc'] = 'NULL'
            else:
                info['verifyDesc'] = usr['official_verify']['desc']

            subscribe.append((usr['mid'], usr['mtime']))
            newID.append(int(info['uid']))
    return newID


def tk_Tuijian():
    window = tkinter.Toplevel()
    window.title('查询用户')
    window.geometry('800x400')
    def box():
        label1 = t_get_label.get('0.0', 'end').strip()
        uid = label1.strip()
        Uid_list=getFollowingList(int(uid))
        #用户关注列表的所有up主的uid
        flag_list = []
        scr.delete('0.0','end')
        for uid in Uid_list:
            for up in Sql:
                if int(up['uid'])==uid:
                    #找到关注列表和数据库重复的up主，提取标签
                    if up['tag'] not in flag_list:
                        flag_list.append(up['tag'])
                        scr.insert('end', "发现您喜欢up主：")
                        scr.insert('end',up['name'])
                        scr.insert('end','\n')
                        scr.insert('end', '为你推荐：')
                        scr.insert('end', '\n')
                        loop = 0
                        for up_2 in Sql:
                            #查找到相同标签的up主，做出推荐
                            if up_2['tag']==up['tag']:
                                loop=loop+1
                                if loop>=10:
                                    break
                                else:
                                    if up_2['name']!=up['name']:
                                        scr.insert('end', up_2['name'])
                                        scr.insert('end', '\t')
                        scr.insert('end', '\n')
        dict={}
        for Sampleuid in Uid_list:
            for up in Sql:
                if int(up['uid']) == int(Sampleuid):
                    if up['tag'] in dict:
                        dict[up['tag']] = dict[up['tag']] + 1
                    else:
                        dict[up['tag']] = 1
        DingZhen=''
        dict['暂无tag'] =0
        import random
        for key in dict:
            if (dict[key] == max(dict.values())):
                DingZhen=key
                break
        if random.randint(0,3)==1:
            Tk_Guanren(DingZhen)
        else:
            Tk_DingZhen(DingZhen)
    def box_Huaxiang():
        label1 = t_get_label.get('0.0', 'end')
        uid = label1.strip()
        Uid_list=getFollowingList(int(uid))
        #用户关注列表的所有up主的uid
        dict={}
        for Sampleuid in Uid_list:
            for up in Sql:
                if int(up['uid'])==int(Sampleuid):
                    if up['tag'] in dict:
                        dict[up['tag']]=dict[up['tag']]+1
                    else:
                        dict[up['tag']]=1
        temp=''
        #============================================================
        MaxKey = []
        dict['暂无tag'] = 0
        DingZhen=''
        for key, value in dict.items():
            if (value == max(dict.values())):
                DingZhen=key
                break
        MaxCount=0
        for i in range(3):
            for key in dict:
                if (dict[key] == max(dict.values())):
                    if value!=0:
                        MaxKey.append(key)
                        dict[key] = 0
                    else:
                        break
        scr.delete("1.0", "end")
        if MaxKey==[]:
            scr.insert('end', '对不起，无法建立您的用户画像')
        else:
            for i in range(len(MaxKey)):
                if i>=3:
                    break
                Rank = ['一', '二', '三']
                Istr = "发现您第" + Rank[i] + "喜欢的类型为："
                scr.insert('end', Istr)
                scr.insert('end', MaxKey[i])
                scr.insert('end', '\n')
                scr.insert('end', '为你推荐：')
                scr.insert('end', '\n')
                loop = 0
                dict[MaxKey[i]] = 0
                for up_2 in Sql:
                    # 查找到相同标签的up主，做出推荐
                    if up_2['tag'] == MaxKey[i]:
                        loop = loop + 1
                        if loop >= 10:
                            break
                        else:
                            scr.insert('end', up_2['name'])
                            scr.insert('end', '\t')
                            # 待会可以加入查重功能，去掉已经关注的up主
                scr.insert('end', '\n')
        #选取tag出现最多的前三个
        import random
        if random.randint(0,3)==1:
            Tk_Guanren(DingZhen)
        else:
            Tk_DingZhen(DingZhen)
    MyX = 10
    MyY = 10
    tishi = tkinter.Label(window, text="请输入UId：")
    tishi.place(x=50, y=10)
    # relx距离左边框的距离, rely距离上边框的距离
    t_get_label = tkinter.Text(window,
                               state='normal',  # 有disabled、normal 两个状态值，默认为normal
                               width=15, height=2
                               )
    t_get_label.place(x=150, y=10)
    label1 = '序号' + '\t' + '姓名' + '\t' + '\t' + '粉丝数' + '\t' + 'uid' + '\t' + 'tag'
    monty = ttk.LabelFrame(window, text=label1)  # 创建一个容器，其父容器为win
    monty.place(x=MyX + 20, y=MyY + 140)
    scr = scrolledtext.ScrolledText(monty, width=80, height=10, wrap=tkinter.WORD)
    scr.pack()
    b1 = tkinter.Button(window, text="根据用户画像推荐", command=box_Huaxiang)
    b1.place(x=MyX + 200, y=MyY + 80)
    b1 = tkinter.Button(window, text="根据关注推荐", command=box)
    b1.place(x=MyX + 400, y=MyY + 80)


def tk_XuanQU():
    window = tkinter.Toplevel()
    window.title('查询用户')
    window.geometry('800x400')

    def choose_1(event):
        # 选中事件
        love[0] = combobox1.get()
    def choose_2(event):
        # 选中事件
        love[1] = combobox2.get()
    def choose_3(event):
        # 选中事件
        love[2] = combobox3.get()
    def box_Huaxiang():
        for i in range(3):
            Hanzi=['一','二','三']
            start='你第'+Hanzi[i]+'喜欢的是：'
            scr.insert('end',start)
            scr.insert('end',love[i])
            scr.insert('end','\n')
            scr.insert('end', '为你推荐\n')
            loop=0
            for up in Sql:
                if up['tag']==love[i]:
                    loop=loop+1
                    if loop<10:
                        scr.insert('end', up['name'])
                        scr.insert('end', '\t')
                    else:
                        break
            scr.insert('end', '\n')

    MyX = 10
    MyY = 10
    love=['尚未选择','尚未选择','尚未选择']
    tishi = tkinter.Label(window, text="请选择标签：")
    tishi.place(x=50, y=10)
    # relx距离左边框的距离, rely距离上边框的距离
    value1 = tkinter.StringVar()
    value1.set('请选择标签')
    value2 = tkinter.StringVar()
    value2.set('请选择标签')
    value3 = tkinter.StringVar()
    value3.set('请选择标签')
    values1 = []
    for up in Sql:
        if up['tag'] not in values1:
            values1.append(up['tag'])
    values3=values2=values1
    combobox1 = ttk.Combobox(
        master=window,  # 父容器
        height=5,  # 高度,下拉显示的条目数量
        width=10,  # 宽度
        state="readonly",  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
        cursor="arrow",  # 鼠标移动时样式 arrow, circle, cross, plus...
        font=("", 20),  # 字体
        textvariable=value1,  # 通过StringVar设置可改变的值
        values=values1,  # 设置下拉框的选项
    )
    combobox2 = ttk.Combobox(
        master=window,  # 父容器
        height=5,  # 高度,下拉显示的条目数量
        width=10,  # 宽度
        state="readonly",  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
        cursor="arrow",  # 鼠标移动时样式 arrow, circle, cross, plus...
        font=("", 20),  # 字体
        textvariable=value2,  # 通过StringVar设置可改变的值
        values=values2,  # 设置下拉框的选项
    )
    combobox3 = ttk.Combobox(
        master=window,  # 父容器
        height=5,  # 高度,下拉显示的条目数量
        width=10,  # 宽度
        state="readonly",  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
        cursor="arrow",  # 鼠标移动时样式 arrow, circle, cross, plus...
        font=("", 20),  # 字体
        textvariable=value3,  # 通过StringVar设置可改变的值
        values=values3,  # 设置下拉框的选项
    )
    combobox1.bind("<<ComboboxSelected>>", choose_1)
    combobox1.place(x=100, y=30)
    combobox2.bind("<<ComboboxSelected>>", choose_2)
    combobox2.place(x=300, y=30)
    combobox3.bind("<<ComboboxSelected>>", choose_3)
    combobox3.place(x=500, y=30)
    label1 = '序号' + '\t' + '姓名' + '\t' + '\t' + '粉丝数' + '\t' + 'uid' + '\t' + 'tag'
    monty = ttk.LabelFrame(window, text=label1)  # 创建一个容器，其父容器为win
    monty.place(x=MyX + 20, y=MyY + 140)
    scr = scrolledtext.ScrolledText(monty, width=80, height=10, wrap=tkinter.WORD)
    scr.pack()
    b1 = tkinter.Button(window, text="确认", command=box_Huaxiang)
    b1.place(x=MyX + 200, y=MyY + 80)


def tk():
    '''
    主界面
    实现功能：
    输入一个标签，显示在所有用户标签属性的占比情况
    随机选取用户显示属性
    输入UID，可以指定用户查询属性
    :return:
    '''
    window = tkinter.Tk()
    window.title('BILIBILI用户画像查询')
    window.geometry('351x464+400+400')
    def Pie_Open():
        tk_pie()
    def Random_OpenBox_Open():
        tk_Box()
    def Users_Button_Open():
        tk_Users()
    def DivByFans_Button_Open():
        tk_DivByFans()
    def Tuijian_Button_Open():
        tk_Tuijian()
    def XuanQU_Button_Open():
        tk_XuanQU()
    '''
    定义函数区
    '''
    im = Image.open("E:\\study\\知识图谱\\111.jpg")
    img = ImageTk.PhotoImage(im)
    imLabel = tkinter.Label(window, image=img).place(x=0, y=0, width=351, height=464)
    Pie_Chart = ttkb.Button(
        window,
        text='查询饼图',
        command=Pie_Open,
        bootstyle=(INFO, OUTLINE)
    )
    Pie_Chart.place(x=40, y=40, width=100, height=50)
    # 实现输入标签名，然后查询标签分布情况并以饼图样式显示
    Random_OpenBox = ttkb.Button(
        window,
        text='随机开盒',
        command=Random_OpenBox_Open,
        bootstyle=(INFO, OUTLINE)
    )
    Random_OpenBox.place(x=210, y=40, width=100, height=50)
    # 随机选取用户显示信息
    Users_Button = ttkb.Button(
        window,
        text='查询用户',
        command=Users_Button_Open,
        bootstyle=(INFO, OUTLINE)
    )
    Users_Button.place(x=40, y=110, width=100, height=50)
    # 查询对应标签的用户
    DivByFans = ttkb.Button(
        window,
        text='根据粉丝数' + '\n' + '分析b站用户爱好',
        command=DivByFans_Button_Open,
        bootstyle=(INFO, OUTLINE)
    )
    DivByFans.place(x=210, y=110, width=120, height=70)
    # 分析粉丝量前几百名up主所属tag
    Tuijian_Button = ttkb.Button(
        window,
        text='爬取数据' + '\n' + '用户画像推荐',
        command=Tuijian_Button_Open,
        bootstyle=(INFO, OUTLINE)
    )
    Tuijian_Button.place(x=40, y=180, width=100, height=50)
    XuanQU_Button = ttkb.Button(
        window,
        text='选取数据' + '\n' + '用户画像推荐',
        command=XuanQU_Button_Open,
        bootstyle=(INFO, OUTLINE)
    )
    XuanQU_Button.place(x=210, y=180, width=100, height=50)
    window.mainloop()


def tk_pie():
    '''
    实现输入标签名，然后查询标签分布情况并以饼图样式显示
    '''
    window = tkinter.Toplevel()
    window.title('饼图查询')
    window.geometry('375x322')
    im = Image.open("E:\\study\\知识图谱\\巨大喷流.jpg")
    img = ImageTk.PhotoImage(im)
    imLabel = tkinter.Label(window, image=img).place(x=0, y=0, width=375, height=322)
    def Pie_Love():
        Pie_Chart('tag')
    '''l1 = tkinter.Label(window, text='输入想查询的标签')
    l1.pack()'''
    b1 = tkinter.Button(window, text='tag', command=Pie_Love)
    b1.place(x = 145,y = 110,width = 100,height = 50)
    window.mainloop()


def tk_Box():
    window = tkinter.Toplevel()
    window.title('随机开盒')
    window.geometry('580x750')
    im = Image.open("E:\\study\\知识图谱\\盒.jpg")
    img = ImageTk.PhotoImage(im)
    imLabel = tkinter.Label(window, image=img).place(x=0, y=0, width=580, height=750)
    def box():
        while(1):
            i = random.randint(0, n - 1)
            node = graph.nodes.get(i)
            if node != None:
                if 'userDescription' not in node:
                    return dict(node)['name'],dict(node)['fans'],dict(node)['uid'],dict(node)['follows'],"暂无简介"
                else:
                    return dict(node)['name'], dict(node)['fans'], dict(node)['uid'], dict(node)['follows'], dict(node)['userDescription']
    def box_all():
        tmp_name,tmp_love,tmp_uid,tmp_follow,tmp_userDescription=box()
        final_name='姓名：'+tmp_name
        final_love='粉丝数：'+tmp_love
        final_uid='UID：'+tmp_uid
        final_follow='关注数：'+tmp_follow
        t_name.delete(1.0, 'end')  # 清除文本框内容
        t_name.insert('insert',final_name)  # 将结果添加到文本框显示
        t_love.delete(1.0, 'end')  # 清除文本框内容
        t_love.insert('insert', final_love)  # 将结果添加到文本框显示
        t_uid.delete(1.0, 'end')  # 清除文本框内容
        t_uid.insert('insert', final_uid)  # 将结果添加到文本框显示
        t_follow.delete(1.0, 'end')  # 清除文本框内容
        t_follow.insert('insert', final_follow)  # 将结果添加到文本框显示
        scr.delete(1.0, 'end')  # 清除文本框内容
        scr.insert('insert', tmp_userDescription)
    b1 = tkinter.Button(window, text="随机显示用户信息", command=box_all)
    b1.pack()
    # 定义文本框
    t_name = tkinter.Text(window,
                     state='normal',  # 有disabled、normal 两个状态值，默认为normal
                     width=20, height=2
                     )
    MyX=390
    MyY=300
    t_name.place(x = MyX,y = MyY)
    t_love = tkinter.Text(window,
                          state='normal',  # 有disabled、normal 两个状态值，默认为normal
                          width=20, height=2
                          )
    t_love.place(x = MyX,y = MyY+35)
    t_uid = tkinter.Text(window,
                          state='normal',  # 有disabled、normal 两个状态值，默认为normal
                          width=20, height=2
                          )
    t_uid.place(x = MyX,y = MyY+70)
    t_follow = tkinter.Text(window,
                         state='normal',  # 有disabled、normal 两个状态值，默认为normal
                         width=20, height=2
                         )
    t_follow.place(x=MyX, y=MyY + 105)
    monty = ttk.LabelFrame(window, text='up主简介')  # 创建一个容器，其父容器为win
    monty.place(x = MyX,y = MyY+140)
    scr = scrolledtext.ScrolledText(monty, width=18, height=5, wrap=tkinter.WORD)
    scr.pack()
    window.mainloop()


def tk_Users():
    window = tkinter.Toplevel()
    window.title('查询用户')
    window.geometry('800x400')
    label=''
    label_Dict={'用户名':'name','uid':'uid','tag':'tag'}
    def box():
        # 定义输入框1
        p1 = t_get.get('0.0','end')
        p=p1.strip()
        #属性值
        id_list=[]
        label=label_Dict[combobox.get()]
        for i in range(len(Sql)):
            if p in Sql[i][label]:
                id_list.append(i)
        return id_list
    def box_all():
        list = box()
        n=0
        # 获取符合条件的id列表
        scr.delete(1.0,END)
        #清空文本框，便于多次查询
        for i in list:
            n=n+1
            node = Sql[i]
            scr.insert('end', n)
            scr.insert('end', '\t')
            scr.insert('end',node['name'])
            scr.insert('end', '\t')
            scr.insert('end', '\t')
            scr.insert('end', node['fans'])
            scr.insert('end', '\t')
            scr.insert('end', node['uid'])
            scr.insert('end', '\t')
            scr.insert('end', node['tag'])
            scr.insert('end', '\n')
        if n==0:
            scr.insert('end', "没有找到符合条件的用户")
    def choose(event):
        label_Dict[combobox.get()]
    '''def delete():  # 删除临时图
        window.destroy()
        gif.close()
    file = r"E:\study\知识图谱\动图.gif"
    label = tkinter.Label(window, text="11", bg="#FFFFFF")
    label.place(x = 300,y =0)
    button = tkinter.Button(window)
    button.place(x = 300,y =0)
    window.protocol('WM_DELETE_WINDOW', delete)  #####【重要】关闭窗口后的事件：delete
    gif = playGif(file)
    gif.playGif(window, button) ''' # 实现动态插放

    # 定义文本框
    MyX=10
    MyY=10
    tishi = tkinter.Label( window,text="请选择标签：")
    tishi.place(x = 50,y =10)
    # relx距离左边框的距离, rely距离上边框的距离
    value = tkinter.StringVar()
    value.set('标签')
    values=['用户名','uid','tag']
    combobox = ttk.Combobox(
        master=window,  # 父容器
        height=5,  # 高度,下拉显示的条目数量
        width=8,  # 宽度
        state="readonly",  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
        cursor="arrow",  # 鼠标移动时样式 arrow, circle, cross, plus...
        font=("", 20),  # 字体
        textvariable=value,  # 通过StringVar设置可改变的值
        values=values,  # 设置下拉框的选项
    )
    combobox.bind("<<ComboboxSelected>>", choose)
    combobox.place(x=150, y=5)
    tishi2 = tkinter.Label(window,text="请输入属性值：")
    tishi2.place(x = 400,y =5)
    t_get = tkinter.Text(window,
                         state='normal',  # 有disabled、normal 两个状态值，默认为normal
                         width=8, height=1,
                         font=("", 20),
                         )
    t_get.place(x = 550,y =5)
    label1='序号'+'\t'+'姓名'+'\t'+'\t'+'粉丝数'+'\t'+'uid'+'\t'+'tag'
    monty = ttk.LabelFrame(window, text=label1)  # 创建一个容器，其父容器为win
    monty.place(x = MyX+20,y = MyY+140)
    scr = scrolledtext.ScrolledText(monty, width=80, height=10, wrap=tkinter.WORD)
    scr.pack()
    b1 = tkinter.Button(
        window,
        text="显示用户信息",
        command=box_all,
        font=("", 20)
    )
    b1.place(x = MyX+250,y = MyY+80)


def tk_DivByFans():
    '''
        实现输入标签名，然后查询标签分布情况并以饼图样式显示
        '''
    window = tkinter.Toplevel()
    window.title('UID')
    window.geometry('800x700')
    new_list=sorted(Sql,key=(lambda Sql:Sql['fans']),reverse=True)
    def SqlSort():

        k=1
        for i in range(1):
            for x in new_list:
                scr.insert('end', k)
                k=k+1
                scr.insert('end', '\t')
                scr.insert('end', x['name'])
                scr.insert('end', '\t')
                scr.insert('end', '\t')
                scr.insert('end', x['uid'])
                scr.insert('end', '\t')
                scr.insert('end', x['fans'])
                scr.insert('end', '\t')
                scr.insert('end', x['follows'])
                scr.insert('end', '\t')
                scr.insert('end', x['userDescription'])
                scr.insert('end', '\t')
                scr.insert('end', x['tag'])
                scr.insert('end', '\t')
                #  name   uid  fans   follows  serDescription   videoNum   tag
                scr.insert('end', '\n')
    def SqlRank():
        from builtins import str
        base = 0
        dect = {}
        for n in range(25):
            base = base + 100
            for i in range(base):
                if new_list[i]['tag'] in dect:
                    dect[new_list[i]['tag']] = dect[new_list[i]['tag']]+1
                else:
                    dect[new_list[i]['tag']] = 1
            Mystr = "粉丝数前" + str(base) + "名的up主主营视频类型分布情况"
            scr_2.insert('end', Mystr)
            scr_2.insert('end', '\n')
            for key in dect:
                scr_2.insert('end', key)
                scr_2.insert('end', "有")
                scr_2.insert('end', dect[key])
                scr_2.insert('end', "个")
                scr_2.insert('end', ' ')
            scr_2.insert('end', '\n')
            scr_2.insert('end', '====================================================================')
            scr_2.insert('end', '\n')
    b1 = tkinter.Button(window, text='用户', command=SqlSort)
    b1.place(x=260, y=0, width=100, height=50)
    label1 = '序号' + '\t' + '姓名' + '\t' + '\t' + 'uid' + '\t' +'粉丝数'+'\t' +  '关注数'+'\t' + '视频数'+'\t' + 'Tag'
    monty = ttk.LabelFrame(window, text=label1)  # 创建一个容器，其父容器为win
    monty.place(x=80, y=50)
    scr = scrolledtext.ScrolledText(monty, width=70, height=10, wrap=tkinter.WORD)
    scr.pack()
    b2 = tkinter.Button(window, text='分析', command=SqlRank)
    b2.place(x=400, y=0, width=100, height=50)
    monty_2 = ttk.LabelFrame(window, text="分析结果")  # 创建一个容器，其父容器为win
    monty_2.place(x=80, y=350)
    scr_2 = scrolledtext.ScrolledText(monty, width=70, height=10, wrap=tkinter.WORD)
    scr_2.pack()
    window.mainloop()



if __name__ == "__main__":
    INIT_PLT()
    tk()