# interaction_manager handles all interactions in the system.
#
# In the future, we want this functionality to be spread across
# multiple modules.
class interaction_manager:
    def __init__(self, storage_manager):
        self.sm = storage_manager
        
        # Util constants.
        
        # numlines_console helps maintain the console nice and tidy.
        self.numlines_console = 0
        
        # It might be a good idea to NOT hardcode this number here, somehow.
        self.numlines_start_header = 3
        
        # Menu choices
        
        # The quit option should be available in all default menus.
        self.quit_flag = "Quit menu"
        
        self.seeCasesChoice = "See cases"
        self.commentCaseChoice = "Comment on case"
        self.createCaseChoice = "Create case"
        self.setCaseStatusChoice = "Set case status"

    def clear_console_lines(self, numlines):
        self.numlines_console -= numlines
        if self.numlines_console < 0:
            self.numlines_console = 0
        for i in range(numlines):
            print ("\033[A{}\033[A".format(" " * 80))
    
    def count_numof_newlines(self, message):
        return message.count("\n")
    
    # print_console prints a message and increments number of printed lines.
    def print_console(self, message):
        # +1 because `print` already inserts a newline
        self.numlines_console += self.count_numof_newlines(message) + 1
        print(message)
    
    # Get input from console and adjust the number of lines printed.
    def console_input(self, ask_message):
        # +1 because `input` already inserts a newline
        self.numlines_console += self.count_numof_newlines(ask_message) + 1
        return input(ask_message)
    
    # attempt_login tries to log in to the system until the user gets his
    # credentials right. If he types in an empty email, we quit.
    def attempt_login(self):
        oneAttemptWrong = False
        login_success = False
        while not login_success:
            if oneAttemptWrong:
                self.print_console("Please try again. To quit, simply leave the email field empty.\n")
            email = self.console_input("Email: ")
            if email == "":
                print("\nEmpty email field. Quitting...")
                return False
            password = self.console_input("Password: ")
            
            login_success = self.sm.login(email, password)
            self.clear_console_lines(self.numlines_console)
            if login_success:
                self.clear_console_lines(self.numlines_start_header)
                return True
            
            # If we got here, we have not been successful :(
            oneAttemptWrong = True
    
    def print_start_header(self):
        print("Welcome to our sales platform!")
        print("Please login to continue:\n")
    
    # start_menu handles the start menu of the application.
    def start_menu(self):
        self.print_start_header()
        
        login_success = self.attempt_login()
        # In case some error occurred or the user quitted, we stop here.
        if not login_success:
            return self.quit_flag
    
    # print_menu prints a menu with `options` in default format.
    def print_menu(self, options):
        for i in range(len(options)):
            print("({})\t{}".format(i + 1, options[i]))
        print("") # Extra line
    
    # Utility function to print out menu and ask for a choice.
    def handle_menu(self, options):
        # Always give the option to quit from menu
        options = [self.quit_flag, *options]
        
        self.print_menu(options)
        
        oneWrongAttempt = False
        while True:
            try:
                if oneWrongAttempt:
                    self.print_console("Invalid option. Please try again.")
                choice = int(self.console_input("Choose an option: "))
                
                if 1 <= choice and choice <= len(options):
                    self.clear_console_lines(self.numlines_console + len(options) + 1)
                    return options[choice - 1]
            except ValueError:
                pass
            except:
                raise
            
            self.clear_console_lines(self.numlines_console)
            oneWrongAttempt = True
    
    # Print cases in table format
    def handle_see_cases(self):
        pass
    
    # Ask for case information and send the information to storage manager
    def handle_create_case(self):
        pass
    
    # Show a list of case ids followed by their titles.
    #
    # Then, the user has to type in one of the case ids.
    #
    # Finally, the user types in the comment itself, and we send the
    # information to the storage manager.
    def handle_comment_case(self):
        pass
    
    # Show a list of case ids followed by their titles.
    #
    # Then, the user has to type in one of the case ids.
    #
    # Finally, the user types in the new status, and we send the
    # information to the storage manager.
    def handle_set_case_status(self):
        pass
    
    def handle_main_menu_options_customer(self):
        choice = self.handle_menu(
            [
                self.seeCasesChoice,
                self.commentCaseChoice,
                self.createCaseChoice,
            ]
        )
        if choice == self.quit_flag:
            return self.quit_flag
        elif choice == self.seeCasesChoice:
            self.handle_see_cases()
        elif choice == self.commentCaseChoice:
            self.handle_comment_case()
        elif choice == self.createCaseChoice:
            self.handle_create_case()
    
    def handle_main_menu_options_sales(self):
        choice = self.handle_menu(
            [
                self.commentCaseChoice,
                self.setCaseStatusChoice,
            ]
        )
        if choice == self.quit_flag:
            return self.quit_flag
        elif choice == self.commentCaseChoice:
            self.handle_comment_case()
        elif choice == self.setCaseStatusChoice:
            self.handle_set_case_status()
    
    def handle_main_menu_options(self):
        menufunc = None
        if self.sm.current_user["type"] == self.sm.user_type_customer:
            menufunc = self.handle_main_menu_options_customer
        elif self.sm.current_user["type"] == self.sm.user_type_sales:
            menufunc = self.handle_main_menu_options_sales
        else:
            raise Exception("main menu: unsupported user type '{}'".format(self.sm.current_user["type"]))
        
        menuException = None
        while menuException == None:
            menuException = menufunc()
        
        return menuException
    
    def run(self):
        menuException = None
        menuException = self.start_menu()
        
        while menuException == None:
            menuException = self.handle_main_menu_options()
            
            if menuException == self.quit_flag:
                # Go back to login page
                menuException = self.start_menu()
                
                # Quit for good
                if menuException == self.quit_flag:
                    return
