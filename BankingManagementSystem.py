import tkinter as tk
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

    tk.Label(login, text= "Password").pack()
    pass_entry = tk.Entry(login,show="*")
    pass_entry.pack()

    def check_login():
        try:
            acc_no = int(acc_entry.get())
        except:
            messagebox.showerror("Error","Invalid Account Number")
            return

        password = pass_entry.get()

        try:
            with open("data.json","r") as file:
                data = json.load(file)
        except:
            messagebox.showerror("Error","No accounts Found")
            return

        for user in data:
            if user["Account_Number"] == acc_no and user["Password"] == hash_password(password):
                messagebox.showinfo("Success", "Login Successful")
                login.destroy()

                root = tk.Tk()
                app = BankSystem(root,user)
                root.mainloop()
                return
        messagebox.showerror("Error","Invalid Account Number or Password")

    tk.Button(login,text="Login",command=check_login).pack(pady=5)
    tk.Button(login,text="Create Account", command=lambda: BankSystem(tk.Toplevel(login))).pack()

    login.mainloop()

class BankSystem:
    def __init__(self, root,user):
        self.root = root
        self.user = user
        self.root.title("Bank Management System")
        self.root.geometry("500x300")
        tk.Label(root, text=f"Welcome, {self.user['FirstName']} {self.user['LastName']}",
                 font=("Arial", 14), fg="green").grid(row=0, column=0, pady=10,columnspan=3)


        self.__file = "data.json"

        tk.Button(root, text="Deposit", width=15, command=self.deposit).grid(row=1, column=0,padx=10,pady=20)
        tk.Button(root, text="Withdraw", width=15, command=self.withdraw).grid(row=1, column=1,padx=10)
        tk.Button(root, text="Check Balance", width=15, command=self.check_balance).grid(row=1, column=2,padx=10)
        tk.Button(root, text="Logout", width=15, command=self.logout).grid(row=2, column=1, pady=20)


    def __load_data(self):
        try:
            with open(self.__file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            with open(self.__file,"w") as file:
                json.dump([],file)
            return []
        except json.JSONDecodeError:
            with open(self.__file,"w") as file:
                json.dump([],file)
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

    def __find_account(self, acc_no):
        data = self.__load_data()
        for user in data:
            if user["Account_Number"] == acc_no:
                return data, user
        return data, None


    def create_account(self):
        window = tk.Toplevel(self.root)
        window.title("Create Account")
        window.geometry("300x250")

        tk.Label(window, text="First Name").grid(row=0, column=0)
        self.e1 = tk.Entry(window)
        self.e1.grid(row=0, column=1)

        tk.Label(window, text="Last Name").grid(row=1, column=0)
        self.e2 = tk.Entry(window)
        self.e2.grid(row=1, column=1)

        tk.Label(window, text="Email").grid(row=2, column=0)
        self.e3 = tk.Entry(window)
        self.e3.grid(row=2, column=1)

        tk.Label(window, text="Phone").grid(row=3, column=0)
        self.e4 = tk.Entry(window)
        self.e4.grid(row=3, column=1)

        tk.Label(window, text="Set Password").grid(row=4,column=0)
        self.e5 = tk.Entry(window,show="*")
        self.e5.grid(row=4,column=1)
        tk.Button(window, text="Create", command=self.__submit_account).grid(row=5, column=1, pady=10)

    def __submit_account(self):
        acc_no = self.__generate_account_number()

        new_user = {
            "Account_Number": acc_no,
            "Password":hash_password(self.e5.get()),
            "FirstName": self.e1.get(),
            "LastName": self.e2.get(),
            "Email": self.e3.get(),
            "Phone": self.e4.get(),
            "Balance": 0
        }

        data = self.__load_data()
        data.append(new_user)
        self.__save_data(data)

        messagebox.showinfo("Success", f"Account Created!\nAccount Number: {acc_no}")

        self.e1.delete(0, tk.END)
        self.e2.delete(0, tk.END)
        self.e3.delete(0, tk.END)
        self.e4.delete(0, tk.END)
        self.e5.delete(0,tk.END)

    def deposit(self):
        window = tk.Toplevel(self.root)
        window.title("Deposit Money")
        window.geometry("300x150")

        tk.Label(window, text="Amount").grid(row=0, column=0)
        amt_entry = tk.Entry(window)
        amt_entry.grid(row=0, column=1)

        def deposit_money():
            try:
                amount = int(amt_entry.get())
            except:
                messagebox.showerror("Error", "Invalid Amount")
                return

            data = self.__load_data()

            for user in data:
                if user["Account_Number"] == self.user["Account_Number"]:
                    user["Balance"] += amount
                    self.user["Balance"] = user["Balance"]
                    break

            self.__save_data(data)
            messagebox.showinfo("Success", "Amount Deposited Successfully")
            window.destroy()

        tk.Button(window, text="Deposit", command=deposit_money).grid(row=1, column=1, pady=10)

    def withdraw(self):
        window = tk.Toplevel(self.root)
        window.title("Withdraw Money")
        window.geometry("300x150")

        tk.Label(window, text="Amount").grid(row=0, column=0)
        amt_entry = tk.Entry(window)
        amt_entry.grid(row=0, column=1)

        def withdraw_money():
            try:
                amount = int(amt_entry.get())
            except:
                messagebox.showerror("Error", "Invalid Amount")
                return

            data = self.__load_data()

            for user in data:
                if user["Account_Number"] == self.user["Account_Number"]:
                    if user["Balance"] >= amount:
                        user["Balance"] -= amount
                        self.user["Balance"] = user["Balance"]
                        self.__save_data(data)
                        messagebox.showinfo("Success", "Amount Withdrawn Successfully")
                        window.destroy()
                    else:
                        messagebox.showerror("Error", "Insufficient Balance")
                    return

        tk.Button(window, text="Withdraw", command=withdraw_money).grid(row=1, column=1, pady=10)

    def logout(self):
        self.root.destroy()
        login_screen()

    def check_balance(self):
        window = tk.Toplevel(self.root)
        window.title("Check Balance")
        window.geometry("300x180")

        tk.Label(window, text="Account Details", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(window, text=f"Name: {self.user['FirstName']} {self.user['LastName']}").pack(pady=5)
        tk.Label(window, text=f"Account Number: {self.user['Account_Number']}").pack(pady=5)
        tk.Label(window, text=f"Current Balance: ₹ {self.user['Balance']}").pack(pady=5)



login_screen()