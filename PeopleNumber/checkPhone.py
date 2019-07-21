import pymysql
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QLineEdit, QPushButton


def checkPhone(str):
    if (len(str) == 12 and str.replace("-", "").isdigit() and str[4:5] == '-'):
        return 7
    elif (len(str) == 12 and str.replace("-", "").isdigit() and str[3:4] == '-'):
        return 8
    elif (str.isdigit()):
        length=len(str)
        if (length == 3 and str[0]!=1):
            return 3
        elif (length == 5 and (str[0]==1 or str[0]==9)):
            return 5
        elif (length == 11):
            return 11
        else:
            return "号码的长度不对哦"
    else:
        return "号码格式不对，请重新输入"

class Demo(QWidget):
    def __init__(self, parent=None):
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
        self.resize(400, 150)
        self.translateButton1.clicked.connect(lambda: self.translate())
    def translate(self):
        str = self.LineEdit1.text()

        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='phone', charset='utf8')
        cur = conn.cursor()
        results="无法查询到您输入的号码信息"
        if not str:
            return
        print(checkPhone(str))
        if (checkPhone(str) == 3):
            print(111)
            cur.execute('select * from threePhone where phone='+str)
            rows=cur.fetchall()
            if(rows==()):
                self.LineEdit2.setText(results)
            else:
                for row in rows:
                    results = row[1]
                    try:
                        self.LineEdit2.setText(results)
                    except Exception as e:
                        print('---->',e)
        elif(checkPhone(str)==5):
            cur.execute('select * from servicenumber where phone=' + str)
            rows=cur.fetchall()
            for row in rows:
                results = row[1]
                try:
                    self.LineEdit2.setText(results)
                except Exception as e:
                    print('---->', e)
        elif(checkPhone(str)==7):
            str=str[0:4]
            cur.execute('select * from areacodefour where phone=' + str)
            rows=cur.fetchall()
            if (rows == ()):
                self.LineEdit2.setText(results)
            else:
                for row in rows:
                    results=row[1]
                    try:
                        self.LineEdit2.setText(results)
                    except Exception as e:
                        print('--->',e)
        else:
            self.LineEdit2.setText("无法找到结果")
        cur.close()
        conn.commit()
        conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
