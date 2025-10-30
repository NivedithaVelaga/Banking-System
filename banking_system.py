"""
Banking System - A Python-based banking application
Author: Niveditha Velaga
Description: A secure banking system with account management and transaction tracking
"""

import os
import datetime

class BankingSystem:
    def __init__(self):
        self.accounts_file = "accounts.txt"
        self.transactions_file = "transactions.txt"
        self.initialize_files()
    
    def initialize_files(self):
        """Create necessary files if they don't exist"""
        if not os.path.exists(self.accounts_file):
            open(self.accounts_file, 'w').close()
        if not os.path.exists(self.transactions_file):
            open(self.transactions_file, 'w').close()
    
    def clear_screen(self):
        """Clear the terminal screen for better UX"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_timestamp(self):
        """Get current timestamp for transactions"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def create_account(self):
        """Create a new bank account"""
        self.clear_screen()
        print("=== CREATE NEW ACCOUNT ===")
        
        try:
            account_number = input("Enter account number: ").strip()
            account_holder = input("Enter account holder name: ").strip()
            initial_deposit = float(input("Enter initial deposit: $"))
            
            if initial_deposit < 0:
                print("❌ Initial deposit cannot be negative!")
                return
            
            # Check if account already exists
            with open(self.accounts_file, 'r') as file:
                for line in file:
                    if line.startswith(account_number + "|"):
                        print("❌ Account number already exists!")
                        return
            
            # Create account
            with open(self.accounts_file, 'a') as file:
                file.write(f"{account_number}|{account_holder}|{initial_deposit}\n")
            
            # Record initial transaction
            self.record_transaction(account_number, "ACCOUNT_CREATION", initial_deposit, initial_deposit)
            
            print(f"✅ Account created successfully!")
            print(f"   Account Number: {account_number}")
            print(f"   Account Holder: {account_holder}")
            print(f"   Initial Balance: ${initial_deposit:.2f}")
            
        except ValueError:
            print("❌ Invalid amount! Please enter numbers only.")
        except Exception as e:
            print(f"❌ Error creating account: {e}")
    
    def deposit_money(self):
        """Deposit money into an account"""
        self.clear_screen()
        print("=== DEPOSIT MONEY ===")
        
        try:
            account_number = input("Enter account number: ").strip()
            amount = float(input("Enter deposit amount: $"))
            
            if amount <= 0:
                print("❌ Deposit amount must be positive!")
                return
            
            accounts = []
            account_found = False
            
            with open(self.accounts_file, 'r') as file:
                for line in file:
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        acc_num, holder, balance = parts
                        if acc_num == account_number:
                            new_balance = float(balance) + amount
                            accounts.append(f"{acc_num}|{holder}|{new_balance}")
                            account_found = True
                            
                            # Record transaction
                            self.record_transaction(account_number, "DEPOSIT", amount, new_balance)
                            
                            print(f"✅ Deposit successful!")
                            print(f"   Amount deposited: ${amount:.2f}")
                            print(f"   New balance: ${new_balance:.2f}")
                        else:
                            accounts.append(line.strip())
            
            if not account_found:
                print("❌ Account not found!")
                return
            
            # Update accounts file
            with open(self.accounts_file, 'w') as file:
                for account in accounts:
                    file.write(account + '\n')
                    
        except ValueError:
            print("❌ Invalid amount! Please enter numbers only.")
        except Exception as e:
            print(f"❌ Error during deposit: {e}")
    
    def withdraw_money(self):
        """Withdraw money from an account"""
        self.clear_screen()
        print("=== WITHDRAW MONEY ===")
        
        try:
            account_number = input("Enter account number: ").strip()
            amount = float(input("Enter withdrawal amount: $"))
            
            if amount <= 0:
                print("❌ Withdrawal amount must be positive!")
                return
            
            accounts = []
            account_found = False
            
            with open(self.accounts_file, 'r') as file:
                for line in file:
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        acc_num, holder, balance = parts
                        if acc_num == account_number:
                            current_balance = float(balance)
                            if current_balance >= amount:
                                new_balance = current_balance - amount
                                accounts.append(f"{acc_num}|{holder}|{new_balance}")
                                account_found = True
                                
                                # Record transaction
                                self.record_transaction(account_number, "WITHDRAWAL", amount, new_balance)
                                
                                print(f"✅ Withdrawal successful!")
                                print(f"   Amount withdrawn: ${amount:.2f}")
                                print(f"   New balance: ${new_balance:.2f}")
                            else:
                                print("❌ Insufficient funds!")
                                return
                        else:
                            accounts.append(line.strip())
            
            if not account_found:
                print("❌ Account not found!")
                return
            
            # Update accounts file
            with open(self.accounts_file, 'w') as file:
                for account in accounts:
                    file.write(account + '\n')
                    
        except ValueError:
            print("❌ Invalid amount! Please enter numbers only.")
        except Exception as e:
            print(f"❌ Error during withdrawal: {e}")
    
    def check_balance(self):
        """Check account balance"""
        self.clear_screen()
        print("=== CHECK BALANCE ===")
        
        account_number = input("Enter account number: ").strip()
        account_found = False
        
        try:
            with open(self.accounts_file, 'r') as file:
                for line in file:
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        acc_num, holder, balance = parts
                        if acc_num == account_number:
                            print(f"✅ Account Details:")
                            print(f"   Account Number: {acc_num}")
                            print(f"   Account Holder: {holder}")
                            print(f"   Current Balance: ${float(balance):.2f}")
                            account_found = True
                            break
            
            if not account_found:
                print("❌ Account not found!")
                
        except Exception as e:
            print(f"❌ Error checking balance: {e}")
    
    def view_transactions(self):
        """View transaction history for an account"""
        self.clear_screen()
        print("=== TRANSACTION HISTORY ===")
        
        account_number = input("Enter account number: ").strip()
        transactions_found = False
        
        try:
            with open(self.transactions_file, 'r') as file:
                print(f"\nTransaction History for Account: {account_number}")
                print("-" * 60)
                
                for line in file:
                    parts = line.strip().split('|')
                    if len(parts) == 5 and parts[1] == account_number:
                        timestamp, acc_num, transaction_type, amount, balance = parts
                        print(f"📅 {timestamp} | {transaction_type:15} | Amount: ${float(amount):>8.2f} | Balance: ${float(balance):>8.2f}")
                        transactions_found = True
                
                if not transactions_found:
                    print("No transactions found for this account.")
                print("-" * 60)
                
        except Exception as e:
            print(f"❌ Error viewing transactions: {e}")
    
    def record_transaction(self, account_number, transaction_type, amount, balance):
        """Record a transaction"""
        try:
            with open(self.transactions_file, 'a') as file:
                file.write(f"{self.get_timestamp()}|{account_number}|{transaction_type}|{amount}|{balance}\n")
        except Exception as e:
            print(f"❌ Error recording transaction: {e}")
    
    def display_all_accounts(self):
        """Display all accounts (admin feature)"""
        self.clear_screen()
        print("=== ALL ACCOUNTS ===")
        
        try:
            with open(self.accounts_file, 'r') as file:
                accounts = file.readlines()
                
                if not accounts:
                    print("No accounts found.")
                    return
                
                print(f"{'Account Number':<15} {'Account Holder':<20} {'Balance':<10}")
                print("-" * 50)
                
                for account in accounts:
                    parts = account.strip().split('|')
                    if len(parts) == 3:
                        acc_num, holder, balance = parts
                        print(f"{acc_num:<15} {holder:<20} ${float(balance):>7.2f}")
                
                print("-" * 50)
                print(f"Total accounts: {len(accounts)}")
                
        except Exception as e:
            print(f"❌ Error displaying accounts: {e}")
    
    def run(self):
        """Main application loop"""
        while True:
            self.clear_screen()
            print("🏦 WELCOME TO BANKING SYSTEM")
            print("=" * 30)
            print("1. Create New Account")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Check Balance")
            print("5. View Transaction History")
            print("6. View All Accounts")
            print("7. Exit")
            print("=" * 30)
            
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.deposit_money()
            elif choice == '3':
                self.withdraw_money()
            elif choice == '4':
                self.check_balance()
            elif choice == '5':
                self.view_transactions()
            elif choice == '6':
                self.display_all_accounts()
            elif choice == '7':
                print("Thank you for using Banking System! 👋")
                break
            else:
                print("❌ Invalid choice! Please enter 1-7.")
            
            input("\nPress Enter to continue...")

# Run the application
if __name__ == "__main__":
    bank = BankingSystem()
    bank.run()
