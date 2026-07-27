class BaseDocException(Exception):
    pass

class NodeAlreadyRegistered(BaseDocException):
    pass

class NodeNotFoundException(BaseDocException):
    pass

class ResolutionException(BaseDocException):
    pass

class DownloadException(BaseDocException):
    pass

class GraphNotSolvedException(BaseDocException):
    pass