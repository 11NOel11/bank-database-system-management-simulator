import cachetools
import mysql.connector
#login functions 
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='csproj')
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except :
        return None
    



#main function runs all the query by catogerising into two types
def execute_query(connection, query, data=None):
    try:
        cursor = connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
    except :
        print("error")
    finally:
        cursor.close()

#for security of bank account customisable encryption logic 
def encrypt_password(password, key=11):
    encrypted_password = ''
    for char in password:
        encrypted_password += chr((ord(char) + key) % 128) 
    return encrypted_password
def create_account(connection, account_number, username, password, key=11):
    encrypted_password = encrypt_password(password, key)    
    query = "INSERT INTO accounts (account_number, username, encrypted_password) VALUES (%s, %s, %s);"
    data = (account_number, username, encrypted_password)
    execute_query(connection, query, data)
def decrypt_password(encrypted_password, key=11):
    decrypted_password = str()
    for char in encrypted_password:
        decrypted_password += chr((ord(char) - key) % 128)  
    return decrypted_password
def verify_password(connection, account_number, input_password, key=11):
    query = "SELECT encrypted_password FROM accounts WHERE account_number = %s;"
    data = (account_number,)
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        result = cursor.fetchone()
        if result:
            stored_encrypted_password = result[0]
            decrypted_password = decrypt_password(stored_encrypted_password, key)
            return decrypted_password == input_password
        else:
            return False
    except :        
        return False
    finally:
        cursor.close()

#transactions live
def main_transactions_menu(connection, account_number):
    while True:
        print("===================================")
        print("       Transactions Menu")
        print("===================================")
        print("1. Account Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Bank Statement (This login session)")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            balance = get_account_balance(connection, account_number)
            print(f"Account Balance: {balance}")
        elif choice == '2':
            amount = float(input("Enter the amount to deposit: "))
            if deposit_money(connection, account_number, amount):
                print("Deposit successful.")
            else:
                print("Deposit failed. Please check your balance.")
        elif choice == '3':
            amount = float(input("Enter the amount to withdraw: "))
            if withdraw_money(connection, account_number, amount):
                print("Withdrawal successful.")
            else:
                print("Withdrawal failed. Insufficient funds.")
        elif choice == '4':
            bank_statement(connection, account_number)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please choose a valid option.")
def get_account_balance(connection, account_number):
    query = "SELECT balance FROM accounts WHERE account_number = %s;"
    data = (account_number,)
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except :        
        return None
    finally:
        cursor.close()

def deposit_money(connection, account_number, amount):
    current_balance = get_account_balance(connection, account_number)

    if current_balance is not None:
        new_balance = float(current_balance) + amount
        query = "UPDATE accounts SET balance = %s WHERE account_number = %s;"
        data = (new_balance, account_number)
        execute_query(connection, query, data)

        # Record the deposit transaction
        record_transaction(connection, account_number, "Deposit", amount)

        return True
    else:
        return False

def withdraw_money(connection, account_number, amount):
    current_balance = get_account_balance(connection, account_number)

    if current_balance is not None and current_balance >= amount:
        new_balance = float(current_balance) - amount
        query = "UPDATE accounts SET balance = %s WHERE account_number = %s;"
        data = (new_balance, account_number)
        execute_query(connection, query, data)

        
        record_transaction(connection, account_number, "Withdrawal", amount)

        return True
    else:
        return False

def bank_statement(connection, account_number):
    query = "SELECT * FROM transactions WHERE account_number = %s;"
    data = (account_number,)
    cursor = connection.cursor()

    try:
        cursor.execute(query, data)
        result = cursor.fetchall()

        if result:
            for row in result:
                print(row)  
        else:
            print("No transactions for this account.")

    except :
        print("Error")

    finally:
        cursor.close()
def clear_transactions(connection, account_number):
    query = "DELETE FROM transactions WHERE account_number = %s;"
    data = (account_number,)
    execute_query(connection, query, data)
    print("Transactions cleared.")
def record_transaction(connection, account_number, transaction_type, amount):
    query = "INSERT INTO transactions (account_number, transaction_type, amount) VALUES (%s, %s, %s);"
    data = (account_number, transaction_type, amount)
    execute_query(connection, query, data)
# investments 
def main_investments_menu(connection, account_number):
    while True:

        print("===================================")
        print("       Investments Menu")
        print("===================================")
        print("1. Apply for Investment")
        print("2. Investment Status")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            investment_amount = float(input("Enter investment amount: "))
            return_rate = float(input("Enter return rate: "))
            make_investment(connection, account_number, investment_amount, return_rate)
        elif choice == '2':
            status = investment_status(connection, account_number)
            print(status)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please choose a valid option.")
def make_investment(connection, account_number, investment_amount, return_rate):
    # Deduct the investment amount from the account balance
    current_balance = get_account_balance(connection, account_number)

    if current_balance is not None and current_balance >= investment_amount:
        new_balance = float(current_balance) - investment_amount
        query_update_balance = "UPDATE accounts SET balance = %s WHERE account_number = %s;"
        data_update_balance = (new_balance, account_number)
        execute_query(connection, query_update_balance, data_update_balance)

        # Record the investment transaction
        record_transaction(connection, account_number, "Investment", investment_amount)

        # Insert investment details into the investments table
        query_insert_investment = "INSERT INTO investments (account_number, investment_amount, return_rate, status) VALUES (%s, %s, %s, %s);"
        data_insert_investment = (account_number, investment_amount, return_rate, "active")
        execute_query(connection, query_insert_investment, data_insert_investment)

        print("Investment made successfully.")
        return True
    else:
        print("Investment failed. Insufficient funds.")
        return False
def investment_status(connection, account_number):
    
    return "Investment status: Not active, pending"

#loans section
def main_loans_menu(connection, account_number):
    while True:
        print("===================================")
        print("           Loans Menu")
        print("===================================")
        print("1. Apply for Loan")
        print("2. Loan Status")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            loan_amount = float(input("Enter loan amount: "))
            interest_rate = float(input("Enter interest rate: "))
            apply_for_loan(connection, account_number, loan_amount, interest_rate)
        elif choice == '2':
            status = loan_status(connection, account_number)
            print(status)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please choose a valid option.")
def apply_for_loan(connection, account_number, loan_amount, interest_rate):
    # Add the loan amount to the account balance
    current_balance = get_account_balance(connection, account_number)

    if current_balance is not None:
        new_balance = float(current_balance) + loan_amount
        query_update_balance = "UPDATE accounts SET balance = %s WHERE account_number = %s;"
        data_update_balance = (new_balance, account_number)      
       # Insert loan details into the loans table
        if loan_amount<2*current_balance:
            print("hi")
            query_insert_loan = "INSERT INTO loans (account_number, loan_amount, interest_rate, status) VALUES (%s, %s, %s, %s);"
            data_insert_loan = (account_number, loan_amount, interest_rate, 'approved')
            execute_query(connection, query_insert_loan, data_insert_loan)
            execute_query(connection, query_update_balance, data_update_balance)
            record_transaction(connection, account_number, "Loan", loan_amount)            
        else:
            query_insert_loan = "INSERT INTO loans (account_number, loan_amount, interest_rate, status) VALUES (%s, %s, %s, %s);"
            data_insert_loan = (account_number, loan_amount, interest_rate, 'rejected')
            execute_query(connection, query_insert_loan, data_insert_loan)
        print("Loan application submitted successfully.")
        return True
    else:
        print("Loan application failed. Please check your balance.")
        return False


def calculate_total_loanpaid(connection, loan_id):
    query = "SELECT SUM(amount) FROM transactions WHERE loan_id = %s;"
    data = (loan_id,)
    cursor = connection.cursor()

    try:
        cursor.execute(query, data)
        total_paid = cursor.fetchone()[0]

        return total_paid if total_paid is not None else 0

    except:
        return 0

    finally:
        cursor.close()
def pay_interest (connection,loan_amount,interest_rate,account_number,current_balance) :
    upcoming_interest = (interest_rate/ 100) * loan_amount
    if current_balance>=upcoming_interest:
        balance=current_balance-upcoming_interest
        query_update_balance = "UPDATE accounts SET balance = %s WHERE account_number = %s;"
        data_update_balance = (current_balance, account_number)
        execute_query(connection, query_update_balance, data_update_balance)
        remaining_amount =loan_amount-upcoming_interest
        print("interest of loan paid")
        return remaining_amount,upcoming_interest
    else:
        print("insufficient balance to pay interest of {}".format(loan_amount))



    
# status of your loan    
def loan_status(connection, account_number):
    query = "SELECT * FROM loans WHERE account_number = %s;"
    data = (account_number,)
    cursor = connection.cursor()
    current_balance = get_account_balance(connection, account_number)
    try:
        cursor.execute(query, data)
        result = cursor.fetchall()
        if result:
            for row in result:
                loan_id,account_number, loan_amount, interest_rate, status = row
                
                remaining_amount, upcoming_interest = pay_interest(connection,loan_amount, interest_rate,account_number,current_balance)
                
                print(f"Loan ID: {loan_id}")
                print(f"Loan Amount: {loan_amount}")
                print(f"Interest Rate: {interest_rate}")
                print(f"Status: {status}")
                print(f"Upcoming Interest To be paid is: {upcoming_interest}")
                print(f"Remaining Amount OF Loan to be Paid is: {remaining_amount}")
                print("--------------")
        else:
            print("No active loans for this account.")
    except :
        print("Error")
    finally:
        cursor.close()
 

#main flow of codes

def mainflow():
    while True:
        print("===================================")
        print("    Welcome to NEXUS Bank")
        print("===================================")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Enter your choice: ")
        connection = connect_to_database()
        key = 11

        if choice == '1':
            while True:
                print("You selected Login. Login sequence initiated")
                account_number = input("Enter your account no: ")
                username = input("Enter the username: ")
                password = input("Enter your password: ")

                if verify_password(connection, account_number, password, key):
                    print("Correct username and password entered")
                    print("Login successful")

                    # Clear transactions menu for the new user
                    clear_transactions(connection, account_number)

                    mainflow2(connection, account_number)
                    break
                else:
                    print("Login failed")
                    print("Wrong username or wrong password entered")

        elif choice == '2':
            print("You selected Register. Welcome! Registration sequence has started.")
            account_number = input("Enter your account no: ")
            username = input("Enter the username: ")
            password = input("Enter your password: ")

            create_account(connection, account_number, username, password, key)
            print("Account creation successful")
            mainflow2(connection, account_number)

        elif choice == '3':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please choose a valid option.")

        connection.close()

def mainflow2(connection, account_number):
    while True:
        print("===================================")
        print("         Welcome to NEXUS Bank")
        print("===================================")
        print("1. Transactions Menu")
        print("2. Investments Menu")
        print("3. Loans Menu")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            main_transactions_menu(connection, account_number)
        elif choice == '2':
            main_investments_menu(connection, account_number)
        elif choice == '3':
            main_loans_menu(connection, account_number)
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please choose a valid option.")
#main program
mainflow()

