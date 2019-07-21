import pymysql
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QLineEdit, QPushButton

# 检查号码是否符合要求
def checkPhone(str):
    str_error=''
    # 判断str是否全部为数字
    if (str.isdigit()):
        length=len(str)
        if length == 3 :
            if str[0]=='1' or str[0]=='9':
                return 3
            else:
                str_error = '号码开头只能是1或9，请重新输入'
                return str_error
        elif length == 5 :
            if str[0]=='1' or str[0]=='9':
                return 5
            else:
                str_error = '号码开头只能是1或9，请重新输入'
                return str_error
        elif length ==7:
            if str[0] != '1' and str[0] != '9' and str[0] != '0':
                return 7
            else:
                str_error = '号码开头不能是0或1或9，请重新输入'
                return str_error
        elif length == 8:
            if str[0] != '1' and str[0] != '9' and str[0] != '0':
                return 8
            else:
                str_error = '号码开头只不能是0或1或9，请重新输入'
                return str_error
        elif (length == 11):
            # 手机号码
            if str[0] == '1':
                return 12
            # 座机号码
            elif str[0] == '0' or str[0]=='8':
                return 11
            else:
                str_error = '号码开头只能是0或1或8，请重新输入'
                return str_error
        else:
            str_error = '号码的长度不对哦,请重新输入'
            return str_error
    else:
        str_error = '号码只能包含数字哦，请重新输入'
        return str_error

class Demo(QWidget):
    def __init__(self, parent=None):
        # 设计一个窗口查询界面
        super().__init__()
        self.setWindowTitle('电话号码查询系统')
        self.Label1 = QLabel('电话号码')
        self.Label2 = QLabel('查询结果')
        self.LineEdit1 = QLineEdit()
        self.LineEdit2 = QLineEdit()
        self.LineEdit2.setReadOnly(True)
        self.translateButton1 = QPushButton()
        self.translateButton1.setText('查询')
        self.grid = QGridLayout()
        self.grid.setSpacing(12)
        self.grid.addWidget(self.Label1, 1, 0)
        self.grid.addWidget(self.LineEdit1, 1, 1)
        self.grid.addWidget(self.Label2, 2, 0)
        self.grid.addWidget(self.LineEdit2, 2, 1)
        self.grid.addWidget(self.translateButton1, 1, 2)
        self.setLayout(self.grid)
        self.resize(800, 350)
        self.translateButton1.clicked.connect(lambda: self.translate())
    # 监听“查询”按钮事件，并且响应
    def translate(self):
        str = self.LineEdit1.text()
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='phone', charset='utf8')
        cur = conn.cursor()
        results = "无法查询到您输入的号码信息"
        # 输入号码类型或者长度错误后，返回相应的错误结果
        if type(checkPhone(str))==type('111'):
            str_error=checkPhone(str)
            self.LineEdit2.setText(str_error)
            return
        if not str:
            return
        # 号码长度为3并且首位字符符合要求，查询phone数据库的threePhone表
        if (checkPhone(str) == 3):
            cur.execute('select * from threePhone where phone=' + str)
            rows = cur.fetchall()
            if (rows == ()):
                self.LineEdit2.setText(results)
            else:
                for row in rows:
                    results = row[1]
                    try:
                        self.LineEdit2.setText(results)
                    except Exception as e:
                        print('---->', e)
        # 号码长度为3并且首位字符符合要求，查询phone数据库的servicenumber表
        elif(checkPhone(str)==5):
            cur.execute('select * from servicenumber where phone=' + str)
            rows=cur.fetchall()
            if (rows == ()):
                self.LineEdit2.setText(results)
            else:
                for row in rows:
                    results = row[1]
                    try:
                        self.LineEdit2.setText(results)
                    except Exception as e:
                        print('---->', e)
        elif(checkPhone(str)==7):
            results="号码为本地座机号码，当前地区为广西柳州"
            self.LineEdit2.setText(results)
        elif (checkPhone(str) == 8):
            results = "号码错误，柳州本地号码只能为7位数"
            self.LineEdit2.setText(results)
        elif (checkPhone(str) == 11):
            cur.execute('select * from areacodethree where phone=' + str[0:3])
            rows = cur.fetchall()
            if (rows == ()) and str[0]!='8':
                cur.execute('select * from areacodefour where phone=' + str[0:4])
                rows = cur.fetchall()
                if (rows == ()):
                    self.LineEdit2.setText(results)
                else:
                    for row in rows:
                        results = row[1]
                        if str[4] == '1' or str[4] == '9' or str[4] == '0':
                            self.LineEdit2.setText("号码区号：" + results + ';但号码第5位不能是0或1或9，请重新输入')
                        else:
                            self.LineEdit2.setText(results)
            elif rows == ():
                self.LineEdit2.setText(results)
            else:
                for row in rows:
                    results = row[1]
                    if str[3] == '1' or str[3] == '9' or str[3] == '0':
                        self.LineEdit2.setText("号码区号：" + results + ';但号码第4位不能是0或1或9，请重新输入')
                    else:
                        self.LineEdit2.setText(results)

        # 号码长度为11并且首位字符符合要求，查询phone数据库的serviceprovide表
        elif (checkPhone(str) == 12):
            cur.execute('select * from serviceprovide where phone=' + str[0:3])
            rows = cur.fetchall()
            if (rows == ()):
                self.LineEdit2.setText('错误，中国无此运营商，请重新输入')
            else:
                for row in rows:
                    results = row[1]
                cur.execute('select * from placenumber where phone=' + str[0:7])
                rows = cur.fetchall()

                if (rows == ()):
                    self.LineEdit2.setText('查询不到结果，号码错误或者数据库无记录')
                else:
                    for row in rows:
                        results = row[1]
                        self.LineEdit2.setText(results)
        cur.close()
        conn.commit()
        conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
