"""Project specific exceptions."""


class LoginError(Exception):
    """The LoginError Exception."""

    def __init__(self, user: str, detail: str = "") -> None:
        """Initialize the an loginError."""
        self.user = user
        self.detail = detail

    def __str__(self) -> str:
        """Return the error."""
        message = 'login for user="{}" failed'.format(self.user)
        if self.detail:
            message += ": " + self.detail
        return message


class NotLoggedInError(Exception):
    """The NotLoggedInError Exception."""

    def __str__(self) -> str:
        """Return the error."""
        return "not logged in, login before doing any requests."


class InvalidError(Exception):
    """The InvalidError Exception."""

    pass
