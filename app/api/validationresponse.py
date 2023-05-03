class ValidationResponse:
    def __init__(self, firstname, lastname, employeenumber, email, mobilenumber, message, responsetype):
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.employeenumber: int = employeenumber
        self.email: str = email
        self.mobilenumber: int = mobilenumber
        self.message : str = message
        self.responsetype : str = responsetype
