
# Your Name:kinga wangchuk
# Your Section:ME
# Your Student ID Number:02230265
################################
# REFERENCES
#https://youtu.be/i6xMBig-pP4?list=PLzMcBGfZo4-lp3jAExUCewBfMx3UZFkh5
#https://youtu.be/2-DNswzCkqk?list=PLzMcBGfZo4-lp3jAExUCewBfMx3UZFkh5
#https://youtu.be/UdsNBIzsmlI?list=PLzMcBGfZo4-lp3jAExUCewBfMx3UZFkh5
#####################################


import os
import random
import hashlib

class Account:
    def __init__(self, account_number, password, account_type, balance=0):
        self.account_number = account_number
        self.password = self.hash_password(password)
        self.account_type = account_type
        self.balance = balance

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.hash_password(password) == self.password

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False
    

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def to_string(self):
        return f"{self.account_number},{self.password},{self.account_type},{self.balance}\n"

    @staticmethod
    def from_string(data):
        account_number, password, account_type, balance = data.split(',')
        return Account(account_number, password, account_type, float(balance))

class BusinessAccount(Account):
    def __init__(self, account_number, password, balance=0):
        super().__init__(account_number, password, 'Business', balance)

class PersonalAccount(Account):
    def __init__(self, account_number, password, balance=0):
        super().__init__(account_number, password, 'Personal', balance)

class Bank:
    def __init__(self, filename="accounts.txt"):
        self.accounts = {}
        self.filename = filename
        self.load_accounts()

    def load_accounts(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    account = Account.from_string(line.strip())
                    self.accounts[account.account_number] = account

    def save_accounts(self):
        with open(self.filename, 'w') as file:
            for account in self.accounts.values():
                file.write(account.to_string())

    def create_account(self, account_type):
        account_number = str(random.randint(100000, 999999))
        password = str(random.randint(1000, 9999))
        if account_type == "Business":
            account = BusinessAccount(account_number, password)
        elif account_type == "Personal":
            account = PersonalAccount(account_number, password)
        else:
            return None

        self.accounts[account.account_number] = account
        self.save_accounts()
        return account_number, password

    def authenticate(self, account_number, password):
        account = self.accounts.get(account_number)
        if account and account.check_password(password):
            return account
        return None

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            self.save_accounts()
            return True
        return False

    def transfer_money(self, from_account, to_account_number, amount):
        if to_account_number not in self.accounts:
            return False, "Receiving account does not exist."
        if from_account.balance < amount:
            return False, "Insufficient funds."
        to_account = self.accounts[to_account_number]
        from_account.withdraw(amount)
        to_account.deposit(amount)
        self.save_accounts()
        return True, "Transfer successful."

def main():
    bank = Bank()
    print("Welcome to the Bank Application")

    while True:
        print("\n1. Open Account")
        print("\n2. Login")
        print("\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            account_type = input("Enter account type (Business/Personal): ")
            account_number, password = bank.create_account(account_type)
            if account_number:
                print(f"Account created successfully! Your account number is {account_number} and your password is {password}")
            else:
                print("Invalid account type.")
        
        elif choice == "2":
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            account = bank.authenticate(account_number, password)
            if account:
                print(f"Login successful! Welcome, {account.account_type} account holder.")
                while True:
                    print("\n1. Check Balance")
                    print("\n2. Deposit Money")
                    print("\n3. Withdraw Money")
                    print("\n4. Transfer Money")
                    print("\n5. Delete Account")
                    print("\n6. Logout")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == "1":
                        print(f"Your balance is: {account.balance}")
                    elif sub_choice == "2":
                        amount = float(input("Enter amount to deposit: "))
                        if account.deposit(amount):
                            bank.save_accounts()
                            print(f"Deposited successfully. New balance: {account.balance}")
                        else:
                            print("Invalid amount.")
                    elif sub_choice == "3":
                        amount = float(input("Enter amount to withdraw: "))
                        if account.withdraw(amount):
                            bank.save_accounts()
                            print(f"Withdrawn successfully. New balance: {account.balance}")
                        else:
                            print("Invalid amount or insufficient balance.")
                    elif sub_choice == "4":
                        to_account_number = input("Enter the account number to transfer to: ")
                        amount = float(input("Enter the amount to transfer: "))
                        _, message = bank.transfer_money(account, to_account_number, amount)
                        print(message)
                    elif sub_choice == "5":
                        if bank.delete_account(account.account_number):
                            print("Account deleted successfully.")
                            break
                        else:
                            print("Error in deleting account.")
                    elif sub_choice == "6":
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Authentication failed. Please check your account number and password.")
        
        elif choice == "3":
            print("Thank you for using the Bank Application. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
