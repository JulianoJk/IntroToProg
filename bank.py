# bank.py
import csv
import os

class Bank:
    def __init__(self):
        self.accounts_file = "accounts.csv"
        self.transactions_file = "transactions.csv"
        self.initialize_accounts_file()
        self.initialize_transactions_file()

    def initialize_accounts_file(self):
        if not os.path.isfile(self.accounts_file):
            with open(self.accounts_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Account Number", "Balance", "Transactions"])
            self.open_account("100", 1000)  # Create a default account for testing

    def initialize_transactions_file(self):
        if not os.path.isfile(self.transactions_file):
            with open(self.transactions_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Account Number", "Transaction"])

    def load_accounts(self):
        accounts = []
        with open(self.accounts_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["Balance"] = float(row["Balance"])
                transactions_str = row.get("Transactions", "")
                row["Transactions"] = transactions_str.split(";") if transactions_str else []
                accounts.append(row)
        return accounts

    def save_accounts(self, accounts):
        with open(self.accounts_file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Account Number", "Balance", "Transactions"])
            writer.writeheader()
            for account in accounts:
                account["Transactions"] = ";".join(account["Transactions"])
                writer.writerow(account)

    def open_account(self, account_number, balance):
        accounts = self.load_accounts()
        accounts.append({"Account Number": account_number, "Balance": balance, "Transactions": []})
        self.save_accounts(accounts)

    def suspend_account(self, account_number):
        accounts = self.load_accounts()
        accounts = [account for account in accounts if account["Account Number"] != account_number]
        self.save_accounts(accounts)

    def add_transaction(self, account_number, transaction):
        with open(self.transactions_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([account_number, transaction])
