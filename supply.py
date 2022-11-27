from msilib import Dialog
import sys
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QListWidget
from PyQt5 import QtCore,QtGui,QtWidgets,uic
from datetime import datetime
import main

UI_class = uic.loadUiType("supply.ui")[0]

try:
    #DB Connection 생성
    cnx = mysql.connector.connect(user='root', password = 'jaewoosql',
                                host = '127.0.0.1', database = 'lotte_supermarket')
except:
    print("database connection error\n")
    sys.exit(1)

class Product:
    def __init__(self, id, stock, price, name, supplier_id):
        self.id = id
        self.stock = stock
        self.price = price
        self.name = name
        self.supplier_id = supplier_id

class User:
    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address

def getItems():
    query = ("SELECT * FROM product") # db에서 상품목록 가지고 오기
    cursor = cnx.cursor()
    cursor.execute(query)
    products = []
    for(product_id, product_stock, product_price, product_name, supplier_id) in cursor:
        product = Product(product_id, product_stock, product_price, product_name, supplier_id)
        products.append(product)
    return products

def dbsupplyItem(product, count, price):
    sql = "INSERT INTO product_supply (product_id, date, count, supply_price) VALUES (%s,%s,%s,%s)"
    today = datetime.today().strftime("%Y%m%d%H%M") #년월시분
    val = (str(product.id), today, str(count), str(price))
    cursor = cnx.cursor()
    # cursor.execute(sql,val)
    sql = "UPDATE product SET product_stock = product_stock + " + str(count) + " WHERE product_id = " + str(product.id) +";"
    cursor.execute(sql)
    cnx.commit()

def findProduct(products, id):
    for product in products:
        if product.id == int(id):
            return product
        
class SupplyWindow(QtWidgets.QMainWindow,UI_class):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setupUi(self)
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle("롯데 슈퍼")
        self.imagelabel.setPixmap(QtGui.QPixmap("./images/lottesuperlogo.png"))
        self.products = getItems()
        self.insertItems()
        self.pushButton_2.clicked.connect(self.suppliedItem)
        self.pushButton.clicked.connect(self.goBack)

    def insertItems(self):
        i = 1
        self.listWidget.insertItem(0,"{0:<4} | {1:<12} | {2:<10} | {3:<10}".format("상품번호","상품명", "상품가격", "상품재고"))
        for product in self.products:
            self.listWidget.insertItem(i, "{0:<10} | {1:<15} | {2:^10} | {3:^10}".format(product.id, product.name, str(product.price), str(product.stock)))
            i+=1

    def suppliedItem(self):
        items = self.listWidget.selectedIndexes()
        item_id = -1
        for item in items:
            item_attributes = item.data().split(" ")
            item_id = item_attributes[0].rstrip()
            product = findProduct(self.products, item_id)
            count = self.textEdit.toPlainText()
            price = self.textEdit_2.toPlainText()
            dbsupplyItem(product, count, price)   
        Dialog = QtWidgets.QDialog() 
        alert = QtWidgets.QMessageBox()
        alert.information(Dialog, "알림", "공급되었습니다.")
        self.supply = SupplyWindow(self.user)
        self.close()

    def goBack(self):
        self.main = main.MainWindow(self.user)
        self.close()

if __name__=='__main__':
    
    app=QtWidgets.QApplication(sys.argv)
    user = User(777,"정재우","경기도")
    mainwindow=SupplyWindow(user)  #SupplyWindow의 인스턴스 생성
    app.exec()