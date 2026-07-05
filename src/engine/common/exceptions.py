class BaseDocException(Exception):
    pass

class NodeAlreadyRegistered(BaseDocException):
    pass

class NodeNotFoundException(BaseDocException):
    pass