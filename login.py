from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
from PyQt5.QtWidgets import (QApplication, QMessageBox)
from PyQt5.QtCore import Qt
import sys
import imagesqt_rc
import logging

#Logging and console
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class MainWindowExample(QMainWindow):

    def __init__(self):
        super(MainWindowExample, self).__init__()
        loadUi('login.ui', self)
        self.ButtonLogin.clicked.connect(self.selectLevel)

#
#Authenticate Module
#
    def selectLevel(self):
        username = self.user.text()
        password = self.password.text()

        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'")
            row = cursor.fetchone()

            if row is not None:
                logger.debug("User Level: %s" % row[3])

                def level1():
                    logger.debug("Hi level 1")
                    self.hide()
                    anotherwin = winlevel1(self)
                    anotherwin.show()

                def level2():
                    logger.debug("Hi level 2:")
                    self.hide()
                    anotherwin = winlevel2(self)
                    anotherwin.show()

                def level3():
                    logger.debug("Hi level 3:")
                    self.hide()
                    anotherwin = winlevel3(self)
                    anotherwin.show()
                #Python switch
                level = row[3]
                options = {1: level1,
                           2: level2,
                           3: level3,
                           }
                options[level]()

            else:
                logger.debug("User or password incorrect/empty")
                Q = QMessageBox()
                Q = QMessageBox.information(Q, 'Error',
                                            'User or password incorrect/empty.',
                                            QMessageBox.Ok)

        except Error as e:
            logger.exception("Authenticated Error DB: %s" % e)

        finally:
            cursor.close()
            conn.close()

#
#End Module Log in
#

#
# Window Level 1
#
class winlevel1(QMainWindow):

    def __init__(self, parent=None):
        super(winlevel1, self).__init__(parent)
        loadUi('level1.ui', self)
        self.btn_exit.clicked.connect(self.exitwinlevel1)
        self.btn_sendValue.clicked.connect(self.sendValue)
        #Combobox where we are going to pass the value of id from this class to another
        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            #Read the products name and id
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM product")
            result_set = cursor.fetchall()
        except Error as error:
            logger.exception(error)

        for products in result_set:
            self.combo_products.addItem(products[1], int(products[0]))
        cursor.close()


    def sendValue(self):
        logger.debug("Send the id value to the other class")
        #Get the Product Id
        id_product = self.combo_products.itemData(self.combo_products.currentIndex())
        logger.debug("Product Int id: %s" % id_product)
        self.hide()
        self.anotherwindow = classWhithValue(id_product)
        self.anotherwindow.show()

    def exitwinlevel1(self):
        self.close()

    def closeEvent(self, event):
        """Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed - Save, Close, Cancel buttons
        """
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure about exit?",
            QMessageBox.Close | QMessageBox.Cancel)

        if reply == QMessageBox.Close:
            logger.debug("Close App")
            app.quit()
        else:
            logger.debug("Cancel Close")
            event.ignore()


    def keyPressEvent(self, event):
        """Close application from escape key.

        results in QMessageBox dialog from closeEvent, good but how/why?
        """
        if event.key() == Qt.Key_Escape:
            logger.debug("Key Scape")
            self.close()
#
#
#End Window Level 1
#
#

#
#Class who get the value
#

class classWhithValue(QMainWindow):

    def __init__(self, id_product, parent=None):
        super(classWhithValue, self).__init__(parent)
        loadUi('getTheValue.ui', self)
        self.btn_exit.clicked.connect(self.exitwinlevel1)
        self.myIdValue = id_product
        logger.debug("Value Obtained: %s" % self.myIdValue)
        self.valueIdfromOhterClass.setText(str(self.myIdValue))


    def exitwinlevel1(self):
        self.close()

    def closeEvent(self, event):
        """Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed - Save, Close, Cancel buttons
        """
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure about exit?",
            QMessageBox.Close | QMessageBox.Cancel)

        if reply == QMessageBox.Close:
            logger.debug("Close App")
            app.quit()
        else:
            logger.debug("Cancel Close")
            event.ignore()


    def keyPressEvent(self, event):
        """Close application from escape key.

        results in QMessageBox dialog from closeEvent, good but how/why?
        """
        if event.key() == Qt.Key_Escape:
            logger.debug("Key Scape")
            self.close()

#
#
#Window Level 2
#
class winlevel2(QMainWindow):

    def __init__(self, parent=None):
        super(winlevel2, self).__init__(parent)
        loadUi('level2.ui', self)
        self.btn_exit.clicked.connect(self.exitwinlevel2)
        self.btn_sendValue.clicked.connect(self.sendValue)
        # Combobox where we are going to pass the value of id from this class to another
        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            # Read the products name and id
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM product")
            result_set = cursor.fetchall()
        except Error as error:
            logger.exception(error)

        for products in result_set:
            self.combo_products.addItem(products[1], int(products[0]))
        cursor.close()

    def sendValue(self):
        logger.debug("Send the id value to the other class")
        # Get the Product Id
        id_product = self.combo_products.itemData(self.combo_products.currentIndex())
        logger.debug("Product Int id: %s" % id_product)
        self.hide()
        self.anotherwindow = classWhithValuelevel2(id_product)
        self.anotherwindow.show()

    def exitwinlevel2(self):
        self.close()

    def closeEvent(self, event):
        """Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed - Save, Close, Cancel buttons
        """
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure about exit?",
            QMessageBox.Close | QMessageBox.Cancel)

        if reply == QMessageBox.Close:
            logger.debug("Close App")
            app.quit()
        else:
            logger.debug("Cancel Close")
            event.ignore()


    def keyPressEvent(self, event):
        """Close application from escape key.

        results in QMessageBox dialog from closeEvent, good but how/why?
        """
        if event.key() == Qt.Key_Escape:
            logger.debug("Key Scape")
            self.close()
#
#
#End Window Level 2
#

#
#Class who get the value
#

class classWhithValuelevel2(QMainWindow):

    def __init__(self, id_product, parent=None):
        super(classWhithValuelevel2, self).__init__(parent)
        loadUi('getTheValuelevel2.ui', self)
        self.btn_exit.clicked.connect(self.exitwinlevel1)
        self.myIdValue = id_product
        logger.debug("Value Obtained: %s" % self.myIdValue)
        self.valueIdfromOhterClass.setText(str(self.myIdValue))


    def exitwinlevel1(self):
        self.close()

    def closeEvent(self, event):
        """Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed - Save, Close, Cancel buttons
        """
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure about exit?",
            QMessageBox.Close | QMessageBox.Cancel)

        if reply == QMessageBox.Close:
            logger.debug("Close App")
            app.quit()
        else:
            logger.debug("Cancel Close")
            event.ignore()


    def keyPressEvent(self, event):
        """Close application from escape key.

        results in QMessageBox dialog from closeEvent, good but how/why?
        """
        if event.key() == Qt.Key_Escape:
            logger.debug("Key Scape")
            self.close()


#
# Window Level 3
#
class winlevel3(QMainWindow):

    def __init__(self, parent=None):
        super(winlevel3, self).__init__(parent)
        loadUi('level3.ui', self)
        self.btn_exit.clicked.connect(self.exitwinlevel3)

    def exitwinlevel3(self):
        self.close()

    def closeEvent(self, event):
        """Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed - Save, Close, Cancel buttons
        """
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure about exit?",
            QMessageBox.Close | QMessageBox.Cancel)

        if reply == QMessageBox.Close:
            logger.debug("Close App")
            app.quit()
        else:
            logger.debug("Cancel Close")
            event.ignore()


    def keyPressEvent(self, event):
        """Close application from escape key.

        results in QMessageBox dialog from closeEvent, good but how/why?
        """
        if event.key() == Qt.Key_Escape:
            logger.debug("Key Scape")
            self.close()

#
# End Window Level 3
#


#Start App
app = QApplication(sys.argv)
main = MainWindowExample()
main.show()
sys.exit(app.exec_())