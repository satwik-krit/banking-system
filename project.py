# __vimdothis__
# set makeprg=py\ project.py
# __vimendthis__
from datetime import date
import mysql.connector as sqlconn

currentState = None

db = sqlconn.connect(host="localhost", user="root", password="nandan99rd", database="nandan")
crsr = db.cursor(buffered=True)

# QUERIES
LOGIN_USER = ("SELECT username, password "
              "FROM Users "
              "WHERE username = '{}';")

CHECK_USERNAME = ("SELECT username "
                  "FROM Users "
                  "WHERE username = '{}';")

INSERT_USER = ("INSERT INTO Users VALUES "
               "('{}', '{}', '{}', '{}', {}, '{}', {});")

CREATE_ACCOUNT = ("INSERT INTO account "
                  "VALUES "
                  "({}, '{}', {}, '{}');")

GET_BALANCE = ("SELECT balance "
               "FROM account "
               "WHERE username = '{}';")

PAY_USER = (("UPDATE account "
             "SET balance = balance - {1} "
             "WHERE username = '{0}'; "),
            ("INSERT INTO transactions "
            "(payerID, receiverID, transDate, amount, comment) "
            "VALUES "
            "('{}', '{}', '{}', {}, '{}'); "),
            ("UPDATE account "
            "SET balance = balance + {1} "
            "WHERE username = '{0}'; "))

DEPOSIT = ("UPDATE account "
           "SET balance = balance + {1} "
           "WHERE username = '{0}'; ")

# PAY_USER = ("UPDATE account "
#             "SET balance = balance - {2} "
#             "WHERE username = '{0}' "
#             ";"
#             "INSERT INTO transactions "
#             "(payerID, receiverID, transDate, amount, comment) "
#             "VALUES "
#             "('{0}', '{1}', '{3}', {2}, '{4}') "
#             ";"
#             "UPDATE account "
#             "SET balance = balance + {2};"
#             "WHERE username = '{1}' ;")

def execute(query : str, args : tuple):
    crsr.execute(query.format(*args))
    db.commit()

def getBalance(username : str) -> int:
    execute(GET_BALANCE, (username,))
    return crsr.fetchone()[0]

def checkUserExists(username : str) -> bool:
    execute(CHECK_USERNAME, (username,))
    if len(crsr.fetchall()) != 0:
        return True
    else:
        return False

class LockedState:
    def __init__(self):
        pass

    def process(self):
        global currentState

        print("======================================================================")
        print("Enter username and password to view details or create a new account")
        print("(1) Login")
        print("(2) Create an account")
        print()

        option = int(input("(Option) -> ").strip())

        if option == 1:
            currentState = LoginState()

        elif option == 2:
            currentState = CreateAccountState()

class LoginState:
    _LOGIN_SUCCESS = 0
    _LOGIN_PASSWORD_INCORRECT = 1
    _LOGIN_USER_NOTFOUND = 2

    def __init__(self):
        pass

    def _login(self, username : str, password : str) -> int:
        execute(LOGIN_USER, (username,))
        record = crsr.fetchone()

        if record == None:
            return self._LOGIN_USER_NOTFOUND 
        elif record[1] != password:
            return self._LOGIN_PASSWORD_INCORRECT
        else:
            return self._LOGIN_SUCCESS

    def process(self):
        global currentState

        print("=======================================")
        username = input("(Enter Username) -> ").strip()
        password = input("(Enter Password) -> ").strip()
        loginStatus = self._login(username, password)

        if loginStatus == self._LOGIN_SUCCESS:
            currentState = UnlockedState(username)

        elif loginStatus == self._LOGIN_PASSWORD_INCORRECT:
            print()
            print("Incorrect Password.")
            currentState = LockedState()

        elif loginStatus == self._LOGIN_USER_NOTFOUND:
            print()
            print("Username not found.")
            currentState = LockedState()

class CreateAccountState:
    def __init__(self):
        self._CREATE_USER_SUCCESS = 0
        self._CREATE_USER_FAILURE = 1

    def _checkUsernameUnique(self, username : str) -> int:
        if checkUserExists(username):
            return self._CREATE_USER_FAILURE
        else:
            return self._CREATE_USER_SUCCESS
    
    def _createNewUser(self, username : str, password : str, firstname : str, 
                       lastname : str, age : int, phone : int) -> int:
        execute(INSERT_USER, (password, username, firstname, lastname, age, phone, 0))
        execute(CREATE_ACCOUNT, (0, str(date.today()), 0, username))

    def process(self):
        global currentState

        print("========================================")
        username = input("(Enter NEW Username) -> ").strip()

        uniqueStatus = self._checkUsernameUnique(username)

        if uniqueStatus == self._CREATE_USER_FAILURE:
            print()
            print("Username not unique.")
            return

        password = input("(Enter NEW Password) -> ").strip()
        firstname = input("(Enter first name) -> ").strip()
        lastname = input("(Enter last name) -> ").strip()
        age = int(input("(Enter age) -> ").strip())
        phone = int(input("(Enter phone no.) -> ").strip())
        print()

        self._createNewUser(username, password, firstname, lastname, age, phone)

        currentState = UnlockedState(username)

class UnlockedState:
    def __init__(self, username : str):
        self._username = username

    def process(self):
        global currentState

        # print and remove updates
        balance = getBalance(self._username)

        print("===================================")
        print(f"BALANCE: {balance}")
        print("(0) Logout")
        print("(1) Pay")
        print("(2) Deposit")
        print("(3) Create a fixed deposit")
        print("(4) Modify/View fixed deposits")
        print()

        option = int(input("(Option) -> ").strip())

        if option == 1:
            currentState = PayState(self._username)

        elif option == 2:
            currentState = DepositState(self._username)

        elif option == 3:
            currentState = CreateFDState(self._username)

        elif option == 0:
            currentState = LockedState()

        elif option == 4:
            currentState = ViewFDState(self._username)

class PayState:
    def __init__(self, username : str):
        self._username = username

        self._PAYMENT_SUCCESS = 0
        self._PAYMENT_NO_RECEIVER = 1
        self._PAYMENT_INSUFFICIENT_BALANCE = 2
        self._PAYMENT_CANT_PAY_SELF = 3

    def _pay(self, receiverName : str, amount : float, comment: str) -> int:
        balance = getBalance(self._username)

        if amount > balance:
            return self._PAYMENT_INSUFFICIENT_BALANCE

        elif not checkUserExists(receiverName):
            return self._PAYMENT_NO_RECEIVER

        elif receiverName == self._username:
            return self._PAYMENT_CANT_PAY_SELF

        else:
            execute(PAY_USER[0], (self._username, amount))
            execute(PAY_USER[1], (self._username, receiverName, str(date.today()), amount, comment))
            execute(PAY_USER[2], (receiverName, amount))

            return self._PAYMENT_SUCCESS 

    def process(self):
        global currentState

        print("===========================")
        print("(0) Pay to another user")
        print("(1) Abort")
        print()

        option = int(input("(Option) -> ").strip())
        print()

        if option == 0:
            receiverName = input("(Enter username of receiver) -> ").strip()
            amount = int(input("(Enter amount to pay) -> ").strip())
            comment =  input("Enter comment (optional)) -> ").strip()

            if not comment:
                comment = "No comment"

            paymentStatus = self._pay(receiverName, amount, comment)

            if paymentStatus == self._PAYMENT_SUCCESS:
                print("Transaction made successfully")

            elif paymentStatus == self._PAYMENT_INSUFFICIENT_BALANCE:
                print("You don't have enough balance to make this payment.")

            elif paymentStatus == self._PAYMENT_NO_RECEIVER:
                print("This receiver does not exist.")

            elif paymentStatus == self._PAYMENT_CANT_PAY_SELF:
                print("You cannot pay to yourself.")

        elif option == 1:
            currentState = UnlockedState(self._username)

class DepositState:
    def __init__(self, username : str):
        self._username = username

    def _deposit(self, amount : int) -> None:
        execute(DEPOSIT, (self._username, amount))

    def process(self):
        global currentState

        print("======================================================================")
        amount = int(input("(Enter amount to deposit (cash to digital money)) -> "))
        self._deposit(amount)

        currentState = UnlockedState(self._username)

class CreateFDState:
    def __init__(self, username : str):
        self._username = username

        self._CREATE_FD_SUCCESS = 0
        self._CREATE_FD_FAILURE = 1

    def _createFD(self, amount : int) -> int:
        # sql stuff
        pass

    def process(self):
        global currentState

        print("(0) Create new FD")
        print("(1) Return")

        option = int(input("(Option) -> "))

        if option == 0:
            amount = int(input("(Enter FD principal amount) -> "))
            createFDStatus = self._createFD(amount)

            if createFDStatus == self._CREATE_FD_SUCCESS:
                print("Fixed deposit created successfuly.")

            elif createFDStatus == self._CREATE_FD_FAILURE:
                print("Bhai kya kar raha hai")
                print("Insufficient balance.")

        elif option == 1:
            currentState = UnlockedState(self._username)

class ViewFDState:
    def __init__(self, username : str):
        self._username = username
    
    def process(self):
        global currentState

        # display FDs

        print("(0) View another FD")
        print("(1) Withdraw an FD")
        print("(2) Return")

        option = int(input("(Option) -> "))

        if option == 0:
            # sql stuff
            pass

        elif option == 1:
            # sql stuff
            pass

        elif option == 2:
            currentState = UnlockedState(self._username)

class Clock:
    def __init__(self):
        pass

if __name__ == '__main__':
    currentState = LockedState()

    while True:
        currentState.process()
