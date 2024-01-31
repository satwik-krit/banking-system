# -*- compile-command: "py main.py"; -*-
from random import randint
import time
from colorama import Fore, Back, Style
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')
LOGIN_SUCCESS, LOGIN_PASSWORD_INCORRECT, LOGIN_USER_NOTFOUND = 0, 1, 2
LOCKED = 0
UNLOCKED = 1
CREATE_ACCOUNT = 2
LOGIN = 3
WITHDRAW = 4
DEPOSIT = 5
CREATE_FD = 6
MODIFY_FD = 7

USERS = {} # Associate user with unique id
STATE = LOCKED
LOGGED_USER = None # User instance
INTEREST_RATE = 2
INTEREST_PERIOD = 10

def login(username, password):
    if username in USERS:
        user = USERS[username]
        if user.password == password:
            return LOGIN_SUCCESS, user 
        else:
            return LOGIN_PASSWORD_INCORRECT, None
    return LOGIN_USER_NOTFOUND, None

def logout() :
    LOGGED_USER = None

def create_new_user(username, password):
    if username not in USERS:
        user = User(username, password)
        USERS[user.username] = user
        return True
    else:
        return False

def withdraw_amount(amount) :
    if amount > LOGGED_USER.balance :
        return False
    else :
        LOGGED_USER.balance -= amount
        return True
    
def deposit_amount(amount) :
    LOGGED_USER.balance += amount

def create_fd(amount):
    if amount > LOGGED_USER.balance:
        return False
    else:
        fd = FixedDeposit(LOGGED_USER.username, amount)
        LOGGED_USER.fixed_deposits.append(fd)
        LOGGED_USER.balance -= amount
        return True

def withdraw_fd(index):
    fd = LOGGED_USER.fixed_deposits.pop(index)
    fd.calculate_interest()
    LOGGED_USER.balance += (fd.principal + fd.interest)

class User:
    balance= 0
    fixed_deposits = []

    def __init__(self, username, password):
        self.username = username
        self.password=password
        

class FixedDeposit:
    interest_rate = INTEREST_RATE
    interest = 0
    
    def __init__(self, username, principal):
        self.username = username
        self.principal = principal
        self.creation_time = time.time()
        print(self.creation_time)

    def calculate_interest(self):
        self.time_passed = (time.time() - self.creation_time) / INTEREST_PERIOD
        self.interest = self.principal * self.time_passed * self.interest_rate / 100

    def __str__(self):
        self.calculate_interest()
        return \
        f'''Principal: {self.principal}
Creation Time: {self.creation_time} 
Interest Rate: {self.interest_rate}
Time Passed: {self.time_passed}
Interest: {self.interest} 
Final Amount: {self.principal+self.interest}'''

if __name__ == '__main__':
    while True:

        if STATE == LOCKED:
            print("Enter username and password to view details or create a new account")
            print("(1) Login")
            print("(2) Create an account")
            _input = int(input("(Command Number) -> "))

            if _input == 1:
                STATE = LOGIN

            elif _input == 2:
                STATE = CREATE_ACCOUNT
            continue

        if STATE == CREATE_ACCOUNT:
            username = input("(Enter NEW Username) -> ")
            password = input("(Enter NEW Password) -> ")
            creation_status = create_new_user(username, password)
            if creation_status:
                _, user = login(username, password)
                STATE = UNLOCKED
                LOGGED_USER = user
            else:
                print("Bhai kya kar rha hai")
                print("A user already exists with this username. Choose anther one.")
            continue

        if STATE == LOGIN:
            username = input("(Enter Username) -> ")
            password = input("(Enter Password) -> ")

            login_status, user = login(username, password)

            if login_status == LOGIN_SUCCESS:
                STATE = UNLOCKED
                LOGGED_USER = user
            elif login_status == LOGIN_PASSWORD_INCORRECT:
                print("Bhai kya kar rha hai")
                print("Incorrect Password.")
                STATE = LOCKED
            elif login_status == LOGIN_USER_NOTFOUND:
                print("Bhai kya kar rha hai")
                print("Username not found.")
                STATE = LOCKED
            continue

        if STATE == UNLOCKED :
            print(f"BALANCE: {LOGGED_USER.balance}")

            print("MENU OPTIONS")
            print("(0) Logout")
            print("(1) Withdraw")
            print("(2) Deposit")
            print("(3) Create a fixed deposit")
            print("(4) Modify/View fixed deposits")

            option = int(input("(Command) -> "))
            if option == 1 :
                STATE = WITHDRAW
            elif option == 2 :
                STATE = DEPOSIT
            elif option == 3 :
                STATE = CREATE_FD
            elif option == 0:
                logout()
                STATE = LOCKED
            elif option == 4:
                STATE = MODIFY_FD

            continue

        if STATE == WITHDRAW :
            amount = int(input("(Enter amount to withdraw) -> "))
            withdraw_status = withdraw_amount(amount)

            if not withdraw_status :
                print("Bhai kya kar raha hai")
                print("You do not have that much money. Try again.")
            else :
                print(f"Your balance : {LOGGED_USER.balance}")

            STATE = UNLOCKED
            continue

        if STATE == DEPOSIT :
            amount = int(input("(Enter amount to deposit) -> "))
            deposit_amount(amount)

            print(f"Your balance : {LOGGED_USER.balance}")
            STATE = UNLOCKED
            continue

        if STATE == CREATE_FD:
            amount = int(input("(Enter amount to deposit) -> "))
            fd_status = create_fd(amount)
            if fd_status:
                print("Fixed deposit created successfuly.")
            else:
                print("Bhai kya kar raha hai")
                print("Insufficient balance.")
            STATE = UNLOCKED
            continue

        if STATE == MODIFY_FD:
            print("------------------------")
            print("FIXED DEPOSITS")
            print("------------------------")
            for index, fd in enumerate(LOGGED_USER.fixed_deposits):
                print(f"Index: {index+1}")
                print(fd)
                print("------------------------")

            print("OPTIONS")
            print("(0) Go back")
            print("(1) Withdraw fixed deposit")
            _input = int(input("(Command) -> "))

            if _input == 0:
                STATE = UNLOCKED
            elif _input == 1:
                index = int(input("(Index of FD to withdraw) -> "))
                withdraw_fd(index-1)
                    
