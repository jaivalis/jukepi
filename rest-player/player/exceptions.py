
class RestPlayerException(Exception):
    pass


class ConfigurationException(RestPlayerException):
    pass


class ResourceNotFoundException(RestPlayerException):
    pass
