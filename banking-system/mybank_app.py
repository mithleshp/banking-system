# -*- coding: utf-8 -*-
import sys
import mysql.connector
from datetime import date

class MyBankDB():
    """
    class MyBankDB is created to interact with mysql bank database 
    """
    def __init__(self) -> None:
        try:
         self._conn = mysql.connector.connect(user="root",password="dev123",host='localhost',port='3306',database='bank_db')
         self._cursor = self._conn.cursor()

        except Exception as error:
            print("Error while connecting to database for job tracker", error)

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor    

    def execute(self, sql, params=None):
        """Implements execute function"""
        self.cursor.execute(sql, params or ())

    def commit(self):
        """Implements commit function"""
        self.connection.commit()
    
    def fetchall(self):
        """Implements fetchall function"""
        return self.cursor.fetchall()

    def fetchone(self):
        """Implement fetchone function"""
        return self.cursor.fetchone()

    def close(self, commit=True):
        """Implement close function"""
        if commit:
            self.commit()
        self.connection.close()
    
    def exit_menu(self):
        sys.exit(0)

class MyBank(MyBankDB):
    def __init__(self) -> None:
        super().__init__()
        self.main_menu()

    def main_menu(self):
        """
        method that shows the interface for all the banking options
        
        """
        print("\n----- MAIN MENU ----- ")
        print("\n1.  Create Account")
        print("\n2.  Deposit_Amount")
        print("\n3.  Withdraw_Amount")
        print("\n4.  Account Details")
        print('\n5.  Close Account')
        print('\n6.  Close application')
        print('\n\n')
        try:
            option = int(input('Enter your option ...: '))

            if option == 1:
                self.create_account()
            elif option == 2:
                self.deposit_amount()
            elif option == 3:
                self.withdraw_amount()
            elif option == 4:
                self.show_details()
            elif option == 5:
                self.close_account()
            elif option == 6:
                self.exit_menu()

        except Exception as error:
            print("Invalid input", error)


    def create_account(self):
        """
        method that creates a new account.

        """

        try:
            self.first_name = input("Enter the account holder first name : ")
            self.last_name = input("Enter the account holder last name : ")
            self.dob = input("Enter the account holder date of birth : ")
            self.phone = input("Enter the account holder phone number: ")
            self.email = input("Enter the account holder email: ")
            self.acc_type = input("Account type (saving/checking): ")
            self.balance = input("Enter opening balance: ")

            sql = "INSERT INTO customer(first_name, last_name, dob, phone, email, acc_type, status, balance) VALUES \
                    (%s, %s, %s, %s, %s, %s, 'active', %s);"

            self.execute(sql,(self.first_name, 
                              self.last_name, 
                              self.dob, 
                              self.phone, 
                              self.email, 
                              self.acc_type, 
                              self.balance))
            print('New customer added successfully!\n\n')

            self.commit()

        except Exception as error:
            print("Error while creating account", error)

    def show_details(self):
        """
            method that shows the customer account detail
        """

        try:
            self.acct_num = input("Enter Account Number: ")
            acct_detail_query = "SELECT * FROM customer WHERE acct_num = %s ;" % self.acct_num
            self.execute(acct_detail_query)
            result = self.fetchone()
            print("\n")
            print("Account Information")
            print("*" * 50)
            print(f"Account Number: {str(result[0])}")
            print(f"Customer Name: {result[1]} {result[2]}")
            print(f"Date of Birth: {str(result[3])}")
            print(f"Contact Number: {result[4]}")
            print(f"Customer Email: {result[5]}")
            print(f"Account Type: {result[6]}")
            print(f"Account Status: {result[7]}")
            print(f"Account Balance: $ {str(result[8])}")
            print("*" * 50)
            print("\n")

            txn_detail_query = "SELECT date, amount, type FROM transaction AS t WHERE t.acct_num = (%s) ;" % self.acct_num
            self.execute(txn_detail_query)
            results = self.fetchall()
            print("**** Transaction History ****")
            if len(results) < 1:
                print("Customer has not made any transaction yet!")
            else:
                for result in results:
                    print(result[0],"$", result[1], result[2])
            
        except Exception as error:
            print("Error while creating account", error)

    def deposit_amount(self):
        """
         method that makes a deposit into an account
        """
        try:
            self.acct_num = input("Enter Account Number: ")
            self.amount = input("Enter Amount: ")
            today = date.today()
            result = self.account_status(self.acct_num)

            if result[0] == 'active':
                update_customer_query = " UPDATE customer SET balance = balance + %s \
                        WHERE acct_num = %s AND status = 'active' ;" % (self.amount, self.acct_num)
                update_transaction_query = " INSERT INTO transaction(date,amount,type,acct_num) \
                        VALUES (%s, %s, 'deposit', %s) ; "
                self.execute(update_customer_query)
                self.execute(update_transaction_query, (today, self.amount, self.acc_num))
                self.commit()
                print("\n\nAmount Deposited!")


            else:
                print("\n\nClosed or Suspended Account!")
            
        except Exception as error:
            print("Error while depositing amount", error)
        
    def withdraw_amount(self):
        """
        method that withdraws an amount from customer account by their account number
        
        """
        try:
            self.acct_num = input("Enter Account Number: ")
            self.amount = input("Enter Amount: ")
            today = date.today()
            result = self.account_status(self.acct_num)
            print(result[1])
            print(result[0])

            if result[0] == 'active' and int(result[1]) >= int(self.amount):
                update_customer_query = " UPDATE customer SET balance = balance - %s \
                        WHERE acct_num = %s AND status = 'active' ;" % (self.amount, self.acct_num)
                update_transaction_query = " INSERT INTO transaction(date, amount, type, acct_num) \
                        VALUES (%s, %s, 'withdraw', %s) ; "

                self.execute(update_customer_query)
                print(update_customer_query)
                self.execute(update_transaction_query, (today, self.amount, self.acct_num))
                print(update_transaction_query)
                self.commit
                print('\n\nAmount Withdrawn!')
            elif result[0] == 'close':
                print('\n\nClosed or Suspended Account!')
            else:
                print('\n\nInsufficient balance!')

        except Exception as error:
            print("Error while withdrawing amount", error)

    def close_account(self):
        """
        method that closes a customer account
       
        """

        try:
            self.acct_num = input("Enter Account Number: ")
            
            find_acct_num = "SELECT status FROM customer WHERE acct_num = %s;" % self.acct_num
            self.execute(find_acct_num)
            result = self.fetchall()
            
            if len(result) < 1:
                print("\nAccount number {} does not exist in the database.\nPlease try again!\n".format(self.acct_num))
               
            else:
                set_acct_status = "UPDATE customer SET status = 'close' WHERE acct_num = %s;" % self.acct_num
                print(set_acct_status)
                self.execute(set_acct_status)
                self.commit
                print("Account Closed!")

        except Exception as error:
            print("Error while closing account", error)
            
            
        

    def account_status(self, acct_num):
        """
        method that returns account status and balance
        """

        try:
            self.acct_num = acct_num
            sql = "SELECT status, balance FROM customer WHERE acct_num = %s;" % self.acct_num
            self.execute(sql)
            self._result = self.fetchone()
            return self._result
        except Exception as error:
            print("Error while finding account  status", error)

def main():
    bankDb = MyBank()
    
if __name__ == '__main__':
    main()

