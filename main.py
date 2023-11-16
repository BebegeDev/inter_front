from PyQt6 import QtWidgets
from front.login_windows import UiMainWindow
from back.login_windows_back import UiAutoWindowBack
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui_back = UiAutoWindowBack()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
