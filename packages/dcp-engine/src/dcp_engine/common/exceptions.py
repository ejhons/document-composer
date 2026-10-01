class BaseDcpException(Exception):
    pass

class GraphNotSolvedException(BaseDcpException):
    pass

class WorkspaceNotDefinedException(BaseDcpException):
    pass

class NodeAlreadyRegistered(BaseDcpException):
    pass

class NodeNotFoundException(BaseDcpException):
    pass

class ResolutionException(BaseDcpException):
    pass

class DownloadException(BaseDcpException):
    pass


class ContentNotAvaliable(BaseDcpException):
    pass