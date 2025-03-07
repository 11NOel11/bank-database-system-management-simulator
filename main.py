import mysql.connector
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='csproj',
            auth_plugin='mysql_native_password'

        )

        if connection.is_connected():
            print("Connected to MySQL database")
            return connection

    except mysql.connector.Error as err:
        print(f"Error: {err}")
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

    except mysql.connector.Error:
        print("Error")

    finally:
        cursor.close()

def encrypt_password(password, key=11):
    encrypted_password = ''
    for char in password:
        encrypted_password += chr((ord(char) + 1) % 128)  # Use modulo to wrap around ASCII characters
    return encrypted_password

def create_account(connection, account_number, username, password, key=11):
    encrypted_password = encrypt_password(password, key)
    
    query = "INSERT INTO accounts (account_number, username, encrypted_password) VALUES (%s, %s, %s);"
    data = (account_number, username, encrypted_password)
    execute_query(connection, query, data)

def decrypt_password(encrypted_password, key=11):
    decrypted_password = str()
    for char in encrypted_password:
        decrypted_password += chr((ord(char) - key) % 128)  # Use modulo to wrap around ASCII characters
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
            print("Decrypted Password from Database:", decrypted_password)
            print("Entered Password:", input_password)
            return decrypted_password == input_password
        else:
            return False

    except mysql.connector.Error as err:
        print(f"Error: {err}")
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

    if choice == '1':
        while True:
            print("You selected Login. Login sequence initiated")
            account_number = int(input("Enter your account no: "))
            username = input("Enter the username: ")
            password = input("Enter your password: ")

            if verify_password(connection, account_number, username, password):
                print("Correct username and password entered")
                print("Login successful")
                break  # Exit the loop if login is successful
            else:
                print("Login failed")
                print("Wrong username or wrong password entered")

    elif choice == '2':
        print("You selected Register. Welcome! Registration sequence has started.")
        account_number = int(input("Enter your account no: "))
        username = input("Enter the username: ")
        password = input("Enter your password: ")
        print("Password under encryption...")
        encrypted_password = encrypt_password(password)
        print("Encryption successful")
        print("Account creation query initiated...")
        create_account(connection, account_number, username, encrypted_password)

    elif choice == '3':
        print("Exiting the program.")

    else:
        print("Invalid choice. Please choose a valid option.")

    # Close the database connection after usage
    connection.close()



mainflow()
