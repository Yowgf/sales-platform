"""consoleInterface class"""

from errors.InvalidLength import InvalidLength
from .console import console
from .menuUtils.menuUtils import menuUtils

# consoleInterface handles all user interactions in the system.
#
# In the future, we want this functionality to be spread across
# multiple modules.
class consoleInterface:
    def __init__(self, storageManager):
        self.sm = storageManager
        
        self.console = console()
        self.menu = menuUtils(self.console)
        
        # Menu choices
        
        # The quit option should be available in all default menus.
        self.quitFlag = "Quit menu"
        
        self.seeCasesChoice = "See cases"
        self.seeCasesAssignedToMe = "See cases assigned to me"
        self.seeAllCasesChoice = "See all cases"
        self.commentCaseChoice = "Comment on case"
        self.createCaseChoice = "Create case"
        self.assignCaseChoice = "Assign case to me"
        self.setCaseStatusChoice = "Set case status"
        self.rateCaseChoice = "Rate case"

    def run(self):
        menuException = None
        menuException = self.startMenu()
        
        while menuException == None:
            menuException = self.handleMainMenuOptions()
            
            if menuException == self.quitFlag:
                # Go back to login page
                self.sm.logout()
                menuException = self.startMenu()
                
                # Quit for good
                if menuException == self.quitFlag:
                    return 
        
################################################################################
# Main menu
################################################################################

    # startMenu handles the start menu of the application.
    def startMenu(self):
        self.menu.printStartHeader()
        
        loginSuccess = self.menu.attemptLogin(self.sm)
        # In case some error occurred or the user quitted, we stop here.
        if not loginSuccess:
            return self.quitFlag

    def handleMainMenuOptions_customer(self):
        choice = self.menu.handleMenu(
            [
                self.seeCasesChoice,
                self.commentCaseChoice,
                self.createCaseChoice,
                self.rateCaseChoice,
            ]
        )
        if choice == self.quitFlag:
            return self.quitFlag
        elif choice == self.seeCasesChoice:
            self.handleSeeCases(self.sm.userType_customer)
        elif choice == self.commentCaseChoice:
            self.handleCommentCase()
        elif choice == self.createCaseChoice:
            self.handleCreateCase()
        elif choice == self.rateCaseChoice:
            self.handleRateCase()
    
    def handleMainMenuOptions_sales(self):
        choice = self.menu.handleMenu(
            [
                self.seeAllCasesChoice,
                self.seeCasesAssignedToMe,
                self.assignCaseChoice,
                self.commentCaseChoice,
                self.setCaseStatusChoice,
            ]
        )
        if choice == self.quitFlag:
            return self.quitFlag
        elif choice == self.seeAllCasesChoice:
            # TODO: include customer name when displaying customer cases from
            # sale's side -aholmquist 2021-12-02
            self.handleSeeCases(self.sm.userType_all)
        elif choice == self.seeCasesAssignedToMe:
            self.handleSeeCases(self.sm.userType_sales)
        elif choice == self.assignCaseChoice:
            self.handleAssignCase()
        elif choice == self.commentCaseChoice:
            self.handleCommentCase()
        elif choice == self.setCaseStatusChoice:
            self.handleSetCaseStatus()
    
    def handleMainMenuOptions(self):
        menufunc = None
        if self.sm.currentUser.type == self.sm.userType_customer:
            menufunc = self.handleMainMenuOptions_customer
        elif self.sm.currentUser.type == self.sm.userType_sales:
            menufunc = self.handleMainMenuOptions_sales
        else:
            raise Exception("main menu: unsupported user type '{}'".format(self.sm.currentUser.type))
        
        menuException = None
        while menuException == None:
            menuException = menufunc()
        
        return menuException

################################################################################
# Secondary menus
################################################################################

    # Print each case and wait to leave.
    def handleSeeCases(self, userType):
        cases = self.menu.fetchAndSeeCases(self.sm, userType)
        if cases == None:
            return
        self.menu.pressEnterToLeave()
    
    # Ask for case information and send the information to storage manager
    def handleCreateCase(self):
        # Print case creation header
        self.console.print("Case creation\n")
        
        case = self.sm.newCase()
        
        title = self.menu.attemptConsoleInput("Case title: ", case.checkTitle)
        category = self.menu.attemptConsoleInput("Case category: ", case.checkCategory)
        description = self.menu.attemptConsoleInput("Case description: ", case.checkDescription)
        
        case.populate(title, category, description)          
        
        self.menu.pressEnterToLeave()
        
    def handleCommentCase(self):
        chosenCase = self.handleAlterCase(self.sm, self.sm.currentUser.type) 
        if chosenCase == None:
            return None
                
        self.menu.attemptConsoleInput("Write your comment here (press enter to end): ",
                                 lambda inStr: self.sm.addCaseComment(chosenCase, inStr)
                                )
        self.console.clearAll()
    
    def handleAssignCase(self):
        chosenCase = self.menu.chooseCase(self.sm, self.sm.userType_all) 
        if chosenCase == None:
            return None
        
        self.sm.assignCaseTo(chosenCase, self.sm.currentUser)
    
    # This is the UI for the user to change a case's status.
    def handleSetCaseStatus(self):
        chosenCase = self.handleAlterCase(self.sm, self.sm.currentUser.type) 
        if chosenCase == None:
            return None
        
        self.console.print("Available statuses:\n")
        self.menu.printConsoleMenu(self.sm.getAllCaseStatuses())
        self.menu.attemptConsoleInput("Choose one status: ",
                                 lambda statusIdx:
                                     self.sm.setCaseStatus(chosenCase, 
                                                           chosenCase.status.allStatuses[int(statusIdx)-1])
                                )
        self.console.clearAll()
    
    # "Rate case" sequence of screens
    def handleRateCase(self):
        chosenCase = self.handleAlterCase(self.sm, self.sm.currentUser.type) 
        if chosenCase == None:
            return None
        
        chosenNumber = self.menu.attemptConsoleInput(
            "Please type your rate (must be a number from {} to {}): "
            .format(chosenCase.rateValidRange[0], 
                    chosenCase.rateValidRange[1]),
            lambda inStr: self.sm.setRate(chosenCase, inStr),
        )
        self.console.clearAll()

################################################################################
# Utility methods that may cover multiple screens
################################################################################

    def handleAlterCase(self, sm, userType):
        chosenCase = self.menu.chooseCase(sm, userType) 
        if chosenCase == None:
            return None
        
        self.console.print("You chose to alter the following case:\n")
        self.console.print(chosenCase)
        self.menu.pressEnterToContinue()
        
        self.console.clearAll()
        
        return chosenCase
