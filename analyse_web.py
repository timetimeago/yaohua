# __*__coding:utf-8__*__
URL_Tuple = []
Tuple_All = []
ALL_Linke = []
import urllib2
import urllib
import re
import threading
import time
import os
import sys
from multiprocessing import Pool,Queue,Process
from Spider.Save_mysql import My_Save
urls = "http://www.webtoons.com/zh-hans/thriller/tales-of-the-unusual/list?title_no=296"
Url = 'http://www.webtoons.com'
class Analyse(object):
    def __init__(self,Url):
        self.__Url__ = Url
        agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
        self.__headers__ = {'username':agent,'Referer':self.__Url__}
    def Get_URL_SRC(self,URL_Tuple,Flag,que):  #得到一个页面的源码,que,Flag
        if  Flag == 2:
            Url = urllib2.Request(url=URL_Tuple,headers=self.__headers__)
            Mid_SRC = urllib2.urlopen(Url).read()
            return Mid_SRC
        else:
            if re.search('.*(png|jpg)$', URL_Tuple,re.MULTILINE):
                print u'不是网页,获取不到源码\n',URL_Tuple
            else:
                try:
                    Url = urllib2.Request(url=URL_Tuple,headers=self.__headers__)
                    Mid_SRC = urllib2.urlopen(Url).read()
                    Url_SRC = re.search('<html lang="zh_CN">(.*?)在周四更新</p>', Mid_SRC, re.S).group(1)
    #                 Url_dict = {URL_Tuple:Url_SRC}
                    if Flag == 1:
                        Data = Url_SRC.replace('\'', '').replace('\n', '').replace('\r', '')
                        mmy = My_Save('xiaozhang')
                        mmy.command("insert into Content(content) values('%s')"%Data)
#                         if que.put(Url_SRC):
#                             print u'failed'
#                             print URL_Tuple
                    else:
                        return Url_SRC
                except urllib2.HTTPError,e:
                    print '\n_________________________________\n',e,u'\n丢弃'
                except urllib2.URLError,e:
                    print u'\n打开失败,稍后重新获取\n'
                except AttributeError,e:
                    print u'\n过滤',URL_Tuple,'\n'
#             finally:
#                 sys.exit()
    def Get_All_Link(self,Src): #获得一共多少个页面
        Link_Tuple = re.findall('href="(http.*?)"', Src, re.S)
        return Link_Tuple
#     def Get_One_URL_ALL_Link(self,URL):  #得到一个页面的所有链接，并生成一个tuple
#         All_Link = re.findall('href=(http.*?)',URL ,re.S)
#         re.findall('', All_Src, re.S)[0][1]  #列表里面包含元组，元组第一项为 网址，第二项为漫画名，第三项为集数
    def Put_Queue(self,que):
        pass
    def Get_One_URL_info(self,One_URL):
        Src = self.Get_One_URL_SRC(One_URL)
        pass
def Many_Process():
    pass
def Splite_Tuple(URL_Tuple):
    count = 0
    Len = len(URL_Tuple)
    if Len < 4:
        Tuple_All.append("T0")
        Tuple_All["0"] = []
    else:
        Len = Len - Len%4 +4
        for Num in range(Len):   #4个链接为一list,然后把所有链接list放到另一list
            Tuple_All.append("T%s"%Num)
            Tuple_All[Num] = []
    Num = 0
#         print Tuple_All
    for i in URL_Tuple:
        if count <4:
            Tuple_All[Num].append(i)
            count += 1
        else:
            Num +=1
            count = 1
            Tuple_All[Num].append(i)
    return Tuple_All
def Find_exist(value,FF):
    My = My_Save('xiaozhang')
    if not My.command("select Flag from url where url = '%s'"%value,type='return'):
        My = My_Save('xiaozhang')
        My.command("insert into adddate(url) values('%s')"%value)
#         print u'发现新连接',value
        FF += 1
    else:
        FF = 0 
    return FF
def Load_Data(Key,Table):
    My = My_Save('xiaozhang')
    return My.command("select %s from %s"%(Key,Table), type='return')
def Q(x):
    print x
def Update_Url(URL_Tuple,A,Que1):
    FF = 0
    URL_Tuple = A.Get_All_Link(A.Get_URL_SRC(urls,0,Que1))
    for i in URL_Tuple:
        FF=Find_exist(i,FF)
    if  FF !=0:
        print u'有更新'
    else:
        print u'无更新'
def Many_process_analyse_web(URL_Tuple,Que1,A):
    URL_Tupl = []
    for i in Load_Data('url','temp'):
        for x in i:
            print x
            URL_Tupl.append(x)
#             URL_Tuple.append[x]
#     URL_Tupl = Splite_Tuple(URL_Tupl)
    for Num in URL_Tupl:
#     for i in Num:
#             print i
        A.Get_URL_SRC(Num,1,Que1)
#         p.daemon = True
#         p.start()
#         p.join(1)
def Find_Key_value(Key):
    mmy = My_Save('xiaozhang')
    print 
    w={'w':Key}
    ww=urllib.urlencode(w)
    date = re.search('=(.*?)$', ww).group(1)
    mmy.command("insert into xiaozhang.temp(url) select url from adddate where url like '%%%s%%'"%date,type = 'save')
    mmy = My_Save('xiaozhang')
    value = mmy.command('select count(*) from temp',  type='return')
    return u'查找到%s'%value
#     Flag = 0
#     data = ''
#     AAA = ''
#     try:
#         data = re.search('<ul id="_listUl">(.*?)</ul>', Key, re.S).group(1)
#     except AttributeError:
#         pass
#     try:
#         AAA = re.search('id="_imageList">(.*?)</div>', Key, re.S).group(1)
#     except AttributeError:
#         pass
#     if data !='':
#         Flag += 1
#     if AAA !='':
#         Flag += 2
#     if Flag == 1:
#         return data
#     elif Flag == 2:
#         return AAA
#     else:
#         return None
def Down_load(A):
    title = []
    text = []
    link = []
    dadada = []
    data= Load_Data('content', 'Content')
    for i in data:
        for x in i:
            title.append(re.findall('title>\[(.*?)\].*?_imageList">(.*)', x, re.S)[0][0])
            date = re.findall('"_imageList">(.*)', x,re.S)[0]
            dadada.append(date)
# #             with open('asd','a') as f:
# #                 f.write(date)
    for i in dadada:
        link.append(re.findall('data-url="(.*?)"', i, re.S))
#             exit
    count = 0
#     print title
#     print title[1]
    ttt = 0
    print len(link)
    for i in link:
#         count +=1
#         print i
#     print count
        title1 = title[ttt].decode('utf-8')
        for x in i:
            data = A.Get_URL_SRC(x, 2,que='')
            if not os.path.exists(title1):
                os.mkdir(title1)
            file = title1 +'/'+str(count)+'.png'
            with open(file,'wb') as f:
                f.write(data)
            count +=1
        ttt +=1
#      
if __name__ == '__main__':
        Tuple_All = []
        URL_Tuple = []
        U1 = Analyse(Url)
        Que1 = Queue()
        Que2 = Queue()
        ttt = []
        FF = 0
#         print U1.Get_URL_SRC(urls, 0, Que1)
          
        choice = raw_input(u'检查更新y/n：')          #更新数据库连接
        if choice == 'y':
            Update_Url(URL_Tuple)
        choice = raw_input(u'查找y/n:')
        if choice  =='y':
            Value = Find_Key_value(raw_input(u'输入关键字:'))
        choice = raw_input(u'是否开始分析源码y/n:')       #数据库取连接
        if choice == 'y':
            Many_process_analyse_web(URL_Tuple,Que1)
            while not Que1.empty():
                Data = Que1.get().replace('\'', '').replace('\n', '').replace('\r', '')
                mmy = My_Save('xiaozhang')
                mmy.command("insert into Content(content) values('%s')"%Data)
        choice = raw_input(u'获取数据y/n:')
        Down_load()
        M = My_Save('xiaozhang')
        M.command('truncate table Content;',type='save')
        M = My_Save('xiaozhang')
        M.command('truncate table temp;',type='save')
        M = My_Save('xiaozhang')
        M.command('truncate table adddate;',type='save')