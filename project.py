import time
import datetime as dt
from dateutil.relativedelta import relativedelta
import mysql.connector as sqlconn

try:

    currentState = None
    TIMEDELTA = 60
    currentDate = None

    db = sqlconn.connect(host="localhost", user="root", password="root", database="t", charset="utf8")
    crsr = db.cursor(buffered=True)
        
    def execute(query : str, args : tuple) -> None:
        crsr.execute(query.format(*args))

    def resultExists(result):
        if len(result):
            return True
        else:
            return False

    def getBalance(username : str) -> int:
        Q_GET_BALANCE = ("SELECT balance "
                         "FROM account "
                         "WHERE username = '{}';")

        execute(Q_GET_BALANCE, (username,))
        return crsr.fetchone()[0]

    def changeBalance(username : str, change : int) -> None:
        QC_CHANGE_BALANCE = ("UPDATE Account "
                             "SET balance = balance + {1} "
                             "WHERE username = '{0}'; ")
        
        execute(QC_CHANGE_BALANCE, (username, change))
        db.commit()

    def checkUserExists(username : str) -> bool:
        Q_CHECK_USERNAME = ("SELECT username "
                            "FROM Users "
                            "WHERE username = '{}';")

        execute(Q_CHECK_USERNAME, (username,))
        if len(crsr.fetchall()) != 0:
            return True
        else:
            return False

    def checkFDExists(username : str, fdName : str) -> bool:
        Q_CHECK_FD_EXISTS = ("SELECT * FROM FixedDepo "
                             "WHERE username = '{}' AND fdName = '{}'; ")

        execute(Q_CHECK_FD_EXISTS, (username, fdName))

        if len(crsr.fetchall()) != 0:
            return True
        else:
            return False

    def intInput(prompt : str, failMsg : str = "Invalid input.") -> int:
        while True:
            inpStr = input(prompt).strip()

            if not inpStr.isdigit():
                print(failMsg)
            else:
                return int(inpStr)
    
    def getUpdates(username, date=None):
        _Q_GET_UPDATES_ALL = ("SELECT baseContent, extraContent, updateDate "
                              "FROM Updates "
                              "WHERE username = '{}';")

        _Q_GET_UPDATES_DAY = ("SELECT baseContent, extraContent, updateDate "
                              "FROM Updates "
                              "WHERE username = '{}' "
                              "AND updateDate = '{}'")

        if date:
            execute(_Q_GET_UPDATES_DAY, (username, date))
            return crsr.fetchall()
        else:
            execute(_Q_GET_UPDATES_ALL, (username, ))
            return crsr.fetchall()

    def createUpdate(username, baseContent, extraContent="No comment", _date=None):
        _QC_CREATE_UPDATE = ("INSERT INTO Updates "
                             "VALUES "
                             "('{}', '{}', '{}', '{}')")

        if _date:
            execute(_QC_CREATE_UPDATE, (username, baseContent, extraContent, _date))
        else:
            execute(_QC_CREATE_UPDATE, (username, baseContent, extraContent, currentDate))

        db.commit()

    def getUserInfo(username):
        _Q_GET_USER = ("SELECT firstname, lastname, age, phone, inactive "
                       "FROM Users "
                       "WHERE username = '{}' ;")

        execute(_Q_GET_USER, (username,))
        return crsr.fetchone()

    class LockedState:
        def __init__(self):
            pass

        def process(self):
            global currentState

            print("======================================================================")
            print("Enter username and password to view details or create a new account")
            print("(1) Login")
            print("(2) Create an account")
            print("(3) Quit")
            print()

            option = intInput("(Option) -> ")

            if option == 1:
                currentState = LoginState()

            elif option == 2:
                currentState = CreateAccountState()

            else:
                print()
                print("Please choose a valid option.")

    class LoginState:
        _LOGIN_SUCCESS = 0
        _LOGIN_PASSWORD_INCORRECT = 1
        _LOGIN_USER_NOTFOUND = 2

        _Q_LOGIN_USER = ("SELECT username, password "
                         "FROM Users "
                         "WHERE username = '{}'; ")

        def __init__(self):
            pass

        def _login(self, username : str, password : str) -> int:
            execute(self._Q_LOGIN_USER, (username,))
            record = crsr.fetchone()

            if record == None:
                print("Username not found.")
                return 
            
            if record[1] != password:
                print("Incorrect password.")
                return 
            
            print("Logged in successfully.")

            global currentState
            currentState = UnlockedState(username)

        def process(self):
            print("=======================================")
            username = input("(Enter Username) -> ").strip()
            password = input("(Enter Password) -> ").strip()
            print()

            self._login(username, password)

    class CreateAccountState:
        _QC_CREATE_USER = ("INSERT INTO Users VALUES "
                           "('{}', '{}', '{}', '{}', {}, '{}', {}); ")

        _QC_CREATE_ACCOUNT = ("INSERT INTO account "
                              "VALUES "
                              "({}, '{}', {}, '{}'); ")

        def __init__(self):
            pass
        
        def _createNewUser(self, username : str, password : str, firstname : str, 
                        lastname : str, age : int, phone : int) -> int:
            execute(self._QC_CREATE_USER, (password, username, firstname, lastname, age, phone, 0))
            execute(self._QC_CREATE_ACCOUNT, (0, str(currentDate), 0, username))
            db.commit()

        def process(self):
            global currentState

            print("========================================")
            print("(0) Create account")
            print("(1) Abort")
            print()

            option = intInput("(Option) -> ")

            if option == 0:
                print()
                username = input("(Enter NEW Username) -> ").strip()

                if checkUserExists(username):
                    print()
                    print("Username not unique.")
                    return

                password = input("(Enter NEW Password) -> ").strip()
                firstname = input("(Enter first name) -> ").strip()
                lastname = input("(Enter last name) -> ").strip()
                age = intInput("(Enter age) -> ")
                phone = intInput("(Enter phone no.) -> ")
                print()

                self._createNewUser(username, password, firstname, lastname, age, phone)

                currentState = UnlockedState(username)

            elif option == 1:
                currentState = LockedState()

            else:
                print()
                print("Please choose a valid option")

    class UnlockedState:
        def __init__(self, username : str):
            self._username = username

        def process(self):
            global currentState
            global currentDate

            # print and remove updates
            balance = getBalance(self._username)
            updates = getUpdates(self._username, currentDate)

            print("===================================")
            print(currentDate)
            print(f"BALANCE: {balance}")
            if resultExists(updates):
                print("TODAY'S UPDATES:", end=" ")
                for content, _, __ in updates:
                    print(f"{content}", end=", ")
            print()
            print("(0) Logout")
            print("(1) Pay")
            print("(2) Deposit")
            print("(3) Create a fixed deposit")
            print("(4) Modify/View fixed deposits")
            print("(5) View all updates for your account")
            print()

            option = intInput("(Option) -> ")

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
            
            elif option == 5:
                currentState = ViewUpdatesState(self._username)

            else:
                print()
                print("Please choose a valid option.")

    class PayState:
        _QC_PAY_USER = ("INSERT INTO transactions "
                        "(payerID, receiverID, transDate, amount, comment) "
                        "VALUES "
                        "('{}', '{}', '{}', {}, '{}'); ")

        def __init__(self, username : str):
            self._username = username

        def _pay(self, receiverName : str, amount : float, comment: str) -> int:
            global currentState
            balance = getBalance(self._username)

            if receiverName == self._username:
                print("You cannot pay yourself.")
                return

            if not checkUserExists(receiverName):
                print("This receiver does not exist.")
                return

            if amount > balance:
                print("You do not have sufficient balance.")
                return

            changeBalance(self._username, -amount)
            execute(self._QC_PAY_USER, (self._username, receiverName, str(currentDate), amount, comment))
            changeBalance(receiverName, amount)

            recFirstName = getUserInfo(receiverName)[0]
            userFirstName = getUserInfo(self._username)[0]
            createUpdate(receiverName, f"{userFirstName} payed {amount}", f"{comment}")
            createUpdate(self._username, f"Payed {amount} to {recFirstName}", f"{comment}")

            db.commit()

            print("Transaction made successfully.")

            currentState = UnlockedState(self._username)

        def process(self):
            global currentState

            print("===========================")
            print("(0) Pay to another user")
            print("(1) Abort")
            print()

            option = intInput("(Option) -> ")

            if option == 0:
                print()
                receiverName = input("(Enter username of receiver) -> ").strip()
                amount = intInput("(Enter amount to pay) -> ")
                comment =  input("Enter comment (optional)) -> ").strip()
                print()

                if not comment:
                    comment = "No comment"

                self._pay(receiverName, amount, comment)

            elif option == 1:
                currentState = UnlockedState(self._username)

            else:
                print()
                print("Please choose a valid option.")

    class DepositState:
        def __init__(self, username : str):
            self._username = username

        def _deposit(self, amount : int) -> None:
            changeBalance(self._username, amount)
            createUpdate(self._username, f"Deposit {amount}")
            db.commit()

        def process(self):
            global currentState

            print("======================================================================")
            amount = intInput("(Enter amount to deposit (cash to digital money)) -> ")
            self._deposit(amount)

            currentState = UnlockedState(self._username)

    class CreateFDState:
        _QC_CREATE_FD = ("INSERT INTO FixedDepo "
                         "(fdName, username, principal, interest, creationdate, timeperiod, maturedate) "
                         "VALUES('{}', '{}', {}, {}, '{}', {}, '{}'); ")

        def __init__(self, username : str):
            self._username = username

        def _createFD(self, name : str, amount : int, period : int) -> None:
            if checkFDExists(self._username, name):
                print("FD with this name already exists")
                return

            if getBalance(self._username) < amount:
                print("You do not have sufficient balance.")
                return

            changeBalance(self._username, -amount)
            execute(self._QC_CREATE_FD, (name, self._username, amount, 2, str(currentDate), period, 
                    dt.date.today() + relativedelta(years=period)))
            db.commit()
            createUpdate(self._username, f"Create {name} FD")
            print("FD created successfully.")

        def process(self):
            global currentState

            print("======================")
            print("(0) Create new FD")
            print("(1) Return")
            print()

            option = intInput("(Option) -> ")

            if option == 0:
                print()
                name = input("(Enter FD name) -> ")
                amount = intInput("(Enter amount) -> ")
                period = intInput("(Enter time period in years (under 10)) -> ")
                print()

                self._createFD(name, amount, period)

            elif option == 1:
                currentState = UnlockedState(self._username)

            else:
                print()
                print("Please choose a valid option.")

    class ViewFDState:
        _Q_GET_FD_DETAILS = ("SELECT * FROM FixedDepo "
                             "WHERE username = '{}' AND fdName = '{}'; ")
        _QC_WITHDRAW_FD = ("UPDATE FixedDepo "
                           "SET withdrawn = 1 "
                           "WHERE username = '{}' AND fdName = '{}'; ")
        _Q_GET_ALL_FDS = ("SELECT fdName FROM FixedDepo "
                          "WHERE username = '{}'; ")

        def __init__(self, username : str):
            self._username = username

        def _getFDComputedDetails(self, record : tuple):
                passedTimeDelta = relativedelta(date.today(), record[4])

                yearsPassed = passedTimeDelta.years + (passedTimeDelta.months / 12) + (passedTimeDelta.days / 365.25)
                matured = False if yearsPassed < record[5] else True
                value = (record[2] * record[3] * (record[5] if matured else yearsPassed) / 100) + record[2]

                return (yearsPassed, matured, value)

        def _printFD(self, fdName : str) -> None:
            if not checkFDExists(self._username, fdName):
                print("FD with this name does not exist.")
                return
            
            execute(self._Q_GET_FD_DETAILS, (self._username, fdName))
            record = crsr.fetchone()
            computedDetails = self._getFDComputedDetails(record)

            print(f"Principal : {record[2]}")
            print(f"Interest : {record[3]}")
            print(f"Created : {record[4]}")
            print(f"Total time period (years) : {record[5]}")
            print(f"Time passed (years) : {computedDetails[0]}")
            print(f"Current value : {computedDetails[2]}")
            print(f"Mature date : {record[6]}")
            print(f"Matured? : {'Yes' if computedDetails[1] else 'No'}")
            print(f"Widthdrawn? : {'Yes' if record[7] else 'No'}")

        def _withdrawFD(self, fdName : str) -> None:
            if not checkFDExists(self._username, fdName):
                print("FD with this name does not exist.")
                return

            execute(self._Q_GET_FD_DETAILS, (self._username, fdName))
            record = crsr.fetchone()

            if record[7]:
                print("You have already withdrawn this FD.")
                return
            
            computedDetails = self._getFDComputedDetails(record)
            execute(self._QC_WITHDRAW_FD, (self._username, fdName))
            changeBalance(self._username, computedDetails[2])

            db.commit()

            print(f"Withdrew amount {computedDetails[2]} from FD {fdName}.")
        
        def process(self):
            global currentState

            # display FDs

            print("=============================")
            print("(0) Show all FDs")
            print("(1) View details of a particular FD")
            print("(2) Withdraw an FD")
            print("(3) Return")
            print()

            option = intInput("(Option) -> ")

            if option == 0:
                execute(self._Q_GET_ALL_FDS, (self._username,))
                fdNames = crsr.fetchall()

                if resultExists():
                    print("You don't have any FDs yet.")
                    return
                
                for fdName in fdNames:
                    print(fdName[0])

            elif option == 1:
                print()
                fdName = input("(Enter FD name) -> ").strip()
                print()
                self._printFD(fdName)

            elif option == 2:
                print()
                fdName = input("(Enter FD name) -> ").strip()
                print()
                self._withdrawFD(fdName)

            elif option == 3:
                currentState = UnlockedState(self._username)

            else:
                print()
                print("Please choose a valid option.")

    class ViewUpdatesState:
        def __init__(self, username):
            self._username = username

        def _displayUpdates(self, updates):
            # sort updates from most recent to last
            updates.sort(key = lambda x: x[2])
            for index, update in enumerate(updates):
                baseContent, extraContent, updateDate = update
                print()
                print(f"({index}): {baseContent}")
                print(f"Date: {updateDate}")
                print(f"Comment: {extraContent}")

        def process(self):
            global currentState

            print("=============================")
            print("(0) View all updates")
            print("(1) View all updates for a day")
            print("(2) Return")
            print()

            option = intInput("(Option) -> ")

            if option == 0:
                updates = getUpdates(self._username)
                if not resultExists(updates):
                    print("You have no updates for your account.")
                
                else:
                    self._displayUpdates(updates)

            elif option == 1:
                inp = input("(Required date, in YYYY-MM-DD format) -> ")

                try:
                    _date = dt.date.fromisoformat(inp)
                    updates = getUpdates(self._username, _date)

                    if not resultExists(updates ):
                        print(f"You have no updates for your account at {inp}.")
                    
                    else:
                        self._displayUpdates(updates)

                except ValueError:
                    print("Invalid date.")

            elif option == 2:
                currentState = UnlockedState(self._username)

            else:
                print("Please choose a valid option.")



    if __name__ == '__main__':
        currentState = LockedState()

        _Q_GETDBCREATIONDATETIME = ("SELECT DBCreationDateTime "
                                    "FROM EnvInfo ;")

        # Get the date and time when we created the database
        execute(_Q_GETDBCREATIONDATETIME, ())

        creationDateTime = crsr.fetchone()[0]
        creationTime = creationDateTime.timestamp()
        creationDate = creationDateTime.date()
        currentTime = time.time() # Get time since epoch

        elapsedTime = currentTime - creationTime # in seconds
        
        elapsedDays = elapsedTime // TIMEDELTA # Days according to us

        currentDate = creationDate + dt.timedelta(days=elapsedDays)
        
        previousTime = time.time()

        while True:
            currentTime = time.time()
            elapsedDays = (currentTime - previousTime) // TIMEDELTA
            currentDate += dt.timedelta(days=elapsedDays)

            currentState.process()
            previousTime = currentTime

except KeyboardInterrupt:
    print("Quit")
    db.close()
