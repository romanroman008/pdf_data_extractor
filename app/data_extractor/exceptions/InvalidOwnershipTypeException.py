class InvalidOwnershipTypeException(Exception):
    """
    Exception raised when an invalid or unknown ownership type is encountered.
    """
    def __init__(self, ownership_kind: str, message: str = "Invalid ownership type encountered"):
        self.ownership_kind = ownership_kind
        self.message = f"{message}: {ownership_kind}"
        super().__init__(self.message)
