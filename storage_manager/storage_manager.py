from datetime import datetime
from uuid import uuid4

class storage_manager:
    # TODO: make users and cases data persistent in a database -aholmquist 2021-11-29
    def __init__(self):
        self.cases = {}
        
        self.user_type_customer = "customer"
        self.user_type_sales = "sales"
        self.user_types = [self.user_type_customer, self.user_type_sales]
        
        self.users = {
            "daniel@email.com": {
                "name": "Daniel",
                "type": "customer",
                "password": "password321",
            },
            "joseph@email.com": {
                "name": "Joseph",
                "type": "sales",
                "password": "password123",
            },
            "c": {
                "name": "c",
                "type": "customer",
                "password": "c",
            },
            "s": {
                "name": "s",
                "type": "sales",
                "password": "s",
            },
        }
        
        self.current_user = None
        
    # TODO: add status to case information -aholmquist 2021-11-29
    # Examples of status:
    #   "resolved",
    #   "under analysis",
    #   "pending response" (waiting for customer to respond),
    #   "pending analysis" (waiting for sales person to analyze the case). This is the status with which a case is created.
    def new_case(self, title, category, description):
        case_id = uuid4().hex
        while case_id in self.cases.keys():
            case_id = uuid4().hex
        self.cases[case_id] = {
            "datetime": datetime.now().strftime("%Y-%M-%dT%H:%M:%S+%f"),
            "title": title,
            "category": category,
            "description": description,
            "comments": [],
        }

    # login returns True if login succeded, or False otherwise.
    def login(self, email, password):
        if (
            email in self.users.keys() and
            self.users[email]["password"] == password
        ):
            self.current_user = self.users[email]
            return True
        else:
            return False
            
    def add_case_comment(self, case_id, comment):
        self.cases[case_id]["comments"].append(comment)
