import sqlite3

class Database:
 def __init__(self, db_name = "test_users.db"):
     self.conn = sqlite3.connect(db_name)
     self.c = self.conn.cursor()
     self.db_name = db_name
     self.CreateTable()

 def CreateTable(self):
     self.c.execute("""
                 CREATE TABLE IF NOT EXISTS test_users (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name VARCHAR(255) NOT NULL,
                     nickname VARCHAR(255) NOT NULL UNIQUE,
                     balance FLOAT NOT NULL,
                     age INTEGER NOT NULL,
                     password VARCHAR(255) NOT NULL
                     )
             """)
     self.conn.commit()


#USERS CRUD
 def fetch_users(self):
     self.c.execute("SELECT * FROM test_users")
     return self.c.fetchall()

 def Insert_User(self, name, nickname, balance, age, password):
     self.c.execute(
             "INSERT INTO test_users(name, nickname, balance, age, password) VALUES(?,?,?,?,?)",
             (name, nickname, balance, age, password)
         )
     self.conn.commit()
 def Update_User(self, id, name,  nickname, balance, age, password):
     self.c.execute("UPDATE test_users SET name=?,nickname=?, balance=?, age=?,password=? WHERE id=?",
                            (name,  nickname, balance, age, password))
     self.conn.commit()
 def Delete_User(self,id):
     self.c.execute("DELETE FROM test_users WHERE id=?",(id,))
     self.conn.commit()



 def Avg_age(self):
     self.c.execute("SELECT AVG(age) FROM test_users")
     return self.c.fetchall()[0][0]

 def AVG_balance(self):
     self.c.execute("SELECT AVG(balance) FROM test_users")

 def age_of_usrs_gt25(self,asaki=25):
     self.c.execute("SELECT * FROM test_users WHERE age >= ?", (asaki,)).fetchall()
     return self.c.fetchall()[0][0]

 def nickname_exists(self, nickname):
     self.c.execute("SELECT 1 FROM test_users WHERE nickname = ?", (nickname,))
     return self.c.fetchone() is not None
 def close(self):
     self.conn.close()





