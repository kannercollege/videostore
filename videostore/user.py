from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, is_admin: bool = False, *args, **kwargs) -> None:
        self.is_admin = is_admin
        super().__init__(*args, **kwargs)
