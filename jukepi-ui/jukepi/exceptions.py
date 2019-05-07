
class JukePiException(Exception):
    pass


class ConfigurationException(JukePiException):
    pass


class EntityNotFoundException(JukePiException):
    pass


class ResourceNotFoundException(JukePiException):
    pass
