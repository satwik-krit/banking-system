CUR_STATE = list()

class State:
    pass

class LockedState:
    def __init__(self):
        pass

    def process(self):
        print("Enter username and password to view details or create a new account")
        print("(1) Login")
        print("(2) Create an account")
        inp = int(input("(Command Number) -> "))

        if inp == 1:
            CUR_STATE.append(LoginState())

        elif inp == 2:
            CUR_STATE.append(CreateAccountState())
        continue

class LoginState:
    def __init__(self):
        self.LOGIN_SUCCESS = 0
        self.LOGIN_PASSWORD_INCORRECT = 1
        self.LOGIN_USER_NOTFOUND = 2

    def process(self):
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

class CreateAccountState:
    def __init__(self):
        pass
    
    def process(self):
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

class UnlockedState:
    def __init__(self):
        pass

    def process(self):
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

class WithdrawState:
    def __init__(self):
        pass

    def process(self):
        amount = int(input("(Enter amount to withdraw) -> "))
        withdraw_status = withdraw_amount(amount)

        if not withdraw_status :
            print("Bhai kya kar raha hai")
            print("You do not have that much money. Try again.")
        else :
            print(f"Your balance : {LOGGED_USER.balance}")

        STATE = UNLOCKED
        continue

class DepositState:
    def __init__(self):
        pass

    def process(self):
        amount = int(input("(Enter amount to deposit) -> "))
        deposit_amount(amount)

        print(f"Your balance : {LOGGED_USER.balance}")
        STATE = UNLOCKED
        continue

class CreateFDState:
    def __init__(self):
        pass

    def process(self):
        amount = int(input("(Enter amount to deposit) -> "))
        fd_status = create_fd(amount)
        if fd_status:
            print("Fixed deposit created successfuly.")
        else:
            print("Bhai kya kar raha hai")
            print("Insufficient balance.")
        STATE = UNLOCKED
        continue

class WithdrawFDState:
    def __init__(self):
        pass
    
    def process(self):
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

if __name__ == '__main__':



