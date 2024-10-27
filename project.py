# __vimdothis__
# set makeprg=py\ project.py
# __vimendthis__
import mysql.connector as sqlconn

currentState = None

db = sqlconn.connect(host="localhost", user="root", password="root", database="t")
crsr = db.cursor()

# QUERIES
CHECK_USER = ("SELECT username, password "
              "FROM Users "
              "WHERE username = '{}';")

class LockedState:
    def __init__(self):
        pass

    def process(self):
        global currentState

        print("Enter username and password to view details or create a new account")
        print("(1) Login")
        print("(2) Create an account")

        option = int(input("(Option) -> "))

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
        crsr.execute(CHECK_USER.format(username))
        record = crsr.fetchone()

        if record == None:
            return self._LOGIN_USER_NOTFOUND 
        elif record[1] != password:
            return self._LOGIN_PASSWORD_INCORRECT
        else:
            return self._LOGIN_SUCCESS

    def process(self):
        global currentState

        username = input("(Enter Username) -> ")
        password = input("(Enter Password) -> ")

        loginStatus = self._login(username, password)

        if loginStatus == self._LOGIN_SUCCESS:
            currentState = UnlockedState(username)

        elif loginStatus == self._LOGIN_PASSWORD_INCORRECT:
            print("Bhai kya kar rha hai")
            print("Incorrect Password.")
            currentState = LockedState()

        elif loginStatus == self._LOGIN_USER_NOTFOUND:
            print("Bhai kya kar rha hai")
            print("Username not found.")
            currentState = LockedState()

class CreateAccountState:
    def __init__(self):
        self._CREATE_USER_SUCCESS = 0
        self._CREATE_USER_FAILURE = 1
    
    def _createNewUser(self, username : str, password : str) -> int:
        # Sql stuff
        return None # return creation status enum

    def process(self):
        global currentState

        username = input("(Enter NEW Username) -> ")
        password = input("(Enter NEW Password) -> ")
        creationStatus = self._createNewUser(username, password)

        if creationStatus == self._CREATE_USER_SUCCESS:
            currentState = UnlockedState(username)

        elif creationStatus == self._CREATE_USER_FAILURE:
            print("Bhai kya kar rha hai")
            print("A user already exists with this username. Choose anther one.")

class UnlockedState:
    def __init__(self, username : str):
        self._username = username

    def process(self):
        global currentState

        # print balance with sql
        # print and remove updates

        print("(0) Logout")
        print("(1) Pay")
        print("(2) Deposit")
        print("(3) Create a fixed deposit")
        print("(4) Modify/View fixed deposits")

        option = int(input("(Option) -> "))

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
        self._PAYMENT_NO_BALANCE = 2
        self._PAYMENT_CANT_PAY_SELF = 3

    def _pay(self, receiverName : str, amount : float) -> int:
        # sql stuff
        return None # return payment status

    def process(self):
        global currentState

        print("(0) Pay to another user")
        print("(1) Return")

        option = int(input("(Option) -> "))

        if option == 0:
            receiverName = input("(Enter username of receiver) -> ")
            amount = int(input("(Enter amount to pay) -> "))
            paymentStatus = self._pay(receiverName, amount)

            if paymentStatus == self._PAYMENT_SUCCESS:
                print("Transaction made successfully")

            elif paymentStatus == self._PAYMENT_NO_BALANCE:
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
        # sql stuff
        pass

    def process(self):
        global currentState

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
