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
import main

UI_class = uic.loadUiType("orderedProduct.ui")[0]

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

class Order:
    def __init__(self, id, user_id, address, total_price):
        self.id = id
        self.user_id = user_id
        self.address = address
        self.total_price = total_price

class OrderProduct:
    def __init__(self, id, product_id, order_id, count):
        self.id = id
        self.product_id = product_id
        self.order_id = order_id
        self.count = count

try:
    #DB Connection 생성
    cnx = mysql.connector.connect(user='root', password = 'jaewoosql',
                                host = '127.0.0.1', database = 'lotte_supermarket')
except:
    print("database connection error\n")
    sys.exit(1)

def getItems():
    query = ("SELECT * FROM product ") # db에서 상품목록 가지고 오기
    cursor = cnx.cursor()
    cursor.execute(query)
    products = []
    for(product_id, product_stock, product_price, product_name, supplier_id) in cursor:
        product = Product(product_id, product_stock, product_price, product_name, supplier_id)
        products.append(product)
    return products

def getOrders(user):
    query = ("SELECT * FROM user_order where user_id = " + str(user.id)) # db에서 order목록 가지고 오기
    cursor = cnx.cursor()
    cursor.execute(query)
    orders = []
    for(order_id, user_id, address, total_price) in cursor:
        order = Order(order_id, user_id, address, total_price)
        orders.append(order)
    return orders

def getOrderProducts(order_id):
    query = ("SELECT * FROM order_product where order_id = " + str(order_id)) # db에서 order상품목록 가지고 오기
    cursor = cnx.cursor()
    cursor.execute(query)
    orderProducts = []
    for(product_id, user_id, address, total_price) in cursor:
        orderProduct = OrderProduct(product_id, user_id, address, total_price)
        orderProducts.append(orderProduct)
    return orderProducts

def getProduct(id, products):
    for product in products:
        if(product.id == id):
            return product

def makeList(products, orders):
    # (주문번호, 상품이름, 상품개수, 상품 총 금액, 주소)
    rows = []
    for order in orders:
        orderProducts = getOrderProducts(order.id)
        for orderProduct in orderProducts:
            row = []
            if orderProduct.order_id != order.id:
                continue
            product = getProduct(orderProduct.product_id, products)
            row.append(order.id)
            row.append(product.name)
            row.append(orderProduct.count)
            row.append(order.total_price)
            row.append(order.address)
            rows.append(row)
            print(row)
    return rows

class OrderWindow(QtWidgets.QMainWindow,UI_class):
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
        self.pushButton.clicked.connect(self.goBack)
        self.products = getItems()
        self.orders = getOrders(self.user)
        self.orderList = makeList(self.products, self.orders)
        self.insertItems()

    def goBack(self):
        self.main = main.MainWindow(self.user)
        self.close()

    def insertItems(self):
        i = 1
        self.listWidget.insertItem(0,"{0:<4} | {1:<10} | {2:<10} | {3:<10} | {4:<10}".format("주문번호" , "상품이름", "상품개수", "상품 총 금액", "주소"))
        for order in self.orderList:
            self.listWidget.insertItem(i, "{0:<10} | {1:<15} | {2:^10} | {3:^10} | {4:<10}".format(order[0], order[1], order[2], order[3], order[4]))
            i+=1
    
if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    user = User(777,"정재우","경기도")
    mainwindow=OrderWindow(user)  #MyWindow의 인스턴스 생성
    app.exec()