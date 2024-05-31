class Error(Exception):
    """Domain base error."""


class DomainError(Error):
    """Base class to mark the errors directly to high tier for user.
    Usually it will have the user friendly message as exception str repr."""
