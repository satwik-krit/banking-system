# -*- compile-command: "py main.py"; -*-
from random import randint
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
USERS = {} # Associate user with unique id
STATE = LOCKED
LOGGED_USER = None # User instance

def login(username, password):
    if username in USERS:
        user = USERS[username]
        if user.password == password:
            return LOGIN_SUCCESS
        else:
            return LOGIN_PASSWORD_INCORRECT
    return LOGIN_USER_NOTFOUND

def create_new_user(username, password):
    if username not in USERS:
        user = User(username, password)
        USERS[user.username] = user
        return True
    else:
        return False


class User:
    balance= 0
    password = None
    username = None

    def __init__(self, username, password):
        self.username = username
        self.password=password
        

class FixedDeposit:
    ...


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
                login(username, password)
                STATE = UNLOCKED
            else:
                print("Bhai kya kar rha hai")
                print("User already exists with this username. Choose anther one.")
            continue

        if STATE == LOGIN:
            username = input("(Enter Username) -> ")
            password = input("(Enter Password) -> ")

            login_status = login(username, password)

            if login_status == LOGIN_SUCCESS:
                STATE = UNLOCKED
            elif login_status == LOGIN_PASSWORD_INCORRECT:
                print("Bhai kya kar rha hai")
                print("Incorrect Password.")
            elif login_status == LOGIN_USER_NOTFOUND:
                print("Bhai kya kar rha hai")
                print("Username not found.")
            continue
