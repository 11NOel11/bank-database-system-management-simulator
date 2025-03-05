# Banking System Simulation

This project simulates a basic banking system using Python and MySQL. It provides functionalities to simulate real-world banking operations, such as creating customer accounts, managing balances, and handling transactions like deposits and withdrawals. Additionally, it includes enhanced security features, such as encrypted account data and authentication mechanisms.

## Features
- ✅ Secure account creation with encryption
- ✅ Connects to a MySQL database using `mysql-connector-python`
- ✅ Simulates customer registration and account creation
- ✅ Supports deposits, withdrawals, and transaction history tracking
- ✅ Uses relational database tables (`Customers`, `Accounts`, `Transactions`)
- ✅ Implements authentication and security measures for account protection
- ✅ Can be extended with more features like loan management and multi-user support

## Technology Stack
- **Programming Language**: Python
- **Database**: MySQL
- **Library Used**: `mysql-connector-python`
- **Security**: Encryption and authentication mechanisms implemented

## Database Schema
The system consists of three main tables:

1. **Customers**: Stores customer details (ID, Name, Address, Email)
2. **Accounts**: Tracks account details (ID, Customer ID, Account Type, Balance, Encrypted Credentials)
3. **Transactions**: Logs transactions (ID, Account ID, Amount, Type)

## Security Measures
- 🔒 **Encryption**: Sensitive account data is encrypted for enhanced security.
- 🔑 **Authentication**: Secure login mechanisms implemented to prevent unauthorized access.
- 🚀 **Data Protection**: Proper security practices are followed to safeguard customer data.

## Setup Instructions
### 1. Install Dependencies
Make sure you have Python installed, then install the required package:
```bash
pip install mysql-connector-python
```

### 2. Set Up MySQL Database
- Create a MySQL database and update the connection details in `config.py`.
- Run the `database_setup.py` script to create the necessary tables.

### 3. Run the Simulation
Execute the main Python script to interact with the banking system:
```bash
python main.py
```

## Future Improvements
- 🔐 Strengthen authentication with multi-factor authentication (MFA)
- 📊 Add features like loan processing and interest calculation
- 🌐 Develop a web interface for a better user experience

## Contributing
Feel free to fork this repository, make enhancements, and submit a pull request!!!

