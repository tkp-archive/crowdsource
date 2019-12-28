from .base import AuthenticatedHandler


class RegisterHandler(BaseRegisterHandler):
    def on_register(self, user):
        # put in perspective
        self._all_users.update([user.to_dict()])
