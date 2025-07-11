
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from database import Database
from casino import Ui_MainWindow
from loginn_logic import Login


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.register_user)
        self.pushButton_2.clicked.connect(self.login_pg)

    def login_pg(self):
        self.login_window = Login(parent=self)
        self.login_window.show()
        self.close()

    def clear_fields(self):
        self.lineEdit_3.clear()
        self.lineEdit_2.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit.clear()

    def register_user(self):
        if int(self.lineEdit_4.text()) >= 21 and self.lineEdit_5.text() == self.lineEdit_6.text():
            self.db.Insert_User(self.lineEdit.text(), self.lineEdit_2.text(), float(self.lineEdit_3.text()),
                                int(self.lineEdit_4.text()), self.lineEdit_5.text())
            self.clear_fields()
            self.lineEdit_7.setText("თქვენ წარმატებით დარეგისტრირდით")
        elif int(self.lineEdit_4.text()) < 21:
            self.lineEdit_7.setText("თქვენი ასაკი ნაკლებია 21-ზე")
            self.lineEdit_4.clear()
        elif self.lineEdit_5.text() != self.lineEdit_6.text():
            self.lineEdit_7.setText("პაროლები არ ემთხვევა")
            self.lineEdit_5.clear()
            self.lineEdit_6.clear()



if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())






