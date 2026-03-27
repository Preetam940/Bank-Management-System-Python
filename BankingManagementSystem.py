import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import hashlib
import json

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_screen():
    login = tk.Tk()
    login.title("Login")
    login.geometry("300x200")

    tk.Label(login, text="Account Number").pack()
    acc_entry = tk.Entry(login)
    acc_entry.pack()

    tk.Label(login, text="Password").pack()
    pass_entry = tk.Entry(login, show="*")
    pass_entry.pack()

    def check_login():
        try:
            acc_no = int(acc_entry.get())
        except:
            messagebox.showerror("Error", "Invalid Account Number")
            return

        password = pass_entry.get()

        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except:
            messagebox.showerror("Error", "No accounts Found")
            return

        for user in data:
            if user["Account_Number"] == acc_no and user["Password"] == hash_password(password):
                messagebox.showinfo("Success", "Login Successful")
                login.destroy()

                root = tk.Tk()
                app = BankSystem(root, user)
                root.mainloop()
                return

        messagebox.showerror("Error", "Invalid Account Number or Password")

    def open_create_account():
        app = BankSystem(login, None)
        app.create_account()

    tk.Button(login, text="Login", command=check_login).pack(pady=5)
    tk.Button(login, text="Create Account", command=open_create_account).pack()

    login.mainloop()


class BankSystem:
    def __init__(self, root, user=None):
        self.root = root
        self.user = user
        self.root.title("Bank Management System")
        self.root.geometry("500x300")
        self.__file = "data.json"

        if self.user:
            tk.Label(root, text=f"Welcome, {self.user['FirstName']} {self.user['LastName']}",
                     font=("Arial", 14), fg="green").grid(row=0, column=0, pady=10, columnspan=3)

            tk.Button(root, text="Deposit", width=15, command=self.deposit).grid(row=1, column=0, padx=10, pady=20)
            tk.Button(root, text="Withdraw", width=15, command=self.withdraw).grid(row=1, column=1, padx=10)
            tk.Button(root, text="Check Balance", width=15, command=self.check_balance).grid(row=1, column=2, padx=10)
            tk.Button(root, text="Logout", width=15, command=self.logout).grid(row=2, column=1, pady=20)

    def __load_data(self):
        try:
            with open(self.__file, "r") as file:
                return json.load(file)
        except:
            return []

    def __save_data(self, data):
        with open(self.__file, "w") as file:
            json.dump(data, file, indent=4)

    def __generate_account_number(self):
        data = self.__load_data()
        if len(data) == 0:
            return 1001
        else:
            return data[-1]["Account_Number"] + 1

    def create_account(self):
        window = tk.Toplevel(self.root)
        window.title("Create Account")
        window.geometry("300x250")

        tk.Label(window, text="First Name").grid(row=0, column=0)
        e1 = tk.Entry(window)
        e1.grid(row=0, column=1)

        tk.Label(window, text="Last Name").grid(row=1, column=0)
        e2 = tk.Entry(window)
        e2.grid(row=1, column=1)

        tk.Label(window, text="Email").grid(row=2, column=0)
        e3 = tk.Entry(window)
        e3.grid(row=2, column=1)

        tk.Label(window, text="Phone").grid(row=3, column=0)
        e4 = tk.Entry(window)
        e4.grid(row=3, column=1)

        tk.Label(window, text="Set Password").grid(row=4, column=0)
        e5 = tk.Entry(window, show="*")
        e5.grid(row=4, column=1)

        def submit():
            acc_no = self.__generate_account_number()

            new_user = {
                "Account_Number": acc_no,
                "Password": hash_password(e5.get()),
                "FirstName": e1.get(),
                "LastName": e2.get(),
                "Email": e3.get(),
                "Phone": e4.get(),
                "Balance": 0
            }

            data = self.__load_data()
            data.append(new_user)
            self.__save_data(data)

            messagebox.showinfo("Success", f"Account Created!\nAccount Number: {acc_no}")
            window.destroy()

        tk.Button(window, text="Create", command=submit).grid(row=5, column=1, pady=10)

    def deposit(self):
        amount = int(tk.simpledialog.askstring("Deposit", "Enter Amount"))
        data = self.__load_data()

        for user in data:
            if user["Account_Number"] == self.user["Account_Number"]:
                user["Balance"] += amount
                self.user["Balance"] = user["Balance"]

        self.__save_data(data)
        messagebox.showinfo("Success", "Amount Deposited")

    def withdraw(self):
        amount = int(tk.simpledialog.askstring("Withdraw", "Enter Amount"))
        data = self.__load_data()

        for user in data:
            if user["Account_Number"] == self.user["Account_Number"]:
                if user["Balance"] >= amount:
                    user["Balance"] -= amount
                    self.user["Balance"] = user["Balance"]
                    messagebox.showinfo("Success", "Amount Withdrawn")
                else:
                    messagebox.showerror("Error", "Insufficient Balance")

        self.__save_data(data)

    def check_balance(self):
        messagebox.showinfo("Balance", f"Current Balance: ₹ {self.user['Balance']}")

    def logout(self):
        self.root.destroy()
        login_screen()


login_screen()