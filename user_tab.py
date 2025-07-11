from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QListWidget

class UserTab(QWidget):
    def __init__(self, db):
        # super().__init__()
        self.db = db
        self.init_ui()
        self.load_users()

    def init_ui(self):
        layout = QVBoxLayout()
        self.user_list = QListWidget()
        layout.addWidget(self.user_list)
        self.user_list.itemClicked.connect(self.load_selected)

        form = QHBoxLayout()
        self.name_input = QLineEdit()
        self.nickname_input = QLineEdit()
        self.age_input = QLineEdit()
        self.balance_input = QLineEdit()
        form.addWidget(QLabel("Username"))
        form.addWidget(self.name_input)
        form.addWidget(QLabel("Nickname"))
        form.addWidget(self.nickname_input)
        form.addWidget(QLabel("Age"))
        form.addWidget(self.age_input)
        form.addWidget(QLabel("Balance"))
        form.addWidget(self.balance_input)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Delete")
        self.avg_age = QLineEdit("Avg Age")
        self.avg_balance = QLineEdit("Avg Balance")
        buttons.addWidget(self.add_btn)
        buttons.addWidget(self.update_btn)
        buttons.addWidget(self.delete_btn)
        buttons.addWidget(self.avg_age_btn)
        buttons.addWidget(self.avg_bal_btn)
        layout.addLayout(buttons)

        self.setLayout(layout)
        self.add_btn.clicked.connect(self.add_user)
        self.update_btn.clicked.connect(self.update_user)
        self.delete_btn.clicked.connect(self.delete_user)
        self.avg_age_btn.clicked.connect(self.avgg_age)
        self.avg_bal_btn.clicked.connect(self.avgg_bal)

    def load_users(self):
        self.user_list.clear()
        for u in self.db.fetch_users():
            self.user_list.addItem(f"{u[0]}: {u[1]} | Balance: {u[2]}")

    def load_selected(self):
        text = self.user_list.currentItem().text()
        uid, rest = text.split(":", 1)
        name, balance = rest.split("|")
        self.name_input.setText(name.strip())
        self.balance_input.setText(balance.replace("Balance:", "").strip())

    def add_user(self):
        self.db.insert_user(self.name_input.text(), float(self.balance_input.text()))
        self.load_users()

    def update_user(self):
        uid = int(self.user_list.currentItem().text().split(":")[0])
        self.db.update_user(uid, self.name_input.text(), float(self.balance_input.text()))
        self.load_users()

    def delete_user(self):
        uid = int(self.user_list.currentItem().text().split(":")[0])
        self.db.delete_user(uid)
        self.load_users()

    def avgg_age(self):
        self.avg_age.setText(float(self.avg_age.text()))
        self.db.AVG_AGE()
        self.load_users()

    def avgg_bal(self):
        self.db.AVG_BAL()
        self.load_users()

