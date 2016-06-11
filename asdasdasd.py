# __*__coding:utf-8__*__

from PyQt5.QtWidgets import *
import sys
from analyse_web import *
class LoginDlg(QDialog):
    def __init__(self, parent=None):
        super(LoginDlg, self).__init__(parent)
        usr = QLabel("欢迎使用Spider(内容默认放在根目录)")
#         pwd = QLabel("密码：")
        ha = QLabel('输入查找内容')
#         self.usrLineEdit = QLineEdit()
        self.pwdLineEdit = QLineEdit()
        self.haha = QLineEdit()
#         self.pwdLineEdit.setEchoMode(QLineEdit.Password)

        gridLayout = QGridLayout()
        gridLayout.addWidget(usr, 0, 1, 1, 1)
#         gridLayout.addWidget(pwd, 1, 0, 1, 1)
        gridLayout.addWidget(ha, 2, 0, 1, 1)
#         gridLayout.addWidget(self.usrLineEdit, 0, 1, 1, 3);
#         gridLayout.addWidget(self.pwdLineEdit, 1, 1, 1, 3);
        gridLayout.addWidget(self.haha, 2, 1, 1, 3);

        okBtn = QPushButton("确定")
        cancelBtn = QPushButton("取消")
        btnLayout = QHBoxLayout()

        btnLayout.setSpacing(60)
        btnLayout.addWidget(okBtn)
        btnLayout.addWidget(cancelBtn)

        dlgLayout = QVBoxLayout()
        dlgLayout.setContentsMargins(40, 40, 40, 40)
        dlgLayout.addLayout(gridLayout)
        dlgLayout.addStretch(40)
        dlgLayout.addLayout(btnLayout)

        self.setLayout(dlgLayout)
        okBtn.clicked.connect(self.accept)
        cancelBtn.clicked.connect(self.reject)
        self.setWindowTitle("登录")
        self.resize(300, 200)

    def accept(self):
        Tuple_All = []
        URL_Tuple = []
        U1 = Analyse(Url)
        Que1 = Queue()
        Que2 = Queue()
        ttt = []
        FF = 0
        Update_Url(URL_Tuple,U1,Que1)
        key = self.haha.text()
        Key = key.encode('utf-8')
        date = Find_Key_value(Key)
        date = date.encode('utf-8')
        QMessageBox.warning(self,"提示","找到%s"%date,QMessageBox.Yes)
        Many_process_analyse_web(URL_Tuple,Que1,U1)
#         while not Que1.empty():
#             Data = Que1.get().replace('\'', '').replace('\n', '').replace('\r', '')
#             mmy = My_Save('xiaozhang')
#             mmy.command("insert into Content(content) values('%s')"%Data)
        Down_load(U1)
        M = My_Save('xiaozhang')
        M.command('truncate table Content;',type='save')
        M = My_Save('xiaozhang')
        M.command('truncate table temp;',type='save')
        M = My_Save('xiaozhang')
        M.command('truncate table adddate;',type='save')
        M = My_Save('xiaozhang')
        M.command('truncate table url;',type='save')
        exit(0)
#         if self.usrLineEdit.text().strip() == "eric" and self.pwdLineEdit.text() == "eric":
#             super(LoginDlg, self).accept()
#         else:
#             QMessageBox.warning(self,
#                     "警告",
#                     "用户名或密码错误！",
#                     QMessageBox.Yes)
#             self.usrLineEdit.setFocus()

app = QApplication(sys.argv)
dlg = LoginDlg()
dlg.show()
dlg.exec_()
app.exit()