class LoginError(Exception):
    def __init__(self, user):
        self.user = user

    def __str__(self):
        return 'login for user="{}" failed'.format(self.user)

class InvalidError(Exception):
    pass

class NotImplemented(Exception):
    pass
