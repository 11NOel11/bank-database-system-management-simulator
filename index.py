import functions
from main import *

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
    connection=connect_to_database()
    if choice == '1':
        while choice=="1":

            print("You selected Login. Login sequence initiated")
            account_number=int(input("enter your account no :"))
            username=input("enter the username :")
            password=input("enter your account no :")
            if verify_password(account_number,username,password):
                print("corrrect username and password entered")
                print("login succesful")
                return True   
            else:
                print("login failed")
                print("wrong uusername or wrong password entered")
                display_welcome_screen()
                choice=input("enter your choice")
        
    elif choice == '2':

        print("You selected Register.welcome! registration sequence has started.")
        account_number=int(input("enter your account no :"))
        username=input("enter the username :")
        password=input("enter your account no :")
        print("password undr encryption.....")
        encrypted_password=encrypt_password(password)
        print("encryption succesful")
        print("account creation query initiated.....")
        create_account(connection,account_number,username,encrypted_password)
        return True


    elif choice == '3':
        print("Exiting the program.")
    else:
        print("Invalid choice. Please choose a valid option.")

mainflow()