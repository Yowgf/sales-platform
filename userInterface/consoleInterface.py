import os

from errors.InvalidLength import InvalidLength

# consoleInterface handles all user interactions in the system.
#
# In the future, we want this functionality to be spread across
# multiple modules.
class consoleInterface:
    def __init__(self, storageManager):
        self.sm = storageManager
        
        # Util constants.
        
        # numLinesConsole helps maintain the console nice and tidy.
        self.numLinesConsole = 0
        
        # It might be a good idea to NOT hardcode this number here, somehow.
        self.numLinesStartHeader = 3
        
        # Menu choices
        
        # The quit option should be available in all default menus.
        self.quitFlag = "Quit menu"
        
        self.seeCasesChoice = "See cases"
        self.commentCaseChoice = "Comment on case"
        self.createCaseChoice = "Create case"
        self.setCaseStatusChoice = "Set case status"

    def run(self):
        menuException = None
        menuException = self.startMenu()
        
        while menuException == None:
            menuException = self.handleMainMenuOptions()
            
            if menuException == self.quitFlag:
                # Go back to login page
                menuException = self.startMenu()
                
                # Quit for good
                if menuException == self.quitFlag:
                    return 
        
################################################################
# Utility functions
################################################################
        
    def clearConsoleLines(self, numLines):
        self.numLinesConsole -= numLines
        if self.numLinesConsole < 0:
            self.numLinesConsole = 0
        for i in range(numLines):
            print ("\033[A{}\033[A".format(" " * os.get_terminal_size().columns))
    
    def countLines(self, message):
        message = str(message)
        numSlashN = message.count("\n")
        if len(message) == 0:
            return numSlashN
        return numSlashN + ((len(message) - 1) // os.get_terminal_size().columns)
    
    # consolePrint prints a message and increments number of printed lines.
    def consolePrint(self, message):
        # +1 because `print` already inserts a newline
        self.numLinesConsole += self.countLines(message) + 1
        print(message)
    
    # Get input from console and adjust the number of lines printed.
    def consoleInput(self, ask_message):
        # +1 because `input` already inserts a newline
        self.numLinesConsole += self.countLines(ask_message) + 1
        return input(ask_message)
    
    def pressEnterToLeave(self):
        self.consoleInput("\nPress enter to leave...")
        self.clearConsoleLines(self.numLinesConsole)
        
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
                    self.consolePrint(oopsMessage)
                inStr = self.consoleInput(inputMessage)
                checkFunc(inStr)
                break
            except InvalidLength as err:
                oopsMessage = "\nOops: {}\n".format(err)
                if oneAttemptWrong:
                     self.clearConsoleLines(self.countLines(oopsMessage))
                self.clearConsoleLines(self.countLines(inputMessage) + 2)
                oneAttemptWrong = True
        # Restore normal menu
        if oneAttemptWrong:
            self.clearConsoleLines(self.countLines(oopsMessage) + 1)
            self.consolePrint(inputMessage + inStr + "\n")
        return inStr
    
    # attemptLogin tries to log in to the system until the user gets his
    # credentials right. If he types in an empty email, we quit.
    def attemptLogin(self):
        oneAttemptWrong = False
        loginSuccess = False
        while not loginSuccess:
            if oneAttemptWrong:
                self.consolePrint("Please try again. To quit, simply leave the email field empty.\n")
            email = self.consoleInput("Email: ")
            if email == "":
                print("\nEmpty email field. Quitting...")
                return False
            password = self.consoleInput("Password: ")
            
            loginSuccess = self.sm.login(email, password)
            self.clearConsoleLines(self.numLinesConsole)
            if loginSuccess:
                self.clearConsoleLines(self.numLinesStartHeader)
                return True
            
            # If we got here, we have not been successful :(
            oneAttemptWrong = True
    
    def printStartHeader(self):
        print("Welcome to our sales platform!")
        print("Please login to continue:\n")

################################################################
# Menu functions
################################################################

    # startMenu handles the start menu of the application.
    def startMenu(self):
        self.printStartHeader()
        
        loginSuccess = self.attemptLogin()
        # In case some error occurred or the user quitted, we stop here.
        if not loginSuccess:
            return self.quitFlag
    
    # printMenu prints a menu with `options` in default format.
    def printMenu(self, options):
        for i in range(len(options)):
            print("({})\t{}".format(i + 1, options[i]))
        print("") # Extra line
    
    # Utility function to print out menu and ask for a choice.
    def handleMenu(self, options):
        # Always give the option to quit from menu
        options = [self.quitFlag, *options]
        
        self.printMenu(options)
        
        oneWrongAttempt = False
        while True:
            try:
                if oneWrongAttempt:
                    self.consolePrint("Invalid option. Please try again.")
                choice = int(self.consoleInput("Choose an option: "))
                
                if 1 <= choice and choice <= len(options):
                    self.clearConsoleLines(self.numLinesConsole + len(options) + 1)
                    return options[choice - 1]
            except ValueError:
                pass
            except:
                raise
            
            self.clearConsoleLines(self.numLinesConsole)
            oneWrongAttempt = True
    
    # Print cases in table format
    def handle_see_cases(self):
        # Fetch the cases from storage manager
        self.consolePrint("These are all the cases you are involved with:\n")
        cases = self.sm.getCasesByCurrentUser()
        
        for case in cases:
            self.consolePrint(case)
        
        self.pressEnterToLeave()
    
    # Ask for case information and send the information to storage manager
    def handleCreateCase(self):
        # Print case creation header
        self.consolePrint("Case creation\n")
        
        case = self.sm.newCase()
        
        title = self.attemptConsoleInput("Case title: ", case.checkTitle)
        category = self.attemptConsoleInput("Case category: ", case.checkCategory)
        description = self.attemptConsoleInput("Case description: ", case.checkDescription)
        
        case.populate(title, category, description)          
        
        self.pressEnterToLeave()
        
    def handleCommentCase(self):
        # Show a list of numbers / cases.
        cases = self.sm.getCasesByCurrentUser()
        if len(cases) == 0:
            self.consolePrint("There are no cases for this user")
            self.pressEnterToLeave()
            return
            
        menuOptions = [
            "{}, {} at {}".format(
            case.category,
            case.title,
            case.createdAt.prettyStr(),
            )
            for case in cases
        ]
        self.handleMenu(menuOptions)    
        
    # TODO: please implement me!
    #
    # This is the UI for the user to change a case's status.
    def handleSetCaseStatus(self):
        pass
    
    def handleMainMenuOptions_customer(self):
        choice = self.handleMenu(
            [
                self.seeCasesChoice,
                self.commentCaseChoice,
                self.createCaseChoice,
            ]
        )
        if choice == self.quitFlag:
            return self.quitFlag
        elif choice == self.seeCasesChoice:
            self.handle_see_cases()
        elif choice == self.commentCaseChoice:
            self.handleCommentCase()
        elif choice == self.createCaseChoice:
            self.handleCreateCase()
    
    def handleMainMenuOptions_sales(self):
        choice = self.handleMenu(
            [
                self.commentCaseChoice,
                self.setCaseStatusChoice,
            ]
        )
        if choice == self.quitFlag:
            return self.quitFlag
        elif choice == self.commentCaseChoice:
            self.handleCommentCase()
        elif choice == self.setCaseStatusChoice:
            self.handleSetCaseStatus()
    
    def handleMainMenuOptions(self):
        menufunc = None
        if self.sm.currentUser["type"] == self.sm.user_type_customer:
            menufunc = self.handleMainMenuOptions_customer
        elif self.sm.currentUser["type"] == self.sm.user_type_sales:
            menufunc = self.handleMainMenuOptions_sales
        else:
            raise Exception("main menu: unsupported user type '{}'".format(self.sm.currentUser["type"]))
        
        menuException = None
        while menuException == None:
            menuException = menufunc()
        
        return menuException
