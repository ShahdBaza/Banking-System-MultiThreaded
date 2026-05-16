import customtkinter as ctk
import socket
import threading
from tkinter import messagebox

class BankGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pro Banking System")
        self.geometry("400x550")
        
        self.sock = socket.socket()
        self.sock.connect(('127.0.0.1', 12221))

        ctk.CTkLabel(self, text="Bank Services", font=("Roboto", 22, "bold")).pack(pady=20)

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Your Name", width=280, height=45)
        self.name_entry.pack(pady=10)

        self.acc_entry = ctk.CTkEntry(self, placeholder_text="Account Number (101, 102, 103)", width=280, height=45)
        self.acc_entry.pack(pady=10)
        
        self.amt_entry = ctk.CTkEntry(self, placeholder_text="Amount ($)", width=280, height=45)
        self.amt_entry.pack(pady=10)

        ctk.CTkButton(self, text="Check Balance", fg_color="#34495e", command=lambda: self.send_action("check")).pack(pady=10)
        ctk.CTkButton(self, text="Deposit Money", fg_color="#27ae60", command=lambda: self.send_action("deposit")).pack(pady=10)
        ctk.CTkButton(self, text="Withdraw Money", fg_color="#c0392b", command=lambda: self.send_action("withdraw")).pack(pady=10)

        threading.Thread(target=self.receive_notifications, daemon=True).start()

    def send_action(self, action):
        name = self.name_entry.get()
        acc = self.acc_entry.get()
        amt = self.amt_entry.get() or "0"
        if not name or not acc:
            messagebox.showwarning("Input Error", "Please enter Name and Account ID")
            return
        self.sock.send(f"{action},{acc},{amt},{name}".encode())

    def receive_notifications(self):
        while True:
            try:
                data = self.sock.recv(1024).decode()
                if data.startswith("RESULT:"):
                    msg = data.replace("RESULT:", "")
                    self.after(0, lambda m=msg: messagebox.showinfo("Bank Response", m))
                elif data.startswith("UPDATE:"):
                    msg = data.replace("UPDATE:", "")
                    self.after(0, lambda m=msg: messagebox.showinfo("Broadcast Notification", m))
            except:
                break

if __name__ == "__main__":
    BankGUI().mainloop()