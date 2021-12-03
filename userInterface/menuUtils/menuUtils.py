"""menuUtils class"""

from errors.InvalidLength import InvalidLength

class menuUtils:
    def __init__(self, console):
        self.console = console
        
        # It might be a good idea to NOT hardcode this number here, somehow.
        self.numLinesStartHeader = 3
        
        # Menu choices
        
        # The quit option should be available in all default menus.
        self.quitFlag = "Quit menu"
        
    def printStartHeader(self):
        print("Welcome to our sales platform!")
        print("Please login to continue:\n")
        
    def pressEnterToContinue(self):
        self.console.input("\nPress enter to continue...")
        self.console.clearAll()
        
    def pressEnterToLeave(self):
        self.console.input("\nPress enter to leave...")
        self.console.clearAll()
        
    # attemptConsoleInput tries to get an input from user until he types
    # something valid.
    #
    # The code is a bit complicated, but this is necessary, so that we don't
    # lose what the user has typed in the middle of the interaction.
    def attemptConsoleInput(self, inputMessage, checkFunc):
        oneAttemptWrong = False
        oopsMessage = ""
        inStr = ""
        while True:
            try:
                if oneAttemptWrong:
                    self.console.print(oopsMessage)
                inStr = self.console.input(inputMessage)
                checkFunc(inStr)
                break
            except (ValueError, InvalidLength) as err:
                oopsMessage = "\nOops: {}\n".format(err)
                if oneAttemptWrong:
                     self.console.clear(self.console.countLines(oopsMessage))
                self.console.clear(self.console.countLines(inputMessage) + 2)
                oneAttemptWrong = True
        # Restore normal menu
        if oneAttemptWrong:
            self.console.clear(self.console.countLines(oopsMessage) + 1)
            self.console.print(inputMessage + inStr + "\n")
        return inStr
    
    # attemptLogin tries to log in to the system until the user gets his
    # credentials right. If he types in an empty email, we quit.
    def attemptLogin(self, sm):
        oneAttemptWrong = False
        loginSuccess = False
        while not loginSuccess:
            if oneAttemptWrong:
                self.console.print("Please try again. To quit, simply leave the email field empty.\n")
            email = self.console.input("Email: ")
            if email == "":
                print("\nEmpty email field. Quitting...")
                return False
            password = self.console.input("Password: ")
            
            loginSuccess = sm.login(email, password)
            self.console.clearAll()
            if loginSuccess:
                self.console.clear(self.numLinesStartHeader)
                return True
            
            # If we got here, we have not been successful :(
            oneAttemptWrong = True
    
    # printMenu prints a menu with `options` in default format.
    def printMenu(self, options):
        for i in range(len(options)):
            print("({})\t{}".format(i + 1, options[i]))
        print("") # Extra line
        
    # Same as printMenu, but with self.console.print method
    def printConsoleMenu(self, options):
        for i in range(len(options)):
            self.console.print("({})\t{}".format(i + 1, options[i]))
        self.console.print("") # Extra line    
    
    # Utility function to print out menu and ask for a choice.
    def handleMenu(self, options):
        # Always give the option to quit from menu
        options = [self.quitFlag, *options]
        
        self.printMenu(options)
        
        oneWrongAttempt = False
        while True:
            try:
                if oneWrongAttempt:
                    self.console.print("Invalid option. Please try again.")
                choice = int(self.console.input("Choose an option: "))
                
                if 1 <= choice and choice <= len(options):
                    self.console.clear(self.console.numLines + len(options) + 1)
                    return options[choice - 1]
            except ValueError:
                pass
            except:
                raise
            
            self.console.clearAll()
            oneWrongAttempt = True
        
    def noCasesForThisUserMenu(self):
        self.console.print("There are no cases for this user")
        self.pressEnterToLeave()

    def fetchCasesForUser(self, sm, userType):
        cases = sm.getCasesByUserType(userType)
        if len(cases) == 0:
            self.noCasesForThisUserMenu()
            return None
        return cases
    
    # TODO: there is a bug when the number of comments is greater than 0. For
    #   some reason the console is not cleared correctly. Maybe the bug is not
    #   exactly in this function. -aholmquist 2021-12-02
    #
    # Fetch and display all cases from storage manager.
    def fetchAndSeeCases(self, sm, userType):
        cases = self.fetchCasesForUser(sm, userType)
        if cases == None:
            return None
        
        self.console.print("These are all the cases you are involved with:\n")
        
        for i in range(len(cases)):
            self.console.print("Case {}".format(i))
            self.console.print(cases[i])
        
        return cases
   
    # Series of menus to help user choose a case, for whatever reason.
    def chooseCase(self, sm, userType):
        cases = self.fetchAndSeeCases(sm, userType)
        if cases == None:
            return None
        
        chosenOption = self.handleMenu([case.title for case in cases])
        if chosenOption == self.quitFlag: # Quit menu
            return None
         
        chosenIdx = [case.title for case in cases].index(chosenOption)
        chosenCase = cases[chosenIdx]
        
        return chosenCase
    
    