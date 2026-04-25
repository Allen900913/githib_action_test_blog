from datetime import datetime
from flask_login import UserMixin
from routes import db, login_manager
from sqlalchemy import Integer, String, BLOB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
import bcrypt

@login_manager.user_loader
def load_user(user_id: int):
    return db.session.get(User, int(user_id))

class User(db.Model,UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    def check_password(self, password: str) -> bool:
        """檢查密碼是否正確（這裡簡單比較，實務應用請用 hash）。"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))