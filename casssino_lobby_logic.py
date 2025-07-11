import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from casino_lobby import Ui_OtherWindow
from registration_logic import MyApp
from loginn_logic import Login


class MainWind(QMainWindow, Ui_OtherWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_6.clicked.connect(self.open_registration)
        self.pushButton_2.clicked.connect(self.open_login_window)
    def open_registration(self):
        self.registration_window = MyApp()
        self.registration_window.show()
        self.close()
    def open_login_window(self):
        self.login_window = Login(parent=self)
        self.login_window.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWind()
    window.show()
    sys.exit(app.exec_())

