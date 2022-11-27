from msilib import Dialog
import sys
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore,QtGui,QtWidgets,uic
import main

UI_class = uic.loadUiType("login.ui")[0]

try:
    #DB Connection 생성
    cnx = mysql.connector.connect(user='root', password = 'jaewoosql',
                                host = '127.0.0.1', database = 'lotte_supermarket')
except:
    print("database connection error\n")
    sys.exit(1)

class User:
    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address

class LoginWindow(QtWidgets.QMainWindow,UI_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle("로그인")
        self.label.setPixmap(QtGui.QPixmap("./images/lottesuperlogo.png"))
        self.login.clicked.connect(self.button1Function)
        self.id.setText('id 입력')
        Dialog.setObjectName("Dialog")
        Dialog.resize(352,147)
        
    def button1Function(self, cursor):
        #db랑 비교 
        loginId = int(self.id.text())

        query = ("SELECT * FROM user where user_id = " + str(loginId)) # db에서 회원정보들 가지고 오기
        cursor = cnx.cursor()
        cursor.execute(query)
        flag = 0
        for(user_id, name, address) in cursor:
            user = User(user_id, name, address)
            flag = 1
        alert = QtWidgets.QMessageBox()
        if flag == 1:
            alert.information(Dialog,"알림", "로그인 성공")
            self.main = main.MainWindow(user)
            self.close()
        else:
            alert.information(Dialog,"알림", "로그인 실패")
        
if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    mywindow=LoginWindow()  #MyWindow의 인스턴스 생성
    app.exec()

