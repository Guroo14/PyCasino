
# import sys
# from PyQt5.QtWidgets import QApplication
# from database import Database
# from UI_main import MainApp
# from registration_tab import MyApp
#
# app = QApplication(sys.argv)
# db = Database()
# window = MainApp(db)
# window.show()
# sys.exit(app.exec_())


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from casino_lobby import Ui_MainWindow

# from login_window import LoginWindow
# from registration_tab import registration_window


# from blackjack_window import BlackjackWindow
# from baccarat_window import BaccaratWindow



# app = QApplication(sys.argv)
# window = registration_window()
# window.show()
# sys.exit(app.exec_())
# class MainApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#
#         # ღილაკებზე დაჭერისას ვაკავშირებთ ფანჯრების გახსნას
#         self.ui.pushButton_2.clicked.connect(self.open_login)  # Login
#         self.ui.pushButton_6.clicked.connect(self.open_registration)  # Registration
#         self.ui.pushButton_4.clicked.connect(self.open_blackjack)  # Blackjack
#         self.ui.pushButton_5.clicked.connect(self.open_baccarat)  # Baccarat
#
#     # def open_login(self):
#     #     self.login_window = LoginWindow()
#     #     self.login_window.show()
#
#     def open_registration(self):
#         self.registration_window = MyApp()
#         self.registration_window.show()
#
#     # def open_blackjack(self):
#     #     self.blackjack_window = BlackjackWindow()
#     #     self.blackjack_window.show()
#
#     # def open_baccarat(self):
#     #     self.baccarat_window = BaccaratWindow()
#     #     self.baccarat_window.show()
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainApp()
#     window.show()
#     sys.exit(app.exec_())


# import sys
# from PyQt5.QtWidgets import QApplication
# from database import Database
# # from UI_main import MainInterface
#
# app = QApplication(sys.argv)
# db = Database()
# window = MainInterface(db)
# window.show()
# sys.exit(app.exec_())

