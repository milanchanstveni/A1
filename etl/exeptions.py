"""Exceptions for the ETL module."""


class LoadError(Exception):
    """Load ETL exception."""

    def __init__(self, message: str) -> None:
        """Initialize the exception."""
        Exception.__init__(self)

        self.message = message

    def __str__(self) -> str:
        """Return the exception message."""
        return self.message


class GatherError(Exception):
    """Gather ETL exception."""

    def __init__(self, message: str, source: str = "") -> None:
        """
        Initialize the exception.
        :param message: The exception message.
        :param source: The source of the failed external call.
        """
        Exception.__init__(self)

        self.message = message
        self.source = source

    def __str__(self) -> str:
        """Return the exception message."""
        return f"Source: {self.source}\nError: {self.message}"
