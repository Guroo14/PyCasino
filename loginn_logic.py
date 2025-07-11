import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from database import Database
from login import Ui_OtherWindow1



class Login(QMainWindow, Ui_OtherWindow1):
    def __init__(self,parent=None):
      super().__init__()
      self.setupUi(self)
      self.database = Database()
      self.parent_window = parent
      self.pushButton_2.clicked.connect(self.home_page)
      self.pushButton_4.clicked.connect(self.to_bj)
      self.pushButton_5.clicked.connect(self.to_bacc)
      self.pushButton_6.clicked.connect(self.login_User)

    def home_page(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()
    def login_User(self):
        nickname = self.lineEdit_2.text()
        if self.database.nickname_exists(nickname):
            self.lineEdit_2.clear()
            self.lineEdit_6.setText("თქვენ წარმატებით გაიარეთ ავტორიზაცია")
        else:
            self.lineEdit_6.setText("თქვენ ვერ გაიარეთ ავტორიზაცია")


    def to_bj(self):
        from Blackjack_logic import Blackjack
        self.blackjack_window = Blackjack()
        self.blackjack_window.show()
        self.close()
    def to_bacc(self):
        from baccarat_logic import Baccarat
        self.bacc_window = Baccarat()
        self.bacc_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())
