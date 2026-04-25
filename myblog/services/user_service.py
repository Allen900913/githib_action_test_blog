from sqlalchemy import select
from flask_login import login_user
from routes import db
from models.user import User


class UserService:
    def do_login(self, username: str, password: str) -> bool:
        query = select(User).where(User.username == username)
        attempted_user = db.session.scalar(query)

        if attempted_user and attempted_user.check_password(password):
            login_user(attempted_user)
            return True
        return False
