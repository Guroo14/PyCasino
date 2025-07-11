class Person:
    def __init__(self, id,name,lastname, nickname, balance, age, password):
        self.id = id
        self.name = name
        self.lastname = lastname
        self.nickname = nickname
        self.balance = balance
        self.age = age
        self.password = password
    def __str__(self):
        return f"სახელი: {self.name}, გვარი: {self.lastname}, ზედმეტსახელი: {self.nickname}, ბალანსი: {self.balance}, ასაკი: {self.age}, პაროლი: {self.password}"