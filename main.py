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
import supply, orderedProduct

UI_class = uic.loadUiType("main.ui")[0]

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

def userOrderCount(user):
    query = ("select count(order_id) from user_order where user_id = " + str(user.id)) # db 에서 user order 개수 셈
    cursor = cnx.cursor()
    cursor.execute(query)
    for(count) in cursor:
        return count[0]

def orderProductCount(order_id):
    query = ("select count(order_product_id) from order_product where product_id = " + str(order_id)) # db 에서 order product 개수 셈
    cursor = cnx.cursor()
    cursor.execute(query)
    for(count) in cursor:
        return count[0]
    
def dborderItem(product, user):
    sql1 = "INSERT INTO user_order (order_id, user_id, address, total_price) VALUES (%s,%s,%s,%s)"
    sql2 = "INSERT INTO order_product (order_product_id, product_id, order_id, count) VALUES (%s,%s,%s,%s)"
    sql3 = "UPDATE product SET product_stock = product_stock - 1 WHERE product_id = " + str(product.id) +";"
    order_id = user.id*1000 + userOrderCount(user)
    order_product_id = order_id*10 + orderProductCount(order_id)
    count = 1
    val1 = (str(order_id), str(user.id), user.address, str(product.price))
    val2 = (str(order_product_id),str(product.id),str(order_id),str(count))

    cursor = cnx.cursor()
    cursor.execute(sql1,val1)
    cursor.execute(sql2,val2)
    cursor.execute(sql3)
    cnx.commit()
    
def findProduct(products, id):
    for product in products:
        if product.id == int(id):
            return product

class MainWindow(QtWidgets.QMainWindow,UI_class):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle("롯데 슈퍼")
        self.imagelabel.setPixmap(QtGui.QPixmap("./images/lottesuperlogo.png"))
        self.textEdit.setText("내정보 \nid : " + str(self.user.id) + "\n이름 : " + self.user.name + "\n주소 : " + self.user.address)
        self.products = getItems()
        self.insertItems()
        self.pushButton.clicked.connect(self.purchaseItem)
        self.pushButton_2.clicked.connect(self.goSupply)
        self.pushButton_3.clicked.connect(self.goOrderedProduct)
        self.pushButton_4.clicked.connect(self.exist)

    def insertItems(self):
        i = 1
        self.listWidget.insertItem(0,"{0:<4} | {1:<12} | {2:<10} | {3:<10}".format("상품번호","상품명", "상품가격", "상품재고"))
        for product in self.products:
            self.listWidget.insertItem(i, "{0:<10} | {1:<15} | {2:^10} | {3:^10}".format(product.id, product.name, str(product.price), str(product.stock)))
            i+=1

    def purchaseItem(self):
        items = self.listWidget.selectedIndexes()
        item_id = -1
        for item in items:
            item_attributes = item.data().split(" ")
            item_id = item_attributes[0].rstrip()
            product = findProduct(self.products, item_id)
            dborderItem(product, self.user)   
        Dialog = QtWidgets.QDialog() 
        alert = QtWidgets.QMessageBox()
        alert.information(Dialog, "알림", "주문했습니다.")
        self.main = MainWindow(self.user)
        self.close()

    def goSupply(self):
        self.supply = supply.SupplyWindow(self.user)
        self.close()

    def goOrderedProduct(self):
        self.order = orderedProduct.OrderWindow(self.user)
        self.close()

    def exist(self):
        self.close()

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    user = User(777,"정재우","경기도")
    mainwindow=MainWindow(user)  #MyWindow의 인스턴스 생성
    app.exec()