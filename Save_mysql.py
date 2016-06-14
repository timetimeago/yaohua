# __*__coding:utf-8__*__
# __*__coding:utf-8__*__
import MySQLdb
class My_Save:
    def __init__(self,dbtable):
        self.con = MySQLdb.connect(host='172.24.4.42',user='web',passwd='123456',db=dbtable)
        self.cur = self.con.cursor()
    def command(self,comm,args=0,Flag=0,type='save'):
        if Flag == 0:
            self.cur.execute(comm)
        else:
            self.cur.executemany(comm,args)
        data = self.cur.fetchall()
        self.con.commit()
        self.cur.close()
        self.con.close()
        if not type == 'save':
            return data
if __name__ == '__main__':
        M = My_Save('xiaozhang')
        M.command('truncate table Content;',type='save')
        M = My_Save('xiaozhang')
        M.command('truncate table temp;',type='save')
        M = My_Save('xiaozhang')
        M.command('truncate table adddate;',type='save')
        M = My_Save('xiaozhang')
        M.command('truncate table url;',type='save')
#         
