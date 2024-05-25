
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

# Base class for UserAccount
class UserAccount:
    def __init__(self, id_number, secret, type_of_account, funds=0, is_encrypted=False):
        self.id_number = id_number
        self.secret = secret if is_encrypted else self.encrypt_secret(secret)  # Encrypt secret only if not already encrypted
        self.type_of_account = type_of_account
        self.funds = funds

    # Method to encrypt secret using SHA-256
    def encrypt_secret(self, secret):
        return hashlib.sha256(secret.encode()).hexdigest()

    # Method to verify if the provided secret matches the stored encrypted secret
    def verify_secret(self, secret):
        return self.encrypt_secret(secret) == self.secret

    # Method to add funds to the account
    def add_funds(self, cash):
        if cash > 0:
            self.funds += cash
            return True
        return False

    # Method to remove funds from the account
    def remove_funds(self, cash):
        if 0 < cash <= self.funds:
            self.funds -= cash
            return True
        return False

    # Method to convert account details to string for storage
    def stringify(self):
        return f"{self.id_number},{self.secret},{self.type_of_account},{self.funds}\n"

    # Static method to parse string data and create a UserAccount object
    @staticmethod
    def parse(data):
        id_number, secret, type_of_account, funds = data.split(',')
        return UserAccount(id_number, secret, type_of_account, float(funds), is_encrypted=True)

# Derived class for CorporateAccount
class CorporateAccount(UserAccount):
    def __init__(self, id_number, secret, funds=0):
        super().__init__(id_number, secret, 'Corporate', funds)

# Derived class for IndividualAccount
class IndividualAccount(UserAccount):
    def __init__(self, id_number, secret, funds=0):
        super().__init__(id_number, secret, 'Individual', funds)

# Class to manage all user accounts within the financial institution
class FinancialInstitution:
    def __init__(self, file_path="user_accounts.txt"):
        self.user_accounts = {}
        self.file_path = file_path
        self.retrieve_accounts()  # Load existing accounts from file

    # Method to retrieve accounts from file
    def retrieve_accounts(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                for line in file:
                    user_account = UserAccount.parse(line.strip())
                    self.user_accounts[user_account.id_number] = user_account

    # Method to record all accounts to file
    def record_accounts(self):
        with open(self.file_path, 'w') as file:
            for user_account in self.user_accounts.values():
                file.write(user_account.stringify())

    # Method to register a new account
    def register_account(self, type_of_account):
        id_number = str(random.randint(100000, 999999))  # Generate random ID
        secret = str(random.randint(1000, 9999))  # Generate random secret
        if type_of_account == "Corporate":
            user_account = CorporateAccount(id_number, secret)
        elif type_of_account == "Individual":
            user_account = IndividualAccount(id_number, secret)
        else:
            return None

        self.user_accounts[user_account.id_number] = user_account
        self.record_accounts()
        return id_number, secret  # Return the plaintext secret

    # Method to validate user credentials
    def validate_user(self, id_number, secret):
        user_account = self.user_accounts.get(id_number)
        if user_account and user_account.verify_secret(secret):
            return user_account
        return None

    # Method to remove an account
    def remove_account(self, id_number):
        if id_number in self.user_accounts:
            del self.user_accounts[id_number]
            self.record_accounts()
            return True
        return False

    # Method to execute fund transfer between accounts
    def execute_transfer(self, source_account, destination_id_number, cash):
        if destination_id_number not in self.user_accounts:
            return False, "Destination account not found."
        if source_account.funds < cash:
            return False, "Not enough funds."
        destination_account = self.user_accounts[destination_id_number]
        if source_account.remove_funds(cash):
            destination_account.add_funds(cash)
            self.record_accounts()
            return True, "Transfer completed."
        return False, "Transfer failed."

# Main function to run the financial application
def run():
    institution = FinancialInstitution()
    print("Welcome to the Financial Application")

    while True:
        menu_options = {
            1: "Create Account",
            2: "Sign In",
            3: "Exit"
        }
        print("Please select an option:")
        for number, option in menu_options.items():
            print(f"\n{number}. {option}")

        user_choice = input("Select an option: ")

        if user_choice == "1":
            type_of_account = input("Choose account type (Corporate/Individual): ")
            account_details = institution.register_account(type_of_account)
            if account_details:
                id_number, secret = account_details
                print(f"Account successfully created! Your ID is {id_number} and your secret is {secret}")
            else:
                print("Invalid account type.")
        
        elif user_choice == "2":
            id_number = input("Enter ID number: ")
            secret = input("Enter secret: ")
            user_account = institution.validate_user(id_number, secret)
            if user_account:
                print(f"Sign in successful! Welcome, {user_account.type_of_account} account holder.")
                while True:
                    options = [
                        "View Funds",
                        "Add Funds",
                        "Withdraw Funds",
                        "Make Transfer",
                        "Close Account",
                        "Sign Out"
                    ]
                    print("Please choose an option:")
                    for index, option in enumerate(options, start=1):
                        print(f"{index}. {option}")

                    action_choice = input("Select an option: ")
                    if action_choice == "1":
                        print(f"Current funds: {user_account.funds}")
                    elif action_choice == "2":
                        cash = float(input("Amount to add: "))
                        if user_account.add_funds(cash):
                            institution.record_accounts()
                            print(f"Added successfully. Available funds: {user_account.funds}")
                        else:
                            print("Invalid amount.")
                    elif action_choice == "3":
                        cash = float(input("Amount to withdraw: "))
                        if user_account.remove_funds(cash):
                            institution.record_accounts()
                            print(f"Withdrawn successfully. Available funds: {user_account.funds}")
                        else:
                            print("Invalid amount or not enough funds.")
                    elif action_choice == "4":
                        destination_id_number = input("Enter destination ID number: ")
                        cash = float(input("Amount to transfer: "))
                        _, transfer_message = institution.execute_transfer(user_account, destination_id_number, cash)
                        print(transfer_message)
                    elif action_choice == "5":
                        if institution.remove_account(user_account.id_number):
                            print("Account closed successfully.")
                            break
                        else:
                            print("Error closing account.")
                    elif action_choice == "6":
                        print("Signed out successfully.")
                        break
                    else:
                        print("Invalid option. Please try again.")
            else:
                print("Sign in failed. Check your ID and secret.")
        
        elif user_choice == "3":
            print("Thank you for using the Financial Application. Farewell!")
            break

        else:
            print("Invalid option. Please try again.")

# Run the application if this script is executed
if __name__ == "__main__":
    run()

