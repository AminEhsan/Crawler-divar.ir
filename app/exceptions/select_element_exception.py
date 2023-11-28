class SelectElementException(Exception):
    """Exception raised when a specific element is not found."""

    def __init__(self, element: str) -> None:
        super().__init__(f"The element selected by '{element}' could not be found.")
