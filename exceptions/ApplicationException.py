class ApplicationException(Exception):
    """
    Custom Exception block to Identify or raise the expected Exceptions
    """

    def __init__(self, message: str, code: int = 0) -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)