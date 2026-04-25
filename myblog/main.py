import bcrypt
from sqlalchemy import inspect
from routes import app, db

def init_db():
    with app.app_context():  # 建立 Flask app 的 context
        inspector = inspect(db.engine)  # 用 inspector 檢查資料庫
        if not inspector.has_table('users'):  # 如果沒有 users 資料表
            from models.user import User
            from models.article import Article

            db.create_all()  # 建立所有定義過的模型對應的資料表

            # 建立一個預設使用者
            password_hashed = bcrypt.hashpw('123456'.encode(), bcrypt.gensalt())
            user = User(username="root", password=password_hashed , fullname="Administrator")

            db.session.add(user)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True, port=8080)
