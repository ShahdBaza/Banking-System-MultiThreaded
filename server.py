import socket 
import threading

class User:
    def __init__(self, name):
        self.name = name 
class Account:
    def __init__(self, acc_id, balance, owner):
        self.acc_id = acc_id 
        self.balance = balance 
        self.owner = owner 
        self.lock = threading.Lock() 
        self.observers = []

    def attach(self, conn):
        if conn not in self.observers:
            self.observers.append(conn) 
    def notify(self, action_type, amount, sender_conn=None):
        message = f"UPDATE:Account {self.acc_id} ({self.owner.name}) {action_type}ed ${amount}. Balance: ${self.balance}"
        for conn in self.observers:
            if conn == sender_conn:
                continue
            try:
                conn.send(message.encode())
            except: 
                self.observers.remove(conn)

# (Command Pattern)and OCP
class Transaction: 
    def __init__(self, account, amount):
        self.account = account
        self.amount = amount

class Deposit(Transaction):
    def execute(self,sender_conn):
        with self.account.lock: 
            self.account.balance += self.amount
            self.account.notify("Deposit", self.amount ,sender_conn) # إرسال تنبيه للمراقبين
            return f"RESULT:Hello {self.account.owner.name}, Deposited ${self.amount}. New Balance: ${self.account.balance}"

class Withdraw(Transaction):
    def execute(self,sender_conn):
        with self.account.lock:
            if self.account.balance >= self.amount:
                self.account.balance -= self.amount
                self.account.notify("Withdraw", self.amount,sender_conn)
                return f"RESULT:Hello {self.account.owner.name}, Withdrew ${self.amount}. New Balance: ${self.account.balance}"
            return "RESULT:Error: Insufficient Funds!"

users = {"Shahd": User("Shahd"), "Ahmed": User("Ahmed"), "Sara": User("Sara")}
accounts_db = {
    "101": Account("101", 1000.0, users["Shahd"]),
    "102": Account("102", 500.0, users["Ahmed"]),
    "103": Account("103", 2500.0, users["Sara"])
}

def handle_client(conn, addr):
    for acc in accounts_db.values(): 
        acc.attach(conn)
    while True:
        try:
            data = conn.recv(1024).decode() 
            if not data: 
                break
            action, acc_id, amt, name = data.split(",")
            acc = accounts_db.get(acc_id)
            
            if acc:
                if action == "deposit": res = Deposit(acc, float(amt)).execute(conn)
                elif action == "withdraw": res = Withdraw(acc, float(amt)).execute(conn)
                elif action == "check": res = f"RESULT:Account {acc_id} ({acc.owner.name}) Balance: ${acc.balance}"
                conn.send(res.encode())
            else:
                conn.send("RESULT:Error: Account Number Not Found!".encode())
        except:
            break
    conn.close()

s = socket.socket()
s.bind(('127.0.0.1', 12221))
s.listen(5)
print("Server is active now...")
while True:
    c, a = s.accept()
    threading.Thread(target=handle_client, args=(c, a)).start()