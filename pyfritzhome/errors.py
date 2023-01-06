"""Project specific exceptions."""


class LoginError(Exception):
    """The LoginError Exception."""

    def __init__(self, user):
        """Initialize the an loginError."""
        self.user = user

    def __str__(self):
        """Return the error."""
        return 'login for user="{}" failed'.format(self.user)


class InvalidError(Exception):
    """The InvalidError Exception."""

    pass
