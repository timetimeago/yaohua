# __*__coding:utf-8__*__
import urllib2
import urllib
import re
import threading
import time
import os
import sys
from multiprocessing import Pool,Queue,Process
from Save_mysql import My_Save
urls = "http://www.webtoons.com/zh-hans/thriller/tales-of-the-unusual/list?title_no=296"
Url = 'http://www.webtoons.com'
class Analyse(object):
    def __init__(self,Url):
        self.__Url__ = Url
        agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
        self.__headers__ = {'username':agent,'Referer':self.__Url__}
    def Get_URL_SRC(self,URL_Tuple,Flag,que):  #得到一个页面的源码,que,Flag
        if re.search('.*(png|jpg)$', URL_Tuple,re.MULTILINE):
            print u'不是网页,获取不到源码\n',URL_Tuple
        else:
            try:
                Url = urllib2.Request(url=URL_Tuple,headers=self.__headers__)
                Url_SRC = urllib2.urlopen(Url).read()
                Url_dict = {URL_Tuple:Url_SRC}
                if Flag == 1:
                    print 'ha'
                    if que.put(Url_dict):
                        print u'failed'
                        print URL_Tuple
                        sys.exit(0)
                    else:
                        sys.exit(0)
                else:
                    return Url_SRC
            except urllib2.HTTPError,e:
                print '\n_________________________________\n',e,u'\n丢弃'
            except urllib2.URLError,e:
                print u'\n打开失败,稍后重新获取\n'
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
    for Num in range(len(URL_Tuple)/4):   #4个链接为一list,然后把所有链接list放到另一list
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
    My = My_Save()
    if not My.command("select Flag from url where url = '%s'"%value,type='return'):
        My.command("insert into url(url) values(%s)"%value)
        print u'发现新连接',value
    else:
        FF += 1
    return FF
def Load_Data():
    My = My_Save()
    return My.command("select url from url", type='return')
def Q(x):
    print x
if __name__ == '__main__':
        p = Pool(4)
        Tuple_All = []
        URL_Tuple = []
        U1 = Analyse(Url)
        Que1 = Queue()
        FF = 0
#         choice = raw_input(u'检查更新y/n：')          #更新数据库连接
#         if choice == 'y':
#             URL_Tuple = U1.Get_All_Link(U1.Get_URL_SRC(urls,0,Que1))  #,Que1,0
#             for i in URL_Tuple:
#                 Find_exist(i,FF)
#             if  FF !=0:
#                 print u'有更新'
#             else:
#                 print u'无更新'
        choice = raw_input(u'是否开始分析数据y/n:')       #数据库取连接
        def f(x,Tuple_All=URL_Tuple):
            for i in x:
                URL_Tuple.append(i)
        if choice =='y':
            map(f,Load_Data())
        URL_Tuple = Splite_Tuple(URL_Tuple)
        for Num in URL_Tuple:
            for i in Num:
                p = Process(target=U1.Get_URL_SRC,args=(i,1,Que1))
                p.start()
                p.join(1)
#                 print multiprocessing.cpu
#                 time.sleep(10)
#                 sys.exit()
#                 Que1.put(-1)
#         print 'asdad'
            
                
#         Tuple_All = Splite_Tuple(URL_Tuple)
#         for Num in Tuple_All:
# #             My = My_Save()
# #             My.command('insert into url(url) values(%s)', Num, 1)
#             for URl in Num:
#                 Find_exist(URl, Tuple_Add)