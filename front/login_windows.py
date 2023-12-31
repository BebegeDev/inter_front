# Form implementation generated from reading ui file 'face_ui.ui'
#
# Created by: PyQt6 UI code generator 6.6.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QLineEdit, QWidget
from PyQt6 import QtCore, QtGui, QtWidgets
from back.work import Worker
from back.login_windows_back import UiAutoWindowBack
from back.main_windows_back import MainWindowBack




class UiMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.main_window = None
        self.auto_window = None
        self.statusbar = None
        self.menubar = None
        self.label_2 = None
        self.label_3 = None
        self.line_password = None
        self.line_login = None
        self.central_widget = None
        self.label = None
        self.progressBar = None
        self.listWidget = None
        self.horizontalScrollBar = None
        self.verticalScrollBar = None
        self.button_autorization = None
        self.ui_back_auto = UiAutoWindowBack()
        self.threadpool = QThreadPool()

    def setup_ui(self, maine_window):
        self.auto_window = maine_window
        self.auto_window.resize(800, 350)
        self.central_widget = QtWidgets.QWidget(parent=self.auto_window)

        self.button_autorization = QtWidgets.QPushButton(parent=self.central_widget)
        self.button_autorization.setGeometry(QtCore.QRect(150, 160, 211, 71))

        self.button_autorization.clicked.connect(self.run_push_user)
        self.verticalScrollBar = QtWidgets.QScrollBar(parent=self.central_widget)
        self.verticalScrollBar.setGeometry(QtCore.QRect(780, 0, 16, 291))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Orientation.Vertical)

        self.horizontalScrollBar = QtWidgets.QScrollBar(parent=self.central_widget)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(535, 290, 241, 20))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Orientation.Horizontal)

        self.listWidget = QtWidgets.QListWidget(parent=self.central_widget)
        self.listWidget.setGeometry(QtCore.QRect(535, 0, 241, 291))

        self.progressBar = QtWidgets.QProgressBar(parent=self.central_widget)
        self.progressBar.setGeometry(QtCore.QRect(60, 270, 391, 23))
        self.progressBar.hide()

        self.label = QtWidgets.QLabel(parent=self.central_widget)
        self.label.setGeometry(QtCore.QRect(150, 10, 211, 41))
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.line_login = QtWidgets.QLineEdit(parent=self.central_widget)
        self.line_login.setPlaceholderText("Логин")
        self.line_login.setGeometry(QtCore.QRect(150, 50, 211, 31))

        self.label_2 = QtWidgets.QLabel(parent=self.central_widget)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 121, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label_3 = QtWidgets.QLabel(parent=self.central_widget)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 121, 31))
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.line_password = QtWidgets.QLineEdit(parent=self.central_widget)
        self.line_password.setPlaceholderText("Пароль")
        self.line_password.setGeometry(QtCore.QRect(150, 110, 211, 31))
        self.line_password.setEchoMode(QLineEdit.EchoMode.Password)


        self.auto_window.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(parent=self.auto_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))

        self.auto_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=self.auto_window)

        self.auto_window.setStatusBar(self.statusbar)

        self.retranslate_ui(self.auto_window)
        QtCore.QMetaObject.connectSlotsByName(self.auto_window)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_autorization.setText(_translate("MainWindow", ""))
        self.button_autorization.setText(_translate("MainWindow", ""))
        self.button_autorization.setText(_translate("MainWindow", "Войти"))
        self.label.setText(_translate("MainWindow", "Авторизация"))
        self.label_2.setText(_translate("MainWindow", "Логин"))
        self.label_3.setText(_translate("MainWindow", "Пароль"))

    def run_push_user(self):
        self.progressBar.setValue(0)
        self.progressBar.setRange(0, 0)
        self.progressBar.show()
        worker = Worker(self.connect_user_mqtt_server)
        worker.signals.result.connect(self.result_connect)
        self.threadpool.start(worker)

    def connect_user_mqtt_server(self):
        if self.ui_back_auto.connection(self.line_login.text(), self.line_password.text()):
            self.add_message_to_list(self.ui_back_auto.message, 'green')
        else:
            self.add_message_to_list(self.ui_back_auto.message, 'red')

    def add_message_to_list(self, message, color):
        if message:
            item = QtWidgets.QListWidgetItem(message)
            item.setBackground(QtGui.QColor(color))
            self.listWidget.addItem(item)


    def result_connect(self):
        self.progressBar.setValue(0)
        self.progressBar.setRange(0, 100)
        self.progressBar.hide()
        if self.ui_back_auto.connected_user:
            self.main_window = MainWindowBack(self.ui_back_auto.mqttc)
            print(123)
            self.main_window.show()
            self.auto_window.close()


