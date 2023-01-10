from Exceptions.custom_exception import CustomException
class DatabaseException(CustomException):

    def __init__(self, msg):
        self.msg = f"Database Error {msg}"
        self.code = 500

    # __str__ is to print() the value
    def __str__(self):
        return(repr(self.value))