import mysql.connector
import random

def generate_key():
    """Generates a random encryption key between 5 and 20."""
    return random.randint(5, 20)

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='csproj')
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

def execute_query(connection, query, data=None):
    """Executes a given SQL query with optional data."""
    try:
        cursor = connection.cursor()
        cursor.execute(query, data if data else ())
        connection.commit()
    except mysql.connector.Error as e:
        print(f"Query execution error: {e}")
    finally:
        cursor.close()

def encrypt_password(password, key):
    """Encrypts a password using a basic shift cipher."""
    return ''.join(chr((ord(char) + key) % 128) for char in password)

def decrypt_password(encrypted_password, key):
    """Decrypts a password using a basic shift cipher."""
    return ''.join(chr((ord(char) - key) % 128) for char in encrypted_password)

def create_account(connection, account_number, username, password):
    """Creates a new user account with a randomly generated encryption key and stores it in the database."""
    key = generate_key()
    encrypted_password = encrypt_password(password, key)    
    query = "INSERT INTO accounts (account_number, username, encrypted_password, encryption_key) VALUES (%s, %s, %s, %s);"
    execute_query(connection, query, (account_number, username, encrypted_password, key))

def verify_password(connection, account_number, input_password):
    """Verifies the user's password by retrieving the stored encryption key and decrypting the password."""
    query = "SELECT encrypted_password, encryption_key FROM accounts WHERE account_number = %s;"
    cursor = connection.cursor()
    try:
        cursor.execute(query, (account_number,))
        result = cursor.fetchone()
        if result:
            stored_encrypted_password, key = result
            return decrypt_password(stored_encrypted_password, key) == input_password
        return False
    except mysql.connector.Error as e:
        print(f"Error verifying password: {e}")
        return False
    finally:
        cursor.close()

def login_menu(connection):
    """Handles the login process with an option to go back."""
    while True:
        print("1. Login")
        print("2. Back to Main Menu")
        choice = input("Enter your choice: ")
        if choice == '1':
            account_number = input("Enter your account number: ")
            password = input("Enter your password: ")
            if verify_password(connection, account_number, password):
                print("Login successful!")
                return account_number
            else:
                print("Incorrect credentials. Try again or choose 2 to go back.")
        elif choice == '2':
            return None
        else:
            print("Invalid option. Please choose again.")

def main():
    """Main program execution."""
    connection = connect_to_database()
    if not connection:
        return
    while True:
        print("1. Login\n2. Register\n3. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            account_number = login_menu(connection)
            if account_number:
                print("Proceeding to banking menu...")
        elif choice == '2':
            account_number = input("Enter account number: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            create_account(connection, account_number, username, password)
            print("Account created successfully")
        elif choice == '3':
            break
        else:
            print("Invalid option")

main()



