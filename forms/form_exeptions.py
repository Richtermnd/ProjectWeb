class FormException(Exception):
    pass


class UserNotExistException(FormException):
    pass


class NotUniqueEmailException(FormException):
    pass


class WrongPasswordException(FormException):
    pass

class FormFileException(FormException):
    pass
