# customer.py
import tkinter as tk
from tkinter import messagebox
import csv
from bank import Bank

class CustomerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ATM - Customer View")

        self.bank = Bank()
        self.accounts = self.bank.load_accounts()

        self.account_number_label = tk.Label(master, text="Account Number:")
        self.account_number_label.grid(row=0, column=0)
        self.account_number_entry = tk.Entry(master)
        self.account_number_entry.grid(row=0, column=1)

        self.balance_label = tk.Label(master, text="Balance:")
        self.balance_label.grid(row=1, column=0)
        self.balance_value = tk.StringVar()
        self.balance_entry = tk.Entry(master, textvariable=self.balance_value, state="readonly")
        self.balance_entry.grid(row=1, column=1)

        self.deposit_label = tk.Label(master, text="Deposit Amount:")
        self.deposit_label.grid(row=2, column=0)
        self.deposit_entry = tk.Entry(master)
        self.deposit_entry.grid(row=2, column=1)

        self.withdraw_label = tk.Label(master, text="Withdraw Amount:")
        self.withdraw_label.grid(row=3, column=0)
        self.withdraw_entry = tk.Entry(master)
        self.withdraw_entry.grid(row=3, column=1)

        self.transactions_label = tk.Label(master, text="Transactions:")
        self.transactions_label.grid(row=4, column=0, columnspan=2)
        self.transactions_text = tk.Text(master, height=10, width=30)
        self.transactions_text.grid(row=5, column=0, columnspan=2)

        self.view_balance_button = tk.Button(master, text="View Balance", command=self.view_balance)
        self.view_balance_button.grid(row=6, column=0)
        self.deposit_button = tk.Button(master, text="Deposit", command=self.deposit)
        self.deposit_button.grid(row=6, column=1)
        self.withdraw_button = tk.Button(master, text="Withdraw", command=self.withdraw)
        self.withdraw_button.grid(row=7, column=0)
        self.view_transactions_button = tk.Button(master, text="View Transactions", command=self.view_transactions)
        self.view_transactions_button.grid(row=7, column=1)

    def view_balance(self):
        account_number = self.account_number_entry.get()
        for account in self.accounts:
            if account["Account Number"] == account_number:
                self.balance_value.set(account["Balance"])
                return
        messagebox.showerror("Error", "Account not found.")

    def deposit(self):
        account_number = self.account_number_entry.get()
        try:
            amount = float(self.deposit_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            return
        for account in self.accounts:
            if account["Account Number"] == account_number:
                account["Balance"] += amount
                if isinstance(account["Transactions"], str):
                    account["Transactions"] = account["Transactions"].split(';') if account["Transactions"] else []
                account["Transactions"].append(f"Deposit: {amount}")
                self.bank.save_accounts(self.accounts)
                self.bank.add_transaction(account_number, f"Deposit: {amount}")
                self.view_balance()
                self.view_transactions()
                messagebox.showinfo("Deposit", "Deposit successful.")
                return
        messagebox.showerror("Error", "Account not found.")

    def withdraw(self):
        account_number = self.account_number_entry.get()
        try:
            amount = float(self.withdraw_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            return
        for account in self.accounts:
            if account["Account Number"] == account_number and account["Balance"] >= amount:
                account["Balance"] -= amount
                if isinstance(account["Transactions"], str):
                    account["Transactions"] = account["Transactions"].split(';') if account["Transactions"] else []
                account["Transactions"].append(f"Withdraw: {amount}")
                self.bank.save_accounts(self.accounts)
                self.bank.add_transaction(account_number, f"Withdraw: {amount}")
                self.view_balance()
                self.view_transactions()
                messagebox.showinfo("Withdraw", "Withdrawal successful.")
                return
            else:
                messagebox.showerror("Error", "Insufficient balance.")
                return
        messagebox.showerror("Error", "Account not found.")

    def view_transactions(self):
        account_number = self.account_number_entry.get()
        transactions = []
        with open(self.bank.transactions_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == account_number:
                    transactions.append(row[1])
        self.transactions_text.delete(1.0, tk.END)
        for transaction in transactions:
            self.transactions_text.insert(tk.END, transaction + "\n")

def main():
    root = tk.Tk()
    app = CustomerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
