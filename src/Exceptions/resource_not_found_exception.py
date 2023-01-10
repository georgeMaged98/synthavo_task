from Exceptions.custom_exception import CustomException
class ResourceNotFoundException(CustomException):

    def __init__(self, msg):
        self.msg = msg
        self.code = 404

    # __str__ is to print() the value
    def __str__(self):
        return(repr(self.value))