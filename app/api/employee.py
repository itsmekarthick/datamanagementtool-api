import string

class Employee:
    def __init__(self, firstname, lastname, employeenumber, email, mobilenumber):
        self.firstname: string = firstname
        self.lastname: string = lastname
        self.employeenumber: int = employeenumber
        self.email: string = email
        self.mobilenumber: int = mobilenumber
