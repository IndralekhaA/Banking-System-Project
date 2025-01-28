from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self, username, password, balance=0 ):
        self.__username = username
        self.__password = password
        self._balance = balance
        self._transactions = []

    @property
    def username(self):
        return self.__username
    
    def authenticate(self, password):
        return self.__password == password
    
    def check_bal(self):
        return self._balance
    
    def add_transaction(self, transaction):
        self._transactions.append(transaction)

    @abstractmethod
    def account_type(self): #to determine every class thier type
        pass

    def display_transactions(self):
        print("\nTransaction History: ")
        if self._transactions:
            for i, transaction in enumerate(self._transactions, 1):
                print(f"{i}. {transaction}")
        else:
            print("\nNo transactions yet!")

class SavingsAccount(Account):
    def account_type(self):
        return "Savings"

    def credit(self, amount):
        if amount <= 0:
            print("Please enter a positive amount.")
        else:
            self._balance += amount
            self.add_transaction(f"Deposited: ${amount}")
            print(f"${amount} credited to your account.")
        self.check_bal()

    def debit(self, amount):
        if amount <= 0:
            print("Please enter a positive amount.")
        elif amount > self._balance:
            print("Insufficient balance.")
        else:
            self._balance -= amount
            self.add_transaction(f"Withdrew: ${amount}")
            print(f"${amount} debited from your account.")
        self.check_bal()


    # def password_change(self, old_password, new_password):
    #     if self.authenticate(old_password):
    #         if len(new_password) != 0:
    #             self.__password = new_password
    #             print("Password Changed successfully!")
    #         else:
    #             print("Invalid password, password should not be empty")
    #     else:
    #         print("Invalid Password!")

class CurrentAccount(Account):
    def account_type(self):
        return "Current"
    
    def credit(self, amount):
        if amount <= 0:
            print("Please enter a positive amount.")
        else:
            self._balance += amount
            self.add_transaction(f"Deposited: ${amount}")
            print(f"${amount} credited to your account.")
        self.check_bal()
        
    def debit(self, amount):
        self.overdraft_limit = 500
        if amount <= 0:
            print("Please enter a positive amount.")
        elif amount > self._balance + self.overdraft_limit:
            print("Exceeds Overdraft limit!")
        else:
            self._balance -= amount
            self.add_transaction(f"Withdrew: ${amount}")
            print(f"${amount} debited from your account.")
        self.check_bal()

class bankingsystem:
    def __init__(self):
        self.accounts = {}
    
    def create_account(self):
        print("\n--- Account Creation ---")
        username = input("Enter a username: ")
        if username in self.accounts:
            print("Username already exists. Please try a different one.")
            return

        password = input("Enter a password: ")
        confirm_password = input("Confirm your password: ")
        if password != confirm_password:
            print("Passwords do not match. Please try again.")
            return

        print("Account Types: 1. Savings  2. Current")
        account_type = input("Choose account type (1/2): ")
        if account_type not in ["1", "2"]:
            print("Invalid account type selected!")
            return
        try:                
            initial_balance = float(input("Enter initial deposit amount: "))
        except:
            print("Enter valid amount in digit (0-9)")
            return None

        if account_type == "1":
            account = SavingsAccount(username, password, initial_balance)
        else:
            account = CurrentAccount(username, password, initial_balance)

        self.accounts[username] = account
        print(f"Account created successfully for {username} with a {account.account_type()} account!")

    def login(self):
        print("\n--- Login ---")
        username = input("Enter your username: ")
        if username not in self.accounts:
            print("Username not found!")
            return None

        password = input("Enter your password: ")
        account = self.accounts[username]

        if account.authenticate(password):
            print("Login successful!")
            return account
        else:
            print("Incorrect password!")
            return None

    def run(self):
        while True:
            print("\n--- Online Banking System ---")
            print("1. Create Account")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.create_account()
            elif choice == "2":
                account = self.login()
                if account:
                    self.user_menu(account)
            elif choice == "3":
                print("Thank you for using the Online Banking System. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def user_menu(self, account):
        while True:
            print(f"\n--- Welcome, {account.username} ---")
            print("1. Deposit Money")
            print("2. Withdraw Money")
            print("3. Balance Inquiry")
            print("4. Transaction History")
            print("5. Logout")
            
            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                try:
                    amount = float(input("Enter the amount to deposit(0-9): "))
                except:
                    print("Enter the amount in digits only(0-9)")
                    return None
                account.credit(amount)
            elif choice == '2':
                try:
                    amount = float(input("Enter the amount to withdraw: "))
                except:
                    print("Enter the amount in digits only(0-9)")
                    return None
                account.debit(amount)
            elif choice == '3':
                print(f"Current balance: ${account.check_bal()}")
            elif choice == '4':
                account.display_transactions()
            elif choice == '5':
                print(f"Logging out {account.username}...")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    system = bankingsystem()
    system.run()
                
    








