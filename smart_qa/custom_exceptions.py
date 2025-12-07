class BaseException(Exception):
    """Base Exception Class"""
    pass
    

class UnsupportedFileType(BaseException):
    """Raised when filetype cannnot be parsed"""
    pass
    
class FileNotFound(BaseException):
    """Raised when file not at specified path"""
    pass

    
class FolderNotFound(BaseException):
    """Raised when folder not at specified path"""
    pass
    
class MaxRetriesExceeded(BaseException):
    """raised after MAX_RETRIES is exceeded"""
    pass
    
class JSONParseError(BaseException):
    """raised when a json parsing error occurs"""
    pass