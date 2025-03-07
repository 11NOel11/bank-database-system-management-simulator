import mysql.connector
mycon=mysql.connector.connect(host="localhost",user="root",password="1234",database="csproj")
mycursor=mycon.cursor()
def createtableaccts():
    mycursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
    account_number INT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    encrypted_password VARCHAR(255) NOT NULL,
    balance DECIMAL(10, 2) DEFAULT 0.0);""")
def createtableloans():
    mycursor.execute("""CREATE TABLE IF NOT EXISTS loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    account_number INT,
    loan_amount DECIMAL(10, 2) NOT NULL,
    interest_rate DECIMAL(5, 2) NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    FOREIGN KEY (account_number) REFERENCES accounts(account_number));""")
def createtableinvestments():
    mycursor.execute("""CREATE TABLE IF NOT EXISTS investments (
    investment_id INT AUTO_INCREMENT PRIMARY KEY,
    account_number INT,
    investment_amount DECIMAL(10, 2) NOT NULL,
    return_rate DECIMAL(5, 2) NOT NULL,
    status ENUM('active', 'completed', 'cancelled') DEFAULT 'active',
    FOREIGN KEY (account_number) REFERENCES accounts(account_number));""")
def createtabletransactions():
    mycursor.execute("""CREATE TABLE  if not exists transactions(
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_number INT,
    transaction_type VARCHAR(20),
    amount DECIMAL(10, 2),
    FOREIGN KEY (account_number) REFERENCES accounts(account_number));""")
