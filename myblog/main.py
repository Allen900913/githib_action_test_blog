import bcrypt
import os
import time
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError
from routes import app, db


def init_db():
    with app.app_context():
        max_attempts = int(os.getenv("DB_INIT_MAX_ATTEMPTS", "20"))
        delay_seconds = float(os.getenv("DB_INIT_DELAY_SECONDS", "2"))
        inspector = None

        for attempt in range(1, max_attempts + 1):
            try:
                inspector = inspect(db.engine)
                break
            except OperationalError as exc:
                if attempt == max_attempts:
                    raise
                print(
                    f"Database not ready yet (attempt {attempt}/{max_attempts}): {exc}. "
                    f"Retrying in {delay_seconds} seconds..."
                )
                time.sleep(delay_seconds)

        if inspector is None:
            raise RuntimeError("Database inspector could not be created.")

        if not inspector.has_table("users"):
            from models.user import User
            from models.article import Article

            db.create_all()

            password_hashed = bcrypt.hashpw("123456".encode(), bcrypt.gensalt())
            user = User(username="root", password=password_hashed, fullname="Administrator")

            db.session.add(user)
            db.session.commit()


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", debug=True, port=8080)
