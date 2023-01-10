from Exceptions.custom_exception import CustomException
class CustomValidationException(CustomException):

    def __init__(self, msg):
        self.msg = str(msg)
        self.code = 400

    # __str__ is to print() the value
    def __str__(self):
        return(repr(self.value))