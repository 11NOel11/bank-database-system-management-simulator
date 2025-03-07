import mysql.connector

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='csproj'
        )

        if connection.is_connected():
            print("Connected to MySQL database")
            return connection

    except:
        print("Error: ")
        return None

def execute_query(connection, query, data=None):
    try:
        cursor = connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")

    except :
        print("Error ")

    finally:
        cursor.close()

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
        print("Error")
        return False

    finally:
        cursor.close()

def display_welcome_screen():
    print("===================================")
    print("    Welcome to NEXUS Bank")
    print("===================================")
    print("1. Login")
    print("2. Register")
    print("3. Exit")

def mainflow():
    display_welcome_screen()

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
                
                break  
            else:
                print("Login failed")
                print("Wrong username or wrong password entered")
        mainflow2()

    elif choice == '2':
        print("You selected Register. Welcome! Registration sequence has started.")
        account_number = input("Enter your account no: ")
        username = input("Enter the username: ")
        password = input("Enter your password: ")

        create_account(connection, account_number, username, password, key)
        print("account creation succesful")
        mainflow2()

    elif choice == '3':
        print("Exiting the program.")

    else:
        print("Invalid choice. Please choose a valid option.")

    
    connection.close()
def display_welcome_screen2():
    print("===================================")
    print("    Welcome to NEXUS Bank")
    print("===================================")
    print("1. account balance")
    print("2. deposit money")
    print("3. withdraw money")
    print("4. apply for loan")
    print("5. apply for investement")
    print("6. bank statement(this login session)")
    print("7. exit")

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

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        cursor.close()
def apply_for_loan(connection, account_number, loan_amount, interest_rate):
    query = "INSERT INTO loans (account_id, loan_amount, interest_rate) VALUES (%s, %s, %s);"
    data = (account_number, loan_amount, interest_rate)
    execute_query(connection, query, data)
    print("Loan application submitted successfully.")

def make_investment(connection, account_number, investment_amount, return_rate):
    query = "INSERT INTO investments (account_id, investment_amount, return_rate) VALUES (%s, %s, %s);"
    data = (account_number, investment_amount, return_rate)
    execute_query(connection, query, data)
    print("Investment made successfully.")

def loan_status(connection, account_number):
    # Add logic to check loan status based on your requirements
    # For simplicity, this function returns a placeholder message
    return "Loan status: Not implemented"

def investment_status(connection, account_number):
    # Add logic to check investment status based on your requirements
    # For simplicity, this function returns a placeholder message
    return "Investment status: Not implemented"

def bank_statement(connection, account_number):
    query = "SELECT * FROM transactions WHERE account_number = %s;"
    data = (account_number,)
    cursor = connection.cursor()

    try:
        cursor.execute(query, data)
        result = cursor.fetchall()

        if result:
            for row in result:
                print(row)  # Modify this based on your actual transaction table structure
        else:
            print("No transactions for this account.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()



def mainflow2(connection, account_number):
    while True:
        display_welcome_screen2()
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
            loan_amount = float(input("Enter loan amount: "))
            interest_rate = float(input("Enter interest rate: "))
            apply_for_loan(connection, account_number, loan_amount, interest_rate)
        elif choice == '5':
            investment_amount = float(input("Enter investment amount: "))
            return_rate = float(input("Enter return rate: "))
            make_investment(connection, account_number, investment_amount, return_rate)
        elif choice == '6':
            transaction_type = input("Enter transaction type: ")
            amount = float(input("Enter transaction amount: "))
            record_transaction(connection, account_number, transaction_type, amount)
        
        elif choice == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please choose a valid option.")



def deposit_money(connection, account_number, amount):
    current_balance = get_account_balance(connection, account_number)

    if current_balance is not None:
        new_balance = current_balance + amount
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
        new_balance = current_balance - amount
        query = "UPDATE accounts SET balance = %s WHERE account_number = %s;"
        data = (new_balance, account_number)
        execute_query(connection, query, data)

        # Record the withdrawal transaction
        record_transaction(connection, account_number, "Withdrawal", amount)

        return True
    else:
        return False

def record_transaction(connection, account_number, transaction_type, amount):
    query = "INSERT INTO transactions (account_number, transaction_type, amount) VALUES (%s, %s, %s);"
    data = (account_number, transaction_type, amount)
    execute_query(connection, query, data)
