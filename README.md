# Secure Banking System 🏦

A robust, Python-based banking system with MySQL integration, providing secure user authentication, transaction management, investment tracking, and loan processing. Built for reliability and security. 🚀

---

## 🔥 Features
✅ **Secure Login System** – Encrypted passwords for user authentication 🔐  
✅ **Banking Transactions** – Deposit, withdraw, and check balance 💰  
✅ **Transaction History** – View account activity 📜  
✅ **Investments & Loans** – Apply for investments and manage loans 📈  
✅ **MySQL Database Integration** – Secure, efficient storage 🔄  
✅ **Error Handling & Security** – Protection against SQL injection & data leaks 🔒  

---

## 📥 Installation & Setup
### **Prerequisites**
- Python 3.x installed ✅
- MySQL installed & configured ✅
- Required Python libraries installed ✅
  ```sh
  pip install mysql-connector-python
  ```

### **Step-by-Step Setup**
1️⃣ **Clone the repository** 🛠️  
   ```sh
   git clone https://github.com/your-username/secure-banking-system.git
   cd secure-banking-system
   ```
2️⃣ **Configure the MySQL Database** 🗄️  
   - Create a database named `csproj`
   - Run the script below to generate tables:
     ```python
     import mysql.connector
     
     mycon = mysql.connector.connect(host="localhost", user="root", password="1234", database="csproj")
     mycursor = mycon.cursor()
     
     def create_tables():
         mycursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
         account_number INT PRIMARY KEY,
         username VARCHAR(255) NOT NULL,
         encrypted_password VARCHAR(255) NOT NULL,
         balance DECIMAL(10, 2) DEFAULT 0.0);""")
         
         mycursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
         transaction_id INT AUTO_INCREMENT PRIMARY KEY,
         account_number INT,
         transaction_type VARCHAR(20),
         amount DECIMAL(10, 2),
         FOREIGN KEY (account_number) REFERENCES accounts(account_number));""")
         
         mycursor.execute("""CREATE TABLE IF NOT EXISTS loans (
         loan_id INT AUTO_INCREMENT PRIMARY KEY,
         account_number INT,
         loan_amount DECIMAL(10, 2) NOT NULL,
         interest_rate DECIMAL(5, 2) NOT NULL,
         status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
         FOREIGN KEY (account_number) REFERENCES accounts(account_number));""")
         
         mycursor.execute("""CREATE TABLE IF NOT EXISTS investments (
         investment_id INT AUTO_INCREMENT PRIMARY KEY,
         account_number INT,
         investment_amount DECIMAL(10, 2) NOT NULL,
         return_rate DECIMAL(5, 2) NOT NULL,
         status ENUM('active', 'completed', 'cancelled') DEFAULT 'active',
         FOREIGN KEY (account_number) REFERENCES accounts(account_number));""")
     
     create_tables()
     print("Database tables created successfully!")
     ```
3️⃣ **Run the Program** 🏃‍♂️  
   ```sh
   python banking.py
   ```

---

## 💡 How to Use
🎟 **Step 1: Login or Register**  
🔹 If new, register an account 🔹 If existing, login with credentials  
📌 **Step 2: Access the Banking Menu**  
🔹 Check balance 🔹 Deposit & withdraw money 🔹 View transaction history  
📊 **Step 3: Investments & Loans**  
🔹 Apply for investments 🔹 Manage loan applications 🔹 Track interest & repayments  

---

## 🔐 Security Features
🔹 **Random Key Encryption** – Protects user passwords  
🔹 **SQL Injection Protection** – Prevents database attacks  
🔹 **Secure Transactions** – Ensures safe financial operations  
🔹 **Environment Safety** – Avoids sensitive data leaks via `.gitignore`  

---

## 🤝 Contributing
We welcome contributions! To contribute:
1️⃣ **Fork the repository** 🍴  
2️⃣ **Create a new branch** (`git checkout -b feature-branch`) 🌿  
3️⃣ **Commit changes** (`git commit -m "Added feature XYZ"`) 📝  
4️⃣ **Push to GitHub** (`git push origin feature-branch`) 🚀  
5️⃣ **Submit a pull request** 🔄  

---

## 📜 License
This project is licensed under the **MIT License**.  
📌 **Author:** Your Name | [GitHub](https://github.com/your-username)  

---

 **Happy Banking!** 
